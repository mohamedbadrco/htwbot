from urllib.request import Request, urlopen
import json
import random
import tweepy
from time import sleep
import os
import dotenv
import requests


dotenv.load_dotenv()

hashtags = ["#NFTCommunity", "#NFTsales" "#Linux",  "#digitalart",  "#penguin" , "#asciiart" ,"#Matrix"]

def getitem():
    # calling rarible api
    req = Request(
        url='https://api.rarible.org/v0.1/items/byOwner?owner=ETHEREUM:0x534cfe9955C453af774BecCeaAD4598E2c41082d', 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req)
    
    # storing the JSON response 
    # from url in data
    data_json = json.loads(webpage.read())
    
    # return  the json response
    return (random.choice(data_json["items"]))

def getapi():
    consumer_key = os.environ["API_KEY"]
    consumer_secret = os.environ["API_KEY_S"]
    access_token = os.environ["ACS_TKN"]
    access_token_secret = os.environ["ACS_TKN_S"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)

def tweet():
    #get twitter api
    api = getapi()

    #get item from rar api 
    item = getitem()

    url = (item["meta"]["content"][0]["url"])
    price = item['bestSellOrder']['makePrice']

     
    cht = [random.choice(hashtags),random.choice(hashtags),random.choice(hashtags)]

    text0 = f"""


    
	
    new collocation of unique #ASCII #gifs art available @ 
    https://rarible.com/Photo_Hash 
    #RT and #Follow @mobadr for the chance to won one free #NFT
     
    #ETH #Crypto #NFTs {cht[0]} {cht[1]} {cht[2]}
    {item["meta"]["name"]}  >  {price} {item["blockchain"]} 
      """

    text1 = f"""
    buy NEW Item #ASCII #gifs art

    {item["meta"]["name"]}  >  {price} {item["blockchain"]} 
	
    available @ 
    https://rarible.com/Photo_Hash 

    #RT and #Follow @mobadr for the chance to won one free #NFT
     
    #ETH #Crypto #NFTs 
    {cht[0]} {cht[1]} {cht[2]} """

    text2 = f"""
	{item["meta"]["name"]}  >  {price} {item["blockchain"]} 
	
    Buy Item  art available @  https://rarible.com/Photo_Hash 

    #RT and #Follow @mobadr for the chance to won one free #NFT
     
     #ASCII #gifs
    #ETH #Crypto #NFTs 
     {cht[0]} {cht[1]} {cht[2]} """
	 
	 
    texts=[text0,text1,text2]

    # print(len(text))
    response = requests.get(url)
    open("image.gif", "wb").write(response.content)

    api.update_status_with_media(status=random.choice(texts),filename="image.gif")

def follow(serchq):
    api = getapi()
    a = 0 
    for tweet in api.search_tweets(q=serchq, lang="en"):
        a += 1
        try:
            api.create_friendship(user_id=tweet.user.id)
        except:
            continue
        if a > 5:
            break

    

def like(serchq):
    api = getapi()
    a = 0
    for tweet in api.search_tweets(q=serchq, lang="en"):
        a += 1
        try:
            api.create_favorite(id=tweet.id)
        except:
            continue
        if a > 5:
            break
        

def News(q):
     
    # BBC news api
    # following query parameters are used
    # source, sortBy
    #  and apiKey
    query_params = {
      "sortBy": "top",
      "apiKey": os.environ["NEWS_API_K"],
      "q": q
    }
    main_url = " https://newsapi.org/v2/everything"
 
    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
    # print(open_bbc_page)
 
    # getting all articles in a string article
    article = open_bbc_page["articles"]
 
    # empty list which will
    # contain all trending news
    results = []
     
    ar = random.choice(article)
         
        # printing all trending news
    return (ar)

def tweetnews():
    api = getapi()
    name = ["nft","Crypto","ETH","Linux"]
    ar = News(random.choice(name))

    cht = [random.choice(hashtags),random.choice(hashtags),random.choice(hashtags)]
    if ar["urlToImage"] != None:
        response = requests.get(ar["urlToImage"])
        open("image.jpeg", "wb").write(response.content)

    title = ar["title"]
    author = ""
    if ar["author"] != None:
        author = ar["author"]
    arurl = ar["url"]
    text = f""" {author} 

    {title } 

    {arurl}

    @mobadr_co
    #ETH #Crypto #NFTs #NEWS
    {cht[0]} {cht[1]} {cht[2]} """
    # print(len(text))
    # print(text)
    if ar["urlToImage"] != None:
        api.update_status(status=text)
    else:
        api.update_status_with_media(status=text,filename="image.jpeg")


def main():
    
    name = ["nft","Crypto","ETH","Linux"]
    while True:
        try:
            follow(random.choice(name))
        except:
            pass
        try:
            like(random.choice(name))
        except:
            pass
        try:
            tweet()
        except:
            pass
        sleep(1800)
        try:
            tweetnews()
        except:
            pass 
        sleep(1800)

if __name__ == "__main__":
    main()



    
            
            