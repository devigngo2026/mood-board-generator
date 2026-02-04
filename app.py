"""
Mood Board Generator - Gradio App for Hugging Face Spaces
AI-powered mood board generation from uploaded photos
"""

import gradio as gr
import numpy as np
from PIL import Image
import io
from typing import Tuple, Optional

# Import our custom modules
from mood_board_generator.mood_analyzer import MoodAnalyzer
from mood_board_generator.board_generator import BoardGenerator


class MoodBoardApp:
    """Main application class for Mood Board Generator"""
    
    def __init__(self):
        self.mood_analyzer = MoodAnalyzer()
        self.board_generator = BoardGenerator()
        
    def process_image(
        self, 
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
            mood_result = self.mood_analyzer.analyze(pil_image)
            mood = mood_result['mood']
            confidence = mood_result['confidence']
            emotions = mood_result['emotions']
            
            # Generate mood board
            mood_board = self.board_generator.generate(
                image=pil_image,
                mood=mood,
                theme=theme,
                style=style,
                color_intensity=color_intensity
            )
            
            # Prepare description
            description = self._create_description(mood, confidence, theme)
            
            # Prepare analysis details
            analysis = {
                "Primary Mood": mood,
                "Confidence": f"{confidence:.1%}",
                "Theme": theme,
                "Style": style,
                **emotions
            }
            
            return mood_board, description, analysis
            
        except Exception as e:
            error_msg = f"Error processing image: {str(e)}"
            print(error_msg)
            # Return placeholder on error
            placeholder = Image.new('RGB', (800, 600), color='lightgray')
            return placeholder, error_msg, {"Error": str(e)}
    
    def _create_description(self, mood: str, confidence: float, theme: str) -> str:
        """Create a descriptive text about the mood analysis"""
        return f"""
### 🎨 Mood Analysis Complete!

**Detected Mood:** {mood.title()}  
**Confidence:** {confidence:.1%}  
**Applied Theme:** {theme}

Your mood board has been generated based on the emotional tone detected in your image. 
The colors, patterns, and composition reflect the {mood.lower()} atmosphere we identified.
        """.strip()
    
    def create_interface(self) -> gr.Blocks:
        """Create and configure the Gradio interface"""
        
        # Define theme options
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
        .main-title {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .description {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        """
        
        # Build interface
        with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as interface:
            
            # Header
            gr.Markdown(
                """
                # 🎨 AI Mood Board Generator
                
                Upload a photo and let AI analyze its emotional tone to create a beautiful mood board.
                Perfect for designers, artists, and creative professionals!
                """,
                elem_classes="main-title"
            )
            
            with gr.Row():
                # Left column - Input
                with gr.Column(scale=1):
                    gr.Markdown("### 📤 Upload & Configure")
                    
                    image_input = gr.Image(
                        label="Upload Your Photo",
                        type="numpy",
                        height=300
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
                        label="Generated Mood Board",
                        height=300
                    )
                    
                    description_output = gr.Markdown(
                        label="Analysis Description"
                    )
                    
                    analysis_output = gr.JSON(
                        label="📊 Detailed Analysis"
                    )
            
            # Examples section
            gr.Markdown("### 💡 Try These Examples")
            gr.Examples(
                examples=[
                    ["examples/sunset.jpg", "Natural", "Warm", 0.8],
                    ["examples/city.jpg", "Urban", "Bold", 0.6],
                    ["examples/flowers.jpg", "Romantic", "Pastel", 0.7],
                ],
                inputs=[image_input, theme_input, style_input, intensity_input],
                label="Click to try sample images"
            )
            
            # Footer
            gr.Markdown(
                """
                ---
                ### ℹ️ About
                This AI-powered tool analyzes the emotional content of your photos using deep learning 
                and generates aesthetically pleasing mood boards. Perfect for:
                - 🎨 Design inspiration
                - 📱 Social media content
                - 🏠 Interior design planning
                - 💼 Brand development
                
                **Note:** Processing may take a few seconds depending on image size.
                """
            )
            
            # Connect the button to the processing function
            generate_btn.click(
                fn=self.process_image,
                inputs=[image_input, theme_input, style_input, intensity_input],
                outputs=[mood_board_output, description_output, analysis_output]
            )
        
        return interface


def main():
    """Main entry point for the application"""
    app = MoodBoardApp()
    interface = app.create_interface()
    
    # Launch the interface
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,        # Default Hugging Face Spaces port
        share=False,             # Don't create a public link (HF Spaces handles this)
        show_error=True          # Show detailed errors for debugging
    )


if __name__ == "__main__":
    main()
