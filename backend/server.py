from flask import Flask
import classifier

app = Flask(__name__)

@app.route('/animals')
def get_prediction():
    model = classifier.load_animal_classifier()
    animal = classifier.guess_animal(model=model)
    return {
        'Animal': animal,
    }

if __name__ == "__main__":
    app.run(debug=True)