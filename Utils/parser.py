# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 17:43:07 2020

@author: ME
"""

import os
import json
from urllib.parse import urlparse

def parse(path, features):
    full_data=[]
    tid=0
    all_files = os.listdir(path)
    
    
    for file in all_files:
        if file.endswith("eml"):
            continue
        data=[]
        file_path = os.path.join(path, file)
        
        with open(file_path, 'r', encoding='utf8') as f:
            json_dict = json.load(f)
        
        for feature in features:
            if isinstance(json_dict[feature], str):
                if (not json_dict[feature]) or (json_dict[feature] == "None"):
                    continue
            if feature == 'readability':
                temp = json_dict.get(feature, None)
                if isinstance(temp, dict):
                    content = temp.get('contentType', None)
                    charset = temp.get('charset', None)
                    if content:
                        data += ["{}:contentType".format(content)]
                    if charset:
                        data += ["{}:charset".format(charset)] 
                continue
            
            if feature == 'embeddedURLs':
                urls = json_dict.get(feature, None)
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
                    val = json_dict.get(feature, None)
                    if val:
                        data += ['{}:{}'.format(val, feature)]
                continue 
            
            if feature == 'emailLayoutText':
                if json_dict['readability']['contentType'] != "multipart/alternative":
                    val = json_dict.get(feature, None)
                    if val:
                        data += ['{}:{}'.format(val, feature)]
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
                attached = json_dict.get(feature, None)
                if not isinstance(attached, list):
                    for attachment in attached:
                        filename = attachment.get('fileName', None)
                        if filename:
                            data+=['{}:{}'.format(filename, feature)]
                continue
            # All other features are handled there other than mentioned and checked above
            val = json_dict.get(feature, None)
            if not val:
                continue
            data += ["{}:{}".format(val, feature)]
        tid+=1
        data+=[str(tid)+':id']
        full_data.append(data)      
        
    return full_data
