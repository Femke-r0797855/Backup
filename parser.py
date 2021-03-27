import time
from bs4 import BeautifulSoup
import requests
import pymongo as mongo
import redis

#MongoDB aanmaken
client = mongo.MongoClient("mongodb://127.0.0.1:27017") #Connect to mongo db
db_BitCoin = client["BitCoinTransactie"]
col_BitCoin = db_BitCoin["BitCoin"]


#Gegevens uit Redis halen
def parse():
  x = []
  highest = 0
  plaats = -1
  bit = -1
  time = -1
  name = 'IetsAnders'
  
  #print("Ik ben niet lui")
  r = redis.Redis()
  for key in r.keys():
    naam = key
    data = r.get(key)
    #print(data)
    x = data.decode().split("-")
    #print(naam)
    #print(x)
    
    q = x[0].replace(',', '')
    #q = q.replace(',','.')  #ja pff foutje met vanalles

    if float(highest) < float(q): 
      name = naam
      highest = float(q)
      bit = x[1] 
      time = x[2]   
  print(str(name) +" "+ str(highest) +" "+ str(bit)+ str(time))
  
  output = {"hash": name , "amount": highest, "bitcoin": bit , "time": time }
  x = col_BitCoin.insert_one(output)
