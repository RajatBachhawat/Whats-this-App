from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from numpy import *
import re
import math

# make the changes to ComposeWindow

class ScrollableFrame(Frame):
    def __init__(self, container):

        super().__init__(container)
        canvas = Canvas(self, bg = 'white')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas, bg = 'white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.place(relx = 1, relheight = 1, anchor = 'ne')

class MessagesFrame(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master, bg = 'white')

        self.labels = []
        
        self.title = ttk.Label(self, background = 'white', foreground = '#0B5345', text = "Incoming Messages", font = ("Arial", 15, 'bold'))
        self.title.place(relx = 0.04, rely = 0.02)
        
        self.scrollableFrameHolder = Frame(self, background = 'white')
        self.scrollableFrameHolder.place(relx = 0, rely = 0.1, relwidth = 1, relheight = 0.9)
        
        self.messagesList = ScrollableFrame(self.scrollableFrameHolder)
        self.messagesList.place(relx = 0.05, rely = 0, relwidth = 0.90, relheight = 1)
        
        for i in range(100):
            self.labels.append(ttk.Label(self.messagesList.scrollable_frame, background = 'white', text= "", image = "", wraplength = 300, font = ("Arial", 12), justify = LEFT))
            self.labels[i].pack(anchor = 'w')
       
        self.updatePosts()

    def updatePosts(self):
        global imgs
        for i in range(100):
            self.labels[i].config(text = "", image = "")
        i = 0
        for messageCompound in userDict[currUser].incomingMessages:
            message = re.split("--",messageCompound)
            grp = ""
            if(message[2] != "**"):
                grp = message[2]
            if len(message) > 3 :
                tmp = Image.open(message[3])
                w, h = tmp.size
                tmp = tmp.resize((250, math.floor(250*h/w)), Image.ANTIALIAS)
                imgs[i] = ImageTk.PhotoImage(tmp)
                self.labels[i].config(image = imgs[i])
                i+=1
            self.labels[i].config(text = ">> " + message[1] + grp + " : " + message[0] + "\n")
            i+=1

class ContactsFrame(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master, bg = '#EAFAF1')

        self.contactsList = ""
        
        self.title = ttk.Label(self, background = '#EAFAF1', foreground = '#0B5345', text = "Contacts", font = ("Arial", 15, 'bold'))
        self.title.place(relx = 0.1, rely = 0.02)

        self.contactHolderHolder = Frame(self, background = 'white')
        self.contactHolderHolder.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.88)
        
        self.contactHolder = ScrollableFrame(self.contactHolderHolder)
        self.contactHolder.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        
        self.contactsLabel = ttk.Label(self.contactHolder, background = 'white', foreground = 'black', text = self.contactsList, font = ("Arial", 12), justify = LEFT)
        self.contactsLabel.place(relx = 0, rely = 0)
        
        self.updateList()
    
    def updateList(self):
        self.contactsList = ""
        for contact in userDict[currUser].contactList:
            self.contactsList = self.contactsList + contact + "\n\n"
        self.contactsLabel.config(text = self.contactsList)

class GroupsFrame(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master, bg = '#EAFAF1')

        self.groupsList = ""
        
        self.title = ttk.Label(self, background = '#EAFAF1', foreground = '#0B5345', text = "Groups", font = ("Arial", 15, 'bold'))
        self.title.place(relx = 0.1, rely = 0.02)
        
        self.groupHolderHolder = Frame(self, background = 'white')
        self.groupHolderHolder.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.88)
        
        self.groupHolder = ScrollableFrame(self.groupHolderHolder)
        self.groupHolder.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        
        self.groupsLabel = ttk.Label(self.groupHolder, background = 'white', foreground = 'black', text = self.groupsList, font = ("Arial", 12), justify = LEFT)
        self.groupsLabel.place(relx = 0, rely = 0)
        
        self.updateList()

    def updateList(self):
        self.groupsList = ""
        for group in userDict[currUser].groupIDList:
            self.groupsList = self.groupsList + group + "\n\n"
        self.groupsLabel.config(text = self.groupsList)

class ComposeWindow():
    def __init__(self, master = None):
        master.geometry("600x400")
        master.wm_title("Compose Message")
        
        
        self.master = master

        self.v = IntVar(master, 1)
        self.r1 = Radiobutton(master, text="Send to users in Contacts", command = self.updateList, variable = self.v, value = 1, font = ("Arial",10,'bold'))
        self.r1.place(relx = 0, rely = 0)
        
        self.r2 = Radiobutton(master, text="Send to Groups", command = self.updateList, variable = self.v, value = 2, font = ("Arial",10,'bold'))
        self.r2.place(relx = 0, rely = 0.05)

        self.typeLabel = ttk.Label(master, text = "Type your message here:", font = ("Arial",10))
        self.typeLabel.place(relx = 0.78, rely = 0, anchor = 'ne')

        self.recepientFrame = Frame(master)
        self.recepientFrame.place(relx = 0, rely = 0.1, relwidth = 0.5, relheight = 0.9)

        self.selectLabel = ttk.Label(self.recepientFrame, text = "Click to Select the Recepients:", font = ("Arial",10))
        self.selectLabel.place(relx = 0.05, rely = 0.05)
        
        self.scroll = Scrollbar(self.recepientFrame)
        self.scroll.pack(side = RIGHT, fill = Y)
        
        self.recepientListbox = Listbox(self.recepientFrame, yscrollcommand = self.scroll.set, font = ("Arial", 10), selectmode = MULTIPLE)
        self.recepientListbox.place(relx = 0.45, rely = 0.55, relwidth = 0.85, relheight = 0.85, anchor = 'center')
        self.updateList()
        self.scroll.config(command = self.recepientListbox.yview)
        
        self.imgFileName = ""

        self.messageText = Text(master)
        self.messageText.place(relx = 0.98, rely = 0.05, relwidth = 0.45, relheight = 0.5, anchor = 'ne')
        
        self.addImageButton = Button(master, text ='Click To Add Image', command = lambda:self.openFile(), font = ("Arial",10)) 
        self.addImageButton.place(relx = 0.85, rely = 0.65, anchor = 'ne') 

        self.backButton = Button(master, text = "Back", command = self.master.destroy, font = ("Arial",10))
        self.backButton.place(relx = 0.75, rely = 0.95, relwidth = 0.20, anchor = 'se')

        self.sendButton = Button(master, text = "Send", command = self.send, font = ("Arial",10))
        self.sendButton.place(relx = 0.95, rely = 0.95, relwidth = 0.20, anchor = 'se')        

    def updateList(self):
        self.recepientListbox.delete(0,END)
        if self.v.get() == 1 :
            for contact in userDict[currUser].contactList:
                self.recepientListbox.insert(END, contact)
        if self.v.get() == 2 :
            for group in userDict[currUser].groupIDList:
                self.recepientListbox.insert(END, group)
    def send(self):
        rnos = list(self.recepientListbox.curselection())
        if self.v.get() == 1 :
            for i in rnos:
                recepient = self.recepientListbox.get(i)
                userDict[currUser].postToContact(self.messageText.get(1.0,END).rstrip(), recepient, self.imgFileName)
        if self.v.get() == 2 :
            for i in rnos:
                group = self.recepientListbox.get(i)
                userDict[currUser].postToGroup(self.messageText.get(1.0,END).rstrip(), group, self.imgFileName)
        self.master.destroy()
    def openFile(self):
        self.imgFileName = askopenfilename(filetypes = [('GIF Files', '*.gif'),('JPG Files','*.jpg'),('PNG Files','*.png')], title = "Choose an image")
        self.master.lift()

class ComposeFrame(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master, bg = '#ABEBC6')
        self.compose = Button(self, text = "+ Compose", bg = '#EAFAF1', fg = '#0B5345', command = self.composeNewMessage, font = ("Arial",11,'bold'))
        self.compose.place(relx = 0.5, rely = 0.5, relwidth = 0.6, anchor = 'center')
    
    def composeNewMessage(self):
        self.composeRoot = Tk()
        self.composeWindow = ComposeWindow(self.composeRoot)
        self.composeRoot.mainloop()

class SignInFrame(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master, bg = '#238A72')
        
        self.menuLabel = ttk.Label(self, background = '#238A72',  foreground = 'white', text = "CHANGE USER:", font = ("Arial",10, 'bold'))
        self.menuLabel.place(relx = 0.32, rely = 0.50, relwidth = 0.15, anchor = 'w')
        
        self.usersList = ttk.Combobox(self, font = ("Arial",11))
        self.usersList.place(relx = 0.53, rely = 0.30, relwidth = 0.20, relheight = 0.50)
        self.usersList['values'] = list(userDict.keys())
        self.usersList.current(1)
        global currUser
        currUser = self.usersList.get()
        self.usersList.bind("<<ComboboxSelected>>", self.callbackFunc)
    
    def callbackFunc(self, event):
        global currUser
        currUser = self.usersList.get()
        app.refreshFrames()

class TitleBar(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master, bg = "#238A72")
        
        self.titleLabel = Label(self, text = "S O C I A L   N E T W O R K", fg = 'white', bg = '#238A72', font = ("Arial", 9, 'bold'))
        self.titleLabel.place(relx = 0.02, rely = 0.5, anchor = 'w')
        
        self.name = Label(self, bg = '#ABEBC6',  fg = '#0B5345', text = "Hi! " + currUser, justify = CENTER, font = ("Arial",12,'bold'))
        self.name.place(relx = 1, rely = 0.5, relwidth = 0.4, relheight = 1, anchor = 'e')

class mainWindow():
    def __init__(self, master = None):
        self.master = master
        master.geometry("1000x600")

        self.background = ttk.Label(master, background='black')
        self.background.place(relwidth=1, relheight=1)

        self.signInFrame = SignInFrame(master)
        self.signInFrame.place(relx=0, rely=0.92, relwidth=1, relheight=0.08)

        self.titleBar = TitleBar(master)
        self.titleBar.place(relx=0, rely=0, relwidth=1, relheight=0.07)

        self.groupsFrame = GroupsFrame(master)
        self.groupsFrame.place(relx=0.60, rely=0.07, relwidth=0.20, relheight=0.77)

        self.contactsFrame = ContactsFrame(master)
        self.contactsFrame.place(relx=0.80, rely=0.07, relwidth=0.20, relheight=0.77)

        self.messagesFrame = MessagesFrame(master)
        self.messagesFrame.place(relx=0, rely=0.07, relwidth=0.60, relheight=0.85)

        self.composeFrame = ComposeFrame(master)
        self.composeFrame.place(relx=0.60, rely=0.84, relwidth=0.4, relheight=0.08)

        master.wm_title("Whats-this-App")

    def refreshFrames(self):
        self.titleBar.name.config(text = "Hi! " + currUser)
        self.contactsFrame.updateList()
        self.groupsFrame.updateList()
        self.messagesFrame.updatePosts()

class User():
    def __init__(self, userID, contactList):
        self.userID = userID
        self.incomingMessages = array([])
        self.groupIDList = array([])
        self.contactList = contactList
    
    def postToContact(self, message, recepientID, imgFileName = ""):
        message = message + "--" + self.userID + "--**"
        if(imgFileName != ""):
            message = message + "--" + imgFileName
        userDict[recepientID].incomingMessages = append(message, userDict[recepientID].incomingMessages)
    
    def postToGroup(self, message, groupID, imgFileName = ""):
        message = message + "--" + self.userID + "-- on \' " + groupID + " \'"
        if(imgFileName != ""):
            message = message + "--" + imgFileName
        for member in groupDict[groupID].memberList:
            if(member!=self.userID):
                userDict[member].incomingMessages = append(message, userDict[member].incomingMessages)
    
    # def showIncomingMessages(self):
    #     for messagePack in self.incomingMessages:
    #         message = re.split("--", messagePack)
    #         print(message[0])
    #         print("----sent by " + message[1])
    #         if message[2] != "**":
    #             print("----on group:" + message[2])

class Group():
    def __init__(self, groupID, memberList):
        self.groupID = groupID
        self.memberList = memberList

#-------------------------------global stuff-------------------------------

#----objects----

userDict = {}
groupDict = {}
currUser = None
imgs = []

#----file write / read functions----

def writeToMessagesFile():
    fout = open("messages.txt", "w")
    for user in userDict:
        fout.write(userDict[user].userID + ": ")
        for message in userDict[user].incomingMessages:
            if message :
                fout.write(message+";")
        fout.write("\n")
    fout.close

def readFromMessagesFile():
    fin = open("messages.txt", "r")
    lines = fin.readlines()
    for userAndText in lines:
        line = re.split(": ", userAndText)
        userID = line[0]
        userDict[userID].incomingMessages = re.split(';', line[1])
        userDict[userID].incomingMessages = userDict[userID].incomingMessages[:-1]
    fin.close

#----getting users and groups from social_network.txt----

f = open("social_network.txt", "r")
lines = f.readlines()
fileInfo = []
userLines = []
groupLines = []

for line in lines:
    
    if(line[0]=='<'):
        line = line[1:-1]
        if(line[len(line)-1]=='>'):
            line = line[:-1]
        fileInfo.append(re.split(", |: ",line))
    
    if(line == "#groups\n"):
        userLines = fileInfo.copy()
        fileInfo.clear()

groupLines = fileInfo

#----storing the users in a dictionary----

for user in userLines:
    userDict[user[0]] = User(user[0], array(user[1:]))

#----storing the groups in a dictionary----

for group in groupLines:
    x = 0
    for ID in group:
        if(x > 0 and ID in userDict):
            userDict[ID].groupIDList = append(userDict[ID].groupIDList, group[0])
        x += 1
    groupDict[group[0]] = Group(group[0], array(group[1:]))

#----reading 'messages.txt' and storing in <User>.incomingMessages----

readFromMessagesFile()

#----starting the user interface----

root = Tk()
for i in range(50):
    imgs.append(PhotoImage(file = ""))
app = mainWindow(root)
root.mainloop()

#----rewriting 'messages.txt' from <User>.incomingMessages----

writeToMessagesFile()