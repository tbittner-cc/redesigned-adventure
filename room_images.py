from io import BytesIO

from PIL import Image 
import concurrent.futures
import replicate
import requests

room_type = "beachfront king"

output = replicate.run(
    "bytedance/sdxl-lightning-4step:5f24084160c9089501c1b3545d9be3c27883ae2239b6f412990e82d4a6210f8f",
    input={
        "width": 1024,
        "height": 1024,
        "prompt": f"a photo-realistic {room_type} hotel room type taken from the perspective of being in the room.",
        "scheduler": "K_EULER",
        "num_outputs": 3,
        "guidance_scale": 0,
        "negative_prompt": "worst quality, low quality",
        "num_inference_steps": 4
    }
)

print (output)

for idx,url in enumerate(output):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(f"{room_type.replace(' ', '_')}_{idx}.png",optimize=True,compression_level=6)
