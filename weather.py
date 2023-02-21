import requests
import json
from tkinter import *
import apiKey

#reset = False

main = Tk()

main.geometry("500x750")

requestL = Label(main, text = "Please Enter Your Zipcode:", pady=15)
requestL.pack()

zipGet = Entry(main, width = 10)
zipGet.pack()

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def apiWork():

    zip = zipGet.get()

    key = apiKey.serviceKey
    
    geoCodeParse1 = "https://api.geoapify.com/v1/geocode/search?postcode="
    geoCodeParse2 = "&filter=countrycode:us,ca&format=json&apiKey="
    geoCode = geoCodeParse1.__add__(str(zip))
    geoCode = geoCode.__add__(geoCodeParse2)
    geoCode = geoCode.__add__(key)
    geoCodeResponse  = requests.get(geoCode)

    temp1 = geoCodeResponse.json()['results'][0]['lon']
    temp2 = geoCodeResponse.json()['results'][0]['lat']

    urlApi = "https://api.weather.gov/gridpoints/"
    coordinates = "https://api.weather.gov/points/" + str(temp2) +"," + str(temp1)

    response = requests.get(coordinates)

    office = str(response.json()['properties']['gridId'])
    resX = str(response.json()['properties']['gridX'])
    resY = str(response.json()['properties']['gridY'])

    urlApi2 = urlApi.__add__(office)
    urlApi2 = urlApi2.__add__("/")
    urlApi2 = urlApi2.__add__(resX)
    urlApi2 = urlApi2.__add__(",")
    urlApi2 = urlApi2.__add__(resY)
    urlApi2 = urlApi2.__add__("/forecast")

    response2 = requests.get(urlApi2)
    
    x = 0
    while x <= 5:
        resultsDay = Label(main, text = response2.json()['properties']['periods'][x]['name'])
        resultsDay.pack()
        resultsTemp = Label(main, text = str(response2.json()['properties']['periods'][x]['temperature']) + 'F')
        resultsTemp.pack()
        resultsWeather = Label(main, text = response2.json()['properties']['periods'][x]['detailedForecast'], pady=10, wraplength=400)
        resultsWeather.pack()
        x = x+1
    """
    if reset:
        resultsDay.destroy()
        resultsTemp.destroy()
        resultsWeather.destroy()

    reset = True    
    """

button = Button(main, text="Enter", padx=10, pady=5, bg='white',fg='black', command=apiWork)
button.pack()

main.mainloop()