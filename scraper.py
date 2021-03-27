import time
from bs4 import BeautifulSoup
import requests
import pymongo as mongo
import redis

#MongoDB aanmaken
client = mongo.MongoClient("mongodb://127.0.0.1:27017") #Connect to mongo db
db_BitCoin = client["BitCoinTransactie"]
col_BitCoin = db_BitCoin["BitCoin"]




#Scaper
def scrape():
  datan =  [] #Data naam
  dataa = [] #Data Amount
  datab= [] #Data BitCoin
  datat=[] #Data Time
  
  url = 'https://www.blockchain.com/btc/unconfirmed-transactions'
  r = requests.get(url)
  soup = BeautifulSoup(r.content, features="html.parser")

  naam = soup.find_all('a', attrs={'class': 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK'})
  amount = soup.find_all('span', attrs={'class': 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC'})

  #Data name
  for tag in range(len(naam)):
    #print(tag.text.strip())
    datan.append(naam[tag].text[1:])
    #print(amount[x].text.strip())

 #Data Amount
  for tag in range(len(amount)):
    if amount[tag].text.find('$') ==0:
      dataa.append(amount[tag].text[1:])
  
  #Data Bitcoin
  for tag in range(len(amount)):
    if amount[tag].text.find('BTC') > 0:
      datab.append(amount[tag].text)
      
  for tag in range(len(amount)):
    if amount[tag].text.find(':') > 0:
      datat.append(amount[tag].text)   
         
  #print("Hallo ik ben klaar voor te scrapen")
  cach(datan, dataa, datab, datat)
  
#Caching in Redis
def cach(datan, dataa, datab,datat):
  if len(datan) == 0: #if no input
    scrape()
    
  r= redis.Redis()
  #print(len(datan))
  #print(len(dataa))
  #print(len(datab))
  #print(datat)
  
  for x in range(len(datan)):
    data = dataa[x]+"-"+datab[x] + "-" +datat[x]
    r.set(datan[x], data , ex = 60)
  
  print('Cached in Redis')
