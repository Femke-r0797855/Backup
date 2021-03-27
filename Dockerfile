FROM ubuntu:latest
COPY Start.sh Start.sh
COPY scraper.py scraper.py
COPY parser.py parser.py
COPY startbc.py startbc.py
COPY MongoInstal MongoInstal
COPY RedisInstal RedisInstal

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y sudo
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

RUN pip3 install bs4
RUN pip3 install requests
RUN pip3 install pymongo 
RUN pip3 install redis 

RUN chmod +x RedisInstal
RUN chmod +x MongoInstal
RUN bash RedisInstal
RUN bash MongoInstal

RUN chmod +x Start.sh
CMD ["./Start.sh"]

