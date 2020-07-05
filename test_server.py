# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 00:52:52 2020

@author: ME
"""

import requests

res = requests.get('http://localhost:5000/recieve', 
              json={"Testkey":"Success! Ran api completed/"})
print(res.text)