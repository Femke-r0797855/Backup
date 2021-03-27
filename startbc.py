import time
import scraper
import parser

while True:
  scraper.scrape()
  time.sleep(59)
  parser.parse()
  
