"""
Mood Board Generator - Minimal Test Version
"""

import gradio as gr
import numpy as np
from PIL import Image

def process_image(image, theme, style, intensity):
    """Simple test function"""
    if image is None:
        placeholder = Image.new('RGB', (800, 600), color='lightgray')
        return placeholder, "Please upload an image", "No analysis"
    
    # Convert to PIL if needed
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image.astype('uint8'), 'RGB')
    else:
        pil_image = image
    
    # Simple response
    description = f"Theme: {theme}, Style: {style}, Intensity: {intensity}"
    analysis = f"Image size: {pil_image.size}"
    
    return pil_image, description, analysis

# Create interface
demo = gr.Interface(
    fn=process_image,
    inputs=[
        gr.Image(label="Upload Photo", type="numpy"),
        gr.Dropdown(["Natural", "Urban", "Vintage"], value="Natural", label="Theme"),
        gr.Dropdown(["Vibrant", "Muted", "Pastel"], value="Vibrant", label="Style"),
        gr.Slider(0, 1, 0.7, label="Intensity")
    ],
    outputs=[
        gr.Image(label="Result"),
        gr.Textbox(label="Description"),
        gr.Textbox(label="Analysis")
    ],
    title="🎨 Mood Board Generator (Test)",
    description="AI-powered mood board generation"
)

if __name__ == "__main__":
    demo.launch()
