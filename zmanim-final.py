import requests
import datetime

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


def get_sunrise_sunset_single(address: str = "Shalhevet High School",
                       date: datetime.datetime = datetime.datetime.now()):
    """
    Get sunrise and sunset times for one specific date, returned as two datetime.datetime objects
    """
    coordinates = geolocate(address)
    datestr = date.isoformat() #YYYY-MM-DD
    url=f"https://api.sunrisesunset.io/json?lat={coordinates[0]}&lng={coordinates[1]}&date={datestr}"
    response = requests.get(url=url)
    response_dict = response.json()["results"] #APIs just all have their own weird formatting i guess
    sunrise = datetime.datetime.combine(date, strtotime(response_dict["sunrise"]))
    sunset = datetime.datetime.combine(date,strtotime(response_dict["sunset"]))
    return sunrise, sunset

def get_sunrise_sunset_range(address: str = "Shalhevet High School",
                             start: datetime.datetime = datetime.datetime.now(),
                             end: datetime.datetime = (datetime.datetime.now()+datetime.timedelta(days=1))):
    """
    Get sunrise and sunset times for a range of dates, returned as a list of [{'sunrise':datetime.datetime,'sunset':datetime.datetime}...]
    """
    coordinates = geolocate(address)
    startstr = start.isoformat() #YYYY-MM-DD
    endstr = end.isoformat()
    url=f"https://api.sunrisesunset.io/json?lat={coordinates[0]}&lng={coordinates[1]}&date_start={startstr}&date_end={endstr}"
    response = requests.get(url=url)
    response_list = response.json()["results"] #APIs just all have their own weird formatting i guess
    times_list = []
    if len(response_list) == 0: #THIS SHOULD BE UNREACHABLE -- HANDLED BEFOREHAND
        print("Please ")
        exit(5)
    for value in response_list:
        sunrise = datetime.datetime.combine(datetime.datetime.strptime(value["date"],"%Y-%m-%d"), strtotime(value["sunrise"]))
        sunset = datetime.datetime.combine(datetime.datetime.strptime(value["date"],"%Y-%m-%d"), strtotime(value["sunset"]))
        times_list.append({'sunrise':sunrise,'sunset':sunset})
    return times_list


def get_zmanim(start: datetime.datetime, end:datetime.datetime):
    """
    For VG and MA:
    Netz Hachama, EO Zman Shma, EO Zman Tefila, Chatzot, Mincha Gedola, Mincha Ketana, Plag HaMincha, Shkiat HaChamah
    """
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
        "Magen Avraham": get_zmanim(sunrise-difference, sunset+difference)
    }

def print_zmanim(zmanim:dict):
    print("\033[22GVilna Gaon  | Magen Avraham")
    for zman in zmanim["Vilna Gaon"].keys(): #they're the same for both
        vg_time = zmanim["Vilna Gaon"][zman].strftime("%I:%M:%S %p")
        ma_time = zmanim["Magen Avraham"][zman].strftime("%I:%M:%S %p")
        print(f"{zman}:\033[22G{vg_time} |   {ma_time}")


def get_date():
    year = ""
    month = ""
    day = ""

    #year
    while True:
        year = input("Year (full): ")
        try:
            year = int(year)
        except:
            print("Please enter a numerical value")
            continue
        if year < 1000 or year > 10000:
            print("Unfortunately, the year must be greater than 1000 and less than 10000")
            continue
        break

    #month
    while True:
        month = input("Month (number): ")
        try:
            month = int(month)
        except:
            print("Please enter a numerical value")
            continue
        if month < 1 or month > 12:
            print("Please enter a valid Gregorian month")
            continue
        break

    #day
    while True:
        day = input("Day: ")
        try:
            day = int(day)
        except:
            print("Please enter a numerical value")
            continue
        if day < 0:
            print("Please enter a real day")
            continue
        elif (month in [1,3,5,7,8,10,12] and day > 31) or \
            (month in [4,6,9,11] and day > 30) or \
            (((not year%400) or (year%100 and not(year%4))) and #leap year
            (month == 2 and day > 29)) or \
            (not ((not year%400) or (year%100 and not(year%4))) and #not leap year
            (month == 2 and day > 28)):
                print("Please enter a valid day for the month you chose")
                continue
        break
    return datetime.datetime(year=year,month=month,day=day)


if __name__ == "__main__":
    while True:
        #location = "Shalhevet High School"
        print("What location would you like zmanim for?")
        location = input()
        if location != "": break
    
    while True:
        length = input("Would you like to know the zmanim for one date or a range? [d/r] ")[0].lower()
        if length == "d" or length == "r": break
    
    if length == "d":
        date = get_date()
        print("-----\n")
        sunrise,sunset = get_sunrise_sunset_single(
            address=location,
            date=date)
        print(date.date())
        print("Sunrise: ", sunrise.strftime("%I:%M:%S %p"))
        print("Sunset:  ",  sunset.strftime("%I:%M:%S %p"))
        print_zmanim(get_all_zmanim(sunrise,sunset))

    elif length == "r":
        while True:
            print("Start of range:")
            start_date = get_date()
            print("End of range:")
            end_date = get_date()
            if not start_date < end_date:
                print("Please make sure the start date is before the end date")
                continue
            if end_date-start_date > datetime.timedelta(weeks=53):
                print("Range must be shorter than one year")
                continue
            break
        print("-----\n")
        times_list = get_sunrise_sunset_range(
            address=location,
            start=start_date,
            end=end_date)
        sunrises = [day['sunrise'] for day in times_list]
        sunsets = [day['sunset'] for day in times_list]
        print("Earliest sunrise: ",min(sunrises))
        print("Latest sunrise:   ",max(sunrises))
        print("Earliest sunset:  ",min(sunsets))
        print("Latest sunset:    ",max(sunsets))
        print()
        del sunrises, sunsets
        for day in times_list:
            sunrise = day['sunrise']
            sunset = day['sunset']
            print(sunrise.date())
            print("Sunrise: ", sunrise.strftime("%I:%M:%S %p"))
            print("Sunset:  ",  sunset.strftime("%I:%M:%S %p"))
            print_zmanim(get_all_zmanim(sunrise,sunset))
            print("\n")
        print("\033[3A")
