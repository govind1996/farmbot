
from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import  requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask import make_response
def news():
	r=requests.get("https://economictimes.indiatimes.com/news/economy/agriculture")
	soup=BeautifulSoup(r.content, "html.parser")

	pp=soup.find("div",attrs={"class":"eachStory"})
	qq=pp.find("h3")
	rr=pp.find("p")

	speech=qq.text+" "+rr.text
	return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }



# for link in trr:
#     pname.append(link.text[1:-1])
# trr=soup.find_all("td",attrs={"width":"20%"},{"color":"#000080"})
# x=0;
# for link in trr:
# 	if x%2==0:
# 		man.append(link.text[1:-1])
# 	else:
# 		minn.append(link.text[1:-1])
# 	x=x+1
# record=[]
# #print(str(len(pname))+" "+str(len(man))+" "+str(len(minn)))
# for x in range(0,len(pname)):
# 	aa=pname[x]
# 	bb=man[x]
# 	cc=minn[x]
# 	record.append((aa,bb,cc))


# #for x in record[0:10]:
# #	print(x[1])
# import pandas as pd
# df=pd.DataFrame(record, columns=['pulse_name','max_price','min_price'])
# df.to_csv('agri.csv',index=False,encoding='utf-8')