import requests
import uuid
import json

key = "16d5e961a6d047fc8b0dc610f3cc213e"
endpoint = "https://api.cognitive.microsofttranslator.com/translate"
location = "eastasia"


def translate(text):
    url = f'{endpoint}?api-version=3.0&to=en'
    # # 设置请求头
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = json.dumps([{'text': text}])

    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        rst = json.loads(response.text)[0]
        return rst['translations'][0]['text']
    else:
        return text
