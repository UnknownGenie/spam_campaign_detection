# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 00:37:09 2020

@author: ME
"""
import os
import json 
import datetime

from flask import Flask, request
app = Flask(__name__)

def get_digits(string):
    new_string = ''
    for char in string:
        if char.isdigit():
            new_string += char
    return new_string

@app.route("/recieve")
def test():
    content = request.json
    current_datetime = str(datetime.datetime.now())
    unique_key = get_digits(current_datetime)
    filename = os.path.join("data", "unread", 
                            unique_key + ".json")
    with open(filename, 'w') as f:
        json.dump(content, f)
    
    return "Success"
    
if __name__ == "__main__":     
    app.run(debug = True)