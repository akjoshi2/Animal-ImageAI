import os
import pandas as pd
from keras.models import Sequential
from keras.layers import Dropout, Dense, Activation, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras import layers, applications, Model
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt

BATCH_SIZE = 15
IMAGE_SIZE = (224,224)

if __name__ == "__main__":
    # Get the training dataframe
    path = "C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/training"
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
    path = "C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/testing"
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
