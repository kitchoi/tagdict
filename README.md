tagdict
=======
This module contains a class TagDict that is similar to the Python 
dictionary container but instead of mapping an object to a user-defined 
key, it uses the id of the object as the key for tracking and manages 
a set of attributes or tags of the object.

The goal is to be able to find a list of objects that share the same 
list of tags given by the user.

Example
-------

**Initialise a dataset**

<pre>
<code class="python">
data = TagDict()
# 4 unhashable items
data.add({'Name':'Ben'},tags=['Male','Student'])
data.add({'Name':'Tom','Age':40},tags=['Male','Teacher'])
data.add({'Name':'Tina','Age':30},tags=['Female','Teacher'])
data.add({'Name':'Ann'},tags=['Female','Student'])
</code>
</pre>

**Retrieve content using tag**

<pre>
<code class="python">
print data["*"]                     # --> All the items
print data['Teacher','Female']      # --> {'Age': 30, 'Name': 'Tina'}
print data['Student']               # --> ({'Name': 'Ben'}, {'Name': 'Ann'})
</code>
</pre>

**Add a tag to an item**

<pre>
<code class="python">
data.add_tag(data['Teacher','Female'],'Mother')
print data['Mother']                # --> {'Age': 30, 'Name': 'Tina'}
</code>
</pre>

**Remove a tag from an item**

<pre>
<code class="python">
data.remove_tag(data['Male','Student'],'Student')
print data['Student']               # --> {'Name': 'Ann'}
</code>
</pre>

**Replace all the tags of an item**

<pre>
<code class="python">
data.replace_tags(data['Female','Mother','Teacher'],['Human',])
print data['Mother']                # --> ()
print data['Human']                 # --> {'Age': 30, 'Name': 'Tina'}
</code>
</pre>

**Change the content of an item**

<pre>
<code class="python">
data['Human']['Age']=31
print data['Human']                 # --> {'Age': 31, 'Name': 'Tina'}
</code>
</pre>


**Remove an item**

<pre>
<code class="python">
data.remove(data['Student'])
print data['Student']               # ()
print data['*']                     # Only 3 items now
</code>
</pre>

**View all items**

<pre>
<code class="python">
print data.view_all()  # --> (({'Name': 'Ben'}, set(['Male', 'Martian'])), ({'Age': 40, 'Name': 'Tom'}, set(['Male', 'Martian', 'Teacher'])), ({'Age': 31, 'Name': 'Tina'}, set(['Human'])))
</code>
</pre>

