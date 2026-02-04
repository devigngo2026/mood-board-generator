"""
Mood Analyzer Module
Handles AI-based mood detection from images
"""

import numpy as np
from PIL import Image
from typing import Dict, Tuple
import io


class MoodAnalyzer:
    """Analyzes mood and emotions from images using AI"""
    
    # Mood categories
    MOODS = ['Happy', 'Calm', 'Energetic', 'Melancholic', 'Mysterious', 'Romantic']
    
    def __init__(self):
        """Initialize the mood analyzer"""
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the TensorFlow model (lightweight version)"""
        try:
            # For now, we'll use a simplified approach
            # In production, you would load a real TensorFlow model here
            # import tensorflow as tf
            # self.model = tf.keras.models.load_model('mood_model.h5')
            
            # Using a mock model for demonstration
            print("Model loaded successfully (mock mode)")
            self.model = "mock_model"
            
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            self.model = None
    
    def analyze(self, image: Image.Image) -> Dict:
        """
        Analyze mood from an image
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary containing mood analysis results
        """
        # Preprocess image
        processed_image = self._preprocess_image(image)
        
        # Analyze colors and composition
        color_analysis = self._analyze_colors(processed_image)
        
        # Determine mood based on analysis
        mood, confidence = self._determine_mood(color_analysis)
        
        # Get emotion breakdown
        emotions = self._get_emotion_breakdown(color_analysis)
        
        return {
            'mood': mood,
            'confidence': confidence,
            'emotions': emotions,
            'color_palette': color_analysis['dominant_colors']
        }
    
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for analysis"""
        # Resize to standard size
        image = image.resize((224, 224))
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Normalize
        img_array = img_array.astype('float32') / 255.0
        
        return img_array
    
    def _analyze_colors(self, image: np.ndarray) -> Dict:
        """Analyze color composition of image"""
        # Calculate average color values
        avg_r = np.mean(image[:, :, 0])
        avg_g = np.mean(image[:, :, 1])
        avg_b = np.mean(image[:, :, 2])
        
        # Calculate brightness
        brightness = (avg_r + avg_g + avg_b) / 3
        
        # Calculate saturation (simplified)
        max_rgb = max(avg_r, avg_g, avg_b)
        min_rgb = min(avg_r, avg_g, avg_b)
        saturation = (max_rgb - min_rgb) / (max_rgb + 0.001)
        
        # Determine dominant colors
        dominant_colors = self._extract_dominant_colors(image)
        
        return {
            'brightness': brightness,
            'saturation': saturation,
            'avg_red': avg_r,
            'avg_green': avg_g,
            'avg_blue': avg_b,
            'dominant_colors': dominant_colors
        }
    
    def _extract_dominant_colors(self, image: np.ndarray, n_colors: int = 5) -> list:
        """Extract dominant colors from image"""
        # Reshape image to list of pixels
        pixels = image.reshape(-1, 3)
        
        # Simple clustering to find dominant colors
        # In production, use k-means clustering
        colors = []
        for i in range(n_colors):
            idx = int(len(pixels) * i / n_colors)
            color = pixels[idx]
            colors.append({
                'r': int(color[0] * 255),
                'g': int(color[1] * 255),
                'b': int(color[2] * 255)
            })
        
        return colors
    
    def _determine_mood(self, color_analysis: Dict) -> Tuple[str, float]:
        """Determine mood based on color analysis"""
        brightness = color_analysis['brightness']
        saturation = color_analysis['saturation']
        
        # Simple rule-based mood detection
        # In production, use trained ML model
        
        if brightness > 0.7 and saturation > 0.5:
            mood = 'Happy'
            confidence = 0.85
        elif brightness > 0.6 and saturation < 0.3:
            mood = 'Calm'
            confidence = 0.78
        elif brightness < 0.4 and saturation > 0.6:
            mood = 'Mysterious'
            confidence = 0.82
        elif brightness < 0.5 and saturation < 0.4:
            mood = 'Melancholic'
            confidence = 0.75
        elif saturation > 0.7:
            mood = 'Energetic'
            confidence = 0.88
        else:
            mood = 'Romantic'
            confidence = 0.72
        
        return mood, confidence
    
    def _get_emotion_breakdown(self, color_analysis: Dict) -> Dict[str, str]:
        """Get detailed emotion breakdown"""
        brightness = color_analysis['brightness']
        saturation = color_analysis['saturation']
        
        emotions = {}
        
        # Calculate emotion percentages
        if brightness > 0.6:
            emotions['Joy'] = f"{int(brightness * 100)}%"
        if saturation > 0.5:
            emotions['Energy'] = f"{int(saturation * 100)}%"
        if brightness < 0.5:
            emotions['Calmness'] = f"{int((1 - brightness) * 100)}%"
        if color_analysis['avg_blue'] > 0.5:
            emotions['Serenity'] = f"{int(color_analysis['avg_blue'] * 100)}%"
        if color_analysis['avg_red'] > 0.5:
            emotions['Passion'] = f"{int(color_analysis['avg_red'] * 100)}%"
        
        return emotions
