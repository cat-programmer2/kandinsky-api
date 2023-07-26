# kandinsky-api
Unofficial API for Kandinsky 2.2 by Sber AI.

This API parses fusionbrain.ai website and may stop working if Fusionbrain request system changes.

`kandinsky.py` contains single `generate()` method that is used to generate images:

- `prompt` - Text prompt for txt2img generation
- `style` - Kandinsky 2.2 supports different image styles. Available styles are currently unknown.
- `width` - Image width, from 1 to 1024
- `height` - Image height, from 1 to 1024
- `timeout` - When timer exceeds this value, TimeoutError will be raised. Set to -1 to disable timeout.

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

