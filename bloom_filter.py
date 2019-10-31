import array, sys
import time
import pandas as pd
#from datetime import date 
from datetime import datetime
from math import exp
from hashlib import sha224,sha256,sha1,md5

start_time = time.time()
print(start_time)

"""first bloom filter"""
class BloomFilter(object):
    
    """A simple BloomFilter applicable to a set S of ints"""    
    def __init__(self, Mbits=2200):
        self.Mbits = Mbits
        self.abits = array.array('b', [0]) * self.Mbits
        self.kHash = 4
        self.Nadds = 0
        
    def _element_index(self, element):
        return [self._hTindex(self._hi(i, element)) for i in range(self.kHash)]

    def _hi(self, i, x):
        
        """
        _hi(x) = _h1(x) + i*_h2(x)
        
        """
        return self._sha256(x) + i * self._sha224(x)

    def _sha256(self, x):
        
        """
        Takes any value x as input, applies SHS256 hash function and returns an int.
        
        """
        return int(sha256(str(x).encode()).hexdigest(), 16)

    def _sha224(self, x):
        
        """
        Takes any value x as input, applies SHS256 hash function and returns an int.
        """
        return int(sha224(str(x).encode()).hexdigest(), 16)

    def _hTindex(self, hash):
        
        """
        Maps output of a hash function to a bit array index
        
        """
        return hash % self.Mbits

    def add(self, element):
        for i in self._element_index(element):
            self.abits[i] = 1
        self.Nadds = self.Nadds + 1

    def query(self, element):
        for i in self._element_index(element):
            if self.abits[i] == 0:
                return False
        return True

    def size(self):
        return sys.getsizeof(self.abits)

    def fp_prob(self):
        return (1 - exp(-(self.kHash * self.Nadds) / self.Mbits)) ** self.kHash

"""Second Bloom Filter"""

class BloomFilter2(object):
    """A simple BloomFilter applicable to a set S of ints"""
    def __init__(self, Mbits=2200):
        self.Mbits = Mbits
        self.abits = array.array('b', [0]) * self.Mbits
        self.kHash = 4
        self.Nadds = 0

    def _element_index(self, element):
        return [self._hTindex(self._hi(i, element)) for i in range(self.kHash)]

    def _hi(self, i, x):
        
        """
        _hi(x) = _h1(x) + i*_h2(x)
        
        """
        return self._sha256(x) + i * self._sha224(x)

    def _sha256(self, x):
        
        """
        Takes any value x as input, applies SHS256 hash function and returns an int.
        
        """
        return int(sha256(str(x).encode()).hexdigest(), 16)

    def _sha224(self, x):
        """
        Takes any value x as input, applies SHS256 hash function and returns an int.
        """
        return int(sha224(str(x).encode()).hexdigest(), 16)

    def _hTindex(self, hash):
        """
        Maps output of a hash function to a bit array index
        """
        return hash % self.Mbits

    def add(self, element):
        for i in self._element_index(element):
            self.abits[i] = 1
        self.Nadds = self.Nadds + 1

    def query(self, element):
        for i in self._element_index(element):
            if self.abits[i] == 0:
                return False
        return True

    def size(self):
        return sys.getsizeof(self.abits)

    def fp_prob(self):
        return (1 - exp(-(self.kHash * self.Nadds) / self.Mbits)) ** self.kHash
    
    
    

if __name__ == '__main__':

   
   filter = BloomFilter()
   filternew = BloomFilter2()
   dsA = []
   dsB = []
   dataset1 = pd.read_csv('dataset1.csv')
   x=dataset1.iloc[:,[0,1,2]].values
   y=dataset1.iloc[:,[2]].values
   def calculateAge(s1):
    mm = int(s1[2:4])
    dd = int(s1[5:7])
    yy = int(s1[8:12])
    todaysDate = str(datetime.today())
    tyy = int(todaysDate[0:4])
    tmm = int(todaysDate[5:7])
    tdd = int(todaysDate[8:10])
    age = tyy - yy
    if tmm < mm:
        age -= 1
        
    if tmm == mm:
        if tdd < dd:
            age -= 1
             
    return age

   Age = ""
   for i in y:      
       temp = calculateAge(str(i))
       if temp >= 0 and temp <= 29:
           Age += 'A'
       elif temp >= 30 and temp <= 59:
           Age += 'B'
       else:
           Age += 'C'

   
   k = 0    
   for line in x:
       element = str(line[0]) + '$' + str(line[1]) + '%' +  Age[k] 
       #print(element)
       k +=1
       filter.add(element)
       dsA.append(element)
       
   print("False positive probability : %f" % filter.fp_prob())
#    print("Original size for S in bytes: %d" % sys.getsizeof(S))
   print("Bloom filter's size in bytes: %d" % filter.size())
     
      
   dataset2 = pd.read_csv('dataset2.csv')
   """
   y=dataset2.iloc[:,[0,1,2]].values
   for sline in y:
       element2 = str(sline[0]) + '$' + str(sline[1]) + '%' + str(sline[2])
       filternew.add(element2)
       dsB.append(element)
   """    
   a=dataset2.iloc[:,[0,1,2]].values
   b=dataset2.iloc[:,[2]].values
   def calculateAge(s2):
    mm = int(s2[2:4])
    dd = int(s2[5:7])
    yy = int(s2[8:12])    
    todaysDate = str(datetime.today())    
    tyy = int(todaysDate[0:4])
    tmm = int(todaysDate[5:7])
    tdd = int(todaysDate[8:10])
    age = tyy - yy
    if tmm < mm:
        age -= 1
        
    if tmm == mm:
        if tdd < dd:
            age -= 1
             
    return age

   Age = ""
   for i in b:      
       temp = calculateAge(str(i))
       if temp >= 0 and temp <= 29:
           Age += 'A'
       elif temp >= 30 and temp <= 59:
           Age += 'B'
       else:
           Age += 'C'

   
   z = 0    
   for sline in a:
       element2 = str(sline[0]) + '$' + str(sline[1]) + '%' +  Age[z]
       #print(element2)
       z += 1
       filternew.add(element2)
       dsB.append(element2)
    
   print("False positive probability : %f" % filternew.fp_prob())
#    print("Original size for S in bytes: %d" % sys.getsizeof(S))
   print("Bloom filter's size in bytes: %d" % filternew.size())
   
   cnt = 0
   cnt2= 0
   
   for i in dsA:
       print(i)              
       if filter.query(i) and filternew.query(i):                      
           print("Matched")
           cnt +=1       
       else:           
           print("Not Matched")
           cnt2 +=1
           
   print("Number of matches(may be include false positive) : " +str(cnt))
   print("Number of non-matches : " +str(cnt2))
   
   
   print("False positive probability : %f" % filter.fp_prob())
#    print("Original size for S in bytes: %d" % sys.getsizeof(S))
   print("Bloom filter's size in bytes: %d" % filter.size())
  
   
end_time = time.time()
print(end_time)
print("time need in second: " + str(end_time-start_time))
print("time need in milisecond: " + str((end_time-start_time)*1000))
   


  
