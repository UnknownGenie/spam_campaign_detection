# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 21:23:22 2020

@author: ME
"""
import os
import sys

from Tree.ops import find_frequent_itemsets

from Utils.parser import parse
from Utils.data import export_csv, get_config

from Watch.ops import init_Observer, stop_Observer

def update_buffer_status():
    return not is_buffer_full
     
config = get_config('config.json')

param=[config['min_num_children'],
       config['freq_threshold'],
       config['obf_features'],
       config['min_num_messages'],
       config['features_to_check']]

features = config['features']
columns = config['columns']

is_buffer_full = False

path_to_messages_read = os.path.join("data", "read")
path_to_messages_unread = os.path.join("data", "unread")

observer, handler = init_Observer(path_to_messages_unread)
print("Initialized...")
while True:
    try:
        if handler.buffer_full:
            print("Executing tree ops")
            dataset = parse(path_to_messages_read, features)
            campaigns = find_frequent_itemsets(dataset,2,param)
            print(f"No of camp. is {len(campaigns)}")
            df = export_csv(campaigns, columns)
            handler.buffer_full = False
    
    except KeyboardInterrupt:
        print("Exiting...")
    
    except Exception as e:
        print("Following error encountered")
        print(e)
        print("Exiting...")

stop_Observer(observer)
sys.exit()