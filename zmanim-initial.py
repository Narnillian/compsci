import requests
import datetime
import time

def strtotime(str:str):
    """Takes string (of specific format -- NOT GENERALIZED) and returns corresponding `datetime.time` value"""
    if len(str[:str.find(":")]) == 1:
        str = "0" + str
    if str[-3:] == " PM":
        str = f"{int(str[:2])+12}{str[2:]}"
    str = str[:-3]
    return datetime.time.fromisoformat(str)

def geolocate(address: str = "Shalhevet High School"):
    """
    A function to geolocate a given address using the LocationIQ API

    Returns a list of [lat,long] of the API's response
    """
    url = "https://us1.locationiq.com/v1/search?format=json&normalizeaddress=1&addressdetails=1&key=pk.cbc1cf1b649ff5d37e57bf7445b43d16&q=" + address
    headers = {"accept": "application/json"}

    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
        response_dict = response.json()[0] #it comes back as a list for some reason
        return [float(response_dict["lat"]),float(response_dict["lon"])]
    else:
        print("ERROR: API UNREACHABLE")
        exit(response.status_code)


def get_sunrise_sunset(address: str = "Shalhevet High School",
                       date: datetime.datetime = datetime.datetime.now()):
    coordinates = geolocate(address)
    datestr = date.isoformat() #YYYY-MM-DD
    url=f"https://api.sunrisesunset.io/json?lat={coordinates[0]}&lng={coordinates[1]}&date={datestr}"
    response = requests.get(url=url)
    response_dict = response.json()["results"] #APIs just all have their own weird formatting i guess
    sunrise = datetime.datetime.combine(date, strtotime(response_dict["sunrise"]))
    sunset = datetime.datetime.combine(date,strtotime(response_dict["sunset"]))
    return sunrise, sunset

def get_zmanim(start: datetime.datetime, end:datetime.datetime):
    result = {}
    hour = (end-start)/12

    result["Netz Hachama"] = start
    result["End of Zman Shma"] = start + 3*hour
    result["End of Zman Tfila"] = start + 4*hour
    result["Chatzot"] = start + 6*hour
    result["Mincha Gedola"] = start + 6.5*hour
    result["Mincha Ketana"] = start + 9.5*hour
    result["Plag HaMincha"] = start + 10.75*hour
    result["Shkiat HaChama"] = start + 12*hour

    return result


def get_all_zmanim(sunrise: datetime.datetime, sunset: datetime.datetime):
    """
    For VG and MA:
    Netz Hachama, EO Zman Shma, EO Zman Tefila, Chatzot, Mincha Gedola, Mincha Ketana, Plag HaMincha, Shkiat HaChamah
    """
    difference = datetime.timedelta(minutes=72)
    return {
        "Vilna Gaon": get_zmanim(sunrise,sunset),
        "Magen Avraham": get_zmanim(sunrise+difference, sunset-difference)
    }

def print_zmanim(zmanim:dict):
    for opinion in "Vilna Gaon","Magen Avraham":
        print(opinion+":")
        for zman in zmanim[opinion].keys():
            print(f"{zman}: {zmanim[opinion][zman]}")

print("Coordinates of Shalhevet High School, according to LocationIQ:")
print(geolocate("Shalhevet High School"))

print("\nSunrise and sunset, according to sunrisesunset.io, with resulting Zmanim:")
for address in ["Shalhevet High School","916 S Holt Ave"]:
    print(address+":")
    for date in [(2024,3,7),(2024,4,1)]:
        print(f"{date[0]}-{date[1]}-{date[2]}:")
        sunrise,sunset = get_sunrise_sunset(address=address,date=datetime.datetime(year=date[0],month=date[1],day=date[2]))
        print("Sunrise: ", sunrise.strftime("%I:%M:%S %p"), "|", int(sunrise.timestamp()))
        print("Sunset:  ",  sunset.strftime("%I:%M:%S %p"), "|", int(sunset.timestamp()))
        print()
        print_zmanim(get_all_zmanim(sunrise,sunset))
        print()
    print()
