
from dotenv import load_dotenv
import os
import requests
import json
import uuid

def main():
    global translator_endpoint
    global cog_key
    global cog_region

    try:
        # 讀取環境設定
        load_dotenv()

        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        translator_endpoint = 'https://api.cognitive.microsofttranslator.com'

        # 檢查金鑰
        if not cog_key or not cog_region:
            raise ValueError("請確認 .env 中的 API Key 和 Region 設定。")

        # reviews 資料夾
        reviews_folder = 'reviews'

        # 讀取資料夾中的文字檔
        for file_name in os.listdir(reviews_folder):

            if not file_name.endswith('.txt'):
                continue

            file_path = os.path.join(reviews_folder, file_name)

            # 讀取文字
            with open(file_path, encoding='utf8') as file:
                text = file.read()

            print('\n-------------')
            print(file_name)
            print('\n原文：')
            print(text)

            # 偵測語言
            language = GetLanguage(text)

            print('\nLanguage:', language)

            # 如果不是英文，翻譯成英文
            if language != 'en':
                translation = Translate(text, language)

                print("\nTranslation:")
                print(translation)

            else:
                print("\n這篇文章已經是英文，不需要翻譯。")

    except Exception as ex:
        print("發生錯誤：", ex)


# ==========================
# 偵測文字語言
# ==========================

def GetLanguage(text):

    url = translator_endpoint + '/detect'

    params = {
        'api-version': '3.0'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=body,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    language = result[0]['language']

    return language


# ==========================
# 翻譯成英文
# ==========================

def Translate(text, source_language):

    url = translator_endpoint + '/translate'

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': 'en'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=body,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    translation = result[0]['translations'][0]['text']

    return translation


if __name__ == "__main__":
    main()
