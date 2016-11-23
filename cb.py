from functools import wraps
from datetime import datetime, timedelta
import time

class CircuitBreaker(object):
    def __init__(self, name=None, expected_exception=Exception, max_failure_to_open=3, reset_timeout=10):
        self._name = name
        self._failure_count = 0
        # Set the initial state
        self.close()
 
    def close(self):
        self._is_closed = True
        self._failure_count = 0
        
    def open(self):
        self._is_closed = False
        #self._opened_since = datetime.utcnow()
        
    def cbTrip(self):
      print "Server is tripping need to take some action"
      if (not self._is_closed):
        return True
      self._failure_count +=1
      if (self._failure_count >= 2):
        self.open()
      return False;

