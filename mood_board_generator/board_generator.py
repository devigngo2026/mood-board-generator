"""
Board Generator Module
Creates mood boards from analyzed images
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from typing import Dict, List, Tuple
import random


class BoardGenerator:
    """Generates aesthetic mood boards based on mood analysis"""
    
    def __init__(self):
        """Initialize the board generator"""
        self.board_size = (800, 600)
        
    def generate(
        self,
        image: Image.Image,
        mood: str,
        theme: str,
        style: str,
        color_intensity: float = 0.7
    ) -> Image.Image:
        """
        Generate a mood board
        
        Args:
            image: Source image
            mood: Detected mood
            theme: User-selected theme
            style: Visual style
            color_intensity: Color intensity level
            
        Returns:
            Generated mood board as PIL Image
        """
        # Create base canvas
        board = Image.new('RGB', self.board_size, color='white')
        
        # Apply theme-based layout
        board = self._apply_layout(board, image, theme)
        
        # Add mood-based effects
        board = self._apply_mood_effects(board, mood, color_intensity)
        
        # Apply style
        board = self._apply_style(board, style, color_intensity)
        
        # Add decorative elements
        board = self._add_decorations(board, mood, theme)
        
        # Add text overlay
        board = self._add_text_overlay(board, mood, theme)
        
        return board
    
    def _apply_layout(
        self,
        board: Image.Image,
        source_image: Image.Image,
        theme: str
    ) -> Image.Image:
        """Apply theme-based layout to the board"""
        draw = ImageDraw.Draw(board)
        
        # Resize source image
        img_resized = source_image.resize((400, 300))
        
        # Different layouts based on theme
        if theme in ['Modern', 'Minimalist']:
            # Center the image
            board.paste(img_resized, (200, 150))
            
        elif theme in ['Vintage', 'Romantic']:
            # Add border and center
            border_color = (240, 230, 220)
            draw.rectangle([190, 140, 610, 460], fill=border_color)
            board.paste(img_resized, (200, 150))
            
        elif theme in ['Urban', 'Industrial']:
            # Asymmetric layout
            board.paste(img_resized, (50, 100))
            # Add geometric shapes
            draw.rectangle([500, 100, 750, 400], fill=(50, 50, 50, 128))
            
        elif theme in ['Natural', 'Bohemian']:
            # Organic layout with rounded corners
            img_with_corners = self._round_corners(img_resized, radius=30)
            board.paste(img_with_corners, (200, 150), img_with_corners)
            
        else:
            # Default center layout
            board.paste(img_resized, (200, 150))
        
        return board
    
    def _apply_mood_effects(
        self,
        board: Image.Image,
        mood: str,
        intensity: float
    ) -> Image.Image:
        """Apply mood-specific visual effects"""
        
        if mood == 'Happy':
            # Increase brightness and saturation
            enhancer = ImageEnhance.Brightness(board)
            board = enhancer.enhance(1.0 + intensity * 0.2)
            enhancer = ImageEnhance.Color(board)
            board = enhancer.enhance(1.0 + intensity * 0.3)
            
        elif mood == 'Calm':
            # Slight blur and desaturation
            board = board.filter(ImageFilter.GaussianBlur(radius=1))
            enhancer = ImageEnhance.Color(board)
            board = enhancer.enhance(0.8)
            
        elif mood == 'Energetic':
            # Increase contrast and saturation
            enhancer = ImageEnhance.Contrast(board)
            board = enhancer.enhance(1.0 + intensity * 0.3)
            enhancer = ImageEnhance.Color(board)
            board = enhancer.enhance(1.0 + intensity * 0.5)
            
        elif mood == 'Melancholic':
            # Desaturate and darken
            enhancer = ImageEnhance.Color(board)
            board = enhancer.enhance(0.6)
            enhancer = ImageEnhance.Brightness(board)
            board = enhancer.enhance(0.9)
            
        elif mood == 'Mysterious':
            # Darken and add vignette effect
            enhancer = ImageEnhance.Brightness(board)
            board = enhancer.enhance(0.8)
            board = self._add_vignette(board)
            
        elif mood == 'Romantic':
            # Soft focus and warm tones
            board = board.filter(ImageFilter.GaussianBlur(radius=0.5))
            # Add warm overlay
            overlay = Image.new('RGB', board.size, (255, 240, 230))
            board = Image.blend(board, overlay, alpha=0.1)
        
        return board
    
    def _apply_style(
        self,
        board: Image.Image,
        style: str,
        intensity: float
    ) -> Image.Image:
        """Apply visual style to the board"""
        
        if style == 'Vibrant':
            enhancer = ImageEnhance.Color(board)
            board = enhancer.enhance(1.0 + intensity * 0.5)
            
        elif style == 'Muted':
            enhancer = ImageEnhance.Color(board)
            board = enhancer.enhance(0.5 + intensity * 0.3)
            
        elif style == 'Pastel':
            # Lighten and desaturate
            enhancer = ImageEnhance.Brightness(board)
            board = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Color(board)
            board = enhancer.enhance(0.7)
            
        elif style == 'Bold':
            enhancer = ImageEnhance.Contrast(board)
            board = enhancer.enhance(1.3)
            
        elif style == 'Monochrome':
            # Convert to grayscale
            board = board.convert('L').convert('RGB')
            
        elif style == 'Warm':
            # Add warm overlay
            overlay = Image.new('RGB', board.size, (255, 230, 200))
            board = Image.blend(board, overlay, alpha=0.15 * intensity)
            
        elif style == 'Cool':
            # Add cool overlay
            overlay = Image.new('RGB', board.size, (200, 220, 255))
            board = Image.blend(board, overlay, alpha=0.15 * intensity)
        
        return board
    
    def _add_decorations(
        self,
        board: Image.Image,
        mood: str,
        theme: str
    ) -> Image.Image:
        """Add decorative elements to the board"""
        draw = ImageDraw.Draw(board, 'RGBA')
        
        # Add subtle patterns based on theme
        if theme == 'Bohemian':
            # Add circular patterns
            for _ in range(5):
                x = random.randint(0, board.width)
                y = random.randint(0, board.height)
                r = random.randint(20, 50)
                color = (random.randint(200, 255), random.randint(200, 255), 
                        random.randint(200, 255), 50)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
                
        elif theme == 'Industrial':
            # Add lines
            for i in range(3):
                y = random.randint(0, board.height)
                draw.line([(0, y), (board.width, y)], 
                         fill=(100, 100, 100, 80), width=2)
        
        return board
    
    def _add_text_overlay(
        self,
        board: Image.Image,
        mood: str,
        theme: str
    ) -> Image.Image:
        """Add text overlay with mood and theme information"""
        draw = ImageDraw.Draw(board)
        
        # Use default font (works on all platforms)
        try:
            # Try to load a nice font if available
            font_large = ImageFont.truetype("DejaVuSans.ttf", 36)
            font_small = ImageFont.truetype("DejaVuSans.ttf", 18)
        except:
            try:
                # Fallback to any available font
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            except:
                # If all else fails, skip text overlay
                return board
        
        # Add mood text at top
        mood_text = f"{mood.upper()}"
        # Get text size for centering
        bbox = draw.textbbox((0, 0), mood_text, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (board.width - text_width) // 2
        
        # Add text with shadow
        draw.text((x+2, 32), mood_text, fill=(0, 0, 0, 100), font=font_large)
        draw.text((x, 30), mood_text, fill=(255, 255, 255), font=font_large)
        
        # Add theme text at bottom
        theme_text = f"Theme: {theme}"
        bbox = draw.textbbox((0, 0), theme_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        x = (board.width - text_width) // 2
        
        draw.text((x+1, board.height - 39), theme_text, 
                 fill=(0, 0, 0, 100), font=font_small)
        draw.text((x, board.height - 40), theme_text, 
                 fill=(255, 255, 255), font=font_small)
        
        return board
    
    def _round_corners(self, image: Image.Image, radius: int) -> Image.Image:
        """Add rounded corners to an image"""
        # Create a mask
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], 
                              radius=radius, fill=255)
        
        # Apply mask
        output = Image.new('RGBA', image.size, (0, 0, 0, 0))
        output.paste(image, (0, 0))
        output.putalpha(mask)
        
        return output
    
    def _add_vignette(self, image: Image.Image) -> Image.Image:
        """Add vignette effect to image"""
        # Create radial gradient mask
        width, height = image.size
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # Draw gradient circles
        for i in range(255, 0, -5):
            r = int(min(width, height) * (i / 255.0) * 0.8)
            x = width // 2
            y = height // 2
            draw.ellipse([x-r, y-r, x+r, y+r], fill=i)
        
        # Apply mask
        dark_overlay = Image.new('RGB', image.size, (0, 0, 0))
        return Image.composite(image, dark_overlay, mask)
