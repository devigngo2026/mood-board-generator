"""
Mood Board Generator - Gradio App for Hugging Face Spaces
AI-powered mood board generation from uploaded photos
"""

import gradio as gr
import numpy as np
from PIL import Image
from typing import Tuple

# Import our custom modules
from mood_board_generator.mood_analyzer import MoodAnalyzer
from mood_board_generator.board_generator import BoardGenerator


# Initialize analyzers
mood_analyzer = MoodAnalyzer()
board_generator = BoardGenerator()


def process_image(
    image: np.ndarray, 
    theme: str,
    style: str,
    color_intensity: float
) -> Tuple[Image.Image, str, dict]:
    """
    Process uploaded image and generate mood board
    
    Args:
        image: Input image as numpy array
        theme: User-selected theme
        style: Visual style preference
        color_intensity: Color intensity level (0-1)
        
    Returns:
        Tuple of (mood_board_image, mood_description, analysis_details)
    """
    try:
        # Convert numpy array to PIL Image
        if isinstance(image, np.ndarray):
            pil_image = Image.fromarray(image.astype('uint8'), 'RGB')
        else:
            pil_image = image
        
        # Analyze mood from image
        mood_result = mood_analyzer.analyze(pil_image)
        mood = mood_result['mood']
        confidence = mood_result['confidence']
        emotions = mood_result['emotions']
        
        # Generate mood board
        mood_board = board_generator.generate(
            image=pil_image,
            mood=mood,
            theme=theme,
            style=style,
            color_intensity=color_intensity
        )
        
        # Prepare description
        description = f"""
### 🎨 Mood Analysis Complete!

**Detected Mood:** {mood.title()}  
**Confidence:** {confidence:.1%}  
**Applied Theme:** {theme}

Your mood board has been generated based on the emotional tone detected in your image. 
The colors, patterns, and composition reflect the {mood.lower()} atmosphere we identified.
        """.strip()
        
        # Prepare analysis details as formatted string
        analysis_text = f"""**Primary Mood**: {mood}
**Confidence**: {confidence:.1%}
**Theme**: {theme}
**Style**: {style}

**Emotions Detected**:
"""
        for emotion, value in emotions.items():
            analysis_text += f"- {emotion}: {value}\n"
        
        return mood_board, description, analysis_text
        
    except Exception as e:
        error_msg = f"Error processing image: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        # Return placeholder on error
        placeholder = Image.new('RGB', (800, 600), color='lightgray')
        error_analysis = f"**Error**: {str(e)}"
        return placeholder, error_msg, error_analysis


# Define theme and style options
themes = [
    "Natural", "Urban", "Vintage", "Modern", 
    "Minimalist", "Bohemian", "Industrial", "Romantic"
]

styles = [
    "Vibrant", "Muted", "Pastel", "Bold", 
    "Monochrome", "Warm", "Cool", "Neutral"
]

# Create custom CSS
custom_css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
}
"""

# Build interface
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(), title="Mood Board Generator") as demo:
    
    # Header
    gr.Markdown(
        """
        # 🎨 AI Mood Board Generator
        
        Upload a photo and let AI analyze its emotional tone to create a beautiful mood board.
        Perfect for designers, artists, and creative professionals!
        """
    )
    
    with gr.Row():
        # Left column - Input
        with gr.Column(scale=1):
            gr.Markdown("### 📤 Upload & Configure")
            
            image_input = gr.Image(
                label="Upload Your Photo",
                type="numpy"
            )
            
            theme_input = gr.Dropdown(
                choices=themes,
                value="Natural",
                label="🎭 Select Theme",
                info="Choose a theme that matches your vision"
            )
            
            style_input = gr.Dropdown(
                choices=styles,
                value="Vibrant",
                label="🎨 Visual Style",
                info="Select the color style for your mood board"
            )
            
            intensity_input = gr.Slider(
                minimum=0.0,
                maximum=1.0,
                value=0.7,
                step=0.1,
                label="🌈 Color Intensity",
                info="Adjust the vibrancy of colors"
            )
            
            generate_btn = gr.Button(
                "✨ Generate Mood Board",
                variant="primary",
                size="lg"
            )
        
        # Right column - Output
        with gr.Column(scale=1):
            gr.Markdown("### 🖼️ Your Mood Board")
            
            mood_board_output = gr.Image(
                label="Generated Mood Board"
            )
            
            description_output = gr.Markdown(
                label="Analysis Description"
            )
            
            analysis_output = gr.Textbox(
                label="📊 Detailed Analysis",
                lines=10,
                interactive=False
            )
    
    # Footer
    gr.Markdown(
        """
        ---
        ### ℹ️ About
        This AI-powered tool analyzes the emotional content of your photos and generates 
        aesthetically pleasing mood boards. Perfect for design inspiration, social media 
        content, and creative projects.
        
        **GitHub**: [devigngo2026/mood-board-generator](https://github.com/devigngo2026/mood-board-generator)
        """
    )
    
    # Connect the button to the processing function
    generate_btn.click(
        fn=process_image,
        inputs=[image_input, theme_input, style_input, intensity_input],
        outputs=[mood_board_output, description_output, analysis_output]
    )

# Ensure demo is available at module level for Hugging Face Spaces
app = demo

# Launch for local testing
if __name__ == "__main__":
    demo.launch()
