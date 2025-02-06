import io
import re
from datetime import datetime, timedelta, timezone
from pprint import pprint

import japanize_matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import requests
from openweather.discord_photo import Discord_Send_Photo


class OpenWeather_To_Discord:
    url=""
    def __init__(self,API_KEY, CITY, lat, lon ,CITY_JapaneseName,reserchDay, MESSAGE,discord_webhook_url, IMAGE_NAME):
        self.API_KEY=API_KEY
        self.CITY=CITY
        self.lat=lat
        self.lon=lon
        self.CITY_JapaneseName=CITY_JapaneseName
        self.reserchDay=reserchDay
        self.MESSAGE=MESSAGE
        self.IMAGE = None  # バイナリデータを保持するための変数
        self.IMAGE_NAME=IMAGE_NAME
        self.discord_webhook_url=discord_webhook_url
        if self.lat == -1:
            self.url = f"http://api.openweathermap.org/data/2.5/forecast?appid={self.API_KEY}&q={self.CITY}&units=metric"
        elif self.CITY == -1:
            self.url = f"http://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&appid={self.API_KEY}&units=metric"
        
    def main_excuse(self):
        # print(self.url)
        response = requests.get(self.url)
        # time.sleep(1.5)
        jsondata = response.json()

        #データフレーム
        df = pd.DataFrame(columns=["気温","体感温度","降水量"])
        #タイムスタンプを変換
        tz = timezone(timedelta(hours=+9), "JST")
        count = 0
        
        for dat in jsondata["list"]:
            if count==8*self.reserchDay+1:
                break
            jst = str(datetime.fromtimestamp(dat["dt"], tz))[:-9]
            # print("UST={ust}, JST={jst}".format(ust=dat["dt_txt"], jst=jst))
            m = re.findall(r'\d+', jst)
            jst=m[1]+"-"+m[2]+"\n"+m[3]+":"+m[4]
            temp = dat["main"]["temp"]
            feels_like = dat["main"]["feels_like"]
            rain=0
            try:
                rain = dat["rain"]["3h"]
            except:
                print('rain=None')
            df.loc[jst] = [temp,feels_like,rain]
            count+=1
            if count==40:
                break
        
        
        temperature = df[["気温","体感温度"]]
        # pprint(temperature)
        precipitation = df["降水量"]

        # pprint(temperature)
        # pprint(precipitation)
        plt.figure(figsize=(15,8))
        # axesオブジェクトの作成
        ax1 = plt.subplot(1,1,1)
        # 軸を反転したaxesオブジェクトの作成
        ax2 = ax1.twinx()
        # グラフの作成
        temperature.plot(kind="line", linewidth=3, color=['r', 'orange'], ax=ax1, style=['-',':'])
        precipitation.plot(kind="bar", alpha=0.6, ax=ax2, figsize=(15,8))

        # 縦軸のラベルの追加
        ax1.set_ylabel("気温(℃)", fontsize=18)
        ax1.set_ylim(-10,40)
        handler1, label1 = ax1.get_legend_handles_labels()
        handler2, label2 = ax2.get_legend_handles_labels()
        ax1.legend(handler1 + handler2, label1 + label2, loc=2, borderaxespad=0.)
        ax1.set_xlabel("時間", fontsize=18)
        ax1.tick_params(labelsize=13)
        ax1.grid()
        ax2.set_ylabel("降水量(mm)", fontsize=18)
        ax2.tick_params(labelsize=13)
        if precipitation.max()<=1.0:
            ax2.set_ylim(0,1.0)
        # グラフの表示
        if count>=3*8:
            plt.xticks(range(0,len(precipitation)+1,3))
        plt.title(self.CITY_JapaneseName+"の"+str(int(count/8))+"日間の天気",fontsize =25, fontweight ="bold")
        
        
        
        # 画像をバイナリデータとして保存
        image_io = io.BytesIO()
        plt.savefig(image_io, format="png")
        plt.close()
        image_io.seek(0)
        return image_io
    
    def send_Discord(self):
        """画像のバイナリデータを `self.IMAGE` に保持して送信"""
        self.IMAGE = self.main_excuse()
        discord = Discord_Send_Photo(self.MESSAGE, self.IMAGE, self.IMAGE_NAME,self.discord_webhook_url)
        discord.send_discord()

