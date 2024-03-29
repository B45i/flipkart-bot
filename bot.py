import json
import requests
import time


TELEGRAM_API = "https://api.telegram.org/bot422654212:AAEWMk1QHJwflVusYaBhOwu5ldTfMIab_BY/"
GOOGLE_URL_SHORTEN_API = 'AIzaSyCTuTmKuO5CFGhWT6VuSKG--L2-0mAwcRk'


def google_url_shortner(url):
    request_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + GOOGLE_URL_SHORTEN_API
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(request_url, data=json.dumps(payload), headers=headers)
    response = json.loads(r.text)
    return response['id']


def get_offers():
    headers = {
        'Fk-Affiliate-Id': 'amalshaja',
        'Fk-Affiliate-Token': '51f8c7a8f5ce4fc19ab3824e2e4bf7d3',
    }

    all_offers = requests.get('https://affiliate-api.flipkart.net/affiliate/offers/v1/all/json', headers=headers).json()
    offers = ""
    i = 0
    for items in all_offers["allOffersList"]:
        offers += "\U000025B6" + items["title"] + " in " + items["description"] + " " + google_url_shortner(items["url"]) + "\n\n"
        if i == 50:
            send_message(offers)
            i = 0
            offers = ""
        i += 1  

def send_message(text):
    params = {'chat_id': -1001134172436, 'text': text}
    response = requests.post(TELEGRAM_API + 'sendMessage', data=params)
    return response


def main():
    last_time = 0
    while True:
        if time.time() - last_time > 86400:
            get_offers()
            last_time = time.time()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
