import collections as _collections
import UserDict as _UserDict

class IdDict(_UserDict.IterableUserDict):
    def __missing__(self,key):
        raise KeyError("Apparently more than one item were requested.")

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
        self._ids = IdDict()
    
    def add(self,item,tags):
        '''  Add an item with a list of tags
        if tags is empty, the item will not be added to
        the TagDict
        
        '''
        if type(tags) is str: tags = [tags,]
        tags = set(tags)
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
        if type(tags) is str: tags = [tags,]
        collected_ids = [ self.data[tag] for tag in tags ]
        unique_ids = list(set.intersection(*collected_ids))
        if len(unique_ids) == 1:
            return self._ids[unique_ids[0]][0]
        else:
            return tuple([ self._ids[itemid][0] for itemid in unique_ids ])
    
    def __repr__(self):
        return "{"+', '.join(
            ['\''+tag +"\' : "+str(len(self.data[tag]))+" items" 
             for tag in self.data.keys()])+"}"
    
    def remove(self,item):
        ''' Remove an item from the TagDict.
        Any tag that points to no object will be removed too.
        '''
        self.replace_tags(item,[])
    
    def add_tag(self,item,tag):
        ''' Add a tag to an item in the TagDict 
        '''
        self._ids[id(item)][1].add(tag)
        self.data[tag].add(id(item))
    
    def remove_tag(self,item,tag):
        ''' Remove a tag from an item in the TagDict
        '''
        self._ids[id(item)][1].remove(tag)
        self.data[tag].remove(id(item))
        if len(self.data[tag]) == 0:
            del self.data[tag]
    
    def replace_tags(self,item,newtags):
        ''' Replace the tags of an item.
        Any tag that points to no object will be removed too.
        '''
        if type(newtags) is not set: newtags = set(newtags)
        oldtags = self._ids[id(item)][1]
        tags2rm = oldtags - newtags
        tags2add = newtags - oldtags
        for tag in tags2rm:
            self.remove_tag(item,tag)
        for tag in tags2add:
            self.add_tag(item,tag)
        if len(newtags) == 0:
            del self._ids[id(item)]
        

if __name__ == '__main__':
    data = TagDict()
    # 4 unhashable items
    data.add({'Name':'Ben'},tags=['Male','Student'])
    data.add({'Name':'Tom','Age':40},tags=['Male','Teacher'])
    data.add({'Name':'Tina','Age':30},tags=['Female','Teacher'])
    data.add({'Name':'Ann'},tags=['Female','Student'])
    print data["*"]                     # --> All the items
    print data['Teacher','Female']      # --> {'Age': 30, 'Name': 'Tina'}
    print data['Student']               # --> ({'Name': 'Ben'}, {'Name': 'Ann'})
    # Add one more tag for one of the items
    data.add_tag(data['Teacher','Female'],'Mother')
    print data['Mother']                # --> {'Age': 30, 'Name': 'Tina'}
    # Remove a tag for one of the items
    data.remove_tag(data['Male','Student'],'Student')
    print data['Student']               # --> {'Name': 'Ann'}
    # Replace all the tags of one of the items
    data.replace_tags(data['Female','Mother','Teacher'],['Human',])
    print data['Mother']                # --> ()
    print data['Human']                 # --> {'Age': 30, 'Name': 'Tina'}
    # Change the content of one of the items
    data['Human']['Age']=31
    print data['Human']                 # --> {'Age': 31, 'Name': 'Tina'}
    # Remove an item
    data.remove(data['Student'])
    print data['Student']               # ()
    print data['*']                     # Only 3 items now
    # Updating a list of items will fail
    try:
        data.add_tag(data['Male'],'Martian')
    except KeyError:
        print "More than one item were requested."
        for man in data['Male']:
            data.add_tag(man,'Martian')
    print data['Martian']              # --> ({'Name': 'Ben'}, {'Age': 40, 'Name': 'Tom'})
