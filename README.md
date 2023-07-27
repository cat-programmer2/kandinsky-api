# kandinsky-api
Unofficial API for Kandinsky 2.2 txt2img model by Sber AI. This model can generate high-quality images of any resolution up to 1024*1024 by text prompt.

This API parses fusionbrain.ai website and may stop working if Fusionbrain request system changes.

`kandinsky.py` contains single `generate()` method that is used to generate images:

- `prompt` - Text prompt for txt2img generation, can be in English or in Russian. Some example of good prompt would be: `cosy wooden hut interior, photo`
- `style` - Kandinsky 2.2 supports different image styles. Available styles are currently unknown.
- `width` - Image width, from 1 to 1024;
- `height` - Image height, from 1 to 1024;
- `timeout` - If server won't return generation with this amount of seconds, TimeoutError will be raised. Set to -1 to disable timeout.

`test.py` demonstrates example of library usage, generating a cat image and saving it to the same folder:
```
from io import BytesIO
import base64
from PIL import Image
import asyncio
from kandinsky import generate

img_bytes, censored = asyncio.run(generate('cat', height=512, width=1024, timeout=-1))
img = Image.open(BytesIO(base64.b64decode(img_bytes)))
img.save(f'./cat.png')
```
# Bonus: small prompt guide
It is recommended to specify desired style of image, e.g. digital art, oil painting etc. Here are few of the known stable style modifiers:
- `octane render` - results in high-quality hyperrealistic images with cinematic visual effects:

  <img src="https://github.com/cat-programmer2/kandinsky-api/assets/140415791/1043f9b0-1173-4d6e-8971-6df8bd0e4aba" width="500">
  
  `carrier vehicle, octane render`
  
  <img src="https://github.com/cat-programmer2/kandinsky-api/assets/140415791/ce98c002-c96b-4ad1-928c-fb3f5e2fbdf9" width="500">
  
  `moss, octane render`

- `classical oil painting` - usually results in detailed image resembling a painting:

  <img src="https://github.com/cat-programmer2/kandinsky-api/assets/140415791/48a347f0-e5d8-4255-981a-7ff01ad74eb6" width="500">
  
  `rural hut, classical oil painting`

- `simple ink on parchment style` - simple, warm and visually appealing sketches:

  <img src="https://github.com/cat-programmer2/kandinsky-api/assets/140415791/eae7b2e3-5277-4329-9fa1-e7c6bea79d45" width="500">
  
  `king, simple ink on parchment style`
 
