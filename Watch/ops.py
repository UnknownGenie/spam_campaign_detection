# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 18:50:56 2020

@author: ME
"""
from watchdog.observers import Observer
from Watch.callback import Handler

def init_Observer(path):
    event_handler = Handler() 
    observer = Observer() 
    observer.schedule(event_handler, path=path, recursive=True) 
    observer.start()
    return observer, event_handler

def stop_Observer(observer):
    observer.stop() 
    observer.join()