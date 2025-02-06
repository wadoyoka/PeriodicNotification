from openweather import tenkiyohou

# from firebase_admin import initialize_app
# from firebase_functions import scheduler_fn

# # Firebase appの初期化（これは既に行われているはずですが、念のため）
# app = initialize_app()

# firebaseRegion="asia-northeast1"
# cronSchedule = "0 22 * * *"

# @scheduler_fn.on_schedule(schedule=cronSchedule, timezone="Asia/Tokyo", region=firebaseRegion)
# def send_weather_data_to_discord(event):
#     tenkiyohou.send_weather_data()


tenkiyohou.send_weather_data()
