"""
Test script to verify the Gradio app works correctly
Run this before deploying to Hugging Face Spaces
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mood_board_generator.mood_analyzer import MoodAnalyzer
from mood_board_generator.board_generator import BoardGenerator
from PIL import Image
import numpy as np


def test_mood_analyzer():
    """Test the mood analyzer"""
    print("Testing Mood Analyzer...")
    
    analyzer = MoodAnalyzer()
    
    # Create a test image
    test_image = Image.new('RGB', (224, 224), color=(100, 150, 200))
    
    # Analyze
    result = analyzer.analyze(test_image)
    
    print(f"✓ Mood: {result['mood']}")
    print(f"✓ Confidence: {result['confidence']:.2%}")
    print(f"✓ Emotions: {result['emotions']}")
    print("✓ Mood Analyzer working!\n")


def test_board_generator():
    """Test the board generator"""
    print("Testing Board Generator...")
    
    generator = BoardGenerator()
    
    # Create a test image
    test_image = Image.new('RGB', (400, 300), color=(200, 100, 150))
    
    # Generate board
    board = generator.generate(
        image=test_image,
        mood='Happy',
        theme='Natural',
        style='Vibrant',
        color_intensity=0.7
    )
    
    print(f"✓ Generated board size: {board.size}")
    print(f"✓ Board mode: {board.mode}")
    print("✓ Board Generator working!\n")
    
    return board


def test_full_pipeline():
    """Test the complete pipeline"""
    print("Testing Full Pipeline...")
    
    analyzer = MoodAnalyzer()
    generator = BoardGenerator()
    
    # Create a colorful test image
    test_array = np.random.randint(0, 255, (300, 400, 3), dtype=np.uint8)
    test_image = Image.fromarray(test_array)
    
    # Analyze mood
    mood_result = analyzer.analyze(test_image)
    
    # Generate board
    board = generator.generate(
        image=test_image,
        mood=mood_result['mood'],
        theme='Modern',
        style='Bold',
        color_intensity=0.8
    )
    
    print(f"✓ Input image: {test_image.size}")
    print(f"✓ Detected mood: {mood_result['mood']}")
    print(f"✓ Output board: {board.size}")
    print("✓ Full pipeline working!\n")
    
    # Save test output
    output_path = "test_output.png"
    board.save(output_path)
    print(f"✓ Test output saved to: {output_path}")


def main():
    """Run all tests"""
    print("=" * 50)
    print("MOOD BOARD GENERATOR - TEST SUITE")
    print("=" * 50 + "\n")
    
    try:
        test_mood_analyzer()
        test_board_generator()
        test_full_pipeline()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nYou can now run: python app.py")
        
    except Exception as e:
        print("\n" + "=" * 50)
        print("❌ TEST FAILED!")
        print("=" * 50)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
