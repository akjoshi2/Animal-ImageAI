from flask import Flask, request
import classifier
import cv2

app = Flask(__name__)


@app.route('/animals', methods = ['POST'])
def get_prediction():
    file = request.files.get('image',"")
    file.save("C:/Users/akjoshi2003/Animal-ImageAI/backend/example/input.jpg")
    print(request.form)
    print(file)
    model = classifier.load_animal_classifier()
    animal = classifier.guess_animal(model=model, imageUrl="C:/Users/akjoshi2003/Animal-ImageAI/backend/example/input.jpg")
    return {
        'Animal': animal,
    }

if __name__ == "__main__":
    app.run(debug=True)