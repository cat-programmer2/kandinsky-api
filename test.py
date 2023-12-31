from io import BytesIO
import base64
from PIL import Image
import asyncio

from kandinsky import generate

if __name__ == '__main__':
    img_bytes, censored = asyncio.run(generate('cat', height=512, width=1024, timeout=-1))
    img = Image.open(BytesIO(base64.b64decode(img_bytes)))
    img.save(f'./cat.png')
    if censored:
        print('Image was censored.')
    print("Done!")
