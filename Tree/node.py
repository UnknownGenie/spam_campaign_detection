from collections import defaultdict, namedtuple

class FPNode(object):
    """A node in an FP tree."""

    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None
        self._num_leaves=None

    @property
    def header_table(self):
        return self.tree.header_table

    def add(self, child):
        """Add the given FPNode `child` as a child of this node."""
        if not isinstance(child, FPNode):
            raise TypeError("Can only add other FPNodes as children")

        if child.item not in self._children:
            self._children[child.item] = child
            child.parent = self

    def remove(self, child):
        """Remove the given FPNode `child` as a child of this node."""

        if not isinstance(child, FPNode):
            raise TypeError("Can only remove other FPNodes as children")
        if child.item in self._children:
            del self._children[child.item]
            
    def disp(self, ind=1):
        print('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

    def search(self, item):
        """
        Check whether this node contains a child node for the given item.
        If so, that node is returned; otherwise, `None` is returned.
        """
        return self._children.get(item, None)
       
    def __contains__(self, item):
        return item in self._children

    @property
    def tree(self):
        """The tree in which this node appears."""
        return self._tree

    @property
    def item(self):
        """The item contained in this node."""
        return self._item

    @property
    def count(self):
        """The count associated with this node's item."""
        return self._count

    def increment(self):
        """Increment the count associated with this node's item."""
        if self._count is None:
            raise ValueError("Root nodes have no associated count.")
        self._count += 1

    @property
    def root(self):
        """True if this node is the root of a tree; false if otherwise."""
        return self._item is None and self._count is None

    @property
    def leaf(self):
        """True if this node is a leaf in the tree; false if otherwise."""
        return len(self._children) ==0

    @property
    def parent(self):
        """The node's parent"""
        return self._parent

    @parent.setter
    def parent(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a parent.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a parent from another tree.")
        self._parent = value

    @property
    def neighbor(self):
        """
        The node's neighbor; the one with the same value that is "to the right"
        of it in the tree.
        """
        return self._neighbor

    @neighbor.setter
    def neighbor(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a neighbor.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a neighbor from another tree.")
        self._neighbor = value

    @property
    def children(self):
        """The nodes that are children of this node."""
        return tuple(self._children.values())
    #         print (tuple(self._children.values()))

    @property
    def num_leaves(self):
        if self.leaf: return 1
        elif self._num_leaves is None: 
            self._num_leaves=sum([i.num_leaves for i in self.children])
        return self._num_leaves 
        
    

    def cond1(self,min_num_children):
        return len(self._children) > min_num_children
    
    
    def cond2(self,freq_threshold):
        count=0
        n=0
        for child in self.children:
            count+=child.count
            n+=1
        return count/n >= freq_threshold

    def cond3(self,n_obf_features):
        temp_node=self
        while(not temp_node.root):
            if temp_node.item not in n_obf_features: return True
            temp_node=temp_node.parent

        return False
    
    def cond4(self,min_num_messages):
        return self.num_leaves>=min_num_messages

    def cond5(self, features):
        return self.item.split(":")[-1] in features
    
    def cond(self,param):
        return (self.cond1(param[0]) 
                and self.cond2(param[1]) 
                and self.cond3(param[2]) 
                and self.cond4(param[3])
                and self.cond5(param[4]))

    def get_items(self,items):
        items.append(self.item)
        
        if self.leaf: return
            
        for child in self.children:
            child.get_items(items)

        
         
    def dfs(self,param,campaign):
        if self.leaf : 
            return
        for child in self.children:
            child.dfs(param,campaign)
        
        if self.cond(param):
            self.parent.remove(self)
            campaign.append(self)
            return              

    def inspect(self, depth=0):
        print(("  " * depth) + repr(self))
        for child in self.children:
            child.inspect(depth + 1)

    def __repr__(self):
        if self.root:
            return "<%s (root)>" % type(self).__name__
        return "<%s %r (%r)>" % (type(self).__name__, self.item, self.count)

