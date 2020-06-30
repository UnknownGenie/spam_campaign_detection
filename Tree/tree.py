from collections import defaultdict, namedtuple
from Tree.node import FPNode

def defdict(dicts):
    return defaultdict(lambda: 0, dicts)

class FPTree(object):
    """
    An FP tree.
    This object may only store transaction items that are hashable
    (i.e., all items must be valid as dictionary keys or set members).
    """

    Route = namedtuple("Route", "head tail")

    def __init__(self, items = defaultdict(lambda: 0)):
        # The root node of the tree.
        self._root = FPNode(self, None, None)

        # A dictionary mapping items to the head and tail of a path of
        # "neighbors" that will hit every node containing that item.
        self._routes = {}
        self._header_table=items
        self._last_merged = self._root

        

    @property
    def header_table(self):
        """The header table of the tree"""
        return self._header_table

    #more like updates the stuff
    def header_table_sort(self):
        
        self._header_table=defdict({k: v for k, v in sorted(self._header_table.items(), key=lambda item: item[1],reverse=True)})

    @property
    def root(self):
        """The root node of the tree."""
        return self._root
    
    def swap_required(self, node):
        if node.parent == self.root:
            return False
        
        all_childs_count = 0
        for child in node.children:
            all_childs_count += child.count
        
        if node.parent.count <= all_childs_count:
            return True
        else:
            return False  
        
    def add_on_fly(self, transaction, start_node = None):
        if not start_node:
            start_node = self.root
            self._last_merged = self.root
        
        if start_node.children:
            for child in start_node.children:
                if child.item in transaction:
                    child.increment()
                    transaction.remove(child.item)
                    self._last_merged = child
                    
                    if self.swap_required(child):
                        while self.swap_required(child):
                            self.tree = child.swap(child.parent)
                            
                transaction = self.add_on_fly(transaction, child)
        if transaction:
            self.add_traditional(transaction, self._last_merged)
            transaction = []
            return transaction 
        return transaction
        
    def add_traditional(self, transaction, start_node):
        """Add a transaction to the tree."""
        point = start_node
        for item in transaction:
            next_point = point.search(item)
            if next_point:
                # There is already a node in this tree for the current
                # transaction item; reuse it.
                next_point.increment()
            else:
                # Create a new point and add it as a child of the point we're
                # currently looking at.
                next_point = FPNode(self, item)
                point.add(next_point)

                # Update the route of nodes that contain this item to include
                # our new node.
                self._update_route(next_point)
            point = next_point
        
    def add(self,transactions, on_fly = True):
        if all(isinstance(i, list) for i in transactions):
            for transaction in transactions:
                if on_fly:
                    print(transaction)
                    _= self.add_on_fly(transaction)
                else:
                    id,content=transaction[-1],transaction[0]
                    transaction=[content]+[k for k,v in self.header_table.items() 
                                       if k in transaction[1:-1]]+[id]
        
                    self.add_traditional(transaction, self._root)
        else:
            print("provide transaction as list")

    

    def _update_route(self, point):
        """Add the given node to the route through all nodes for its item."""
        assert self is point.tree

        try:
            route = self._routes[point.item]
            route[1].neighbor = point  # route[1] is the tail
            self._routes[point.item] = self.Route(route[0], point)
        except KeyError:
            # First node for this item; start a new route.
            self._routes[point.item] = self.Route(point, point)

    def items(self):
        """
        Generate one 2-tuples for each item represented in the tree. The first
        element of the tuple is the item itself, and the second element is a
        generator that will yield the nodes in the tree that belong to the item.
        """
        for item in self._routes.keys():
            yield (item, self.nodes(item))

    def nodes(self, item):
        """
        Generate the sequence of nodes that contain the given item.
        """

        try:
            node = self._routes[item][0]
        except KeyError:
            return

        while node:
            yield node
    #             print(node)
            node = node.neighbor
    #         print(node)

    def prefix_paths(self, item):
        """Generate the prefix paths that end with the given item."""

        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))

    def inspect(self):
        print("Tree:")
        self.root.inspect(1)

        print()
        print("Routes:")
        for item, nodes in self.items():
            print("  %r" % item)
            for node in nodes:
                print("    %r" % node)

    def getcampaign(self,param):
        campaign=[]
        self.root.dfs(param,campaign)
        itemlist=[]
        for item in campaign:
            t=[]
            item.get_items(t)
            itemlist+=[t]
        return itemlist