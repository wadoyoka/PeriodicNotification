from openweather import tenkiyohou

from firebase_admin import initialize_app
from firebase_functions import scheduler_fn

app = initialize_app()
# Firebaseの諸設定
firebaseRegion="asia-northeast1"
firebaseTimezone = "Asia/Tokyo"

# 各cron情報
weatherSchedule = "0 22 * * *"# 天気送信

# 天気送信
@scheduler_fn.on_schedule(schedule=weatherSchedule, timezone=firebaseTimezone, region=firebaseRegion)
def send_weather_data_to_discord(event):
    tenkiyohou.send_weather_data()



