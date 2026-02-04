"""
Mood Board Generator - Gradio App for Hugging Face Spaces
AI-powered mood board generation from uploaded photos
"""

import gradio as gr
import numpy as np
from PIL import Image

# Import our custom modules
from mood_board_generator.mood_analyzer import MoodAnalyzer
from mood_board_generator.board_generator import BoardGenerator


# Initialize analyzers
mood_analyzer = MoodAnalyzer()
board_generator = BoardGenerator()


def process_image(image, theme, style, intensity):
    """
    Process uploaded image and generate mood board
    
    Args:
        image: Input image as numpy array
        theme: User-selected theme
        style: Visual style preference
        intensity: Color intensity level (0-1)
        
    Returns:
        Tuple of (mood_board_image, mood_description, analysis_details)
    """
    try:
        if image is None:
            return None, "Please upload an image", ""
        
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
            color_intensity=intensity
        )
        
        # Prepare description
        description = f"""### 🎨 Mood Analysis Complete!

**Detected Mood:** {mood.title()}  
**Confidence:** {confidence:.1%}  
**Applied Theme:** {theme}

Your mood board has been generated based on the emotional tone detected in your image."""
        
        # Prepare analysis details
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
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        placeholder = Image.new('RGB', (800, 600), color='lightgray')
        return placeholder, error_msg, f"Error: {str(e)}"


# Create Gradio interface
demo = gr.Interface(
    fn=process_image,
    inputs=[
        gr.Image(label="📤 Upload Your Photo", type="numpy"),
        gr.Dropdown(
            choices=["Natural", "Urban", "Vintage", "Modern", "Minimalist", "Bohemian", "Industrial", "Romantic"],
            value="Natural",
            label="🎭 Select Theme"
        ),
        gr.Dropdown(
            choices=["Vibrant", "Muted", "Pastel", "Bold", "Monochrome", "Warm", "Cool", "Neutral"],
            value="Vibrant",
            label="🎨 Visual Style"
        ),
        gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=0.7,
            step=0.1,
            label="🌈 Color Intensity"
        )
    ],
    outputs=[
        gr.Image(label="🖼️ Generated Mood Board"),
        gr.Textbox(label="📝 Analysis Description", lines=5),
        gr.Textbox(label="📊 Detailed Analysis", lines=10)
    ],
    title="🎨 AI Mood Board Generator",
    description="""
    Upload a photo and let AI analyze its emotional tone to create a beautiful mood board.
    Perfect for designers, artists, and creative professionals!
    """,
    article="""
    ### ℹ️ About
    This AI-powered tool analyzes the emotional content of your photos and generates 
    aesthetically pleasing mood boards. 
    
    **GitHub**: [devigngo2026/mood-board-generator](https://github.com/devigngo2026/mood-board-generator)
    """,
    theme="soft",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
