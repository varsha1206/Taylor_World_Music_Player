#Importing libraries
import socket
import sys
import os
import pygame
from pydub import AudioSegment
from zipfile import ZipFile
import msvcrt as m


#Function to send necessary items to Client Main window used for album playing
def Serverconn():

    #Initiallizing host (server) name, ip and port
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = 9999

    #Establishing connection with client
    print("Starting servconn")
    s1=socket.socket()
    s1.bind((host_name, (port-1)))
    s1.listen(1)

    #Obtaining album name from client
    print("Waiting for album name: ")
    conn,addr=s1.accept()
    album=conn.recv(4096).decode()

    #Changin directories depending on album name
    if album=="RED TV":
        os.chdir(r"C:\Users\DELL\Music\Songs\RED")
        path=r"C:\Users\DELL\Music\Songs\RED"
    elif album=="REPUTATION":
        os.chdir(r"C:\Users\DELL\Music\Songs\REP")
        path=r"C:\Users\DELL\Music\Songs\REP"
    elif album=="FOLKLORE":
        os.chdir(r"C:\Users\DELL\Music\Songs\FOLK")
        path=r"C:\Users\DELL\Music\Songs\FOLK"
    elif album=="EVERMORE":
        os.chdir(r"C:\Users\DELL\Music\Songs\EVER")
        path=r"C:\Users\DELL\Music\Songs\EVER"


    #List of songs in the directory
    songtracks = os.listdir()
    #Sending the list after encoding it in bytes
    print("Sending song directory")
    sdir = str(songtracks).encode()
    conn.send(sdir)

    #Obtaining client's song of choice
    print("Waiting for selected song:")
    choice=conn.recv(4096).decode()
    print(choice)

    #sending wav file
    f = open(os.path.join(path,choice),'rb')
    print("Sending...")
    l = f.read(4096)
    print("Sending...")
    while (l):
        conn.send(l)
        l = f.read(4096)
    f.close()

    s1.close()

def wait():
    m.getch()

def PlayPlaylist(): #Playing the custom playlist made by client

    #Initiallizing host (server) name, ip and port
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = 9999
    s2 = socket.socket()
    # Bind to the port Now wait for client connection.
    s2.bind((host_name, (port-3)))
    s2.listen(1)

    #Mentioning the path of directory with all songs
    path=r"C:\Users\DELL\Music\Songs\ALL"

    #Making socket connection to send
    print ('Server listening....')
    conn, addr = s2.accept()
    l = conn.recv(4096)
    print(l.decode())

    #Obtaining choice of song from client
    print("Waiting for selected song:")
    choice=conn.recv(4096).decode()
    print(choice)

    #sending wav file
    f = open(os.path.join(path,choice),'rb')
    print("Sending...")
    l = f.read(4096)
    print("Sending...")
    while (l):
        conn.send(l)
        l = f.read(4096)
    f.close()

    s2.close()


def Playlist(): #Making a Custom Playlist

    ##Initiallizing host (server) name, ip and port
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = 9999
    s2 = socket.socket()

    # Bind to the port# Now wait for client connection.
    s2.bind((host_name, (port-2)))
    s2.listen(1)

    #Mentioning the path of directory with all songs
    path=r"C:\Users\DELL\Music\Songs\ALL"

    #Making socket connection to send
    print ('Server listening....')
    conn, addr = s2.accept()
    l = conn.recv(4096)
    print(l.decode())

    #Obtaining directory of songs and sending list of available songs
    os.chdir(path)
    songdir=os.listdir()
    y=str(songdir).encode()
    conn.send(y)



if __name__=='__main__':
    #Initiallizing server ip
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = 9999

    #Socket creation
    s = socket.socket()

    # Bind to the port# Now wait for client connection.
    s.bind((host_name, port))
    s.listen(1)


    print ('Server listening....')
    #Making connection
    conn, addr = s.accept()
    l = conn.recv(4096)
    print(l.decode())

    #Making the server run desired fucntion
    print("Deciding what to run: ")
    while True:
        dec=conn.recv(4096).decode()
        if dec=='album':
            print("Running ServerConn")
            Serverconn()
        elif dec == 'playlist':
            print("Running Playlist")
            Playlist()
        elif dec == 'playplaylist':
            print("Running Play Playlist")
            PlayPlaylist()
        else:
            print("Something went wrong, please try again:")
            break
    wait()
