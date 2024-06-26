# DALL-E 3 to pixel art converter

This is a experimental project to convert DALL-E 3 generated pixel art to 'real' pixel art.

## How to use

Make sure you install atleast Python 3 and install the required packages using `pip`. You will also need an OpenAI API account with credits.

To test the tool:

To run the server: `uvicorn main:app --reload`

1. Visit `http://127.0.0.1:8000/docs`
2. Try out the `/generate` endpoint

Example body:

```json
{
  "api_token": "test",
  "prompt": "Create a pixel art image of a dark knight with his sword in the ground, resting on it. The scenery is a battlefield.",
  "grid_size": 64,
  "image_size": 64,
  "mode": "png",
}
```

3. The mode can either be `png` or `svg`
4. The progress is printed in your Terminal as well as the generated image URL
5. The response will be either a SVG (HTML) or a PNG (base64) (note: the larger the dimensions, the bigger the response)

## Example results

### Exhausted knight

*Create a pixel art image of a dark knight with his sword in the ground, resting on it. The scenery is a battlefield.*

![example1](https://github.com/larswolters98/dall-e-3-to-pixel-art-converter/assets/32078923/f8c61fba-a6f8-4ace-aaf6-307f51bf81ae)

---

### Developer

*Create a pixel art image of a web developer having a dark blue backpack with a laptop in his right hand and a coffee mug in the other. He has to wear black pants, a dark-grey t-shirt with a black body warmer over it. The body warmer has no sleeves. He has blonde hair and white shoes. Add no background.*

![example2](https://github.com/larswolters98/dall-e-3-to-pixel-art-converter/assets/32078923/cb9e96c0-7231-4ca3-a1a2-f3a6eca34758)
