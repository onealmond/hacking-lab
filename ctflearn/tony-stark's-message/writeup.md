
Key information:

- Lossless compression based on frequency => Huffman Encoding
- Node data is pickled

In ``info.txt`` there is an encoded message and a url to ``node_data.txt``. We need to unpickle node data to rebuild huffman tree, address from the root to decode the data. To unpickle the *Node* object, we need to define a fake *Node* class to bypass the unpickle error *AttributeError: Can't get attribute 'Node' on <module '__main__'...*.


```python
class Node():

    def __init__(self):
        print('fake node to bypass attribute-not-found error in pickle.load')
```

In a *Node* object, *left* and *right* is the left and right child, respectively, *data* field on leaves is the value we need, so decoded as following.


```python
def decode(node, data):
    flag = ''
    cur = node

    for i in range(len(data)):
        if not cur.left and not cur.right:
            flag += cur.data
            cur = node

        if data[i] == '0':
            cur = cur.left
        else:
            cur = cur.right

    if not cur.left and not cur.right:
        flag += cur.data

    return flag
```

The decoded message is *Tony_Stark:_I_Build_Neat_Stuff,_Got_A_Great_Girl,_Occasionally_Save_The_World._So_flag{Why_Can’t_I_Sleep?}*.
