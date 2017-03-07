import socket
import json
import time
import os
from datetime import datetime

class log_format:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    write=1 #to act as global variable for writing
    error_write=0

    @classmethod
    def get_time(self):
        time=datetime.now().strftime(' [%d-%b-%y %H:%M:%S] ')
        return time

    @classmethod
    def get_sec(self):
        sec=datetime.now().strftime('%S')
        return int(sec)


#prints the message to output screen and logs to text file
#typ= 0:Normal Message  1:Warning Message 2:Error Message
def log(message,res):
    if(res==1 or res==2  ):
        log_format.error_write=1
    res=0 #will do the colorfull things later :P
    if res==0:
        message=message
    elif res==1:
        message=  log_format.WARNING+message+log_format.ENDC
    elif res==2 :
        message= log_format.FAIL+message+log_format.ENDC

    if(log_format.write==1 or log_format.error_write==1):
        message=log_format.get_time()+message
        print message
        f = open(file_name, 'a')
        f.write(message+"\n")
        f.close()
        if(log_format.error_write==1):
            log_format.error_write==0


#function checks if the machine ip is reachable on the specified port
def ping_check(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        msg=str(ip)+" Reachable"
        log(msg,0)
    except socket.error as e:
        msg=str(ip)+ str(e)
        log(msg,2)
    s.close()


conf = json.load(open('config.json'))
file_name=conf["file_name"]
server_ips=conf["server"]
rpi_ips=conf["rpi"]
camera_ips=conf["camera"]

while True:
    sec=log_format.get_sec()
    if(sec%10==0): #hard coded here... need to modify based on the time interval for logging
        log_format.write=1



    #port 22 :  Port that is used for ssh
    #port 22 will work for most of the unix machines on the network
    log("Checking Servers",0)
    for ip in server_ips:
         ping_check(ip,22)

    log("Checking RPi's",0)
    for ip in rpi_ips:
         ping_check(ip,22)

    #port 80: Port which is used for default website
    #can be checked in the port 1024 or 554 for rtsp links
    log("Checking Cameras",0)
    for ip in camera_ips:
         ping_check(ip,8)

    log_format.write=0
    time.sleep(2)
