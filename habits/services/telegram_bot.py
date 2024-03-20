import requests

from django.conf import settings

from users.models import User


class TelegramBotService:
    API_URL = f"{settings.TELEGRAM_URL}{settings.BOT_TOKEN}"

    PATHS = {
        "send_message": "sendMessage"
    }

    BASIC_CHAT_ID = "1354243205"

    def __init__(self, username):
        self.user = self.get_user_or_none(username)

    def api_request(
        self,
        url,
        method: str,
        data=None,
        params=None,
        headers=None
    ) -> requests.Response:
        url = f"{self.API_URL}/{url}"

        if data is None:
            data = {}

        if params is None:
            params = {}

        if headers is None:
            headers = {}

        response = requests.request(
            method=method,
            url=url,
            data=data,
            params=params,
            headers=headers
        )

        return response

    def send_message(self, message):
        chat_id = (
            chat_id if (chat_id := self.user.chat_id) else self.BASIC_CHAT_ID
        )

        data = {
            "chat_id": chat_id,
            "text": message,
        }

        self.api_request(
            url=self.PATHS["send_message"],
            method="POST",
            data=data
        )

    def get_user_or_none(self, username: str):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        return user
