import requests
import os
from tkinter import *
from PIL import Image, ImageTk

#global Variables and setup
window = Tk(className='weather menu')
window.title('weather menu')
window.geometry('400x500')
imagePath = os.curdir + 'weatherImage.png'

#Request
URL = "https://api.weatherapi.com/v1/current.json?"
apiKey = "INSERT API KEY HERE"
city = 'Toronto'
apiURL = f"{URL}key={apiKey}&q={city}&aqi=no"
response = requests.get(apiURL)

if response.status_code == 200:
    print('Successfull')
    data = response.json()
else:
    print(f"Error {response.status_code}, - {response.text}")

#secondary global object setup
locationObj: dict = data["location"]
locationKeys: list = [x for x in locationObj.keys()]
forcastObj: dict = data["current"]
forcastKeys: list = [x for x in forcastObj.keys()]

#My actual "main" function
def displayWeather() -> None:
    #Display Location data first since minmal formatting required
    displayItems(locationObj)

    #formatting our object with dict comprehension
    wantedForcastKeys = ['temp_c', 'is_day', 'condition', 'wind_kph', 'wind_dir', 'precip_mm', 'humidity', 'cloud', 'feelslike_c', 'windchill_c', 'heatindex_c', 'vis_c', 'gust_kph']
    wantedForcastObj = {key:forcastObj[key] for key in forcastObj.keys() if key in wantedForcastKeys}

    #Displaying the rest of the items and creating the window loop
    displayItems(wantedForcastObj)
    window.mainloop()
    
#GET request the image found in the value associated with condition and download it
def getImage(url: str):
    response = requests.get("https:" + url, stream=True)
    with open(imagePath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

#iterate through dictionaries and display key values to tkinter window
def displayItems(iterable: dict) -> None:
    for key in iterable.keys():
        #Since localtime epoch is the only one we don't wnat from the location obj, we just filter it out.
        #Lat is also skipped because Lat and Lon are to be in the same row
        if key == 'localtime_epoch' or key == 'lat':
            continue

        #the value stored in condition is an object that has weather the weather condition and the image resource link, so we deal with it seperately
        if key == 'condition':
            condition = iterable['condition']
            getImage(condition['icon'])
            header = Label(window, text=f"{key}: {condition['text']}")
            header.pack()
            displayImage()
            continue

        #since Lat and Lon are to be put on the same row, we deal with it separately
        if key == 'lon':
            header = Label(window, text=f"Lat: {locationObj['lat']}        {key}: {locationObj[key]}")
        else:
            header = Label(window, text=f"{key}: {iterable[key]}")
        header.pack()
    
#display's the image onto the tkinter window. Please note that photo_image is a global variable in order to avoid dereference until we are done with it
def displayImage():
    original_image = Image.open(imagePath)
    global photo_image
    photo_image = ImageTk.PhotoImage(original_image)
    image_label = Label(window, image=photo_image)
    image_label.pack()
    

def main():
    displayWeather()

#os.remove(imagePath) in order to not create duplicate weatherImage.png's. We also put it inside a try except in order to not get a resource leak of the png
if __name__ == "__main__":
    try:
        main()
        os.remove(imagePath)
    except EXCEPTION:
        os.remove(imagePath)