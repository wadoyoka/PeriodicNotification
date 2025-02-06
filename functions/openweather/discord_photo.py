from discordwebhook import Discord


class Discord_Send_Photo:
    def __init__(self, MESSAGE, IMAGE, IMAGE_NAME,DISCORD_WEBHOOK):
        self.MESSAGE = MESSAGE
        self.IMAGE = IMAGE  # `BytesIO` オブジェクトを受け取る
        self.IMAGE_NAME=IMAGE_NAME
        self.DISCORD_WEBHOOK = DISCORD_WEBHOOK

    def send_discord(self):
        discord = Discord(url=self.DISCORD_WEBHOOK)
        discord.post(content=self.MESSAGE, file={self.IMAGE_NAME: self.IMAGE.getvalue()})
