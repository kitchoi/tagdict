import collections as _collections


class TagDict(object):
    ''' 
    TagDict is similar to a dictionary except 
    
    Keys are unique tags/attributes of all the items
    Each key can be mapped onto multiple items that have
    that key as a tag
    
    TagDict[*tags] returns a list of items that share the same tags
    TagDict["*"] returns all the items
    '''
    def __init__(self):
        # Keys are tags. Values are sets of ids
        self.data = _collections.defaultdict(set)
        # Keys are ids of the objects. Values are (object,tags)
        self._ids = {}
    
    def add(self,item,tags):
        '''  Add an item with a list of tags.
        
        If tags is empty, the item will not be added to the TagDict
        Input:
        item   - an object
        tags   - a string or a list of strings
        Also raise an Exception if the item is already added
        '''
        if isinstance(tags,str) : tags = [tags,]
        tags = set(tags)
        if id(item) in self._ids:
            raise ValueError("Item already exists in the TagDict")
        self._ids[id(item)] = (item,tags)
        for tag in tags:
            self.data[tag].add(id(item))
    
    def __getitem__(self,tags):
        ''' Get the items that share the tags
        
        Return:
        A list of object
        If the list contains only one object, return the object
        
        Example:
        TagDict["a","b"] returns all items that have both "a" 
                         and "b" as tags
        TagDict["*"] returns all the items in the TagDict
        
        '''
        if tags[0] == '*':
            return [ value[0] for value in self._ids.values() ]
        if isinstance(tags,str): tags = [tags,]
        collected_ids = [ self.data.get(tag,set())
                          for tag in tags ]
        unique_ids = list(set.intersection(*collected_ids))
        if len(unique_ids) == 1:
            return self._ids[unique_ids[0]][0]
        else:
            return tuple([ self._ids[itemid][0] 
                           for itemid in unique_ids ])
    
    def __repr__(self):
        pairs = [ "{tag} : {count} item{plural}".\
                  format(tag=tag,
                         count=len(self.data[tag]),
                         plural='s' if len(self.data[tag]) > 1 else '')
                  for tag in self.data.keys() ]
        return "<TagDict {"+", ".join(pairs)+"}>"
    
    def remove(self,item):
        ''' Remove an item from the TagDict.
        Any tag that points to no object will be removed too.
        Input:
        item   - an object inside the TagDict
        '''
        self.replace_tags(item,[])
    
    def add_tag(self,item,tag):
        ''' Add a tag to an item in the TagDict
        
        Input:
        item   - an object inside the TagDict
        tag    - a string
        '''
        assert isinstance(tag,str)
        try:
            self._ids[id(item)][1].add(tag)
        except KeyError:
            raise KeyError(str(item)+" is not in the TagDict.")
        self.data[tag].add(id(item))
    
    def remove_tag(self,item,tag):
        ''' Remove a tag from an item in the TagDict
        
        Input:
        item   - an object inside the TagDict
        tag    - a string
        '''
        assert isinstance(tag,str)
        try:
            self._ids[id(item)][1].remove(tag)
        except KeyError:
            raise KeyError(str(item)+" is not in the TagDict.")
        self.data[tag].remove(id(item))
        if len(self.data[tag]) == 0:
            del self.data[tag]
    
    def replace_tags(self,item,newtags):
        ''' Replace the tags of an item.
        
        Any tag that points to no object will be removed too.
        
        Input:
        item     - an object inside the TagDict
        newtags  - a string or a list of strings
        '''
        if isinstance(newtags,str): newtags = {newtags}
        if not isinstance(newtags,set): newtags = set(newtags)
        try:
            oldtags = self._ids[id(item)][1]
        except KeyError:
            raise KeyError(str(item)+" is not in the TagDict.")
        tags2rm = oldtags - newtags
        tags2add = newtags - oldtags
        for tag in tags2rm:
            self.remove_tag(item,tag)
        for tag in tags2add:
            self.add_tag(item,tag)
        if len(newtags) == 0:
            del self._ids[id(item)]
    
    def view_all_inputs(self):
        ''' Show all the items and their tags'''
        return tuple(self._ids.values())
    
    def view_all_bytags(self,tags=None):
        ''' Show tags and all the corresponding items

        Input:
        tags  - a tag or a list of tags (default: all tags)
        '''
        if tags is None: tags = self.data.keys()
        if isinstance(tags,str):
            tags = [tags,]
        return { tag: [ self._ids[itemid][0] 
                        for itemid in self.data[tag]] 
                 for tag in tags }
    
    def get_tags(self,item):
        try:
            return list(self._ids[id(item)][1])
        except KeyError:
            raise KeyError(str(item)+" is not in the TagDict.")
    
    def update(self,other):
        ''' Update this TagDict with another TagDict'''
        for itemid,item_info in other._ids.items():
            other_item,other_tags = item_info
            if itemid in self._ids:
                self_item,self_tags = self._ids[itemid]
                self.replace_tags(item,self_tags.union(other_tags))
            else:
                self.add(other_item,other_tags)

if __name__ == '__main__':
    data = TagDict()
    # 4 unhashable items
    data.add({'Name':'Ben'},tags=['Male','Student'])
    data.add({'Name':'Tom','Age':40},tags=['Male','Teacher'])
    data.add({'Name':'Tina','Age':30},tags=['Female','Teacher'])
    data.add({'Name':'Ann'},tags=['Female','Student'])
    print data["*"]                    # --> All the items
    print data['Teacher','Female']     # --> {'Age': 30, 'Name': 'Tina'}
    print data['Student']              # --> ({'Name': 'Ben'}, 
                                       #      {'Name': 'Ann'})
    # Add one more tag for one of the items
    data.add_tag(data['Teacher','Female'],'Mother')
    print data['Mother']               # --> {'Age': 30, 'Name': 'Tina'}
    # Remove a tag for one of the items
    data.remove_tag(data['Male','Student'],'Student')
    print data['Student']              # --> {'Name': 'Ann'}
    # Replace all the tags of one of the items
    data.replace_tags(data['Female','Mother','Teacher'],'Human')
    print data['Mother']               # --> ()
    print data['Human']                # --> {'Age': 30, 'Name': 'Tina'}
    # Change the content of one of the items
    data['Human']['Age']=31
    print data['Human']                # --> {'Age': 31, 'Name': 'Tina'}
    # Remove an item
    data.remove(data['Student'])
    print data['Student']              # ()
    print data['*']                    # Only 3 items now
    # Updating a list of items will fail
    try:
        data.add_tag(data['Male'],'Martian')
    except KeyError:
        print "More than one item were requested."
        for man in data['Male']:
            data.add_tag(man,'Martian')
    print data['Martian']             # --> ({'Name': 'Ben'}, 
                                      #      {'Age': 40, 'Name': 'Tom'})
