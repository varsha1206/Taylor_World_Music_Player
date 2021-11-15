#Importing Libraries
from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
import tkinter.font as tkFont
import album as a
from PIL import ImageTk, Image
import pygame
import os
import socket
import _thread

#Initiallizing host credentials
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999

#Creating sockets
s = socket.socket()
s.connect((host_name, port))
l="Hey connected"
s.send(bytes(l,'utf=8'))


customlist=[] #list containing songs in custom playlist

#Initiallizing GUI window
top = Tk()
top.title('Taylor World')
top.geometry("600x630")
top.configure(background='black')

#Function to manage playing songs in custom playlist
def PlayCustomPlaylist():
    #letting server know what function to run
    print("Making Server run Play Playlist function: ")
    s.send(b'playplaylist')

    #Creation of socket
    s2=socket.socket()
    s2.connect((host_name, (port-3)))
    l="Connected"
    s2.send(bytes(l,'utf-8'))

    #Initiallizing mixer to run audio functionalities
    pygame.mixer.init()
    pygame.init()

    #Making GUI window
    cp = tk.Toplevel()
    cp.title("Playing Custom Playlist")
    cp.geometry("425x650")
    cp.configure(background='black')

    #Set text font properties
    fontStyle = tkFont.Font(family="Calibri", size=25,weight='bold')
    fontStyle1 = tkFont.Font(family="Calibri", size=25)

    #Image for the window
    red= ImageTk.PhotoImage(file=r"C:\Users\DELL\Desktop\temp\ts.png")

    #Label to display song name
    label = tk.Label(cp, image=red)
    label.place(x=100,y=20)
    lb = Label(cp,text ="Your Playlist",font=fontStyle,bg='black',fg='#FFFDD0',borderwidth=2)
    lb.place(x=125,y=250)

    #Creating Label Frame
    songsframe = LabelFrame(cp,font=fontStyle1,bg="#313131",fg="#f9f9f9",bd=10,width=200, height=30,relief=GROOVE)
    songsframe.place(x=25,y=350)

    # Inserting scrollbar
    scrol_y = Scrollbar(songsframe,orient=VERTICAL)

    # Inserting Playlist listbox
    playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="#71abf4",selectmode=SINGLE,font=("Calibri",15,"bold"),bg="#313131",fg="#f9f9f9",bd=5,width=30, height=7,relief=GROOVE)

    # Applying Scrollbar to listbox
    scrol_y.pack(side=RIGHT,fill=Y)
    scrol_y.config(command=playlist.yview)
    playlist.pack(side=LEFT)

    #Making variables to main song and status of song being played etc.
    track = ''
    status = ''

    # Creating the Track Frames for Song label & status label
    trackframe = LabelFrame(cp,font=("times new roman",15,"bold"),bg="Black",fg="white",bd=5,relief=GROOVE)
    trackframe.place(x=25,y=300,width=375,height=50)

    # Inserting Song Track Label
    songtrack = Label(trackframe,text=track,width=20,font=("times new roman",15,"bold"),bg="grey",fg="white")
    songtrack.grid(row=0,column=0,padx=10,pady=5)

    # Inserting Status Label
    trackstatus = Label(trackframe,text=status,font=("times new roman",15,"bold"),bg="grey",fg="white")
    trackstatus.grid(row=0,column=1,padx=10,pady=5)

    # Inserting Songs into Playlist
    for track in customlist:
        playlist.insert(END,track)

    #Function to play song after button click
    def playsong():
        #Changing working directory
        os.chdir(r"C:\Users\DELL\Desktop\temp")

        #Getting the name of song that have been clicked
        curr_song=playlist.get(ACTIVE)
        songtrack.config(text=curr_song)

        # Displaying Status
        trackstatus.config(text="-Playing-")

        print(curr_song)

        # Receiving song from server side
        s2.send(bytes(playlist.get(ACTIVE),'utf-8'))
        print("Receiving song:")
        curr_song=os.path.join(r"C:\Users\DELL\Desktop\temp","curr_song.wav")
        f = open(curr_song, 'wb')
        l=s2.recv(4096)
        while (l):
            f.write(l)
            l = s2.recv(4096)
        f.close()
        print('Done receiving')

        #Loading song and playing it
        pygame.mixer.music.load(curr_song)
        pygame.mixer.music.play()

    #Function to stop playing after button click
    def stopsong():
        # Displaying Status
        trackstatus.config(text="-Stopped-")
        # Stop Song
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    #Function to pause song being played
    def pausesong():
        # Displaying Status
        trackstatus.config(text="-Paused-")
        # Paused Song
        pygame.mixer.music.pause()

    #Function to resume song
    def unpausesong():
        # It will Display the  Status
        trackstatus.config(text="-Playing-")
        # Playing back Song
        pygame.mixer.music.unpause()



    #Button Frame
    buttonframe = LabelFrame(cp,font=("times new roman",15,"bold"),bg="black",fg="#71abf4",bd=5)
    buttonframe.place(x=10,y=560,width=400,height=53)

    # Inserting Play button
    playbtn = Button(buttonframe,text="PLAY",command=playsong,width=5,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954").grid(row=0,column=0,padx=5,pady=5)

    # Inserting Pause Button
    playbtn = Button(buttonframe,text="PAUSE",command=pausesong,width=7,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954").grid(row=0,column=1,padx=5,pady=5)

    # Inserting Unpause Button
    playbtn = Button(buttonframe,text="RESUME",command=unpausesong,width=9,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954").grid(row=0,column=2,padx=5,pady=5)

    # Inserting Stop Button
    playbtn = Button(buttonframe,text="STOP",command=stopsong,width=5,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954").grid(row=0,column=3,padx=5,pady=5)

    #GUI mainloop to keep gui window alive
    cp.mainloop()




#Function to create custom playlist
def CustomPlaylist():
    #letting server know what function to run
    print("Making Server run Playlist function: ")
    s.send(b'playlist')
    s2=socket.socket()
    s2.connect((host_name, (port-2)))
    l="Connected"
    s2.send(bytes(l,'utf-8'))

    #GUI Window
    pl = tk.Toplevel()
    pl.title("Make your playlist")
    pl.geometry("1000x200+200+200")
    pl.configure(background='black')

    # Creating Playlist Frame
    songsframe = LabelFrame(pl,text="Custom_Playlist",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
    songsframe.place(x=600,y=0,width=400,height=200)

    # Inserting scrollbar
    scrol_y = Scrollbar(songsframe,orient=VERTICAL)

    # Inserting Playlist listbox
    cplaylist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="#71abf4",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="#313131",fg="#f9f9f9",bd=5,relief=GROOVE)

    # Applying Scrollbar to listbox
    scrol_y.pack(side=RIGHT,fill=Y)
    scrol_y.config(command=cplaylist.yview)
    cplaylist.pack(fill=BOTH)

    # Creating Playlist Frame
    songsframe1 = LabelFrame(pl,text="Song Directory",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
    songsframe1.place(x=0,y=0,width=400,height=200)

    # Inserting scrollbar
    scrol_y1 = Scrollbar(songsframe1,orient=VERTICAL)

    # Inserting Playlist listbox
    songlist = Listbox(songsframe1,yscrollcommand=scrol_y.set,selectbackground="#71abf4",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="#313131",fg="#f9f9f9",bd=5,relief=GROOVE)

    # Applying Scrollbar to listbox
    scrol_y1.pack(side=LEFT,fill=Y)
    scrol_y1.config(command=songlist.yview)
    songlist.pack(fill=BOTH)

    #Connecting to server to get all the songs in the library
    print("Waiting for song list from server: ")
    data = s2.recv(2046)
    data= data.decode()
    allsongs= eval(data)

    #Inserting the songs into the listbox
    for track in allsongs:
        print(type(track))
        songlist.insert(END,track)

    #Function to add chosen songs into custom playlist listbox
    def Add():
        CURR=songlist.get(ACTIVE)
        customlist.append(songlist.get(ACTIVE))
        cplaylist.insert(END,CURR)

    #Button to add songs to custom playlist
    addbutton = Button(pl,text="ADD",command=Add,width=5,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954")
    addbutton.place(x=450,y=75)

    def closewindow():
        pl.destroy()
    #Button to close window after adding the songs
    Donebutton = Button(pl,text="DONE",command=closewindow,width=5,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954")
    Donebutton.place(x=450,y=120)

    pl.mainloop()


def Album(album,pic):
    #letting server know what function to run
    print("Making Server run Album function: ")
    s.send(b'album')

    #Creation of socket
    s1=socket.socket()
    s1.connect((host_name,(port-1)))

    #Sending album name to get songs from server
    print("Sending album name to retrieve songs: ")
    s1.send(bytes(album,'utf=8'))
    songs=[]

    print("Getting songs: ")
    data = s1.recv(1024).decode()
    songs= eval(data) #Making receiced data into list
    #Calling pygame functions
    pygame.mixer.init()
    pygame.init()

    #Making GUI window
    al = tk.Toplevel()
    al.title(album)
    al.geometry("425x650")
    al.configure(background='black')

    #Switching directories
    os.chdir(r"C:\Users\DELL\Desktop\temp")

    #Image to be placed
    red= ImageTk.PhotoImage(file=pic)
    label = tk.Label(al, image=red)
    label.place(x=100,y=20)

    #Set text font properties
    fontStyle = tkFont.Font(family="Calibri", size=25,weight='bold')
    fontStyle1 = tkFont.Font(family="Calibri", size=25)
    lb = Label(al,text = album,font=fontStyle,bg='black',fg='#FFFDD0',borderwidth=2).place(x=100,y=250)

    #Creating Label Frame
    songsframe = LabelFrame(al,font=fontStyle1,bg="#313131",fg="#f9f9f9",bd=10,width=200, height=30,relief=GROOVE)
    songsframe.place(x=25,y=350)

    # Inserting scrollbar
    scrol_y = Scrollbar(songsframe,orient=VERTICAL)

    # Inserting Playlist listbox
    playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="#71abf4",selectmode=SINGLE,font=("Calibri",15,"bold"),bg="#313131",fg="#f9f9f9",bd=5,width=30, height=7,relief=GROOVE)

    # Applying Scrollbar to listbox
    scrol_y.pack(side=RIGHT,fill=Y)
    scrol_y.config(command=playlist.yview)
    playlist.pack(side=LEFT)

    #Making variables to main song and status of song being played etc.
    track = ''
    status = ''

    # Creating the Track Frames for Song label & status label
    trackframe = LabelFrame(al,font=("times new roman",15,"bold"),bg="Black",fg="white",bd=5,relief=GROOVE)
    trackframe.place(x=25,y=300,width=375,height=50)

    # Inserting Song Track Label
    songtrack = Label(trackframe,text=track,width=20,font=("times new roman",15,"bold"),bg="grey",fg="white")
    songtrack.grid(row=0,column=0,padx=10,pady=5)

    # Inserting Status Label
    trackstatus = Label(trackframe,text=status,font=("times new roman",15,"bold"),bg="grey",fg="white")
    trackstatus.grid(row=0,column=1,padx=10,pady=5)

    # Inserting Songs into Playlist
    for track in songs:
      playlist.insert(END,track)

    #Function to play song after button click
    def playsong():
        #Changing working directory
        os.chdir(r"C:\Users\DELL\Desktop\temp")

        # Displaying Selected Song title
        curr_song=playlist.get(ACTIVE)
        songtrack.config(text=curr_song)

        # Displaying Status
        trackstatus.config(text="-Playing-")

        print(curr_song)

        #Receiving song from server
        s1.send(bytes(playlist.get(ACTIVE),'utf-8'))
        print("Receiving song:")
        curr_song=os.path.join(r"C:\Users\DELL\Desktop\temp","curr_song.wav")
        f = open(curr_song, 'wb')
        l=s1.recv(4096)
        while (l):
            f.write(l)
            l = s1.recv(4096)
        f.close()
        print('Done receiving')

        #Playing the song chosen
        pygame.mixer.music.load(curr_song)
        pygame.mixer.music.play()

    #Function to stop playing after button click
    def stopsong():
        # Displaying Status
        trackstatus.config(text="-Stopped-")
        # Stopped Song
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    #Function to pause song being played
    def pausesong():
        # Displaying Status
        trackstatus.config(text="-Paused-")
        # Paused Song
        pygame.mixer.music.pause()

    #Function to resume song
    def unpausesong():
        # It will Display the  Status
        trackstatus.config(text="-Playing-")
        # Playing back Song
        pygame.mixer.music.unpause()





    #Button Frame
    buttonframe = LabelFrame(al,font=("times new roman",15,"bold"),bg="black",fg="#71abf4",bd=5)
    buttonframe.place(x=10,y=560,width=400,height=53)

    # Inserting Play button
    playbtn = Button(buttonframe,text="PLAY",command=playsong,width=5,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954").grid(row=0,column=0,padx=5,pady=5)
    #playbtn = Button(buttonframe,text="PLAYSONG",command=self.playsong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=0,padx=10,pady=5)

    # Inserting Pause Button
    playbtn = Button(buttonframe,text="PAUSE",command=pausesong,width=7,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954").grid(row=0,column=1,padx=5,pady=5)

    # Inserting Unpause Button
    playbtn = Button(buttonframe,text="RESUME",command=unpausesong,width=9,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954").grid(row=0,column=2,padx=5,pady=5)

    # Inserting Stop Button
    playbtn = Button(buttonframe,text="STOP",command=stopsong,width=5,height=1,font=("times new roman",16,"bold"),fg="#1b1515",bg="#1DB954").grid(row=0,column=3,padx=5,pady=5)

    #Running GUI windowloop
    al.mainloop()

#Set of funtions to call ALBUM function with necessary arguments
def OpenguiRed():
    Album("RED TV","red.png")
def OpenguiRep():
    Album("REPUTATION","rep.png")
def OpenguiFolk():
    Album("FOLKLORE","folk.png")
def OpenguiEver():
    Album("EVERMORE","ever.png")

#Assigning images
red=PhotoImage(file="red.png")
rep=PhotoImage(file="rep.png")
folk=PhotoImage(file="folk.png")
ever=PhotoImage(file="ever.png")

#Font properties
fontStyle = tkFont.Font(family="Calibri", size=15,weight='bold')

#Making buttons to run Album depending on album clicked
b3=tk.Button(top,image=red,command=OpenguiRed,padx=10,pady=10,relief="raised")
b5=tk.Button(top,image=rep,command=OpenguiRep,padx=10,pady=10,relief="raised")
b7=tk.Button(top,image=folk,command=OpenguiFolk,padx=10,pady=10,relief="raised")
b8=tk.Button(top,image=ever,command=OpenguiEver,padx=10,pady=10,relief="raised")

#Button to create custom playlist
b9=tk.Button(top,text="Create Custom Playlist",command=CustomPlaylist,font=fontStyle,bg='black',fg='#1DB954',borderwidth=2,padx=5,pady=5,relief="raised")

#Button to play custom playlist
b10=tk.Button(top,text="Play Custom Playlist",command=PlayCustomPlaylist,font=fontStyle,bg='black',fg='#1DB954',borderwidth=2,padx=5,pady=5,relief="raised")

#Label heading of window
lb = Label(top,text = "Choose An Album ",font=fontStyle,bg='black',fg='#1DB954',borderwidth=2, relief="sunken").place(x=200,y=10)

#Button placements on the screen
b3.place(x=50,y=50)
b5.place(x=325,y=50)
b7.place(x=50,y=325)
b8.place(x=325,y=325)
b9.place(x=50,y=560)
b10.place(x=325,y=560)


#Looping GUI window
top.mainloop()
