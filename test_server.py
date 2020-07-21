# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 00:52:52 2020

@author: ME
"""

import requests
import json


data = json.loads("""{"subject":"eBay - verify your account information","originEmailAddress":"aw45-confirm@ebay.com","originName":"Ebay Team","originDomain":"ebay.com","originSourceIP":"217.129.34.6","originDate":"2005-07-01T23:53:39.000+0000","originDayOfWeek":"FRIDAY","phpScript":null,"xMailer":"Microsoft Outlook Express 6.00.2600.0000","list_unsubscribe":null,"list_id":null,"emailLayoutText":"T","emailLayoutHtml":"T","language":"en","readability":{"lengthSubject":38,"lengthBody":1174,"charset":"windows-1251","contentType":"text/html","numberSentences":12,"numberComplexWords":24,"numberOfWords":197,"numberSyllables":316,"numberCharacters":938,"numberUniqueTerms":0,"SMOG":11.208,"fleschReadingEase":54.469,"fleschKincaidGradeLevel":9.74,"ARI":9.205,"gunningFog":11.2,"colemanLiau":11.245,"SMOGIndex":10.746,"smog":11.208,"ari":9.205,"smogindex":10.746},"top10simpleWord":{"-191501435":3,"3202466":2,"1343373508":3,"3492908":2,"3106197":7,"747805177":3,"1233099618":2,"1978310868":4,"109201676":3,"1823":2},"top10_2gram":{"375973481":1,"559289431":1,"-680225034":1,"2509861":1,"-278515104":1,"-7149420":1,"1370729227":2,"2014611228":1,"527417444":1,"-923511015":2},"embeddedURLs":null,"attachments":[]}""")
res = requests.get('http://127.0.0.1:443/api/1.0/campaign/recieve', 
              json=data)
with open('resonse_recieve.json', 'w') as f:
	json.dump(res.text, f)


res = requests.get('http://127.0.0.1:443/api/1.0/campaign/report/3')
with open('resonse_report.json', 'w') as f:
	json.dump(res.text, f)
print(res.text)
print(res.status_code)