import redis
import threading
import time
from cb import CircuitBreaker

class RedisConnection:
    serverList =[]
    def __init__(self, host, port):
        self.server = redis.StrictRedis(host=host, 
            port=port, db=0)
        
    def getList(self):
        return self.serverList

    def removeAppInstance(self, hostname):
        print "%s is not reachable or has too many errors, removing it from pool" % (hostname)
        self.server.delete(hostname)
        for server in self.serverList:
            if hostname in server:
                self.serverList.remove(server)
                
    def addServerToList(self, host, port):
        print "New App Instance found!!! adding in proxy:@ %s,%d" %(host, port)
        print "Adding circuit breaker object to host"
        cb =  CircuitBreaker();
        self.serverList.append((host, port, cb))

    def keepLookingRedis(self, checkRedisInTime):
        print "Looking for app server in redis"
        while(True):
            app_instance = self.server.keys()
            for host in app_instance:
                port = int(self.server.get(host))
                print "Host: %s running on port: %d" %(host, port)
                serverAbsent = True
                for server in self.serverList:
                  if host in server:
                     serverAbsent = False
                     break;
                if (serverAbsent):
                   self.addServerToList(host, port)
            time.sleep(checkRedisInTime)



    def startThread(self, checkRedisInTime):
        try:
            t = threading.Thread(target=self.keepLookingRedis, args=(checkRedisInTime,))
            t.daemon = True
            t.start()
            
        except:
            print "Error: unable to start thread"



    

