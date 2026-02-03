## FlaskApp.py
from flask import Flask, request, jsonify
from mood_analysis import TensorFlowModel
from MoodBoardGenerator import MoodBoardGenerator

app = Flask(__name__)

# Initialize the TensorFlow model and MoodBoardGenerator
tensorflow_model = TensorFlowModel()
mood_board_generator = MoodBoardGenerator()

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    photo = request.files['photo']
    theme = request.form.get('theme', 'default')
    
    # Ensure the photo is uploaded
    if photo.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Perform mood analysis
        mood, confidence = tensorflow_model.analyze_mood(photo.read())
        
        # Generate mood board
        mood_board = mood_board_generator.generate_mood_board(photo.read(), theme)
        
        # Return the mood board URL
        return jsonify({'mood_board_url': mood_board.save()}), 200
    except Exception as e:
        # Handle exceptions that may occur during mood analysis or mood board generation
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
