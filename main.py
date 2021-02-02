from torchvision import models
import torch
import cv2
import PIL
import serial
import time
import json


# Arduino communication
ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyUSB0'
ser.open()


def shute_pos(bag_pos, door_open):
    if door_open == False:
        door_angle = 40
    if door_open == True:
        door_angle = 120
    if bag_pos == 0:
        bag_angle = 0
    if bag_pos == 1:
        bag_angle = 90
    if bag_pos == 2:
        bag_angle = 180
    send_code = str(bag_angle) + " " + str(door_angle)
    ser.write(str.encode(send_code) + b'\n')


def empty_procedure(shute_no):
    shute_pos(shute_no, False)
    time.sleep(1)
    shute_pos(shute_no, True)
    time.sleep(1.5)
    shute_pos(1, False)


# Object detection with resnet101 trained on imagenet
from torchvision import transforms
transform = transforms.Compose([
transforms.Resize(256),
transforms.CenterCrop(224),
transforms.ToTensor(),
transforms.Normalize(
mean=[0.485, 0.456, 0.406],
std=[0.229, 0.224, 0.225]
)])

with open('imagenet_class_index.json') as json_file:
    labels_string_key = json.load(json_file)
labels = dict()
for key in labels_string_key:
    labels[int(key)] = labels_string_key[key][1]
    
resnet = models.resnet101(pretrained=True)
resnet.eval()

cap = cv2.VideoCapture(7) #Set the webcam
cap.set(3,1280)
cap.set(4,720)

while True:
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    img_t = transform(image)
    batch_t = torch.unsqueeze(img_t, 0)
    out = resnet(batch_t)
    _, indices = torch.sort(out, descending=True)

    bin_0_trash = [
        'ballpoint',
        'lotion',
        'sunscreen',
        'water_bottle',
        'packet'
    ]
    
    bin_1_trash = [
        'banana',
        'hot dog',
        'burrito',
        'mashed_potato',
        'conch'
    ]
    
    bin_2_trash = [
        'hair_spray',
        'pop_bottle',
        'ladle',
        'lighter',
        'oil_filter'
    ]
    
    if labels[int(indices[0][0])] in bin_0_trash :
        print("plastic")
        empty_procedure(0)
    if labels[int(indices[0][0])] in bin_1_trash :
        print("bio")
        empty_procedure(1)
    if labels[int(indices[0][0])] in bin_2_trash :
        print("metal")
        empty_procedure(2)      
        
          
    time.sleep(0.5)
