from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from typing import Tuple, BytesIO
import io
import os

# MoodBoard class
class MoodBoard:
    def __init__(self, image_path: str, theme: str):
        self.image_path = image_path
        self.theme = theme

    def save(self) -> str:
        # Placeholder for saving the mood board image
        # This should include the logic to save the image to a file or a URL
        # For the sake of this example, we'll return a placeholder URL
        return f"https://example.com/{self.theme}/{self.image_path}"

# TensorFlowModel class
class TensorFlowModel:
    def __init__(self, model_path: str = 'mood_model.h5', model_weights_path: str = 'mood_model_weights.h5'):
        self.model = self.load_model(model_path, model_weights_path)

    def load_model(self, model_path: str, model_weights_path: str) -> tf.keras.Model:
        model = load_model(model_path)
        model.load_weights(model_weights_path)
        return model

    def analyze_mood(self, photo: bytes) -> Tuple[str, float]:
        processed_image = self.preprocess_image(photo)
        mood_prediction = self.model.predict(processed_image)
        mood = self.decode_mood(mood_prediction)
        confidence = max(mood_prediction[0])
        return mood, confidence

    def preprocess_image(self, photo: bytes) -> tf.Tensor:
        # Placeholder for image preprocessing
        # This should include resizing, normalization, etc.
        # For the sake of this example, we'll just return the photo as a tensor
        return tf.convert_to_tensor(photo)

    def decode_mood(self, prediction: tf.Tensor) -> str:
        mood_labels = ['Happy', 'Sad', 'Angry', 'Surprised']
        return mood_labels[int(prediction.argmax())]

# MoodBoardGenerator class
class MoodBoardGenerator:
    def __init__(self, app: Flask = None):
        self.app = app or Flask(__name__)
        self.tensorflow_model = TensorFlowModel()

    def generate_mood_board(self, photo: bytes, theme: str) -> MoodBoard:
        mood, confidence = self.tensorflow_model.analyze_mood(photo)
        image_path = f"{mood}_{confidence:.2f}.jpg"
        return MoodBoard(image_path, theme)

# FlaskApp class
class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.tensorflow_model = TensorFlowModel()
        self.mood_board_generator = MoodBoardGenerator(self.app)

    def run_server(self) -> None:
        @self.app.route('/upload_photo', methods=['POST'])
        def upload_photo():
            photo = request.files['photo']
            theme = request.form.get('theme', 'default')
            
            if photo.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            
            try:
                mood_board = self.mood_board_generator.generate_mood_board(photo.read(), theme)
                return jsonify({'mood_board_url': mood_board.save()}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        self.app.run(debug=True)

# Initialize and run the Flask application
if __name__ == '__main__':
    flask_app = FlaskApp()
    flask_app.run_server()
