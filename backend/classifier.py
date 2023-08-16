import os
import pandas as pd
from keras import models
from keras.models import Sequential
from keras.layers import Dropout, Dense, Activation, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras import layers, applications, Model
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from aenum import Enum

BATCH_SIZE = 15
IMAGE_SIZE = (224,224)
    
def get_dictionary():
    animalDict = {
        0: "Antelope",
        1: "Badger",
        2: "Bat",
        3: "Bear",
        4: "Bee",
        5: "Beetle",
        6: "Bison",
        7: "Boar",
        8: "Butterfly",
        9: "Cat",
        10: "Caterpillar",
        11: "Chimpanzee",
        12: "Cockroach",
        13: "Cow",
        14: "Coyote",
        15: "Crab",
        16: "Crow",
        17: "Deer",
        18: "Dog",
        19: "Dolphin",
        20: "Donkey",
        21: "Dragonfly",
        22: "Duck",
        23: "Eagle",
        24: "Elephant",
        25: "Flamingo",
        26: "Fly",
        27: "Fox",
        28: "Goat",
        29: "Goldfish",
        30: "Goose",
        31: "Gorilla",
        32: "Grasshopper",
        33: "Hamster",
        34: "Hare",
        35: "Hedgehog",
        36: "Hippopotamus",
        37: "Hornbill",
        38: "Horse",
        39: "Hummingbird",
        40: "Hyena",
        41: "Jellyfish",
        42: "Kangaroo",
        43: "Koala",
        44: "Ladybug",
        45: "Leopard",
        46: "Lion",
        47: "Lizard",
        48: "Lobster",
        49: "Mosquito",
        50: "Moth",
        51: "Mouse",
        52: "Octopus",
        53: "Okapi",
        54: "Orangutan",
        55: "Otter",
        56: "Owl",
        57: "Ox",
        58: "Oyster",
        59: "Panda",
        60: "Parrot",
        61: "Pelican",
        62: "Penguin",
        63: "Pig",
        64: "Pigeon",
        65: "Porcupine",
        66: "Possum",
        67: "Raccoon",
        68: "Rat",
        69: "Reindeer",
        70: "Rhinoceros",
        71: "Sandpiper",
        72: "Seahorse",
        73: "Seal",
        74: "Shark",
        75: "Sheep",
        76: "Snake",
        77: "Sparrow",
        78: "Squid",
        79: "Squirrel",
        80: "Starfish",
        81: "Swan",
        82: "Tiger",
        83: "Turkey",
        84: "Turtle",
        85: "Whale",
        86: "Wolf",
        87: "Wombat",
        88: "Woodpecker",
        89: "Zebra"
    }
    return animalDict

def load_animal_classifier():
    return models.load_model("C:/Users/akjoshi2003/Animal-ImageAI/backend/model.keras")

def guess_animal(model: Model, imageUrl):
    test_image = image.load_img(imageUrl, target_size=IMAGE_SIZE)
    test_image - image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    resultIndex = np.array(result[0]).argmax()
    animalDict = get_dictionary()
    return animalDict[resultIndex]


def train_model():
    # Get the training dataframe
    path = "C:/Users/akjoshi2003/Animal-ImageAI/backend/animals/animals/training"
    trainData = {"imgpath": [], "labels": []}
    category = os.listdir(path)
    for folder in category:
        folderPath = os.path.join(path, folder)
        files =  os.listdir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath, file)
            trainData["imgpath"].append(filePath)
            trainData["labels"].append(folder)
    trainDf = pd.DataFrame(trainData)
    print(trainDf.head(5))
    print(trainDf.shape)

    # Get the testing datafarme
    path = "C:/Users/akjoshi2003/Animal-ImageAI/backend/animals/animals/testing"
    testData = {"imgpath": [], "labels": []}
    category = os.listdir(path)
    for folder in category:
        folderPath = os.path.join(path, folder)
        files =  os.listdir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath, file)
            testData["imgpath"].append(filePath)
            testData["labels"].append(folder)
    testDf = pd.DataFrame(testData)
    print(testDf.shape)

    # Example images from dataset
    plt.figure(figsize=(15,12))
    for i,row in testDf.sample(n=16).reset_index().iterrows():
        plt.subplot(4,4,i+1)
        image_path = row['imgpath']
        image = Image.open(image_path)
        plt.imshow(image)
        plt.title(row["labels"])
        plt.axis("off")
    plt.show()

    # Get training and testing data sets from dataframes
    gen = ImageDataGenerator(preprocessing_function=applications.efficientnet.preprocess_input)
    train_set = gen.flow_from_dataframe(dataframe=trainDf, x_col='imgpath', y_col='labels', target_size=IMAGE_SIZE, color_mode='rgb', class_mode='categorical', batch_size=BATCH_SIZE, shuffle=True, seed=33)
    test_set = gen.flow_from_dataframe(dataframe=testDf, x_col='imgpath', y_col='labels', target_size=IMAGE_SIZE, color_mode='rgb', class_mode='categorical', batch_size=BATCH_SIZE, shuffle=False, seed=33)

    pt_model = applications.EfficientNetB3(
        input_shape = (224,224,3),
        include_top=False,
        weights='imagenet',
        pooling='max'
    )

    for index, layer in enumerate(pt_model.layers):
        pt_model.layers[index].trainable = False
    
    # 90 animals in our dataset
    classNum = 90

    randomLayer = Sequential([
        layers.experimental.preprocessing.RandomFlip("horizontal"),
        layers.experimental.preprocessing.RandomRotation(0.15),
        layers.experimental.preprocessing.RandomZoom(0.15),
        layers.experimental.preprocessing.RandomContrast(0.15),
    ])

    inputs = layers.Input(shape = (224,224,3))
    classifier = randomLayer(inputs)
    pt_out = pt_model(classifier, training=False)
    classifier = Dense(256, activation='relu')(pt_out)
    classifier = BatchNormalization()(classifier)
    classifier = Dropout(0.45)(classifier)
    classifier = Dense(classNum)(classifier)
    outputs = Activation(activation='softmax', dtype=tf.float32)(classifier)
    model = Model(inputs = inputs, outputs = outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print(model.summary())

    history = model.fit(train_set, steps_per_epoch = len(train_set), validation_data = test_set, validation_steps = len(test_set), epochs=10)
    model.save("C:/Users/akjoshi2003/Animal-ImageAI/backend/model.keras")

if __name__ == "__main__":
    model = load_animal_classifier()
    guess_animal(model)