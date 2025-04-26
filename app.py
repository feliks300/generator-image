import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from diffusers import StableDiffusionPipeline
import torch
import time

app = Flask(__name__)
CORS(app)

# Directory for storing generated images
GENERATED_IMAGES_DIR = "generated_images"
IMAGES_URL = "/images/"

# Ensure the generated_images directory exists
if not os.path.exists(GENERATED_IMAGES_DIR):
    os.makedirs(GENERATED_IMAGES_DIR)

# Load the Stable Diffusion model with increased timeout
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, timeout=600)  # Увеличиваем тайм-аут до 600 секунд
# pipe = pipe.to("cuda")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    print("Received /generate request")
    data = request.get_json()
    prompt = data.get('prompt', '')
    type = data.get('type', 'image')  # По умолчанию image
    style = data.get('style', 'realistic')  # По умолчанию realistic

    # Log the request data
    print(f"Prompt: {prompt}, Type: {type}, Style: {style}")

    if type != 'image':
        return jsonify({'error': 'Only image generation is supported for now.'}), 400

    # Combine prompt with style for better results
    styled_prompt = f"{prompt}, {style} style"
    print(f"Generating image with prompt: {styled_prompt}")

    # Generate the image using Stable Diffusion
    try:
        image = pipe(styled_prompt).images[0]
    except Exception as e:
        print(f"Error generating image: {e}")
        return jsonify({'error': 'Failed to generate image.'}), 500

    # Generate a unique filename based on timestamp
    timestamp = str(int(time.time() * 1000))
    image_filename = f"image_{timestamp}.png"
    image_path = os.path.join(GENERATED_IMAGES_DIR, image_filename)

    # Save the image
    image.save(image_path)
    print(f"Image saved: {image_path}")

    # Return the image URL
    image_url = f"{IMAGES_URL}{image_filename}"
    print(f"Returning: {image_url}")
    return jsonify({'image_url': image_url})

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(GENERATED_IMAGES_DIR, filename)

if __name__ == '__main__':
    print("Starting server...")
    port = int(os.getenv("PORT", 7860))
    app.run(debug=True, host='0.0.0.0', port=port)