"""
Mood Board Generator - Minimal Version for Testing
"""

import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance


def process_image(image, theme, style, intensity):
    """Simple image processing without complex modules"""
    
    if image is None:
        placeholder = Image.new('RGB', (800, 600), color='lightgray')
        return placeholder, "Please upload an image first", "No analysis available"
    
    # Convert to PIL Image
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image.astype('uint8'), 'RGB')
    else:
        pil_image = image
    
    # Simple processing - resize and apply effects
    result = pil_image.resize((800, 600))
    
    # Apply simple color adjustment based on style
    if style == "Vibrant":
        enhancer = ImageEnhance.Color(result)
        result = enhancer.enhance(1.5)
    elif style == "Muted":
        enhancer = ImageEnhance.Color(result)
        result = enhancer.enhance(0.7)
    
    # Create description
    description = f"Theme: {theme}\nStyle: {style}\nIntensity: {intensity}"
    
    # Create analysis
    analysis = f"Image processed successfully!\nSize: {result.size}\nMode: {result.mode}"
    
    return result, description, analysis


# Create interface
demo = gr.Interface(
    fn=process_image,
    inputs=[
        gr.Image(label="Upload Photo", type="numpy"),
        gr.Dropdown(
            ["Natural", "Urban", "Vintage", "Modern"],
            value="Natural",
            label="Theme"
        ),
        gr.Dropdown(
            ["Vibrant", "Muted", "Pastel", "Bold"],
            value="Vibrant",
            label="Style"
        ),
        gr.Slider(0.0, 1.0, 0.7, label="Intensity")
    ],
    outputs=[
        gr.Image(label="Result"),
        gr.Textbox(label="Description", lines=3),
        gr.Textbox(label="Analysis", lines=3)
    ],
    title="🎨 Mood Board Generator",
    description="AI-powered mood board generation (Test Version)"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
