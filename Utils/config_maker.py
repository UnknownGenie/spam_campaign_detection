# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 18:41:53 2020

@author: ME
"""


features = ['readability', 'emailLayoutHtml', 'emailLayoutText', 
                'embeddedURLs', 'originDomain', 'originSourceIP', 
                'language', 'originEmailAddress', 'originName', 
                'subject', 'originDate', 'attachments']
columns = ['campaignName', 'id', 'contentType', 'charset', 'emailLayoutHtml', 'emailLayoutText', 
            'embeddedURLs_netloc', 'embeddedURLs_path', 'embeddedURLs_params',
            'originDomain', 'originSourceIP', 
            'language', 'originEmailAddress', 'originName', 
            'subject', 'originDate', 'attachments']    
features_to_check = ['embeddedURLs_path', 'contentType', 'language']
min_num_children = 1
freq_threshold = 1
obf_features = []
min_num_messages = 1


config = {'features': features,
          'columns' : columns,
          'features_to_check': features_to_check,
          'min_num_children': min_num_children,
          'freq_threshold': freq_threshold,
          'obf_features': obf_features,
          'min_num_messages': min_num_messages}
with open('config.json', 'w') as f:
    json.dump(config, f, sort_keys=True, indent=4)
