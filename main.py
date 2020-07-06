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
     

def create_tree():
    dataset = parse(path_to_messages_read, features)
    campaigns = find_frequent_itemsets(dataset,
                                       min_support,
                                       param)
    print(f"No of camp. is {len(campaigns)}")
    _ = export_csv(campaigns, columns, csv_path)

config = get_config('config.json')

param=[config['min_num_children'],
       config['freq_threshold'],
       config['obf_features'],
       config['min_num_messages'],
       config['features_to_check']]

features = config['features']
columns = config['columns']
path_to_messages_read = config['dest_path']
path_to_messages_unread = config['src_path']
min_support = config['min_support']
csv_path = config['csv_path']

observer, handler = init_Observer(path_to_messages_unread)
create_tree()
print("Initialized...")
while True:
    try:
        if handler.buffer_full:
            create_tree()
            handler.buffer_full = False
    
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print("Following error encountered")
        print(e)
        print("Exiting...")
        break
stop_Observer(observer)
sys.exit()