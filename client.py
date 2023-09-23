import socket
from threading import Thread
from tkinter import *
from tkinter import ttk


PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096


name = None
listbox =  None
textarea= None
labelchat = None
text_message = None




# Boilerplate Code
def recieveMessage():
    global SERVER
    global BUFFER_SIZE

    while True:

        chunk = SERVER.recv(BUFFER_SIZE)
        
        try:
            if('tiul' in chunk.decode() and '1.0,' not in chunk.decode()):
                letter_list = chunk.decode().split(' ,')
                listbox.insert(letter_list[0], letter_list[0] + ":"+
                                letter_list[1] , letter_list[1] + ":" +
                                  letter_list[2], letter_list[2] + ":" + 
                                  letter_list[3], letter_list[3] + ":" +
                                  letter_list[4], letter_list[4] + ":" + 
                                  letter_list[5])
            else:
                textarea.insert(END, "/n" + chunk.decode('ascii'))
                textarea.send('end')
                print(chunk.decode('ascii'))
        except:
            pass
                

def connectWithClient():
    global SERVER
    global listbox

    text=listbox.get(ANCHOR)
    list_item = text.split(":")
    msg = "connect" + list_item[1]

    SERVER.send(msg.encode("ascii"))

def connectClients(message, client, client_name):
    global clients

    entered_client_name = message[0:].strip()

    if(entered_client_name in clients):
        if(not clients[client_name['connected_with']] ):
            clients[entered_client_name]['connected_with'] = client_name
            clients[client_name]['connected_with'] = entered_client_name
            
            other_client_socket = clients[entered_client_name]['client']
            greet_msg = f"Hello, {entered_client_name}{client_name} connected with you..."
            other_client_socket.send(greet_msg.encode('ascii'))

            msg = f"Your successfully connected with us {entered_client_name}"
            client.send(msg.encode('ascii'))
        
        else:
            other_client_name = clients[client_name]['connect_with']
            msg = f"You are already connected with us {other_client_name}"
            client.send(msg.encode('ascii'))
    
def handleMessage(client, message, client_name):
    if(message=='show list'):
        handleShowList(client)
    elif(message[:7]=='connect'):
        connectClients(message, client, client_name)
    elif(message[:10]=='disconnect'):
        pass


# Teacher Activity
def showClientsList():
    global listbox
    listbox.delete(0,'end')
    SERVER.send('Show list'.encode('ascii'))

# Prevoius class code
# Here we ended the last class
def connectToServer():
    global SERVER
    global name
    global sending_file

    cname = name.get()
    SERVER.send(cname.encode())


def openChatWindow():

    print("\n\t\t\t\tIP MESSENGER")

    #Client GUI starts here
    window=Tk()

    window.title('Messenger')
    window.geometry("500x350")

    global name
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    namelabel = Label(window, text= "Enter Your Name", font = ("Calibri",10))
    namelabel.place(x=10, y=8)

    name = Entry(window,width =30,font = ("Calibri",10))
    name.place(x=120,y=8)
    name.focus()

    connectserver = Button(window,text="Connect to Chat Server",bd=1, font = ("Calibri",10), command = connectToServer)
    connectserver.place(x=350,y=6)

    separator = ttk.Separator(window, orient='horizontal')
    separator.place(x=0, y=35, relwidth=1, height=0.1)

    labelusers = Label(window, text= "Active Users", font = ("Calibri",10))
    labelusers.place(x=10, y=50)

    listbox = Listbox(window,height = 5,width = 67,activestyle = 'dotbox', font = ("Calibri",10))
    listbox.place(x=10, y=70)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    # Student Activity 1
    connectButton=Button(window,text="Connect",bd=1, font = ("Calibri",10), command=connectWithClient)
    connectButton.place(x=282,y=160)

    # Bolierplate Code
    disconnectButton=Button(window,text="Disconnect",bd=1, font = ("Calibri",10))
    disconnectButton.place(x=350,y=160)

    # Teacher Activity
    refresh=Button(window,text="Refresh",bd=1, font = ("Calibri",10), command=showClientsList)
    refresh.place(x=435,y=160)

    labelchat = Label(window, text= "Chat Window", font = ("Calibri",10))
    labelchat.place(x=10, y=180)

    textarea = Text(window, width = 67,height = 6,font = ("Calibri",10))
    textarea.place(x=10,y=200)

    scrollbar2 = Scrollbar(textarea)
    scrollbar2.place(relheight = 1,relx = 1)
    scrollbar2.config(command = listbox.yview)

    attach=Button(window,text="Attach & Send",bd=1, font = ("Calibri",10))
    attach.place(x=10,y=305)

    text_message = Entry(window, width =43, font = ("Calibri",12))
    text_message.pack()
    text_message.place(x=98,y=306)

    send=Button(window,text="Send",bd=1, font = ("Calibri",10))
    send.place(x=450,y=305)

    filePathLabel = Label(window, text= "",fg= "blue", font = ("Calibri",8))
    filePathLabel.place(x=10, y=330)

    window.mainloop()


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))


    # Boilerlate Code
    receive_thread = Thread(target=recieveMessage)               #receiving multiple messages
    receive_thread.start()

    openChatWindow()

setup()
