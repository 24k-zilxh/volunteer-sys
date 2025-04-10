### | All the imports | ###
import os
import datetime 
import csv
import pandas as pd
from datetime import datetime
from datetime import * 
import customtkinter as ckt
import re
from tabulate import tabulate 
from PIL import ImageTk,Image
import logging
import subprocess
### | Program-wide constants | ###
global setup_organisation_PIN
setup_organisation_PIN=3916
global all_organisations_list
all_organisations_list=[]
global Organisation_CSV_Path
global Volunteer_CSV_Path
Organisation_CSV_Path=r'\volunteersys\{p}_org.csv'  
Volunteer_CSV_Path=r'\volunteersys\vol_files\{n}{k}_vol.csv' # k is volunteer name, n is phone number 
def write_csv(givenpath,adding_target,top_row):
    with open(givenpath, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=top_row,extrasaction='ignore')
        writer.writerow({'First Name': adding_target.Firstname, 'Last Name': adding_target.LastName, 'Phone Number': adding_target.Phone, 'Address': adding_target.Address, 'Admin_ID': adding_target.Admin_ID, 'Timestamp': adding_target.Timestamp})
logging.disable(logging.CRITICAL)

ctr=0

def load_select_frm(): # loading the home frame
    global choose_opts
    choose_opts = ckt.CTkFrame(master=app, width=720, height=480)
    global w
    w = ckt.CTkLabel(choose_opts, text="Select one please")
    w.pack(padx=10, pady=10)
    addvol=ckt.CTkButton(choose_opts, text="Add Volunteer", command=add_volunteer)
    addhr=ckt.CTkButton(choose_opts, text="Add Hours", command=add_hours)
    remvol=ckt.CTkButton(choose_opts,text='Remove Volunteer', command=remove_volunteer, fg_color="#FF0000")
    snap=ckt.CTkButton(choose_opts, text="View Hours", command=volunteer_snapshot)
    repgen=ckt.CTkButton(choose_opts, text="Generate Report", command=generate_report)
    comp_csv=ckt.CTkButton(choose_opts,text="Aggregate CSVs",command=compile_csv,fg_color="#FF8C00")
    addvol.pack(padx=10,pady=10)
    addhr.pack(padx=10,pady=10)
    snap.pack(padx=10,pady=10)
    repgen.pack(padx=10,pady=10)
    w.pack(padx=10,pady=10)
    comp_csv.pack(padx=10,pady=10)
    remvol.pack(padx=10,pady=10)
    choose_opts.pack()


def compile_csv():
    frame_list = []
    for v_csv in os.listdir(r"A:\volunteersys\vol_files"):
        pt = os.path.join(r"A:\volunteersys\vol_files",v_csv)
        frame_list.append(pd.read_csv(pt))
    if len(frame_list) == 0: w.configure(text="No volunteer files found")
    else:
        full=pd.concat(frame_list, ignore_index=True)
        full_sort = full.sort_values(by="Date")
        full_sort.to_excel(r"\volunteersys\compiled_list.xlsx")

        os.startfile(r"\volunteersys\compiled_list.xlsx")
        

### | Start of program | ###

def restofproject():
    postLoginFrame.pack_forget()

    access_org_frame = ckt.CTkFrame(master=app,width=720,height=480)
    title = ckt.CTkLabel(access_org_frame, text="Enter the Organisation's name that you would like to access.")
    title.pack(padx=10, pady=10)
    access_org_frame.pack() 


    orgname=ckt.CTkEntry(access_org_frame, placeholder_text='Enter Organisation Name')
    orgname.pack(padx=10, pady=10)
    def sendof():            
            global accessable
            accessable=orgname.get()
            accessable=accessable.lower()
            global access_org
            access_org=Organisation_CSV_Path.format(p=accessable)
            
            existsa=os.path.isfile(access_org)
            if existsa == False:
                title.configure(access_org_frame, text="Please try again, that organisation does NOT exist")
                return None
            else:
                access_org_frame.forget()
                load_select_frm()

    
    abc=ckt.CTkButton(access_org_frame, text="Submit",command=sendof)
    abc.pack(padx=20, pady=10) 
    aso=ckt.CTkImage(light_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"), dark_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"),size=(70,70))
    lbll=ckt.CTkLabel(access_org_frame, text='',image=(aso))
    lbll.pack(pady=10)
    access_org_frame.mainloop()
    
    
        
class Organisation:
    def __init__(self,list_of_volunteers,name):
        self.list_of_volunteers=list_of_volunteers
        self.name=name


def setup_organisation():
        postLoginFrame.pack_forget()
        newOrgFrame = ckt.CTkFrame(master=app, width=720, height=480)

        title = ckt.CTkLabel(newOrgFrame, text="Enter your organisation's name")
        title.pack(padx=10, pady=10)

        orgname=ckt.CTkEntry(newOrgFrame, placeholder_text='Enter Organisation Name')
        orgname.pack(padx=20, pady=10)

        newOrgFrame.pack()

        def sendoff():
            a=orgname.get()
            a=a.lower()
            global Newpath_org
            Newpath_org=Organisation_CSV_Path.format(p=a)
            NewOrg=Organisation([],a)
            header_org=["Fullname","PhoneNumber","Address", "AdminID", "Timestamp"]
            try: open(Newpath_org, 'x')
            except FileExistsError: 
                title.configure(newOrgFrame, text = "That organization already exists")
                return None
            with open(Newpath_org, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header_org)
                writer.writeheader()
                title.configure(newOrgFrame, text = f"Organization named {a} has been created")
            
  
        submit=ckt.CTkButton(newOrgFrame, text="Submit",command=sendoff)
        submit.pack(padx=20, pady=10)
        
        aso=ckt.CTkImage(light_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"), dark_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"),size=(70,70))

        lbll=ckt.CTkLabel(newOrgFrame, text='',image=(aso))
        lbll.pack(pady=10)
        
        
        

def add_volunteer():

    choose_opts.forget()
    volwin = ckt.CTkFrame(master=app, width=720,height=480)

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

    volwin.pack()
    def submit():
        Phone=PH.get()
        first=FNAME.get()
        first=first.lower()
        last=LNAME.get()
        last=last.lower()
        Address=Location.get()
        Adder=Admin.get()

        PN_criteria = re.compile(r"^\d{10}$")
        condition=PN_criteria.match(Phone)


        if bool(condition) == True:  
                TimeStamp=datetime.today().strftime('%Y-%m-%d')    # HH:MIN:SECONDS
                Hours=0
                Fullname= f"{first} {last}"  
                NewVolunteer=Volunteer(Fullname,Address,Adder,TimeStamp,Hours,Phone)
                df_dstm="Date, Start Time, End Time, Admin, Name"
                newpath_vol=Volunteer_CSV_Path.format(k=Fullname,n=Phone)
                access_org=Organisation_CSV_Path.format(p=accessable)
                newvolfile = open(newpath_vol, "w")
                newvolfile.write(df_dstm)
                with open(access_org,'a') as thecsv:  
                    thecsv.write(str(NewVolunteer))                  
                labell.configure(volwin,text=f"Volunteer named {first} {last} has been added by {Adder} on {TimeStamp}")
        else: labell.configure(volwin, text="Incorrect phone number format, please enter it with 10 digits \n Please edit what you wrote and resubmit")



    newsub=ckt.CTkButton(volwin, text="Submit",command=submit)
    newsub.pack(padx=20, pady=10)
    
    aso=ckt.CTkImage(light_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"), dark_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"),size=(70,70))
    def abc():
        volwin.forget()
        load_select_frm()
    backbutton=ckt.CTkButton(volwin, text="Back", command=abc,fg_color="#808080")
    backbutton.pack(padx=20,pady=10)    
    lbll=ckt.CTkLabel(volwin, text='',image=(aso))
    lbll.pack(pady=10)
    volwin.pack()



def add_hours(): 
    choose_opts.forget()
    addhrwin = ckt.CTkFrame(master=app, width=720, height=480)
    
    label=ckt.CTkLabel(addhrwin,text="Use 24 hour time")
    label.pack(padx=10,pady=10)

    name = ckt.CTkEntry(addhrwin,placeholder_text="Name?")
    name.pack(padx=10,pady=10)
    phn = ckt.CTkEntry(addhrwin,placeholder_text="Phone #")
    phn.pack(padx=10,pady=10)
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
        nom=nom.lower()
        phone=phn.get()
        if len(str(phone)) != 10: label.configure(addhrwin, text="Enter the phone number again with only 10 digits")
        else:
            StartTime=BeginTime.get()
            CompletionTime=EndTime.get()    
            Admin=Adm.get()
            newsession=Volunteer_Session(Day,StartTime,CompletionTime,Admin,nom)
            newpath_vol=Volunteer_CSV_Path.format(k=nom,n=phone)

            if os.path.isfile(newpath_vol):
                newvolfile = open(newpath_vol, "a")
                newvolfile.write(str(newsession))
                label.configure(addhrwin,text=f"Hours have been updated for {nom}")   
            else: label.configure(addhrwin,text=f"That volunteer does not exist\nCheck the spelling or the phone #")

    hit=ckt.CTkButton(addhrwin,text='Submit',command=sumbit)
    hit.pack(padx=10,pady=12)

    def abc():
        addhrwin.forget()
        load_select_frm()
    backbutton=ckt.CTkButton(addhrwin, text="Back", command=abc,fg_color="#808080")
    backbutton.pack(padx=20,pady=10)   

    aso=ckt.CTkImage(light_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"), dark_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"),size=(70,70))
    lbll=ckt.CTkLabel(addhrwin, text='',image=(aso))
    lbll.pack(pady=10)

    addhrwin.pack()

    
    
def remove_volunteer():
    choose_opts.forget()
    removepplwin = ckt.CTkFrame(master=app, width=720, height=480)

    label=ckt.CTkLabel(removepplwin,text="WARNING: You are removing a volunteer \nThis change is IRREVERSABLE")
    label.pack(padx=10,pady=10)
    
    choice=ckt.CTkEntry(removepplwin,placeholder_text="Full name", placeholder_text_color="Red")
    choice.pack(padx=10,pady=10)
    ph_nmb = ckt.CTkEntry(removepplwin,placeholder_text="Phone number")
    ph_nmb.pack(padx=10,pady=10)
    bolol = ckt.CTkLabel(removepplwin,text="-----")
    

    def sumbit():
        nom=choice.get()
        nom=nom.lower()
        vp=ph_nmb.get()
        if len(str(vp)) != 10: label.configure(removepplwin, text="Enter the phone number again with only 10 digits")
        else: 
            del_path_vol=Volunteer_CSV_Path.format(k=nom,n=vp) ####################################--------------------------------------------------
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
    def abc():
        removepplwin.forget()
        load_select_frm()
    backbutton=ckt.CTkButton(removepplwin, text="Back", command=abc,fg_color="#808080")
    backbutton.pack(padx=20,pady=10)    
    bolol.pack(padx=10,pady=10)

    removepplwin.pack()



def volunteer_snapshot():
    choose_opts.forget()
    snapwin = ckt.CTkFrame(master=app, width=720, height=480)

    newlab=ckt.CTkLabel(snapwin,text="Enter their name", font=("Arial", 18))
    newlab.pack(padx=10,pady=10)
    namein=ckt.CTkEntry(snapwin,placeholder_text="Full Name")
    namein.pack(padx=10,pady=10)
    numin=ckt.CTkEntry(snapwin,placeholder_text="Phone Number")
    numin.pack(padx=10, pady=10)
    result=ckt.CTkLabel(snapwin,text="",font=("Arial", 20))
    result.pack(padx=10,pady=10)

    def wawa(): 
        fullnom=namein.get()
        fullnom=fullnom.lower()
        nmb = numin.get()
        if len(str(nmb)) != 10: result.configure(snapwin, text="Enter the phone number again with only 10 digits")
        else:
            orgsnappath=Organisation_CSV_Path.format(p=accessable)
            volunteer_snappath=Volunteer_CSV_Path.format(k=fullnom,n=nmb)
            try: reader=open(volunteer_snappath,'r')
            except FileNotFoundError: result.configure(snapwin,text=f"That volunteer doesn't exist")

            namenumber=open(orgsnappath,'r')
            namereader=csv.DictReader(namenumber)
            listofnames=[]        

            numlis=[]
            for j in namereader:
                listofnames.append(j['Fullname'])
                numlis.append(j["PhoneNumber"])

            try: p=listofnames.index(fullnom)
            except ValueError: result.configure(snapwin,text=f"That volunteer doesn't exist")
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
                final =timedelta(seconds=ppp)
                final= final.total_seconds()
                final=final/ 3600
                result.configure(snapwin,text=f"{fullnom.capitalize()} with phone number {numsel} has:\n{final} hours")

    sumbit=ckt.CTkButton(snapwin,text="Submit", command=wawa)
    sumbit.pack(padx=10,pady=10)

    def abc():
        snapwin.forget()
        load_select_frm()
    backbutton=ckt.CTkButton(snapwin, text="Back", command=abc,fg_color="#808080")
    backbutton.pack(padx=20,pady=10)   

    aso=ckt.CTkImage(light_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"), dark_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"),size=(70,70))
    lbll=ckt.CTkLabel(snapwin, text='',image=(aso))
    lbll.pack(padx=10,pady=10)

    snapwin.pack()
    
    ckt.set_appearance_mode("system")
    ckt.set_default_color_theme("blue")

def generate_report():
    choose_opts.forget()
    repwin = ckt.CTkFrame(master=app,width=720,height=480)
    labeler=ckt.CTkLabel(repwin,text="This will generate a TXT file containing a report of a volunteer's activities. \n You can print the report")
    labeler.pack(padx=10,pady=10)
    namein=ckt.CTkEntry(repwin,placeholder_text="Name")
    namein.pack(padx=10,pady=10)
    numberin = ckt.CTkEntry(repwin,placeholder_text="Phone #")
    numberin.pack(padx=10,pady=10)
    adm=ckt.CTkEntry(repwin,placeholder_text="Admin")
    adm.pack(padx=10,pady=10)
    def entred():   
        aaaj=numberin.get()
        jkx=namein.get()
        jkx=jkx.lower()
        newad=adm.get()
        repvolpath=Volunteer_CSV_Path.format(k=jkx,n=aaaj)

        if len(str(aaaj)) != 10: labeler.configure(repwin, text="Enter the phone number again with only 10 digits")
        else:
            try: reader=open(repvolpath,'r')
            except: labeler.configure(repwin,text=f"That volunteer doesn't exist\nCheck their phone #")

            reportgen=csv.DictReader(reader)

            starttimess=[]
            endtimess=[]
            dates=[]
            admins=[]
            listhr=[]

            for p in reportgen:

                dates.append(p['Date'])
                starttimess.append(str(p[' Start Time']))
                endtimess.append(str(p[' End Time']))
                admins.append(p[' Admin'])
            
            for j in range(0,len(starttimess)):
                x=starttimess[j]
                y=endtimess[j]
                beg = datetime.strptime(x, '%H:%M')
                end = datetime.strptime(y, '%H:%M')
                res=end-beg
                res=res.total_seconds()
                res=res/3600
                listhr.append(res)
                

            waa=fr'\volunteersys\{jkx}_report.txt'  
            
            
            datas=[["Date","Start Time","End Time","Hours","Admin"]]

            for hh in range (len(dates)):
                apender=[dates[hh],starttimess[hh],endtimess[hh],listhr[hh],admins[hh]]
                datas.append(apender)
            datas.append(["","","",sum(listhr),""])
            
            tabels = tabulate(datas, headers="firstrow", tablefmt="fancy_grid")

            with open(waa, 'w', encoding="utf-8") as f:
                f.write(f"Volunteer report on {jkx}, requested by {newad}\n \n")
                f.write(tabels)         
                f.write(f"\n\nGenerated by the volunteersys on {datetime.today().strftime('%Y-%m-%d')}")
                f.close()

            repwin.forget()
            x=[]
            with open(Volunteer_CSV_Path.format(k=jkx,n=aaaj), 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    x.append(row)

            grid_view = ckt.CTkScrollableFrame(master=app) 
            grid_view.pack(expand=True, fill="both",padx=20,pady=20,anchor="center")
            grid_view.grid_columnconfigure(5, weight=1)
            grid_view.grid_rowconfigure(len(x)+1, weight=1)

            
            for a in range(len(x)):
                    for b in range(5):
                            xp = ckt.CTkLabel(grid_view,text=x[a][b]) 
                            xp.grid(row=a,column=b)
            def abc():
                grid_view.pack_forget()
                load_select_frm()
            def prt():        
                os.startfile(waa,'print')

            pbtn=ckt.CTkButton(grid_view, text="Print", command=prt, fg_color="#cc6666")
            pbtn.grid(row=len(x)+1,column=2)  

            backbutton=ckt.CTkButton(grid_view, text="Back", command=abc,fg_color="#808080")
            backbutton.grid(row=len(x)+1,column=4)  
    
    entre=ckt.CTkButton(repwin, text='Submit', command=entred)
    entre.pack(padx=10,pady=10)
    def abc():
        repwin.forget()
        load_select_frm()

    backbutton=ckt.CTkButton(repwin, text="Back", command=abc,fg_color="#808080")
    backbutton.pack(padx=20,pady=10)   
    aso=ckt.CTkImage(light_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"), dark_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"),size=(70,70))
    lbll=ckt.CTkLabel(repwin, text='',image=(aso))
    lbll.pack(pady=10)
    repwin.pack()

class Volunteer_Session:
    def __init__(self,date,start_time,end_time,admin,name):
        self.date=date
        self.start_time=start_time
        self.end_time=end_time
        self.admin=admin
        self.name = name
    def __str__(self):
        return (f'\n{self.date},{self.start_time},{self.end_time},{self.admin},{self.name}') 
    
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
    app.title("volunteersys")

    global postLoginFrame

    postLoginFrame = ckt.CTkFrame(master=app, width=720, height=480)
   
    logo=ckt.CTkImage(light_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"),dark_image=Image.open(r"Z:\Nikon-1-V3-sample-photo.jpg"),size=(70,70))
    imageLabel=ckt.CTkLabel(postLoginFrame, text='',image=(logo))
    imageLabel.pack(pady=10)

    title = ckt.CTkLabel(postLoginFrame, text="Welcome to the volunteersys")
    title.pack(padx=10, pady=10)

    setupNewOrg=ckt.CTkButton(postLoginFrame, text="Create New Organisation",command=setup_organisation)
    accessOrg=ckt.CTkButton(postLoginFrame, text="Access Existing Organisation",command=restofproject, fg_color="#35530A")

    accessOrg.pack(padx=20, pady=10)    
    setupNewOrg.pack(padx=10, pady=10)

    postLoginFrame.pack(padx=20, pady=20)


    app.mainloop()

codebegin()

# Program written by 24k-zilxh on GitHub
# Python 3.12.7
