import datetime
import os
from os.path import join, dirname

from dotenv import load_dotenv
from openweather.openWeatherDay import OpenWeather_To_Discord

# .envファイルの内容を読み込見込む
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv('OPEN_WEATHER_TOKEN')
CITY = os.getenv('OPEN_WEATHER_CITY')
CITY_JapaneseName =os.getenv('OPEN_WEATHER_CITY_JAPANESE_NAME')
reserchDay =1
MESSAGE=""
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
IMAGE_NAME=os.getenv('SEND_FILE_IMAGE_NAME')



def send_weather_data():
    # ↑Xserverにアップロードするために、リンクがローカルと違うローカルならhome/wadoyoka/pythonproject/tenkiyohou/"+CITY_JapaneseName+".jpgである
    openWeather = OpenWeather_To_Discord(API_KEY=API_KEY,CITY=CITY,lat=-1,lon=-1,CITY_JapaneseName=CITY_JapaneseName,reserchDay=reserchDay,MESSAGE=MESSAGE,discord_webhook_url=discord_webhook_url, IMAGE_NAME=IMAGE_NAME)
    openWeather.send_Discord()
    dt_now = datetime.datetime.now()
    if dt_now.day%5==0:
        extraReserch =5
        openWeather_extra = OpenWeather_To_Discord(API_KEY=API_KEY,CITY=CITY,lat=-1,lon=-1,CITY_JapaneseName=CITY_JapaneseName,reserchDay=extraReserch,MESSAGE=MESSAGE,discord_webhook_url=discord_webhook_url, IMAGE_NAME=IMAGE_NAME)
        openWeather_extra.send_Discord()