# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 00:37:09 2020

@author: ME
"""
import os
import json 
import datetime
import pandas as pd
from Utils.data import get_config
from flask import Flask, request
app = Flask(__name__)


def get_digits(string):
    new_string = ''
    for char in string:
        if char.isdigit():
            new_string += char
    return new_string

@app.route("/api/1.0/campaign/report/<page>")
def retrieve_campaign(page):
    df = pd.read_csv('Campaigns.csv')
    total_pages = len(df)//10
    current_page = int(page)
    
    if current_page > total_pages:
        return "Page not found"
    
    row_index = current_page * 10
    page = df.iloc[row_index:row_index+10]
    out_dict = {}
    out_dict['total_pages'] = total_pages
    out_dict['current_page'] = current_page
    out_dict['campaigns'] = [] 
    for _, row in page.iterrows():
        record = {}
        for index, value in zip(row.index, row.values):
            record[index] = value
        out_dict['campaigns'].append(record)
    return json.dumps(out_dict, indent=4)

@app.route("/api/1.0/campaign/recieve")
def recieve():
    content = request.json
    current_datetime = str(datetime.datetime.now()) # 2020-07-05 08:34 
    unique_key = get_digits(current_datetime)
    filename = os.path.join("data", "unread", 
                            unique_key + ".json")
    with open(filename, 'w') as f:
        json.dump(content, f)
    return "Success"
    
if __name__ == "__main__":
    filename = 'config.json'
    config = get_config(filename)
    url = config["url"]
    port = config["port"]     
    app.run(host=url, port=port, debug = True)
    
    
    # 127.0.0.1/recieve