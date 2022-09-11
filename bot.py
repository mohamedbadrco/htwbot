from urllib.request import Request, urlopen
import json
import random
import tweepy
from time import sleep
import os
import dotenv
import requests


dotenv.load_dotenv()

def getitem():
    req = Request(
        url='https://api.rarible.org/v0.1/items/byOwner?owner=ETHEREUM:0x534cfe9955C453af774BecCeaAD4598E2c41082d', 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req)
    
    # storing the JSON response 
    # from url in data
    data_json = json.loads(webpage.read())
    
    # print the json response
    return (random.choice(data_json["items"]))

def tweet():
    
    consumer_key = os.environ["API_KEY"]
    consumer_secret = os.environ["API_KEY_S"]
    access_token = os.environ["ACS_TKN"]
    access_token_secret = os.environ["ACS_TKN_S"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    item = getitem()
    url = (item["meta"]["content"][0]["url"])
    price = item['bestSellOrder']['makePrice']

   

    text = f"""{item["meta"]["name"]}  >  {price} ${item["blockchain"]}

    new collocation of unique #ASCII #gifs art available @ https://rarible.com/Photo_Hash 
    #RT and #Follow for the chance to won one free #NFTs 

    #NFTCommunity #NFTsales #Linux #ETH #Crypto #digitalart #NFTs #penguin #asciiart #Matrix"""


    print(len(text))
    response = requests.get(url)
    open("image.gif", "wb").write(response.content)

    api.update_status_with_media(status=text,filename="image.gif")

def main():
    while True:
        tweet()
        sleep(1800)


if __name__ == "__main__":
    main()