
import json
import codecs
import urllib as req
import os
import configparser

import locale
def getpreferredencoding(do_setlocale = True):
   return "utf-8"
locale.getpreferredencoding = getpreferredencoding
#Загружаем настройки из файла
class MyConfigParser(configparser.RawConfigParser):
    def get(self, section, option):
        val = configparser.RawConfigParser.get(self, section, option)
        return val.strip('"').strip('/')

if __name__ == "__main__":
    #config = ConfigParser.RawConfigParser()
    conf = MyConfigParser()

conf.read("config/settings.conf")
ace_ip = conf.get("settings", "ip")
ace_port = conf.get("settings", "port")
pomoyka_url = conf.get("settings","pomoyka_url")

list_path = conf.get("path","list_path")
fav_path = conf.get("path","fav_path")
logos_path = conf.get("path","logos_path")
json_path = conf.get("path","json_path")

#Класс логитопв
class logos(object):
    """__init__() functions as the class constructor"""
    def __init__(self, name=None, link=None):
        self.name = name
        self.link = link
        
#Класс списка каналов
class ttv_channel(object):
    """__init__() functions as the class constructor"""
    def __init__(self, name=None, cat=None, fname=None, cid=None):
        self.name = name
        self.cat = cat
        self.fname = fname
        self.cid = cid

def printRAW(*Text):
     RAWOut = open(1, 'w', encoding='utf8', closefd=False)
     print(*Text, file=RAWOut)
     RAWOut.flush()
     RAWOut.close()
#Appen fav file to list
try:
    with codecs.open('/'+fav_path+'/fav.txt','r',encoding='utf8') as fav:
        fav_list = fav.read().splitlines()
except IOError:
    print("File not found")


try:
    with open('logos.json','r',encoding='utf-8') as read_file:
        logos_json = json.load(read_file)
        
except IOError:
    print("File not found")

logos_list=[]
for logo in logos_json:
    logos_list.append(logos(name=logo["name"],link=logo["link"]))

#Download json from pomoyka.win

#url = "http://"+pomoyka_url+"/trash/ttv-list/acelive.json"
#try:
#    req.urlretrieve (url, "acelive.json")
#except Exception,e:
#   print(e.reason)
try:
    with open("acelive.json", "r",encoding='utf-8') as read_file:
        data = json.load(read_file)
except IOError:
    print("File not found")

#Создаем лист объектов и заполняем его
ttv_channel_list = []

for item in data:
    if item["source"] == 'ttv.json': #Провйдер ttv
        printRAW(item["name"])
        ttv_channel_list.append(ttv_channel(item["name"],item["cat"],item["fname"],item["cid"]))
print ("------------")
#Ищем имя канала в списке избранного
with codecs.open('/'+list_path+'/playlist.m3u','w',encoding='utf-8') as acelive:
    acelive.write('#EXTM3U\n')
    for ttv in ttv_channel_list:
        if (any(ttv.name in f for f in fav_list)):
            logo_url =  [x.link for x in logos_list if x.name == ttv.name]
            string_logo_url = ''.join(logo_url)
            
            acelive.write('#EXTINF:-1 group-title='+'"'+ttv.cat+'" tvg-logo="'+string_logo_url+'", '+ttv.name+'\n')
            acelive.write('http://'+ace_ip+':'+ace_port+'/ace/getstream?url=http://91.92.66.82/trash/ttv-list/acelive/'+ttv.fname + '\n')






