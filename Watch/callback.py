# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:58:15 2020

@author: ME
"""
import watchdog.events
import shutil
import os

class Handler(watchdog.events.PatternMatchingEventHandler): 
    def __init__(self, threshold = 5): 
        # Set the patterns for PatternMatchingEventHandler 
        watchdog.events.PatternMatchingEventHandler.__init__(self, #patterns=['*.json'], 
                                                             ignore_directories=True, case_sensitive=False) 
        self.dest_dir = os.path.join("data", "read") 
        self.src_dir = os.path.join("data", "unread")
        self.threshold = threshold
        self.buffer_full = False
        
    def on_created(self, event): 
        nb_files = self.count_files(self.src_dir)
        if nb_files >= self.threshold:
            for file in os.listdir(self.src_dir):
                 src_path = os.path.join(self.src_dir, file)
                 dest_path = os.path.join(self.dest_dir, file)
                 shutil.move(src_path, dest_path)
            self.buffer_full = True
    
    def count_files(self, path):
        return len(os.listdir(path))