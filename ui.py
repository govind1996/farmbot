
from bs4 import BeautifulSoup
import os
import sys
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import requests
import cv2  # working with, mainly resizing, images
import numpy as np  # dealing with arrays
import os  # dealing with directories
from tqdm import \
tqdm  # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
rem1=""
diseasename=""
status=""
'''window = tk.Tk()

window.title("Dr. Plant")

window.geometry("500x510")
window.configure(background ="lightgreen")

title = tk.Label(text="Click below to choose picture for testing disease....", background = "lightgreen", fg="Brown", font=("", 15))
title.grid()'''
#print("Get photo:")

def bact():
    global rem1
    rem1= " Discard or destroy any affected plants. \n  Do not compost them. \n  Rotate yoour tomato plants yearly to prevent re-infection next year. \n Use copper fungicites"

def vir():
   global rem1
   rem1= " Monitor the field, handpick diseased plants and bury them. \n  Use sticky yellow plastic traps. \n  Spray insecticides such as organophosphates, carbametes during the seedliing stage. \n Use copper fungicites"

def latebl():
    global rem1
    rem1= " Monitor the field, remove and destroy infected leaves. \nTreat organically with copper spray. \nUse chemical fungicides,the best of which for tomatoes is chlorothalonil."


def analysis():

    mydir = os.path.dirname(__file__)
    verify_dir = os.path.join(mydir + "/" + "testpicture")
    IMG_SIZE = 50
    LR = 1e-3
    MODEL_NAME = 'healthyvsunhealthy-{}-{}.model'.format(LR, '2conv-basic')

    def process_verify_data():
        verifying_data = []
        for img in tqdm(os.listdir(verify_dir)):
            path = os.path.join(verify_dir, img)
            img_num = img.split('.')[0]
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            verifying_data.append([np.array(img), img_num])
        np.save('verify_data.npy', verifying_data)
        return verifying_data

    verify_data = process_verify_data()
    #verify_data = np.load('verify_data.npy')

    import tflearn
    from tflearn.layers.conv import conv_2d, max_pool_2d
    from tflearn.layers.core import input_data, dropout, fully_connected
    from tflearn.layers.estimator import regression
    import tensorflow as tf
    tf.reset_default_graph()

    convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 128, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 4, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')

    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)

    import matplotlib.pyplot as plt

    fig = plt.figure()
    for num, data in enumerate(verify_data):

        img_num = data[1]
        img_data = data[0]

        y = fig.add_subplot(3, 4, num + 1)
        orig = img_data
        data = img_data.reshape(IMG_SIZE, IMG_SIZE, 3)
        # model_out = model.predict([data])[0]
        model_out = model.predict([data])[0]
        global status,diseasename
        if np.argmax(model_out) == 0:
            str_label = 'healthy'
        elif np.argmax(model_out) == 1:
            str_label = 'bacterial'
        elif np.argmax(model_out) == 2:
            str_label = 'viral'
        elif np.argmax(model_out) == 3:
            str_label = 'lateblight'

        if str_label =='healthy':
            status ="HEALTHY"
        else:
            status = "UNHEALTHY"

        
        #message = tk.Label(text='Status: '+status, background="lightgreen",
                           #fg="Brown", font=("", 15))
        #message.grid(column=0, row=3, padx=10, pady=10)
        if str_label == 'bacterial':
            diseasename = "Bacterial Spot "
            bact()
            '''
            #disease = tk.Label(text='Disease Name: ' + diseasename, background="lightgreen",fg="Black", font=("", 15))
            #disease.grid(column=0, row=4, padx=10, pady=10)
            r = tk.Label(text='Click below for remedies...', background="lightgreen", fg="Brown", font=("", 15))
            r.grid(column=0, row=5, padx=10, pady=10)
            button3 = tk.Button(text="Remedies", command=bact)

            button3.grid(column=0, row=6, padx=10, pady=10)'''
        elif str_label == 'viral':
            diseasename = "Yellow leaf curl virus "
            vir()
            '''
            #disease = tk.Label(text='Disease Name: ' + diseasename, background="lightgreen",fg="Black", font=("", 15))
            #disease.grid(column=0, row=4, padx=10, pady=10)
            r = tk.Label(text='Click below for remedies...', background="lightgreen", fg="Brown", font=("", 15))
            r.grid(column=0, row=5, padx=10, pady=10)
            button3 = tk.Button(text="Remedies", command=vir)
            button3.grid(column=0, row=6, padx=10, pady=10)'''
        elif str_label == 'lateblight':
            diseasename = "Late Blight "
            latebl()
            #disease = tk.Label(text='Disease Name: ' + diseasename, background="lightgreen",fg="Black", font=("", 15))
            #disease.grid(column=0, row=4, padx=10, pady=10)
            #r = tk.Label(text='Click below for remedies...', background="lightgreen", fg="Brown", font=("", 15))
            #r.grid(column=0, row=5, padx=10, pady=10)
            #button3 = tk.Button(text="Remedies", command=latebl)
            #button3.grid(column=0, row=6, padx=10, pady=10)
        else:
            #r = tk.Label(text='Plant is healthy', background="lightgreen", fg="Black",font=("", 15))
            #r.grid(column=0, row=4, padx=10, pady=10)
            button = tk.Button(text="Exit", command=exit)
            button.grid(column=0, row=9, padx=20, pady=20)

def openphoto(url):
    mydir = os.path.dirname(__file__)
    dirPath = os.path.join(mydir + "/" + "testpicture")
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + "/" + fileName)
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    image = Image.open(response.raw)
    image.save(dirPath+"/leaf.jpg","JPEG")
    #dst = "C:/Users/user/Downloads/PlantDiseaseDetection-master/PlantDiseaseDetection-master/testpicture"
    #shutil.copy(fileName, dst)
    #load = Image.open(image)
    '''
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render, height="250", width="500")
    img.image = render
    img.place(x=0, y=0)
    img.grid(column=0, row=1, padx=10, pady = 10)'''
    #title.destroy()
    #button1.destroy()
    #button2 = tk.Button(text="Analyse Image", command=analysis)
    #plt.imshow(load)
    analysis()
    ans="Status:\t"+status+"\nDisease Name:\t"+diseasename+"\nRemedies can be:\t"+rem1
    return ans
    #button2.grid(column=0, row=2, padx=10, pady = 10)
#button1 = tk.Button(text="Get Photo", command = openphoto)
#button1.grid(column=0, row=1, padx=10, pady = 10)





