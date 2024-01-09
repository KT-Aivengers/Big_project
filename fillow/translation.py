import os
import urllib.request
from dotenv import load_dotenv
import json
import deepl

load_dotenv()



auth_key = os.getenv("auth_key",None)
translator = deepl.Translator(auth_key)

def translate(text):

    result = translator.translate_text(text, target_lang="EN-US")
    return result


# 파파고 번역
# client_id=os.getenv("client_id",None)

# client_secret = os.getenv("client_secret",None)

# def translate(text):
#     encText = urllib.parse.quote(text)
#     data = "source=ko&target=en&text=" + encText
#     url = "https://openapi.naver.com/v1/papago/n2mt"
#     request = urllib.request.Request(url)
#     request.add_header("X-Naver-Client-Id",client_id)
#     request.add_header("X-Naver-Client-Secret",client_secret)
#     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
#     rescode = response.getcode()
#     if(rescode==200):
#         response_body = response.read()
#         response_string = response_body.decode('utf-8')
#         response_json = json.loads(response_string)

#         translated_text = response_json['message']['result']['translatedText']
#         return translated_text
#     else:
#         print("Error Code:" + rescode)