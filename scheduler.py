import schedule 
import time 
from twitter import *


global i

i=0

def update_word_cloud():
    global i
    print("hiiiii")
    i=i+1
    if(i==3):
        schedule.clear()

#schedule.every(6).hours.do(update_word_cloud) 

schedule.every(3).minutes.do(func_twitter) 

# Loop so that the scheduling task 
# keeps on running all time. 
while True: 
  
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending() 
    time.sleep(1)
    


