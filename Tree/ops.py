# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 17:49:30 2020

@author: ME
"""
from collections import defaultdict
from .tree import FPTree

def defdict(dicts):
    return defaultdict(lambda: 0, dicts)
    
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
    transactions=transactions
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
    # print(master.inspect())
    master.add(transactions)
    # print(master.inspect())
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