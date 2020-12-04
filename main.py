
from flask import render_template 
from flask import Flask 
from flask import request 
from pyowm.owm import OWM
import requests
import time
import sched
import datetime 
from uk_covid19 import Cov19API
import threading
import pyttsx3
import json
import os

app= Flask(__name__,template_folder='template')



@app.route('/index')
def index():
   
    """Inside this function are functions called that are needed in the app route,
    this function returns the render template"""
    close_notif()
    get_time() 
    update_label()
    return render_template("index.html",title="Daily Update",notifications=listfornotification,alarms=listforalarm,image="alarm.png" )
    
    
listfornotification=[{'title':'','content':''}]
listforalarm=[{'title':'','content':''}]
 
 """So the Alarm and Notification list don't return and empty element in the list """
listfornotification=[]
listforalarm=[]
 
 """To find the number of elements in the Alarm and Notification list for deletion"""
a=len(listforalarm)
n=len(listfornotification)

def weather():
    """Opens Config file to get information useful to this function"""
    script_dir=os.path.dirname(__file__)
    relative='/config.json'
    combined_file_path=script_dir+relative
    with open(combined_file_path,'r') as config:
        data=json.load(config)
    
    """Returns Notification list with contents of The Weather Update"""
    
    owm = OWM(data['APIWEATHERNEWS'])
    mgr = owm.weather_manager()
    location=data['WEATHERLOCATION'] #location is here
    observation = mgr.weather_at_place(location)  #observation object is a box containing a weather object
    weather = observation.weather
    status=weather.detailed_status  #detailed  status
    temperature = weather.temperature('celsius')#temperature in Celsius
    finaltemp=(str(int(temperature['temp'])))#gets temp alone from the list and converts it to a string
    final='The temperature today in '+location+' is ' + finaltemp+'°C' ' and today will have ' + status#cleans up the final output
    return listfornotification.append({'title':"Weather Update",'content':final})
    

def tts_request(announcement):
    engine = pyttsx3.init()
    engine.say(announcement)
    engine.runAndWait()
    return "Hello text-to-speech example"   

def close_notif():
    close_notifs=request.args.get('notif')
    if close_notifs:
        del listfornotification[n]
        


def covid_update():
    script_dir=os.path.dirname(__file__)
    relative='/config.json'
    combined_file_path=script_dir+relative
    with open(combined_file_path,'r') as config:
        data=json.load(config)
    Area=[
    'areaName=Exeter'
    ] 
    cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeathsByDeathDate": "newDeathsByDeathDate",
    "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }
    apiforarea = Cov19API(
    filters=Area,
    structure=cases_and_deaths,
    latest_by="newCasesByPublishDate"
    )
    
    Areadata= apiforarea.get_json()
   
    
    finalAreadata=Areadata['data']
    newcasesbydate=finalAreadata[0]['newCasesByPublishDate']
    newcasestotal=finalAreadata[0]['cumCasesByPublishDate']
    newseathstoday=finalAreadata[0]['newDeathsByDeathDate']
    totaldeath=finalAreadata[0]['cumDeathsByDeathDate']
    strnewcasesbydate=str(newcasesbydate)
    strnewcasestotal=str(newcasestotal)
    strnewdeathstoday=str(newseathstoday)
    strtotaldeath=str(totaldeath)
    

    finalcovid=("In your area there has been "+ strnewcasesbydate +" cases, and a total of "+ strnewcasestotal + " new cases. For deaths there have been "+strnewdeathstoday+" today, and in total there have been "+strtotaldeath+".")
    return listfornotification.append({'title':"Covid Update",'content':finalcovid})
    


def news():
    script_dir=os.path.dirname(__file__)
    relative='/config.json'
    combined_file_path=script_dir+relative
    with open(combined_file_path,'r') as config:
        data=json.load(config)
    API_KEY = data['APIKEYNEWS']
    params = {'q': 'corona virus','source': 'bbc-news','sortBy': 'top','language': 'en',}
    headers = {'X-Api-Key': API_KEY} 
    url = 'https://newsapi.org/v2/top-headlines'
    response = requests.get(url, params=params, headers=headers)
    responsedata = response.json()
    article = responsedata["articles"] 
    results = [arr["title"] for arr in article]
    finalresults=((results[1]),results[2],results[3],results[4],results[5],results[6])
    resultsinline=("‎‎                                          ☞ ".join(finalresults))
    return listfornotification.append({'title':"Top Headlines",'content':resultsinline})
    
    


def clock():
    yearnow=str(datetime.datetime.now().year)
    monthnow=str(datetime.datetime.now().month).zfill(2)
    datenow=str(datetime.datetime.now().day)
    hournow=str(datetime.datetime.now().hour).zfill(2)
    minutenow=str(datetime.datetime.now().minute).zfill(2)
    fulldatenow="0"+datenow+"-"+monthnow+"-"+yearnow+" at "+hournow+":"+minutenow
    return('You have an alarm set for '+fulldatenow)

def notif_update():
    if str(datetime.datetime.now().minute).zfill(2)=="59":
        news()
        weather()
    

def get_time():
        alarm_time=request.args.get('alarm')
        close=request.args.get('alarm_item')
        label=update_label()
        
        
        

        while alarm_time:
            news_inc=news_inc=request.args.get('news')
            weather_inc=weather_inc=request.args.get('weather')
            year=alarm_time[0]+alarm_time[1]+alarm_time[2]+alarm_time[3]
            month=alarm_time[5]+alarm_time[6]
            date=alarm_time[8]+alarm_time[9]
            hour=alarm_time[11]+alarm_time[12]
            minute=alarm_time[14]+alarm_time[15]
            fulldate=date+"-"+month+"-"+year+" at "+hour+":"+minute
            if alarm_time and not news_inc and not weather_inc:
                return listforalarm.append({'title':label,'content':'You have an alarm set for '+fulldate})
            if alarm_time and news_inc and not weather_inc:
                return listforalarm.append({'title':label,'content':'You have an alarm set for '+fulldate+" with "+news_inc})
            if alarm_time and weather_inc and not news_inc:
                return listforalarm.append({'title':label,'content':'You have an alarm set for '+fulldate+" with "+weather_inc})
            if alarm_time and news_inc and weather_inc:
                return listforalarm.append({'title':label,'content':'You have an alarm set for '+fulldate+" with "+news_inc+" and "+weather_inc})
                

        else:
            if close:
                del listforalarm[a]
        
        
            
            def do_alarm():
                if clock()==listforalarm[0]['content']:
                        covid_update()
                        tts_request("You have an Alarm Update")
                        del listforalarm[0]

                if clock()+" with news"==listforalarm[0]['content']:
                        news()
                        covid_update()
                        tts_request("You have an Alarm Update")
                        del listforalarm[0]
                
                if clock()+" with weather"==listforalarm[0]['content']:
                        weather()
                        covid_update()
                        tts_request("You have an Update")
                        del listforalarm[0]
                        
                if clock()+" with news and weather"==listforalarm[0]['content']:
                        news()
                        weather()
                        covid_update()
                        tts_request("You have an Update")
                        del listforalarm[0]

                        
                  
            def alarm_run():
                while True:
                    notif_update()
                    (do_alarm())
                    time.sleep(59)
                    
            thread = threading.Thread(target=alarm_run)
            thread.start()

                    
def update_label():
   label=request.args.get('two')
   if label:
       return label



if __name__=='__main__':
    app.run()
            

    
            
            
            







    

    
   
        
        
    