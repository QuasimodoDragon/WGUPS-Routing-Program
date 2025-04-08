class HashMap:
    def __init__(self):
        self.size = 6 # TODO update size
        self.map = [None] * self.size

    # TODO update hashing
    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size
    
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        # if no key-value is in cell then add to 
        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                # if key already exists in cell then iterate and update associated value
                if pair[0] == key:
                    pair[1] = value
                    return True
            # appends key-value to cell list chain
            self.map[key_hash].append(key_value)
            return True

    def get(self, key):
        return
    
    def delete(self, key):
        return

    def print(self):
        return