class HashTable:

    # HashTable code cited from WGU C950 - Webinar-1 - Let’s Go Hashing, https://srm--c.vf.force.com/apex/coursearticle?Id=kA03x000000e1fpCAA 

    # Constructor with a defualt size of 10 but can be set manually during creation
    def __init__(self, init_size = 10):
        self.table = []

        # Create the number of cells matching the desired size
        for i in range(init_size):
            self.table.append([])
    
    # Creates the hash to determine the bucket
    # Get hash function cited from Python: Creating a HASHMAP using Lists, https://www.youtube.com/watch?v=9HFbhPscPU0&list=LL&index=4 
    def _get_hash(self, key):
        hash_num = hash(key) % len(self.table)
        return hash_num

    # Adds a key-value pair to the hash map
    def add(self, key, value):
        # Uses the get hash function to find the bucket
        hash_num = self._get_hash(key)
        key_value = [key, value]

        # If bucket is empty add key-value pair
        if self.table[hash_num] is None:
            self.table[hash_num] = list(key_value)
            return True
        else: # Bucket not empty
            # iterate over every key-value pair in the bucket
            for pair in self.table[hash_num]:
                # If the key already exists in the bucket then its value is updated
                if pair[0] == key:
                    pair[1] = value
                    return True

            # Appends the key-value pair to the bucket list
            self.table[hash_num].append(key_value)
            return True
        
    # Searches the hash table using a key and returns the associated value
    def find(self, key):
        hash_num = self._get_hash(key)
        bucket_list = self.table[hash_num]

        # If bucket is not empty iterate through bucket list
        if bucket_list is not None:
            for pair in bucket_list:
                if pair[0] == key:
                    # return value
                    return pair[1]
        return None
    
    def remove(self, key):
        hash_num = self._get_hash(key)
        bucket_list = self.table[hash_num]

        # If bucket is not empty iterate through bucket list
        if bucket_list is not None:
            for pair in bucket_list:
                if pair[0] == key:
                    # Remove the key-value pair list in the bucket
                    self.table[hash_num].remove([pair[0], pair[1]])

# Test
hashBoy = HashTable()
hashBoy.add(125245, "Boy")
hashBoy.add(5134, "Girl")
print(hashBoy.table)

print(hashBoy.find(5134))

hashBoy.remove(5134)

print(hashBoy.table)