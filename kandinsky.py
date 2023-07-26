import aiohttp
import asyncio
from json import dumps as jsondumps
import logging

class rudalleClient:
    def __init__(self, enable_logging=False):
        self.enable_logging = enable_logging
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarytXy6y3KLVNWmrqUb',
            'Origin': 'https://editor.fusionbrain.ai',
            'Referer': 'https://editor.fusionbrain.ai/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.params = {
            'model_id': '1',
        }

        if self.enable_logging:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = None

    async def send(self, prompt='cat', style='', width=1024, height=1024):
        jsondata = jsondumps({"type":"GENERATE","style":style,"width":width,"height":height,"generateParams":{"query":prompt}})
        data = f'------WebKitFormBoundarytXy6y3KLVNWmrqUb\r\nContent-Disposition: form-data; name="params"; filename="blob"\r\nContent-Type: application/json\r\n\r\n{jsondata}\r\n------WebKitFormBoundarytXy6y3KLVNWmrqUb--\r\n'

        if self.enable_logging:
                self.logger.info(f'Sending request to Fusionbrain server with prompt: {prompt}')

        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.fusionbrain.ai/web/api/v1/text2image/run', params=self.params, headers=self.headers, data=data) as resp:
                json = await resp.json()

                if json['status'] == 'INITIAL':
                    if self.enable_logging:
                        self.logger.info(f'Checking status of image generation with id: {id}')
                    return json['uuid']
                else:
                    raise RuntimeError('Failed to post request to Fusionbrain server.')
        
    async def check(self,id):
        async with aiohttp.ClientSession() as session:
            if self.enable_logging:
                self.logger.info(f'Checking status of image generation with id: {id}')

            async with session.get(f'https://api.fusionbrain.ai/web/api/v1/text2image/status/{id}', headers=self.headers) as response:
                json = await response.json()

                if json['status'] in ['INITIAL', 'PROCESSING']:
                    return False, False
                if json['status'] == 'DONE':
                    new_jpg_txt: str = json.get('images')[0]
                    censored: bool = json['censored']
                    if new_jpg_txt:
                        return new_jpg_txt, censored
                    else:
                        raise RuntimeError('Fusionbrain server failed to generate images')


async def generate(prompt:str, style:str='', width:int=1024, height:int=1024, timeout = 180):
    """
    :param prompt: Prompt used to generate image
    :param style: Style used in Kandinsky model
    :param width: 1 to 1024
    :param height: 1 to 1024
    :param timeout: In seconds. If set to -1, then no timeout;

    Returns tuple (str, bool) of generated image encoded as Base64 string and bool showing whether the image was censored or not.
    """
    if width>1024 or height>1024:
        raise ValueError('Width and height must be lower than 1024')
    
    if width<1 or height<1:
        raise ValueError('Width and height must be positive')
    
    client = rudalleClient()
    spent_time = 0
    wait_interval = 0.5
    id = await client.send(prompt, style, width, height)

    result: str = False
    censored: bool
    while not (result or (spent_time>timeout and timeout>0)):
        result, censored = await client.check(id)
        await asyncio.sleep(wait_interval)
        spent_time += wait_interval
    if result:
        return result, censored
    else:
        raise TimeoutError(f'Timeout exceeded ({timeout} seconds)')
