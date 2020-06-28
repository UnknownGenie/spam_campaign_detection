# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 21:23:22 2020

@author: ME
"""

import json
import os
from urllib.parse import urlparse
from collections import defaultdict
from Tree.tree import FPTree
import pandas as pd

def parse(path="data"):
    full_data=[]
    tid=0
    all_files = os.listdir(path)
    
    features = ['readability', 'emailLayoutHtml', 'emailLayoutText', 
                'embeddedURLs', 'originDomain', 'originSourceIP', 
                'language', 'originEmailAddress', 'originName', 
                'subject', 'originDate', 'attachments']
    
    for file in all_files:
        if file.endswith("eml"):
            continue
        data=[]
        file_path = os.path.join(path, file)
        
        with open(file_path, 'r', encoding='utf8') as f:
            json_dict = json.load(f)
        
        for feature in features:
            if feature == 'readability':
                temp = json_dict.get(feature, "None")
                if isinstance(temp, dict):
                    content = temp.get('contentType', "None")
                    charset = temp.get('charset', "None")
                    data += ["{}:contentType".format(content),
                             "{}:charset".format(charset)] 
                continue
            
            if feature == 'embeddedURLs':
                urls = json_dict.get(feature, "None")
                if isinstance(urls, list):
                    for item in urls:
                        tokens =urlparse(item['url'])
                        data+=['{}:{}_netloc'.format(tokens.netloc, feature)]
                        if tokens.path and not tokens.path == '/' :
                            data+=['{}:{}_path'.format(tokens.path, feature)]
                        if tokens.params:
                            data+=['{}:{}_params'.format(tokens.params, feature)]
                continue
            if feature == 'emailLayoutHtml':
                if json_dict['readability']['contentType'] == "multipart/alternative":
                    data += ['{}:{}'.format(json_dict[feature], feature)]
                continue 
            
            if feature == 'emailLayoutText':
                if json_dict['readability']['contentType'] != "multipart/alternative":
                    data += ['{}:{}'.format(json_dict[feature], feature)]                
                continue
        
            # if feature == 'top10simpleWord':
            #     words = json_dict.get(feature, "None")
            #     if not isinstance(words,dict):
            #         for item in words.keys():
            #             data += ['{}:word'.format(item)]
            #     else:
            #         data += ["None:word"]
            #     continue

            if feature == 'attachments':
                attached = json_dict.get(feature, "None")
                if not isinstance(attached, list):
                    for attachment in attached:
                        filename = attachment.get('fileName', "None")
                        data+=['{}:{}'.format(filename, feature)]
                continue
            # All other features are handled there other than mentioned and checked above
            val = json_dict.get(feature, "None")
            if val == "":
                continue
            data += ["{}:{}".format(val, feature)]
        tid+=1
        data+=[str(tid)+':id']
        full_data.append(data)      
        
    return full_data

def defdict(dicts):
    return defaultdict(lambda: 0, dicts)

def export_csv(campaigns):
    columns = ['contentType', 'charset', 'emailLayoutHtml', 'emailLayoutText', 
            'embeddedURLs_netloc', 'embeddedURLs_path', 'embeddedURLs_params',
            'originDomain', 'originSourceIP', 
            'language', 'originEmailAddress', 'originName', 
            'subject', 'originDate', 'attachments']
    df = pd.DataFrame(columns = columns)
    for i, campaign in enumerate(campaigns):
        # print(campaign)
        row = dict()
        multiline_column = []
        for item in campaign:
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
    df.to_csv("Campaigns.csv", index=False)
    return df
    
def find_frequent_itemsets(transactions, minimum_support, params, include_support=True):
    """
    Find frequent itemsets in the given transactions using FP-growth. This
    function returns a generator instead of an eagerly-populated list of items.
    The `transactions` parameter can be any iterable of iterables of items.
    `minimum_support` should be an integer specifying the minimum number of
    occurrences of an itemset for it to be accepted.
    Each item must be hashable (i.e., it must be valid as a member of a
    dictionary or a set).
    If `include_support` is true, yield (itemset, support) pairs instead of
    just the itemsets.
    """
    if 0 < minimum_support <= 1:
        minimum_support = minimum_support * len(transactions)
    
    # onflytran=transactions[len(transactions)//2:]
    transactions=transactions[:len(transactions)//2]
    items = defaultdict(lambda: 0)  # mapping from items to their supports

    # if using support rate instead of support count
    

    # Load the passed-in transactions and count the support that individual
    # items have.
    for transaction in transactions:
        for item in transaction:
            items[item] += 1
    

    
    # items = dict(
    #     (item, support) for item, support in items.items() if support >= minimum_support
    # )
    # Remove infrequent items from the item support dictionary and
    #sorts the dictionary  according to value
    items= defdict({k: v for k, v in 
                   sorted(items.items(), 
                          key=lambda item: item[1], 
                          reverse=True) \
                   if v >= minimum_support or \
                   k.split(":")[1] == 'id'or \
                   k.split(":")[1] == 'content'})
    # Build our FP-tree. Before any transactions can be added to the tree, they
    # must be stripped of infrequent items and their surviving items must be
    # sorted in decreasing order of frequency.
    
    master = FPTree(items)
    print(master.inspect())
    master.add(transactions,on_fly = False)
    # Tree is built

    # while True:
    #     if is_new_transcation:
    #         master.add(onflytran, on_fly = True)

    #         # On fly method:
    #         append to header_table
    #         resort it
    #         key: value   difference key: value 
    # print(master.inspect())
    return master.getcampaign(params)

dataset = parse("data")
# print(dataset)
features_to_check = ['embeddedURLs_path', 'contentType', 'language']
param=[1,1,[],1, features_to_check]

campaigns = find_frequent_itemsets(dataset,2,param)
print(f"No of camp. is {len(campaigns)}")
df = export_csv(campaigns)