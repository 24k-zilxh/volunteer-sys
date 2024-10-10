import sys
import os
import datetime 
import csv
import pandas as pd
from datetime import datetime
from datetime import *
import customtkinter as ckt
import re


### | Start of program | ###


global setup_organisation_PIN
setup_organisation_PIN=3916
global all_organisations_list
all_organisations_list=[]
global Organisation_CSV_Path
global Volunteer_CSV_Path
Organisation_CSV_Path='C:\\Users\\abhir\\OneDrive\\Education\\Computer Science\\Python\\Projects\\Volunteer System\\{p}_org.csv' #RECODE PATH MAKE SURE TO KEEP THE _org 
Volunteer_CSV_Path='C:\\Users\\abhir\\OneDrive\\Education\\Computer Science\\Python\\Projects\\Volunteer System\\{k}_vol.csv' #RECODE PATH, MAKE SURE TO KEEP THE _vol
def write_csv(givenpath,adding_target,top_row):
    with open(givenpath, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=top_row,extrasaction='ignore')
        writer.writerow({'First Name': adding_target.Firstname, 'Last Name': adding_target.LastName, 'Phone Number': adding_target.Phone, 'Address': adding_target.Address, 'Admin_ID': adding_target.Admin_ID, 'Timestamp': adding_target.Timestamp})

# "First Name, Last Name,Phone Number,Address, Admin ID, Timestamp"
def restofproject():

    app.destroy()
    ckt.set_appearance_mode("system")
    ckt.set_default_color_theme("blue")
    restwin = ckt.CTk()
    restwin.geometry("720x480")
    restwin.title("EZ Volunteer System-Access")
    title = ckt.CTkLabel(restwin, text="Enter the Organisation's name that you would like to access.")
    title.pack(padx=10, pady=10)
    orgname=ckt.CTkEntry(restwin, placeholder_text='Enter Organisation Name')
    orgname.pack(padx=10, pady=10)
    def sendof():            
            global accessable
            accessable=orgname.get()
            global access_org
            access_org=Organisation_CSV_Path.format(p=accessable)
            
            existsa=os.path.isfile(access_org)
            if existsa == False:
                title.configure(restwin, text="Please try again, that organisation doesnt exist")
                return None

            restwin.destroy() # THIS MAY BE AN ISSUE
            ckt.set_appearance_mode("system")
            ckt.set_default_color_theme("blue")
            choxwin = ckt.CTk()
            choxwin.geometry("720x480")
            choxwin.title("EZ Volunteer System-Access")
            w = ckt.CTkLabel(choxwin, text="Select one please")
            w.pack(padx=10, pady=10)
            addvol=ckt.CTkButton(choxwin, text="Add Volunteer", command=add_volunteer)
            addhr=ckt.CTkButton(choxwin, text="Add Hours", command=add_hours)
            remvol=ckt.CTkButton(choxwin,text='Remove Volunteer', command=remove_volunteer)
            snap=ckt.CTkButton(choxwin, text="View Hours", command=volunteer_snapshot)
            addvol.pack(padx=10,pady=10)
            addhr.pack(padx=10,pady=10)
            remvol.pack(padx=10,pady=10)
            snap.pack(padx=10,pady=10)
            choxwin.mainloop()
    
    abc=ckt.CTkButton(restwin, text="Submit",command=sendof)
    abc.pack(padx=20, pady=10) 
    restwin.mainloop()
    
    
        
class Organisation:
    def __init__(self,list_of_volunteers,name):
        self.list_of_volunteers=list_of_volunteers
        self.name=name


def setup_organisation():
        app.destroy()
        ckt.set_appearance_mode("system")
        ckt.set_default_color_theme("blue")

        setupwin = ckt.CTk()
        
        setupwin.geometry("720x480")
        setupwin.title("EZ Volunteer System")

        title = ckt.CTkLabel(setupwin, text="Enter your organisation's name")
        title.pack(padx=10, pady=10)

        orgname=ckt.CTkEntry(setupwin, placeholder_text='Enter Organisation Name')
        orgname.pack(padx=20, pady=10)

        def sendoff():
            a=orgname.get()
            global Newpath_org
            Newpath_org=Organisation_CSV_Path.format(p=a)
            NewOrg=Organisation([],a)
            header_org=["Fullname","PhoneNumber","Address", "AdminID", "Timestamp"]
            with open(Newpath_org, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header_org)
                writer.writeheader()
            try:
                setupwin.destroy()
            except: pass 
  
        submit=ckt.CTkButton(setupwin, text="Submit",command=sendoff)
        submit.pack(padx=20, pady=10)
        setupwin.mainloop()
        

def add_volunteer():

    ckt.set_appearance_mode("system")
    ckt.set_default_color_theme("blue")
    volwin = ckt.CTk()
    volwin.geometry("720x480")
    volwin.title("EZ Volunteer System-Volunteer Create")
    labell = ckt.CTkLabel(volwin, text="Please fill in all fields about the volunteer")
    labell.pack(padx=10, pady=10)

    FNAME=ckt.CTkEntry(volwin, placeholder_text='First Name')
    FNAME.pack(padx=20, pady=10)
    LNAME=ckt.CTkEntry(volwin, placeholder_text='Last Name')
    LNAME.pack(padx=20, pady=10)
    Location=ckt.CTkEntry(volwin, placeholder_text='Address (123 Countryside Drive)')
    Location.pack(padx=20, pady=10)    
    PH=ckt.CTkEntry(volwin, placeholder_text='Phone Number 123-456-7890')
    PH.pack(padx=20, pady=10)  
    Admin=ckt.CTkEntry(volwin, placeholder_text='Admin Name')
    Admin.pack(padx=20, pady=10)
    def submit():
        first=FNAME.get()
        last=LNAME.get()
        Address=Location.get()
        Adder=Admin.get()
        Phone=PH.get()

        PN_criteria = re.compile(r"^\d{10}$")
        condition=PN_criteria.match(Phone)


        if bool(condition) == True:  
                TimeStamp=datetime.today().strftime('%Y-%m-%d')    # HH:MIN:SECONDS
                Hours=0
                Fullname= f"{first} {last}"  
                NewVolunteer=Volunteer(Fullname,Address,Adder,TimeStamp,Hours,Phone)
                df_dstm="Date, Start Time, End Time, Admin"
                newpath_vol=Volunteer_CSV_Path.format(k=Fullname)
                access_org=Organisation_CSV_Path.format(p=accessable)
                newvolfile = open(newpath_vol, "w")
                newvolfile.write(df_dstm)
                with open(access_org,'a') as thecsv: #Newpath org is not defined, 
                    thecsv.write(str(NewVolunteer))                  
                labell.configure(volwin,text=f"Volunteer named {first} {last} has been added by {Adder} on {TimeStamp}")
        else:
            labell.configure(volwin, text="Incorrect phone number format, please enter it with 10 digits \n Please edit what you wrote and resubmit")
            
    newsub=ckt.CTkButton(volwin, text="Submit",command=submit)
    newsub.pack(padx=20, pady=10)
    volwin.mainloop()


def add_hours(): 
    ckt.set_appearance_mode("system")
    ckt.set_default_color_theme("blue")
    addhrwin = ckt.CTk()
    
    addhrwin.geometry("720x480")
    addhrwin.title("EZ Volunteer System-Add Hours")
    label=ckt.CTkLabel(addhrwin,text="Use 24 hour time")
    label.pack(padx=10,pady=10)
    name = ckt.CTkEntry(addhrwin,placeholder_text="Name?")
    name.pack(padx=10,pady=10)
    Day=datetime.today().strftime('%Y-%m-%d')
    BeginTime=ckt.CTkEntry(addhrwin,placeholder_text="Start Time")
    BeginTime.pack(padx=10,pady=10)
    EndTime=ckt.CTkEntry(addhrwin,placeholder_text="End Time")
    EndTime.pack(padx=10,pady=10)
    Adm=ckt.CTkEntry(addhrwin,placeholder_text="Admin")
    Adm.pack(padx=10,pady=12)
    def sumbit():
        global nom
        nom=name.get()
        StartTime=BeginTime.get()
        CompletionTime=EndTime.get()    
        Admin=Adm.get()
        newsession=Volunteer_Session(Day,StartTime,CompletionTime,Admin)
        newpath_vol=Volunteer_CSV_Path.format(k=nom)
        newvolfile = open(newpath_vol, "a")
        newvolfile.write(str(newsession))
        label.configure(addhrwin,text=f"Hours have been updated for {nom}")    
    hit=ckt.CTkButton(addhrwin,text='Submit',command=sumbit)
    hit.pack(padx=10,pady=12)
    addhrwin.mainloop()

    
    
def remove_volunteer():
    ckt.set_appearance_mode("system")
    ckt.set_default_color_theme("blue")
    removepplwin = ckt.CTk()
    removepplwin.geometry("720x480")
    removepplwin.title("EZ Volunteer System - Remove Volunteer")    
    label=ckt.CTkLabel(removepplwin,text="You are removing a volunteer, fill in the fields")
    label.pack(padx=10,pady=10)
    choice=ckt.CTkEntry(removepplwin,placeholder_text="Full name", placeholder_text_color="Red")
    choice.pack(padx=10,pady=10)
    def sumbit():
        nom=choice.get()
        del_path_vol=Volunteer_CSV_Path.format(k=nom)
        x=os.path.isfile(del_path_vol)
        if x==True:
            os.remove(del_path_vol)
            df = pd.read_csv(access_org)
            df = df.drop(df[df.Fullname == nom].index)
            df.to_csv(access_org, index=False)
            label.configure(removepplwin,text=f"Volunteer named {nom} has been deleted")
        else:
            label.configure(removepplwin,text="That volunteer wasn't found, check spelling or maybe they don't exist.")
    
    hit=ckt.CTkButton(removepplwin,text='Submit',command=sumbit)
    hit.pack(padx=10,pady=13)
    removepplwin.mainloop()



def volunteer_snapshot():
    ckt.set_appearance_mode("system")
    ckt.set_default_color_theme("blue")
    snapwin = ckt.CTk()
    snapwin.geometry("720x480")
    snapwin.title("EZ Volunteer System-View Hours")
    newlab=ckt.CTkLabel(snapwin,text="Enter their name")
    newlab.pack(padx=10,pady=10)
    namein=ckt.CTkEntry(snapwin,placeholder_text="Name")
    namein.pack(padx=10,pady=10)
    def wawa(): 
        fullnom=namein.get()
        orgsnappath=Organisation_CSV_Path.format(p=accessable)
        volunteer_snappath=Volunteer_CSV_Path.format(k=fullnom)
        try: reader=open(volunteer_snappath,'r')
        except FileNotFoundError: newlab.configure(snapwin,text=f"That volunteer doesn't exist")

        namenumber=open(orgsnappath,'r')
        namereader=csv.DictReader(namenumber)
        listofnames=[]        

        numlis=[]
        for j in namereader:
            listofnames.append(j['Fullname'])
            numlis.append(j["PhoneNumber"])

        p=listofnames.index(fullnom)

        numsel=numlis[p]

        dreader=csv.DictReader(reader)
        starttimes=[]
        endtimes=[]
        listofhrs=[]
        for i in dreader:
            starttimes.append(i[' Start Time'])
            endtimes.append(i[' End Time'])

        for j in range(0,len(starttimes)):
            x=starttimes[j]
            y=endtimes[j]
            beg = datetime.strptime(x, '%H:%M')
            end = datetime.strptime(y, '%H:%M')
            res=end-beg
            listofhrs.append(res)
            ppp=[]
            for d in listofhrs:
                ppp.append(d.seconds)
            ppp=sum(ppp)
            final =str(timedelta(seconds=ppp))
            newlab.configure(snapwin,text=f"The amount of hours that {fullnom} has volunteered for is> {final} \nTheir phone number is {numsel}")
    sumbit=ckt.CTkButton(snapwin,text="Submit", command=wawa)
    sumbit.pack(padx=10,pady=10)
    snapwin.mainloop()


    ckt.set_appearance_mode("system")
    ckt.set_default_color_theme("blue")



class Volunteer_Session:
    def __init__(self,date,start_time,end_time,admin):
        self.date=date
        self.start_time=start_time
        self.end_time=end_time
        self.admin=admin
    def __str__(self):
        return (f'\n{self.date},{self.start_time},{self.end_time},{self.admin}') 
    
class Volunteer:
    def __init__(self,Fullname,Address,Admin_ID,Timestamp,hours,Phone):
        self.Fullname=Fullname
        self.Address=Address
        self.Admin_ID=Admin_ID
        self.Timestamp=Timestamp
        self.hours=hours
        self.Phone=Phone
    def __str__(self):
        return (f'\n{self.Fullname},{self.Phone},{self.Address},{self.Admin_ID},{self.Timestamp}') 

def codebegin():
    global app
    app = ckt.CTk()
    app.geometry("720x480")
    app.title("EZ Volunteer System")

    title = ckt.CTkLabel(app, text="Welcome to the EZ Volunteer System.")
    title.pack(padx=10, pady=10)

    setup=ckt.CTkButton(app, text="Create New Organisation",command=setup_organisation)
    exist=ckt.CTkButton(app, text="Access Existing Organisation",command=restofproject)

    setup.pack(padx=10, pady=10)
    exist.pack(padx=20, pady=10)
    app.mainloop()

codebegin()


# Program written by Abhiram Vadali
# Python 3.12
# For Windows
# 9/3/2024
