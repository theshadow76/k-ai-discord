import disco_diffusion

# Initialize the Disco Diffusion model.
model = disco_diffusion.DiscoDiffusion(
    text="A photorealistic 3D rendering of a white kitten sitting on a blue couch",
    width=512,
    height=512,
    device="cuda",
    num_iterations=100,
)

# Generate an image.
image = model.generate()

# Save the image.
image.save("image.png")