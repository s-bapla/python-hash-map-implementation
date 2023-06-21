# Name: Simran Bapla
# OSU Email: baplas@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: Dec 2, 2022
# Description: Hash map using separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

        # resize table if load factor greater or equal to 1.0
        if self._size / self._capacity >= 1.0:
            self.resize_table(2 * self._capacity)
        # get initial index
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity

        # find the node at that matches the key
        linked_list = self._buckets.get_at_index(index)
        node_if_contains_key = linked_list.contains(key)
        # if node matches key replace that nodes value with new value, otherwise
        # add node to linked list
        if node_if_contains_key is not None:
            node_if_contains_key.value = value
        else:
            linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.

        :params:

        return: number of empty buckets
        """
        count = 0
        # determine count of buckets that are empty
        for index in range(self._buckets.length()):
            if self._buckets.get_at_index(index).length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.

        :params:

        :return: the current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity

        :params:

        :returns:
        """
        # replace every linked list in buckets with an empty linked list
        for index in range(self._buckets.length()):
            self._buckets.set_at_index(index, LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table.

        :params: new_capacity: the new capacity of the hash table

        :returns: None
        """
        # create a copy of the buckets
        arr = DynamicArray()
        for index in range(self._buckets.length()):
            arr.append(self._buckets.get_at_index(index))

        if new_capacity < 1:
            return
        # determine next prime capacity and replace the capacity with it
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        # empty all buckets and resize capacity
        self._size = 0
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # copy all values from the old capacity bucket to the new capacity bucket
        for index in range(arr.length()):
            linked_list = arr.get_at_index(index)
            for node in linked_list:
                self.put(node.key, node.value)

    def get(self, key: str):
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.

        :params: key: the key we are looking for

        :returns: the value associated with the given key. If the key is not in the hash
                  map, the method returns None.
        """
        # determine index which contains the linked list with the key
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity

        # find the node with the key
        linked_list = self._buckets.get_at_index(index)
        node = linked_list.contains(key)

        # return None if it does not exist or the value of the node
        if node is None:
            return node
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.

        :params: key: the key we are looking for

        :returns: True if the given key is in the hash map, otherwise it returns False
        """
        if self._size == 0:
            return False

        # determine index which contains the linked list with the key
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        # if index is outside the range of valid index return False
        if index < 0 or index >= self._capacity:
            return False
        # get linked list at the index which contains the key
        linked_list = self._buckets.get_at_index(index)

        # if linked list has key return True otherwise return false
        if linked_list.contains(key) is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.

        :params: key: the key we are looking for

        :returns: None
        """
        # determine index which contains the linked list with the key
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        # if index is outside the range of valid index return
        if index < 0 or index >= self._capacity:
            return
        # get linked list at the index which contains the key
        linked_list = self._buckets.get_at_index(index)
        # remove the node which contains key
        removed = linked_list.remove(key)
        if removed is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.

        :params:

        :return: a dynamic array where each index contains a tuple of key/value pairs

        """
        # create result array
        arr = DynamicArray()
        # store key value pair tuples of all nodes in the mape in the result array
        for index in range(self._capacity):
            linked_list = self._buckets.get_at_index(index)
            for node in linked_list:
                arr.append((node.key, node.value))

        return arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    receives a dynamic array (that is not guaranteed to be sorted). This function will return a tuple containing, in this
    order, a dynamic array comprising the mode (most occurring) value/s of the array, and an
    integer that represents the highest frequency (how many times they appear).

    if there is more than one value with the highest frequency, all values at that frequency
    will be included in the array being returned

    :params: da: a dynamic array

    :returns: a tuple of to a dynamic array with all modes and the frequency
    """
    # create new hash map
    map = HashMap()
    # store all different modes as keys and frequencies as values in map
    for index in range(da.length()):
        freq = map.get(da.get_at_index(index))
        if freq is not None:
            map.put(da.get_at_index(index), freq + 1)
        else:
            map.put(da.get_at_index(index), 1)

    # get an array of all keys and values of the map
    arr_of_keys_and_values = map.get_keys_and_values()
    # create dynamic array to store modes
    modes = DynamicArray()
    freq = 0
    # store all modes and the frequency in modes/freq
    for index in range(arr_of_keys_and_values.length()):
        if arr_of_keys_and_values.get_at_index(index)[1] == freq:
            modes.append(arr_of_keys_and_values.get_at_index(index)[0])
        elif arr_of_keys_and_values.get_at_index(index)[1] > freq:
            freq = arr_of_keys_and_values.get_at_index(index)[1]
            modes = DynamicArray()
            modes.append(arr_of_keys_and_values.get_at_index(index)[0])

    return (modes, freq)




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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
