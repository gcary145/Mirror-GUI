######################### Libraries #######################################################################################################################################
import datetime as dt
import json
import requests
import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import ImageTk, Image

gui = tk.Tk(className= 'Smart Mirror GUI')
gui.geometry("800x480") #resolution
gui.configure(bg='black') #default background

############################## Images #####################################################################################################################################

# Heart Image

HeartImage = Image.open('./Heart.gif')
Heart = ImageTk.PhotoImage(HeartImage)
Heartdisplay = Label(image=Heart, bg = 'black')

# Heart Image Does Not Update based on Variables, So It Can Be Implemented Now

Heartdisplay.grid(row=0,column=0,pady=4)

# Calendar Image

CalendarImage = Image.open('./Calendar.gif')
Calendar = ImageTk.PhotoImage(CalendarImage)
Calendardisplay = Label(image=Calendar, bg = 'black')

# Calendar Image Does Not Update based on Variables, So It Can Be Implemented Now

Calendardisplay.grid(row=1,column=0,pady=4)

# Clock Image

ClockImage = Image.open('./Clock.gif')
Clock = ImageTk.PhotoImage(ClockImage)
Clockdisplay = Label(image=Clock, bg = 'black')

# Clock Image Does Not Update based on Variables, So It Can Be Implemented Now

Clockdisplay.grid(row=2,column=0,pady=4)

# Thermometer Images for Temperature and Feels Like

ThermometerHotImage = Image.open('./ThermometerHot.gif')
ThermometerHot = ImageTk.PhotoImage(ThermometerHotImage)

ThermometerColdImage = Image.open('./ThermometerCold.gif')
ThermometerCold = ImageTk.PhotoImage(ThermometerColdImage)

# Setting Default Thermomoter Image as the ThermometerHotImage, is configured to change later in showWeather()
Thermometerdisplay = Label(image=ThermometerHot, bg = 'black')
Thermometerdisplay.grid(row=3,column=0,pady=4)

############################## Date and Time #############################################################################################################################

# Fetching date and time information
global date
date = dt.datetime.now()

# Creating label for the day "monday, tuesday, etc."
global daydisplay 
daydisplay = Label(gui, text=f"{date:%A}", fg = "white", bg = "black", font = ('Courier', 45, 'bold'), justify = LEFT)
daydisplay.grid(row=0,column=1,sticky=W,pady=4)

# Creating label for the date "Month, Numeric Day, Year"
global datedisplay
datedisplay = Label(gui, text=f"{date:%B %d, %Y}", fg = "white", bg = "black", font = ('Courier', 45, 'bold'), justify = LEFT)
datedisplay.grid(row=1,column=1,sticky=W,pady=4)

# Creating label for the time
global timedisplay 
timedisplay = Label(gui, text=f"{date:%I:%M}", fg = "white" , bg = "black" , font = ('Courier', 45, 'bold'), justify = LEFT)
timedisplay.grid(row=2,column=1,sticky=W,pady=4)

############################## Weather ##################################################################################################################################

# Counter for Update function to trigger Weather Update every ten minutes
i = 0

# Setting the time zone
def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()

# Gathering weather data
def showWeather():
    #API
    api_key = "" #insert API key
 
    #City Name
    global city_name
    city_name = "Shreveport"
 
    # API url
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid='+api_key
    
    # url response
    response = requests.get(weather_url)
 
    # json to python readable 
    weather_info = response.json()
 
    #if cod = 200, info was successfuly retrieved
    if weather_info['cod'] == 200:
        kelvin = 273 # value of kelvin
        #all collected values
        global temp
        temp = int((weather_info['main']['temp'] - kelvin) * 9 / 5 + 32)    #converting default kelvin value to Fahrenheit
        #if(temp > 72):
        #    Thermometerdisplay.config(Image = ThermometerHot)
        #else:
        #    Thermometerdisplay.config(Image = ThermometerCold)
        global feels_like_temp
        feels_like_temp = int(weather_info['main']['feels_like'] - kelvin) * 9/5 + 32
        global pressure
        pressure = weather_info['main']['pressure']
        global humidity
        humidity = weather_info['main']['humidity']
        global wind_speed
        wind_speed = weather_info['wind']['speed'] * 3.6
        global sunrise
        sunrise = weather_info['sys']['sunrise']
        global sunset
        sunset = weather_info['sys']['sunset']
        global timezone
        timezone = weather_info['timezone']
        global cloudy
        cloudy = weather_info['clouds']['all']
        global description
        description = weather_info['weather'][0]['description']
        global sunrise_time
        sunrise_time = time_format_for_location(sunrise + timezone)
        global sunset_time
        sunset_time = time_format_for_location(sunset + timezone)

# Fetch Initial Data 
showWeather()

# Creating Label for Temperature Display 
tempdisplay = Label(gui, text=f"Temperature : {temp}", fg = 'white', bg = 'black', font=("Courier", 45, 'bold'), justify = LEFT)
tempdisplay.grid(row=3,column=1,pady=4)

# Creating Label for Feels Like Display
feelslikedisplay = Label(gui, text=f"Feels  like : {feels_like_temp}", fg = 'white', bg = 'black', font=("Courier", 45, 'bold'), justify = LEFT)
feelslikedisplay.grid(row=4,column=1,pady=4)

# Creating Label for Weather Description Display
weatherdisplay = Label(gui, text=f"{description.rstrip()}     ", fg = 'white', bg = 'black', font=("Courier", 45, 'bold'), justify = LEFT)
weatherdisplay.grid(row=5,column=1,pady=4, sticky=W)

############################## Updating Information #####################################################################################################################

# Function to Keep All Information up to Date
def Update():
    # Update Weather Every 10 Minutes 
    global i
    i += 1
    if(i >= 600):
        i = 0
        # Gathering Current Weather Data
        showWeather()
    # Updates Variable to Current Date and Time Every Second 
    
    # Gathering Current Date and Time Data
    date = dt.datetime.now() 

    # Updating Labels

    # Date and Time Labels

    daydisplay.config(text=f"{date:%A}")
    datedisplay.config(text=f"{date:%B %d, %Y}")
    timedisplay.config(text=f"{date:%I:%M}")

    # Weather Labels

    tempdisplay.config(text=f"Temperature : {temp}  ")
    feelslikedisplay.config(text=f"Feels like  : {feels_like_temp}")
    weatherdisplay.config(text=f"{description.rstrip()}     ")

    gui.after(1000, Update) # Function Calls Itself Every One Second

# Initial Call for Update Function
Update()

gui.mainloop()
