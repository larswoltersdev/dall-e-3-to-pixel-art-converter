import os
import requests
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom
import base64

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
from io import BytesIO
from PIL import Image
from fastapi.responses import HTMLResponse

load_dotenv()

app = FastAPI()

class PixelArt(BaseModel):
    api_token: str
    prompt: str
    grid_size: int
    image_size: int
    mode: str

client = AsyncOpenAI()

def authorize(token: str):
    if token != os.getenv('API_TOKEN'):
        raise HTTPException(status_code=401, detail="Invalid API token")

@app.get("/")
def read_root():
    return {"status": "success"}

@app.post("/generate", response_class=HTMLResponse)
async def generate(pixel_art: PixelArt):
    authorize(pixel_art.api_token)

    prevention = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:"
    prompt = pixel_art.prompt

    prevent_revision_prompt = prevention + ' make a pixel art illustration of ' + prompt + ' with a height of ' + str(pixel_art.grid_size) + ' and a width of ' + str(pixel_art.grid_size) + ' pixels.'

    print('Generating image with prompt: ' + prompt)
    response = await client.images.generate(
        model="dall-e-3",
        prompt=str(prevent_revision_prompt),
        size="1024x1024",
        quality="hd",
        n=1,
    )

    print('Image generation success')
    image_url = response.data[0].url
    print(image_url)

    print('Retrieving image from URL')
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))

    print('Resizing and pixelizing image')
    image = image.resize((pixel_art.grid_size, pixel_art.grid_size), Image.LANCZOS)

    # If the mode is 'png', return the image as a base64 encoded .png file
    if pixel_art.mode == 'png':
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        base64_encoded_result = base64.b64encode(img_byte_arr).decode('ascii')

        return JSONResponse(content={"image": base64_encoded_result})

    # If the mode is 'svg', return the image as an SVG file
    if pixel_art.mode == 'svg':
        print('Converting image to numpy array')
        pixels = np.array(image)

        print('Generating SVG image')
        pixel_size = pixel_art.image_size / pixel_art.grid_size
        svg = ET.Element('svg', width=str(pixel_art.image_size), height=str(pixel_art.image_size), xmlns="http://www.w3.org/2000/svg")
        for i in range(pixel_art.grid_size):
            for j in range(pixel_art.grid_size):
                color = f'rgb({pixels[i, j, 0]}, {pixels[i, j, 1]}, {pixels[i, j, 2]})'
                ET.SubElement(svg, 'rect', x=str(j*pixel_size), y=str(i*pixel_size), width=str(pixel_size), height=str(pixel_size), fill=color)

        print('Converting SVG to HTML')
        rough_string = ET.tostring(svg, 'utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)
        svg_code = reparsed.toprettyxml(indent="  ")

        return HTMLResponse(content=svg_code)