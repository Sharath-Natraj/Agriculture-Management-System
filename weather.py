
# import required modules
from datetime import datetime


from selenium import webdriver
import requests

# def open_chrome():
#     drive = webdriver.Chrome("/home/amogha/Downloads/chromedriver")
#     drive.get("https://www.cactus2000.de/uk/unit/masshum.shtml")
#     return drive


def convert2h(temperature,percentage,pressure,drive):

    temp = drive.find_element_by_name("temp")
    temp.clear()
    temp.send_keys(temperature)

    pres = drive.find_element_by_name("pres")
    pres.clear()
    pres.send_keys(pressure)

    prec = drive.find_element_by_name("rh_H2O")
    # prec.clear()
    prec.send_keys(percentage)
    # print(percentage)
    # time.sleep(8)
    but = drive.find_element_by_xpath("//input[@type='button']")
    but.click()
    # import time
    # time.sleep(1)
    hum = drive.find_element_by_name("spc_H2O")
    # print()
    ans = hum.get_attribute("value")
    reset = drive.find_element_by_xpath("//input[@type='reset']")
    reset.click()

    a0w=6.107799961
    a1w= 4.436518521*(10**(-1))
    a2w=1.428945805*(10**(-2))
    a3w=2.650648471*(10**(-4))
    a4w=3.031240396*(10**(-6))
    a5w=2.034080948*(10**(-8)) 
    a6w=6.136820929*(10**(-11))

    a0i=6.109177956
    a1i=5.034698970*(10**(-1))
    a2i=1.886013408*(10**(-2))
    a3i=4.176223716*(10**(-4))
    a4i=5.824720280*(10**(-6))
    a5i=4.838803174*(10**(-8)) 
    a6i=1.838826904*(10**(-10))

    ew=a0w+temp-(a1w+temp*(a2w+temp*(a3w+temp*(a4w+temp*(a5w+temp*a6w)))))
    ei=a0i+temp-(a1i+temp*(a2i+temp*(a3i+temp*(a4i+temp*(a5i+temp*a6i)))))

    e=min(ew,ei)

    Ph20= ans*e*temp*0.01
    Pair=1013.25

    Xh20=Ph20/pres

    q=(Xh20*18.01534)/((Xh20*18.01534)+((1-Xh20)*28.9644))

    return q*1000


   # return ans
    # RH


def call_an_api():
    api_key = "443a0e042702dbb50ca2e32194e1b326"

    base_url = "http://api.openweathermap.org/data/2.5/onecall?lat=13.5&lon=76&units=metric&"

    complete_url = base_url + "appid=" + api_key


    response = requests.get(complete_url)
    x = response.json()

    return x

def calculate_dict(x):

    arr=x
    a=[]
    for i in arr:
        if i=="daily":
            a = arr[i]
            # print(arr[i])

    d = {}

    drive = open_chrome()

    for i in a:
        date = datetime.utcfromtimestamp(i["dt"]).strftime('%Y-%m-%d')
        print(date)

        pr = float(format(i["pressure"]*0.1,".2f"))
        print("Surface Pressure",pr)
        print("Temperature",i["temp"]["day"])
        print("humi %", i["humidity"])
        hum = convert2h(i["temp"]["day"],i["humidity"],i["pressure"],drive)
        hum = float(format(float(hum),".2f"))
        print("humidity",hum)
        print(i["pop"])
        d[date] = [pr,i["temp"]["day"],hum,i["pop"]]

    drive.quit()

    return d

def main():
    x = call_an_api()
    print("weather api called !!")
    # x={'lat': 13.5, 'lon': 76, 'timezone': 'Asia/Kolkata', 'timezone_offset': 19800, 'current': {'dt': 1651465626, 'sunrise': 1651451659, 'sunset': 1651497093, 'temp': 30.28, 'feels_like': 29.46, 'pressure': 1010, 'humidity': 35, 'dew_point': 13.13, 'uvi': 6.13, 'clouds': 47, 'visibility': 10000, 'wind_speed': 2.98, 'wind_deg': 323, 'wind_gust': 3.52, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}]}, 'minutely': [{'dt': 1651465680, 'precipitation': 0}, {'dt': 1651465740, 'precipitation': 0}, {'dt': 1651465800, 'precipitation': 0}, {'dt': 1651465860, 'precipitation': 0}, {'dt': 1651465920, 'precipitation': 0}, {'dt': 1651465980, 'precipitation': 0}, {'dt': 1651466040, 'precipitation': 0}, {'dt': 1651466100, 'precipitation': 0}, {'dt': 1651466160, 'precipitation': 0}, {'dt': 1651466220, 'precipitation': 0}, {'dt': 1651466280, 'precipitation': 0}, {'dt': 1651466340, 'precipitation': 0}, {'dt': 1651466400, 'precipitation': 0}, {'dt': 1651466460, 'precipitation': 0}, {'dt': 1651466520, 'precipitation': 0}, {'dt': 1651466580, 'precipitation': 0}, {'dt': 1651466640, 'precipitation': 0}, {'dt': 1651466700, 'precipitation': 0}, {'dt': 1651466760, 'precipitation': 0}, {'dt': 1651466820, 'precipitation': 0}, {'dt': 1651466880, 'precipitation': 0}, {'dt': 1651466940, 'precipitation': 0}, {'dt': 1651467000, 'precipitation': 0}, {'dt': 1651467060, 'precipitation': 0}, {'dt': 1651467120, 'precipitation': 0}, {'dt': 1651467180, 'precipitation': 0}, {'dt': 1651467240, 'precipitation': 0}, {'dt': 1651467300, 'precipitation': 0}, {'dt': 1651467360, 'precipitation': 0}, {'dt': 1651467420, 'precipitation': 0}, {'dt': 1651467480, 'precipitation': 0}, {'dt': 1651467540, 'precipitation': 0}, {'dt': 1651467600, 'precipitation': 0}, {'dt': 1651467660, 'precipitation': 0}, {'dt': 1651467720, 'precipitation': 0}, {'dt': 1651467780, 'precipitation': 0}, {'dt': 1651467840, 'precipitation': 0}, {'dt': 1651467900, 'precipitation': 0}, {'dt': 1651467960, 'precipitation': 0}, {'dt': 1651468020, 'precipitation': 0}, {'dt': 1651468080, 'precipitation': 0}, {'dt': 1651468140, 'precipitation': 0}, {'dt': 1651468200, 'precipitation': 0}, {'dt': 1651468260, 'precipitation': 0}, {'dt': 1651468320, 'precipitation': 0}, {'dt': 1651468380, 'precipitation': 0}, {'dt': 1651468440, 'precipitation': 0}, {'dt': 1651468500, 'precipitation': 0}, {'dt': 1651468560, 'precipitation': 0}, {'dt': 1651468620, 'precipitation': 0}, {'dt': 1651468680, 'precipitation': 0}, {'dt': 1651468740, 'precipitation': 0}, {'dt': 1651468800, 'precipitation': 0}, {'dt': 1651468860, 'precipitation': 0}, {'dt': 1651468920, 'precipitation': 0}, {'dt': 1651468980, 'precipitation': 0}, {'dt': 1651469040, 'precipitation': 0}, {'dt': 1651469100, 'precipitation': 0}, {'dt': 1651469160, 'precipitation': 0}, {'dt': 1651469220, 'precipitation': 0}, {'dt': 1651469280, 'precipitation': 0}], 'hourly': [{'dt': 1651464000, 'temp': 30.28, 'feels_like': 29.46, 'pressure': 1010, 'humidity': 35, 'dew_point': 13.13, 'uvi': 6.13, 'clouds': 47, 'visibility': 10000, 'wind_speed': 2.98, 'wind_deg': 323, 'wind_gust': 3.52, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651467600, 'temp': 30.77, 'feels_like': 29.78, 'pressure': 1010, 'humidity': 33, 'dew_point': 12.65, 'uvi': 9.67, 'clouds': 48, 'visibility': 10000, 'wind_speed': 4.38, 'wind_deg': 327, 'wind_gust': 4.31, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651471200, 'temp': 31.92, 'feels_like': 30.73, 'pressure': 1009, 'humidity': 30, 'dew_point': 12.2, 'uvi': 12.37, 'clouds': 50, 'visibility': 10000, 'wind_speed': 5.44, 'wind_deg': 331, 'wind_gust': 4.62, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'pop': 0.2, 'rain': {'1h': 0.1}}, {'dt': 1651474800, 'temp': 33.4, 'feels_like': 32.07, 'pressure': 1008, 'humidity': 27, 'dew_point': 11.86, 'uvi': 13.54, 'clouds': 27, 'visibility': 10000, 'wind_speed': 5.39, 'wind_deg': 341, 'wind_gust': 4.31, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651478400, 'temp': 35.05, 'feels_like': 33.5, 'pressure': 1006, 'humidity': 23, 'dew_point': 10.83, 'uvi': 12.34, 'clouds': 17, 'visibility': 10000, 'wind_speed': 5.04, 'wind_deg': 350, 'wind_gust': 3.93, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'pop': 0}, {'dt': 1651482000, 'temp': 36.64, 'feels_like': 34.79, 'pressure': 1004, 'humidity': 19, 'dew_point': 9.56, 'uvi': 9.41, 'clouds': 8, 'visibility': 10000, 'wind_speed': 5.08, 'wind_deg': 6, 'wind_gust': 4.01, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'pop': 0}, {'dt': 1651485600, 'temp': 36.62, 'feels_like': 34.77, 'pressure': 1003, 'humidity': 19, 'dew_point': 9.36, 'uvi': 5.25, 'clouds': 10, 'visibility': 10000, 'wind_speed': 5.32, 'wind_deg': 19, 'wind_gust': 3.41, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'pop': 0}, {'dt': 1651489200, 'temp': 36.1, 'feels_like': 34.31, 'pressure': 1003, 'humidity': 20, 'dew_point': 9.26, 'uvi': 2.38, 'clouds': 18, 'visibility': 10000, 'wind_speed': 4.33, 'wind_deg': 20, 'wind_gust': 2.72, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'pop': 0}, {'dt': 1651492800, 'temp': 34.62, 'feels_like': 32.99, 'pressure': 1004, 'humidity': 23, 'dew_point': 10.16, 'uvi': 0.66, 'clouds': 26, 'visibility': 10000, 'wind_speed': 1.81, 'wind_deg': 324, 'wind_gust': 3.2, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651496400, 'temp': 32.24, 'feels_like': 31.21, 'pressure': 1005, 'humidity': 31, 'dew_point': 12.66, 'uvi': 0, 'clouds': 100, 'visibility': 10000, 'wind_speed': 3.47, 'wind_deg': 271, 'wind_gust': 5.04, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'pop': 0}, {'dt': 1651500000, 'temp': 29.67, 'feels_like': 29.65, 'pressure': 1006, 'humidity': 43, 'dew_point': 15.27, 'uvi': 0, 'clouds': 86, 'visibility': 10000, 'wind_speed': 2.42, 'wind_deg': 272, 'wind_gust': 3.41, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651503600, 'temp': 28.29, 'feels_like': 28.88, 'pressure': 1007, 'humidity': 51, 'dew_point': 17.06, 'uvi': 0, 'clouds': 78, 'visibility': 10000, 'wind_speed': 1.89, 'wind_deg': 233, 'wind_gust': 2.21, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651507200, 'temp': 27.42, 'feels_like': 28.46, 'pressure': 1008, 'humidity': 58, 'dew_point': 18.06, 'uvi': 0, 'clouds': 80, 'visibility': 10000, 'wind_speed': 3.32, 'wind_deg': 251, 'wind_gust': 4.11, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651510800, 'temp': 26.44, 'feels_like': 26.44, 'pressure': 1008, 'humidity': 63, 'dew_point': 18.58, 'uvi': 0, 'clouds': 84, 'visibility': 10000, 'wind_speed': 3.13, 'wind_deg': 259, 'wind_gust': 4.81, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651514400, 'temp': 25.9, 'feels_like': 26.27, 'pressure': 1008, 'humidity': 66, 'dew_point': 18.74, 'uvi': 0, 'clouds': 87, 'visibility': 10000, 'wind_speed': 1.52, 'wind_deg': 253, 'wind_gust': 2.63, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651518000, 'temp': 25.18, 'feels_like': 25.56, 'pressure': 1008, 'humidity': 69, 'dew_point': 18.85, 'uvi': 0, 'clouds': 100, 'visibility': 10000, 'wind_speed': 1.1, 'wind_deg': 200, 'wind_gust': 1.8, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651521600, 'temp': 24.63, 'feels_like': 25, 'pressure': 1007, 'humidity': 71, 'dew_point': 18.96, 'uvi': 0, 'clouds': 100, 'visibility': 10000, 'wind_speed': 2.24, 'wind_deg': 215, 'wind_gust': 3.03, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651525200, 'temp': 24.15, 'feels_like': 24.53, 'pressure': 1007, 'humidity': 73, 'dew_point': 18.86, 'uvi': 0, 'clouds': 100, 'visibility': 10000, 'wind_speed': 2.15, 'wind_deg': 238, 'wind_gust': 2.91, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651528800, 'temp': 23.58, 'feels_like': 23.98, 'pressure': 1007, 'humidity': 76, 'dew_point': 18.68, 'uvi': 0, 'clouds': 100, 'visibility': 10000, 'wind_speed': 1.38, 'wind_deg': 271, 'wind_gust': 1.72, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651532400, 'temp': 23.04, 'feels_like': 23.44, 'pressure': 1008, 'humidity': 78, 'dew_point': 18.66, 'uvi': 0, 'clouds': 100, 'visibility': 10000, 'wind_speed': 1.21, 'wind_deg': 332, 'wind_gust': 1.62, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651536000, 'temp': 22.44, 'feels_like': 22.85, 'pressure': 1009, 'humidity': 81, 'dew_point': 18.76, 'uvi': 0, 'clouds': 100, 'visibility': 10000, 'wind_speed': 1.51, 'wind_deg': 348, 'wind_gust': 2.1, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651539600, 'temp': 22.49, 'feels_like': 22.91, 'pressure': 1010, 'humidity': 81, 'dew_point': 18.78, 'uvi': 0, 'clouds': 45, 'visibility': 10000, 'wind_speed': 0.59, 'wind_deg': 260, 'wind_gust': 1.21, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651543200, 'temp': 24.25, 'feels_like': 24.58, 'pressure': 1010, 'humidity': 71, 'dew_point': 18.47, 'uvi': 0.84, 'clouds': 40, 'visibility': 10000, 'wind_speed': 0.18, 'wind_deg': 267, 'wind_gust': 0.91, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651546800, 'temp': 26.65, 'feels_like': 26.65, 'pressure': 1011, 'humidity': 59, 'dew_point': 17.87, 'uvi': 2.77, 'clouds': 50, 'visibility': 10000, 'wind_speed': 1.24, 'wind_deg': 64, 'wind_gust': 1.14, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651550400, 'temp': 29.05, 'feels_like': 29.49, 'pressure': 1011, 'humidity': 48, 'dew_point': 16.66, 'uvi': 5.92, 'clouds': 57, 'visibility': 10000, 'wind_speed': 1.28, 'wind_deg': 346, 'wind_gust': 1.5, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'pop': 0}, {'dt': 1651554000, 'temp': 31.68, 'feels_like': 31.21, 'pressure': 1010, 'humidity': 36, 'dew_point': 14.86, 'uvi': 9.34, 'clouds': 48, 'visibility': 10000, 'wind_speed': 3.16, 'wind_deg': 355, 'wind_gust': 3.02, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651557600, 'temp': 33.69, 'feels_like': 32.88, 'pressure': 1009, 'humidity': 30, 'dew_point': 13.46, 'uvi': 11.94, 'clouds': 42, 'visibility': 10000, 'wind_speed': 3.77, 'wind_deg': 351, 'wind_gust': 3.61, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651561200, 'temp': 35.19, 'feels_like': 33.99, 'pressure': 1007, 'humidity': 25, 'dew_point': 12.56, 'uvi': 13.86, 'clouds': 2, 'visibility': 10000, 'wind_speed': 4.38, 'wind_deg': 359, 'wind_gust': 4.21, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'pop': 0}, {'dt': 1651564800, 'temp': 36.08, 'feels_like': 34.78, 'pressure': 1006, 'humidity': 23, 'dew_point': 11.86, 'uvi': 12.64, 'clouds': 1, 'visibility': 10000, 'wind_speed': 4.65, 'wind_deg': 358, 'wind_gust': 4.3, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'pop': 0}, {'dt': 1651568400, 'temp': 36.48, 'feels_like': 35.11, 'pressure': 1005, 'humidity': 22, 'dew_point': 11.19, 'uvi': 9.63, 'clouds': 1, 'visibility': 10000, 'wind_speed': 4.16, 'wind_deg': 7, 'wind_gust': 4.12, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'pop': 0}, {'dt': 1651572000, 'temp': 36.69, 'feels_like': 35.19, 'pressure': 1004, 'humidity': 21, 'dew_point': 10.96, 'uvi': 5.28, 'clouds': 4, 'visibility': 10000, 'wind_speed': 4.02, 'wind_deg': 15, 'wind_gust': 3.9, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'pop': 0}, {'dt': 1651575600, 'temp': 35.9, 'feels_like': 34.38, 'pressure': 1003, 'humidity': 22, 'dew_point': 10.76, 'uvi': 2.39, 'clouds': 22, 'visibility': 10000, 'wind_speed': 4.11, 'wind_deg': 9, 'wind_gust': 3.7, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'pop': 0}, {'dt': 1651579200, 'temp': 35.33, 'feels_like': 33.69, 'pressure': 1004, 'humidity': 22, 'dew_point': 10.66, 'uvi': 0.67, 'clouds': 32, 'visibility': 10000, 'wind_speed': 4.05, 'wind_deg': 353, 'wind_gust': 4, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'pop': 0}, {'dt': 1651582800, 'temp': 33.96, 'feels_like': 32.61, 'pressure': 1005, 'humidity': 26, 'dew_point': 11.63, 'uvi': 0, 'clouds': 96, 'visibility': 10000, 'wind_speed': 2.66, 'wind_deg': 324, 'wind_gust': 4.72, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'pop': 0}, {'dt': 1651586400, 'temp': 31.26, 'feels_like': 31.57, 'pressure': 1006, 'humidity': 42, 'dew_point': 16.36, 'uvi': 0, 'clouds': 98, 'visibility': 10000, 'wind_speed': 4.57, 'wind_deg': 281, 'wind_gust': 6.3, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651590000, 'temp': 30.16, 'feels_like': 30.97, 'pressure': 1006, 'humidity': 48, 'dew_point': 17.86, 'uvi': 0, 'clouds': 99, 'visibility': 10000, 'wind_speed': 3.61, 'wind_deg': 281, 'wind_gust': 5.4, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651593600, 'temp': 29.48, 'feels_like': 30.44, 'pressure': 1007, 'humidity': 51, 'dew_point': 18.16, 'uvi': 0, 'clouds': 99, 'visibility': 10000, 'wind_speed': 3.22, 'wind_deg': 277, 'wind_gust': 5.16, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651597200, 'temp': 27.76, 'feels_like': 29.1, 'pressure': 1008, 'humidity': 60, 'dew_point': 18.88, 'uvi': 0, 'clouds': 81, 'visibility': 10000, 'wind_speed': 2.93, 'wind_deg': 229, 'wind_gust': 4.13, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651600800, 'temp': 26.52, 'feels_like': 26.52, 'pressure': 1008, 'humidity': 66, 'dew_point': 19.53, 'uvi': 0, 'clouds': 71, 'visibility': 10000, 'wind_speed': 1.96, 'wind_deg': 191, 'wind_gust': 2.6, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651604400, 'temp': 25.32, 'feels_like': 25.81, 'pressure': 1008, 'humidity': 73, 'dew_point': 19.96, 'uvi': 0, 'clouds': 32, 'visibility': 10000, 'wind_speed': 3.52, 'wind_deg': 186, 'wind_gust': 4.51, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'pop': 0}, {'dt': 1651608000, 'temp': 24.68, 'feels_like': 25.21, 'pressure': 1008, 'humidity': 77, 'dew_point': 20.12, 'uvi': 0, 'clouds': 62, 'visibility': 10000, 'wind_speed': 4.23, 'wind_deg': 227, 'wind_gust': 6, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651611600, 'temp': 24.78, 'feels_like': 25.3, 'pressure': 1008, 'humidity': 76, 'dew_point': 19.96, 'uvi': 0, 'clouds': 71, 'visibility': 10000, 'wind_speed': 3.14, 'wind_deg': 246, 'wind_gust': 3.9, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'pop': 0}, {'dt': 1651615200, 'temp': 24.45, 'feels_like': 24.96, 'pressure': 1008, 'humidity': 77, 'dew_point': 19.76, 'uvi': 0, 'clouds': 72, 'visibility': 10000, 'wind_speed': 1.49, 'wind_deg': 328, 'wind_gust': 2.41, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10n'}], 'pop': 0.32, 'rain': {'1h': 1.31}}, {'dt': 1651618800, 'temp': 24.07, 'feels_like': 24.57, 'pressure': 1009, 'humidity': 78, 'dew_point': 19.76, 'uvi': 0, 'clouds': 73, 'visibility': 10000, 'wind_speed': 0.71, 'wind_deg': 323, 'wind_gust': 2.11, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10n'}], 'pop': 0.52, 'rain': {'1h': 1.25}}, {'dt': 1651622400, 'temp': 24.33, 'feels_like': 24.83, 'pressure': 1009, 'humidity': 77, 'dew_point': 19.74, 'uvi': 0, 'clouds': 72, 'visibility': 10000, 'wind_speed': 1.83, 'wind_deg': 255, 'wind_gust': 2.4, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'pop': 0.56, 'rain': {'1h': 0.5}}, {'dt': 1651626000, 'temp': 24.35, 'feels_like': 24.82, 'pressure': 1010, 'humidity': 76, 'dew_point': 19.55, 'uvi': 0, 'clouds': 67, 'visibility': 10000, 'wind_speed': 1.54, 'wind_deg': 270, 'wind_gust': 2.11, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'pop': 0.08}, {'dt': 1651629600, 'temp': 25.51, 'feels_like': 25.92, 'pressure': 1011, 'humidity': 69, 'dew_point': 19.18, 'uvi': 0.92, 'clouds': 74, 'visibility': 10000, 'wind_speed': 2.61, 'wind_deg': 345, 'wind_gust': 3.02, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'pop': 0.08}, {'dt': 1651633200, 'temp': 27.46, 'feels_like': 28.6, 'pressure': 1011, 'humidity': 59, 'dew_point': 18.66, 'uvi': 3.06, 'clouds': 58, 'visibility': 10000, 'wind_speed': 2.21, 'wind_deg': 309, 'wind_gust': 2.41, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'pop': 0.04}], 'daily': [{'dt': 1651473000, 'sunrise': 1651451659, 'sunset': 1651497093, 'moonrise': 1651454940, 'moonset': 1651501980, 'moon_phase': 0.04, 'temp': {'day': 31.92, 'min': 22.3, 'max': 36.64, 'night': 25.9, 'eve': 34.62, 'morn': 23.65}, 'feels_like': {'day': 30.73, 'night': 26.27, 'eve': 32.99, 'morn': 24.03}, 'pressure': 1009, 'humidity': 30, 'dew_point': 12.2, 'wind_speed': 5.44, 'wind_deg': 331, 'wind_gust': 5.04, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': 50, 'pop': 0.2, 'rain': 0.1, 'uvi': 13.54}, {'dt': 1651559400, 'sunrise': 1651538035, 'sunset': 1651583506, 'moonrise': 1651543920, 'moonset': 1651591500, 'moon_phase': 0.08, 'temp': {'day': 33.69, 'min': 22.44, 'max': 36.69, 'night': 26.52, 'eve': 35.33, 'morn': 22.44}, 'feels_like': {'day': 32.88, 'night': 26.52, 'eve': 33.69, 'morn': 22.85}, 'pressure': 1009, 'humidity': 30, 'dew_point': 13.46, 'wind_speed': 4.65, 'wind_deg': 358, 'wind_gust': 6.3, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': 42, 'pop': 0, 'uvi': 13.86}, {'dt': 1651645800, 'sunrise': 1651624411, 'sunset': 1651669920, 'moonrise': 1651633080, 'moonset': 1651681080, 'moon_phase': 0.11, 'temp': {'day': 34.62, 'min': 24.07, 'max': 36.97, 'night': 27.29, 'eve': 36.37, 'morn': 24.33}, 'feels_like': {'day': 33.59, 'night': 28.8, 'eve': 34.97, 'morn': 24.83}, 'pressure': 1009, 'humidity': 27, 'dew_point': 12.76, 'wind_speed': 4.87, 'wind_deg': 347, 'wind_gust': 6.23, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'clouds': 45, 'pop': 0.56, 'rain': 3.06, 'uvi': 14.17}, {'dt': 1651732200, 'sunrise': 1651710788, 'sunset': 1651756333, 'moonrise': 1651722420, 'moonset': 1651770540, 'moon_phase': 0.14, 'temp': {'day': 33.24, 'min': 24.89, 'max': 35.61, 'night': 26.85, 'eve': 34.26, 'morn': 24.89}, 'feels_like': {'day': 33.14, 'night': 28.17, 'eve': 33.29, 'morn': 25.21}, 'pressure': 1008, 'humidity': 35, 'dew_point': 15.54, 'wind_speed': 6.24, 'wind_deg': 2, 'wind_gust': 6.74, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': 42, 'pop': 0.68, 'rain': 2.19, 'uvi': 13.13}, {'dt': 1651818600, 'sunrise': 1651797166, 'sunset': 1651842747, 'moonrise': 1651811880, 'moonset': 1651859940, 'moon_phase': 0.17, 'temp': {'day': 34.27, 'min': 24.33, 'max': 37.13, 'night': 25.85, 'eve': 35.39, 'morn': 24.33}, 'feels_like': {'day': 34.9, 'night': 26.21, 'eve': 34.42, 'morn': 24.83}, 'pressure': 1007, 'humidity': 36, 'dew_point': 16.76, 'wind_speed': 5.55, 'wind_deg': 233, 'wind_gust': 7.93, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': 82, 'pop': 0.48, 'rain': 0.75, 'uvi': 14.06}, {'dt': 1651905000, 'sunrise': 1651883545, 'sunset': 1651929162, 'moonrise': 1651901400, 'moonset': 0, 'moon_phase': 0.2, 'temp': {'day': 33.92, 'min': 24.25, 'max': 36.78, 'night': 24.55, 'eve': 32.08, 'morn': 24.25}, 'feels_like': {'day': 33.18, 'night': 25.02, 'eve': 31.88, 'morn': 24.71}, 'pressure': 1007, 'humidity': 30, 'dew_point': 14.06, 'wind_speed': 6.5, 'wind_deg': 315, 'wind_gust': 7.72, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': 40, 'pop': 0.56, 'rain': 1.25, 'uvi': 15}, {'dt': 1651991400, 'sunrise': 1651969924, 'sunset': 1652015577, 'moonrise': 1651990920, 'moonset': 1651949160, 'moon_phase': 0.23, 'temp': {'day': 34.48, 'min': 22.13, 'max': 36.21, 'night': 24.76, 'eve': 33.97, 'morn': 22.13}, 'feels_like': {'day': 33.41, 'night': 25.25, 'eve': 32.77, 'morn': 22.46}, 'pressure': 1004, 'humidity': 27, 'dew_point': 12.69, 'wind_speed': 7.64, 'wind_deg': 312, 'wind_gust': 9.61, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'clouds': 89, 'pop': 0, 'uvi': 15}, {'dt': 1652077800, 'sunrise': 1652056304, 'sunset': 1652101992, 'moonrise': 1652080380, 'moonset': 1652038200, 'moon_phase': 0.25, 'temp': {'day': 33.35, 'min': 23.24, 'max': 33.35, 'night': 24.33, 'eve': 29.11, 'morn': 23.45}, 'feels_like': {'day': 33.9, 'night': 24.8, 'eve': 30.06, 'morn': 23.76}, 'pressure': 1003, 'humidity': 38, 'dew_point': 16.86, 'wind_speed': 9.19, 'wind_deg': 294, 'wind_gust': 11.54, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': 96, 'pop': 0.64, 'rain': 1.63, 'uvi': 15}]}

    di = calculate_dict(x)
    print(di)
    try:
        fil = open("/data_wth.txt", "wt")
        fil.write(str(di))
        fil.close()
    except:
        print("unable to write !!")


if __name__ == '__main__':
    main()
