import os

# Create new folder if a folder does not already exist
def createFolders(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

# Create testing and training folder for each animal
# Put 25% of images into testing folder, 75% into training folder
def createTestTrain(animal: str):
    anPath = "C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/" + animal
    directory = os.fsencode(anPath)
    numImages = 0
    createFolders(anPath)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        imgPath = anPath + "/" + filename
        print(imgPath)
        if (filename.endswith(".jpg")):
            numImages += 1
            if numImages % 4 == 0:
                testingPath = anPath + "/testing/" + filename
                os.replace(imgPath, testingPath)
            else:
                trainingPath = anPath + "/training/" + filename
                os.replace(imgPath, trainingPath)
            continue
        else:
            continue

# Move the training and testing folders outside the individual animal folders
def moveToOuterFolders(animal: str):
    anTestPath = "C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/" + animal + "/testing"
    anTrainPath = "C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/" + animal + "/training"
    testDir = os.fsencode(anTestPath)
    trainDir = os.fsencode(anTrainPath)
    createFolders("C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/testing/" + animal)
    createFolders("C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/training/" + animal)
    for file in os.listdir(testDir):
        filename = os.fsdecode(file)
        imgPath = anTestPath + "/" + filename
        outerTestPath = "C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/testing/" + animal + "/" + filename
        os.replace(imgPath, outerTestPath)
    for file in os.listdir(trainDir):
        filename = os.fsdecode(file)
        imgPath = anTrainPath + "/" + filename
        outerTrainPath = "C:/Users/akjoshi2003/Animal-ImageAI/animals/animals/training/" + animal + "/" + filename
        os.replace(imgPath, outerTrainPath)

