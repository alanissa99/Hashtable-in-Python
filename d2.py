class HashNode:
    def __init__(self,key,data):        #Class that creates node containing both key and data
        self.key=key
        self.data=data

class HashTable:
    def __init__(self):
        self.size=2000003        #remember it should be a prime number (and that it should have about double the size of amount of songs (which is 1000))
        self.slots=[None]*self.size
    
    
    def hashfunction(self,nyckel):             # Gives an index for a given key (got it from lectur notes, however i use 2 instead of 32)
        result = 0            # s[0]*2^[n-1] + s[1]*2^[n-2] + ... + s[n-1]
        i=1
        for letter in nyckel:                    
            result = result + ord(letter)*2**(len(nyckel)-i) 
            i+=1
        return result%self.size    
    
    
    def rehash(self,hashvalue,i):                   #Quadratic probing!
        return (hashvalue+i**2)%self.size

    
    def store(self,key,data):
        node=HashNode(key,data)     #Call the HashNode class and enter the key and data
        hashvalue=self.hashfunction(key)    #Find the index of a given key

        if self.slots[hashvalue]==None:     #If the position in the hashtable is empy then i enter the node
            self.slots[hashvalue]=node
        
        else:                               #Two cases here: First is that i have updated my key with new data, or that the position is simply taken by a different key
            if self.slots[hashvalue].key==key:   #This is the first case, we replace the data
                self.slots[hashvalue].data=data

            else:
                newhashvalue=hashvalue  #Not really the same hash value, it will just be used in the rehash function
                stop=False
                i=1                   #The i is used in quadratic probing 
                while stop==False:    #A while loop to keep probing until i am back to my original index
                    newhashvalue=self.rehash(hashvalue,i)

                    if self.slots[newhashvalue]==None:      #same as before, if the spot is empty, enter the node
                        self.slots[newhashvalue]=node
                        stop=True

                    elif self.slots[newhashvalue].key==key:     #same as before, if the spot has the same key, update the data
                        self.slots[newhashvalue].data=data
                        stop=True
                    
                    elif newhashvalue==hashvalue:               #once you are back at originial index (This shouldnt happen)
                        print('no empty spaces left')
                        stop=True
                    
                    i=i+1
    
    
    def search(self,key):               #Function to retrieve dataa
        hashvalue=self.hashfunction(key)    #Calculate index

        if self.slots[hashvalue]==None:
            raise KeyError('Key doesnt exist')

        elif self.slots[hashvalue].key==key:      #if at given index you get your key, then simply return data
            return self.slots[hashvalue].data

        else:                               #This means if its not at its intended slot
            found=False
            i=1
            newhashvalue=self.rehash(hashvalue,i)
            while found!=True:              #While loop that keeps rehashing until i either find the key or return to original place

                if newhashvalue==hashvalue:    #If returned at original place then i put up the key error
                    raise KeyError('Key doesnt exist')

                elif self.slots[newhashvalue].key==key: #If i find the key then i simply give it
                    found=True                      #Technically this line isnt needed, since i have return under it which will cancel the loop
                    return self.slots[newhashvalue].data
                    
            
                else:                               #Keep rehashing!
                    i=i+1
                    newhashvalue=self.rehash(hashvalue,i)
    

    def __getitem__(self,key):
        return self.search(key)



############################# Testing with the file given
####Entering all the artists and songs
testing=HashTable()
file=open("unique_tracks.txt",'r')  #Enter any file you like, unable to upload this tsxt file on gitbub
content=file.readlines()              #read each line in the file and place it as an element in the vector
vector=[]                             #Just a random vector i will use in the loop
for line in content:
    vector=line.strip().split('<SEP>')          #For every line, a vector is created with 4 elements (splitting at <sep>)
    testing.store(vector[2],vector[3])  #The last two elements in the vector is the artist (our key) and song name (our data)


####Checking i get the right song
print(testing['Texta'])
print(testing['Elude'])
print(testing['Gabriel Le Mar'])
print(testing['Kuldeep Manak'])
print(testing['Kiko Navarro'])
print(testing['Killer Mike feat. Gangsta Pill and Nario of Grind Time Rap Gang'])
print(testing['Loose Shus'])
print(testing['JC'])
print(testing['Faster Pussy cat'])
print(testing['A song that isnt in the list should give me key error'])


