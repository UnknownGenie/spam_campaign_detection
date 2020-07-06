# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 17:47:24 2020

@author: ME
"""
import pandas as pd
import json

def get_config(filename):
    with open(filename, 'rb') as f:
        config = json.load(f)
    return config

def export_csv(campaigns, columns, output_path):
    df = pd.DataFrame(columns = columns)
    for i, campaign in enumerate(campaigns):
        # print(campaign)
        row = dict()
        # change to item[0]
        row['campaignName'] = campaign[0]
        multiline_column = []
        for item in campaign[1:]:
            parts = item.split(":")
            key = parts[-1]
            
            if len(parts) > 2:
                value = ':'.join(parts[:-1])
            else:
                value = parts[0]
            current_value = row.get(key, "Not Found")
            if current_value == "Not Found":
                row[key] = value
            else:
                multiline_column.append(key)
                updated_value = str(current_value + ', ' + value)
                row[key] = updated_value
        row = pd.DataFrame(row, index = [0])
        df = pd.concat((df, row), ignore_index = True)
    df = df.fillna("None")
    df.to_csv(output_path, index=False)
    return df