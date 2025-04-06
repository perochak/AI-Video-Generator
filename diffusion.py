from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16).to("cuda")

def generate_image(prompt, output_path):
    image = pipe(prompt).images[0]
    image.save(output_path)

