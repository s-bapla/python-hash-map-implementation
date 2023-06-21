# Name: Simran Bapla
# OSU Email: baplas@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: Dec 2, 2022
# Description: Hash map using open addressing with quadratic probing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a new key/value pair is be added.

        :param: key: the key of the entry we are storing
                value: the value of associated

        :return: None
        """
        # resize table if load factor greater than 0.5
        if self._size / self._capacity >= 0.5:
            self.resize_table(2 * self._capacity)

        # determine whether key is already in map
        contains_key = self.contains_key(key)
        # get initial index
        hash_val = self._hash_function(key)
        init_index = hash_val % self._capacity
        index = init_index
        j = 1

        # get val at the current index
        val_at_index = self._buckets.get_at_index(init_index)

        # find index to place entry
        if contains_key is False:
            while val_at_index is not None and val_at_index.key != key:
                index = (init_index + (j * j)) % self._capacity
                j += 1
                val_at_index = self._buckets.get_at_index(index)
        else:
            while val_at_index is not None and val_at_index.is_tombstone is False and val_at_index.key != key:
                index = (init_index + (j * j)) % self._capacity
                j += 1
                val_at_index = self._buckets.get_at_index(index)

        # if key is in map replace the value, otherwise add new value at the index
        if val_at_index is not None and val_at_index.key == key and val_at_index.is_tombstone is False:
            self._buckets.set_at_index(index, HashEntry(key, value))
        else:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.

        :params:

        :return: the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.

        :params:

        :return: the number of empty buckets in the hash table.
        """
        count = 0
        # count how many empty buckets by iterating through map
        for index in range(self._capacity):
            if self._buckets.get_at_index(index) is None or self._buckets.get_at_index(index).is_tombstone is True:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table.

        :params: new_capacity: the new capacity of the hash table

        :returns: None
        """
        if new_capacity < self._size:
            return

        # create copy of all buckets
        arr = DynamicArray()
        for index in range(self._buckets.length()):
            arr.append(self._buckets.get_at_index(index))

        # determine prime capacity
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        # empty all buckets, and resize map to new capacity
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

        # copy old values into new resized map
        for index in range(arr.length()):
            if arr.get_at_index(index) is not None and arr.get_at_index(index).is_tombstone is False:
                self.put(arr.get_at_index(index).key, arr.get_at_index(index).value)

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.

        :params: key: the key we are looking for

        :returns: the value associated with the given key. If the key is not in the hash
                  map, the method returns None.
        """
        # determine initial index
        hash_val = self._hash_function(key)
        init_index = hash_val % self._capacity
        index = init_index

        j = 1
        # get val at initial index
        val_at_index = self._buckets.get_at_index(index)
        # determine which index the key is at
        while val_at_index is not None and val_at_index.key != key:
            index = (init_index + j * j) % self._capacity
            j += 1
            val_at_index = self._buckets.get_at_index(index)
        # return value or None if no key exists
        if val_at_index is not None and val_at_index.key == key and val_at_index.is_tombstone is False:
            return val_at_index.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.

        :params: key: the key we are looking for

        :returns: True if the given key is in the hash map, otherwise it returns False
        """
        if self._size == 0:
            return False
        # determine initial index
        hash_val = self._hash_function(key)
        init_index = hash_val % self._capacity
        index = init_index

        j = 1
        # get entry at initial index
        val_at_index = self._buckets.get_at_index(index)
        # find index where key is
        while val_at_index is not None and val_at_index.key != key:
            index = (init_index + j * j) % self._capacity
            j += 1
            val_at_index = self._buckets.get_at_index(index)

        # return true if key exists, otherwise false
        if val_at_index is not None and val_at_index.key == key and val_at_index.is_tombstone == False:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.

        :params: key: the key we are looking for

        :returns: None
        """
        if self._size == 0:
            return
        # get inital index
        hash_val = self._hash_function(key)
        init_index = hash_val % self._capacity
        index = init_index

        j = 1
        # get val at initial index
        val_at_index = self._buckets.get_at_index(index)

        # determine where the key is at
        while val_at_index is not None and val_at_index.key != key:
            index = (init_index + (j * j)) % self._capacity
            j += 1
            val_at_index = self._buckets.get_at_index(index)

        # if key exists set its tombstone to true and decrement size
        if val_at_index is not None and val_at_index.key == key and val_at_index.is_tombstone == False:
            val_at_index.is_tombstone = True
            self._size = self._size - 1

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity

        :params:

        :returns:
        """
        self._size = 0
        for index in range(self._buckets.length()):
            self._buckets.set_at_index(index, None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.

        :params:

        :return: a dynamic array where each index contains a tuple of key/value pairs
        """
        # initial result array
        result_arr = DynamicArray()
        # insert tuples of all key value pairs in result array
        for index in range(self._buckets.length()):
            val_at_index = self._buckets.get_at_index(index)
            if val_at_index is not None and val_at_index.is_tombstone is False:
                result_arr.append((val_at_index.key, val_at_index.value))

        return result_arr

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself

        :params:

        :return: self
        """
        self._index = 0

        return self

    def __next__(self):
        """
        This method will return the next item in the hash map, based on the current location of the
        iterator

        :param:

        :return: the next item in the hash map
        """
        try:
            # get first value of the map
            value = self._buckets.get_at_index(self._index)
            while value is None or value.is_tombstone is True:
                self._index += 1
                value = self._buckets.get_at_index(self._index)
        except DynamicArrayException:
            raise StopIteration
        # increment index and return that value
        self._index += 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    #
    # m.remove(str(keys[0]))
    # hash_val = hash_function_1("key127")
    # init_index = hash_val % 449
    # index = init_index
    #
    # j = 1
    #
    # while True:
    #     index = (init_index + (j * j)) % 449
    #     j += 1

