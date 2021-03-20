from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import datetime
import os
import time
import random
import csv
from pygame import mixer
import pandas as pd 
import numpy as np




root=Tk()
root.title('Alarm Clock')
root.geometry("400x200")
frame1 = ttk.Frame(root)
frame1.pack()
frame1.config(height = 500, width = 500)

# HOUR
labelh= ttk.Label(frame1,text = "Enter HOUR in 24-Hour Format: ")
labelh.pack()
entryh = ttk.Entry(frame1, width = 30)
entryh.pack()

# MINUTE
labelm= ttk.Label(frame1,text = "Enter MINUTES: ")
labelm.pack()
entrym = ttk.Entry(frame1, width = 30)
entrym.pack()

# SECOND
labels= ttk.Label(frame1,text = "Enter SECONDS: ")
labels.pack()
entrys = ttk.Entry(frame1, width = 30)
entrys.pack()

labels= ttk.Label(frame1,text = "*************************************")
labels.pack()


def SubmitAction():
    # getting the current path of script 
    path=os.getcwd()

    # setting alarm path
    alarm_path=path+'\Alarm_ringtones'

    # to create alarm path if not present in working folder
    if not os.path.isdir(alarm_path):
        os.makedirs(alarm_path)

    # adds tunes to Alarm_path if its empty 
    while len(os.listdir(alarm_path))==0:
        print("NO Alarm ringtones in Alarm_ringtones folder please add some to proceed")
        confirm=input("Have you added ringtones? Press Y or N:  ")
        if (confirm=="Y"):
            print('OK lets Continue!')
            break
        else:
            continue

    def List_difference(list1,list2):
        if len(list1)>=len(list2):
            return (list(set(list1)-set(list2)))
        else:
            return (list(set(list2)-set(list1)))

    # create CSV file to store data
    if not os.path.isfile("ringtone_parameters.csv"):
        ringtone_list=os.listdir(alarm_path)
        ringtone_time=[60]*len(ringtone_list)
        ringtone_counter=[1]*len(ringtone_list)
        ringtone_avg=[60]*len(ringtone_list)
        ringtone_prob_reverse=[1/len(ringtone_list)]*len(ringtone_list)
        ringtone_prob=[1/len(ringtone_list)]*len(ringtone_list)

    #if CSV file is present already then read from it
    else:
        ringtone_df = pd.read_csv("ringtone_parameters.csv")
        ringtone_list_os = os.listdir(alarm_path)
        ringtone_list = list(ringtone_df['Tunes'])
        ringtone_diff = List_difference(ringtone_list_os, ringtone_list)
        ringtone_time = list(ringtone_df['Delay Times'])
        ringtone_counter = list(ringtone_df['Count'])
        ringtone_avg = list(ringtone_df['Average'])
        ringtone_prob_reverse = list(ringtone_df['Reverse Probability'])
        ringtone_prob = list(ringtone_df['Probability']) 

        if len(ringtone_list_os)>=len(ringtone_list):
            for i in range(0,len(ringtone_diff)):
                ringtone_list.append(ringtone_diff[i])
                ringtone_time.append(60)
                ringtone_counter.append(1)
                ringtone_avg.append(60)
                ringtone_prob_reverse.append(0.1)
                ringtone_prob.append(0.1)
    
        else:
            for i in range(0,len(ringtone_diff)):
                ringtone_diff_index = ringtone_list.index(ringtone_diff[i])
                ringtone_list.pop(ringtone_diff_index)
                ringtone_time.pop(ringtone_diff_index)
                ringtone_counter.pop(ringtone_diff_index)
                ringtone_avg.pop(ringtone_diff_index)
                ringtone_prob_reverse.pop(ringtone_diff_index)
                ringtone_prob.pop(ringtone_diff_index)
    
        avg_sum = sum(ringtone_avg)
    
        for i in range(0,len(ringtone_prob_reverse)):
            ringtone_prob_reverse[i] = 1 - ringtone_avg[i]/avg_sum
    
        avg_prob = sum(ringtone_prob_reverse)
    
        for i in range(0,len(ringtone_prob)):
            ringtone_prob[i] = ringtone_prob_reverse[i]/avg_prob
    
    # verify user entered time is correct or not
    def verify_alarm(hour,minute,seconds):
        if((hour>=0 and hour<=23) and (minute>=0 and minute<=59) and (seconds>=0 and seconds<=59)):
            return True
        else:
            return False
            


    # setting Alarm time and verifying it 
    while(True):
        hour = int(entryh.get())
        minute = int(entrym.get())
        seconds = int(entrys.get())
        if verify_alarm(hour,minute,seconds):
            break 
        else:
            print("Error: Wrong Time Entered! Please enter again!")
            

    # Converting the alarm time to seconds
    alarm_sec = hour*3600 + minute*60 + seconds

    # Getting the current time and converting it to seconds
    curr_time = datetime.datetime.now()
    curr_sec = curr_time.hour*3600 + curr_time.minute*60 + curr_time.second
    print(curr_time)

    # Calculating the number of seconds left for alarm
    time_diff = alarm_sec - curr_sec

    #If time difference is negative, it means the alarm is for next day so add total seconds in one day
    if time_diff < 0:
        time_diff += 86400

    # Displaying the time left for alarm
    #print("Time left for alarm is %s" % datetime.timedelta(seconds=time_diff))
    messagebox.showinfo(title= 'Alarm Message', message= "Time left for alarm is %s" % datetime.timedelta(seconds=time_diff))

    # Sleep until the time at which alarm rings
    time.sleep(time_diff)
    # my code starts...............
    # Alarm ringing Message
    print("Alarm time! Wake up! Wake up!")             #it will print ("Alarm time! Wake up! Wake up!")

    # Choose a ringtone based on probability  
    # choose a ringtone randomly by using numpy.random.choice from the csv file of ringtone lists          
    ringtone_choice_np = np.random.choice(ringtone_list, 1, ringtone_prob)
    ringtone_choice = ringtone_choice_np[0]

    # Getting the index of chosen ringtone in list
    # knowing the index of the ringtone choosen from the csv file to play the music,so we are using the index funtion to ringtone_choice. 
    ringtone_index = ringtone_list.index(ringtone_choice)

    # Play the alarm tune
    # playing the ringtone
    # in the alarm path length is zero then it shows there is no song to play .add the song to continue.
    #press y if added or press N to not added .
    mixer.init()
    mixer.music.load(alarm_path+"/"+ringtone_choice)

    # Setting loops=-1 to ensure that alarm only stops when user stops it!
    mixer.music.play(loops=-1)  # this code is to not stop the song upto the user press enter to stop so its loop and again .
    # Asking user to stop the alarm
    input("Press ENTER to stop alarm")  # if hi/she press enter then the alarm stops .
    mixer.music.stop()   # the code for stopping the music or song

    # Finding the time of stopping the alarm
    # after the pressing the enter to stop the alarm the time stores in csv file
    time_stop = datetime.datetime.now()
    stop_sec = time_stop.hour*3600 + time_stop.minute*60 + time_stop.second

    # Calculating the time delay
    time_delay = stop_sec - alarm_sec #time after the alarm rings and user stops

    # Updating the values
    ringtone_time[ringtone_index] += time_delay #updating the time deay and all the things foe next alarm time
    ringtone_counter[ringtone_index] += 1
    ringtone_avg[ringtone_index] = ringtone_time[ringtone_index] / ringtone_counter[ringtone_index]

    new_avg_sum = sum(ringtone_avg)
    for i in range(0,len(ringtone_list)):
        ringtone_prob_reverse[i] = 1 - ringtone_avg[i] / new_avg_sum
    
    new_avg_prob = sum(ringtone_prob_reverse)
    
    for i in range(0,len(ringtone_list)):
        ringtone_prob[i] = ringtone_prob_reverse[i] / new_avg_prob

    #Create the merged list of all six quantities
    ringtone_rec = [[[[[[]]]]]]   
    for i in range (0,len(ringtone_list)):
        temp=[]  #updating the the temp values in the exal sheet 
        temp.append(ringtone_list[i]) #appending the ringtone_list
        temp.append(ringtone_time[i])
        temp.append(ringtone_counter[i])
        temp.append(ringtone_avg[i])
        temp.append(ringtone_prob_reverse[i])
        temp.append(ringtone_prob[i])
        ringtone_rec.append(temp)
    ringtone_rec.pop(0)
    #Convert merged list to a pandas dataframe
    #conversion of all the data into pandas data frame
    df = pd.DataFrame(ringtone_rec, columns=['Tunes','Delay Times','Count','Average','Reverse Probability','Probability'],dtype=float)

    #Save the dataframe as a csv (if already present, will overwrite the previous one)
    df.to_csv('ringtone_parameters.csv',index=False) #if the data saved is already exits it overwrites the previous one
    

button1= ttk.Button(frame1, text= "SET", command=SubmitAction)
button1.pack()
root.mainloop()
