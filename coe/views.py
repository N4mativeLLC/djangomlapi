#from django.shortcuts import render

# Create your views here.
import re
import pika
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
import os
#import gzip
import pandas
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json
import time
import socket

from django.conf.urls import url
#from rest_framework_swagger.views import get_swagger_view

#schema_view = get_swagger_view(title='ML Models API')

def home(request):
    return HttpResponse("Hello, Django!")

def help(request):
    f = open("help.txt", "r")
    content=f.read()
    return HttpResponse(content)

def status(request):
    return HttpResponse("this is stub for Status!")

@csrf_exempt
def predict(request):
    
    try:
        if request.method == 'POST':
            start = time.time()
            reqin = datetime.now()
            received_json_data=json.loads(request.body)
            manufacturer = (received_json_data["ManufacturerName"])
            description = (received_json_data["ItemDescription"])
            content =  settings.MODEL.predict(pandas.DataFrame({'ManufacturerName': [manufacturer], 'ItemDescription': [description]}))[0]
            end = time.time()
            reqout = datetime.now()
            duration = str(round(end - start, 5))
            hostName = socket.gethostname()
            data = {"start": str(reqin),"end":str(reqout), "duration": duration, "host": hostName,"input":received_json_data, "output":content}
            json_output = json.dumps(data)
            if 'MQ_HOST_NAME' in os.environ:
                pub_rabbitmq(json_output)
            if 'KF_BROKERS' in os.environ:
                #key_bytes = bytes(os.environ['KF_TOPIC'], encoding='utf-8')
                value_bytes = bytes(json_output, encoding='utf-8')
                settings.KAFKA_PRODUCER.send(os.environ['KF_TOPIC'], value_bytes)
                print("message sent")
            return HttpResponse(json_output)
        else:
            print("Not  post")
            return HttpResponse("Not post")
    except Exception as e:
        print('Not able to send the message ' + str(e))

def health(request):
    return HttpResponse("Hello, Django!")

def hello_there(request, name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, <b>" + clean_name + "</b>! It's " + formatted_now
    return HttpResponse(content)

def pub_rabbitmq(message):
    try:
        if 'MQ_HOST_NAME' in os.environ:
            mqHost = os.environ['MQ_HOST_NAME']
            qname = os.environ['MQ_QUEUE_NAME']
        else:
            print('Need to define MQ hostname in env variable MQ_HOST_NAME')
            exit(2)
        connection = pika.BlockingConnection(pika.ConnectionParameters(mqHost))
        channel = connection.channel()
     
        channel.queue_declare(queue=qname)
        now = datetime.now().strftime("%b %d %Y %H:%M:%S")
        message = now + ' :' + message
        ###
        # Following for message Q
        channel.basic_publish(exchange='',
             routing_key=qname,
             body = message)
        
        print(now + ' Sent the message: ' + message + ', on: '+ qname)
    except Exception as e:
        print('Not able to send the message ' + str(e) + ' on '+ qname)
    
    connection.close()


def pub_kafkamq():
    pass