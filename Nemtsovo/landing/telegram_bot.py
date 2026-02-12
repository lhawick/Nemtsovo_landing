import json

from django.conf import settings
import requests

telegram_api_url = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}'

def send_message(chat_id: int, text: str, inline_keyboard: list[list[dict]] | None = None) -> dict:
    parameters = ['parse_mode=HTML']
    url = telegram_api_url + '/sendMessage?' + '&'.join(parameters)

    payload={
        'chat_id': chat_id, 
        'text': text,
    }

    if inline_keyboard:
        reply_markup = {"inline_keyboard": [list(row) for row in inline_keyboard]}
        payload["reply_markup"] = json.dumps(reply_markup)

    response = requests.post(url, data=payload, timeout=5)
    response.raise_for_status()

    return response.json()