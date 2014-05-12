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
<pre>
<code class="python">
data = TagDict()
data.add({'Name':'Ann'},tags=['Female','Student'])
data.add({'Name':'Ben'},tags=['Male','Student'])
data.add({'Name':'Tina'},tags=['Female','Volunteer'])
data.add({'Name':'Mark'},tags=['Male','Volunteer','Student'])
data['Student'] # --> ({'Name':'Ann'},{'Name':'Ben'},{'Name':'Mark'})
data['Female','Volunteer'] # --> {'Name':'Tina'}
data['Volunteer','Male'] # --> {'Name':'Mark'}
</code>
</pre>
