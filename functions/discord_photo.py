from discordwebhook import Discord


class Discord_Send_Photo:
    def __init__(self, MESSAGE, IMAGE, DISCORD_WEBHOOK):
        self.MESSAGE = MESSAGE
        self.IMAGE = IMAGE  # `BytesIO` オブジェクトを受け取る
        self.DISCORD_WEBHOOK = DISCORD_WEBHOOK

    def send_discord(self):
        discord = Discord(url=self.DISCORD_WEBHOOK)
        discord.post(content=self.MESSAGE, file={"weather.png": self.IMAGE.getvalue()})
