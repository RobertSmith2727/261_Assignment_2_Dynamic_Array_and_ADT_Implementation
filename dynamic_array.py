# Name: Robert Smith
# OSU Email: Smithro8@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment: 2
# Due Date: 02/06/2023
# Description: A dynamic array data structure that has a lot of methods to act similar to
#              python list and features associated with python lists.

from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.data = None
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)
        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration
        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Changes the capacity of the dynamic array
        It doesn't change value or order of objects
        It only accepts positive numbers bigger than the size of array
        """

        if new_capacity <= 0 or new_capacity < self.length():
            return
        else:
            # sets capacity and keeps old list
            self._capacity = new_capacity
            temp_arr = self._data
            self._data = StaticArray(self._capacity)
            for item in range(self.length()):
                self._data[item] = temp_arr.get(item)

    def append(self, value: object) -> None:
        """
        Adds value to the end of the array
        Doubles capacity when full
        """
        # if there is no room in da
        if self._data.get(self._data.length() - 1) is not None:
            new_capacity = self._capacity * 2
            self.resize(new_capacity)

        # if there is room in da
        if self._data.get(self._data.length() - 1) is None:
            self._data[self._size] = value
            self._size = self._size + 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Adds new value at specific index
        Doubles capacity when full
        TODO test if it will insert at index 3 if index 2 and 3 are none
        """

        if index < 0 or index > self.length():
            raise DynamicArrayException
        if self._data[0] is None:
            self.append(value)
            return

        # appends val then shifts to index
        self.append(value)
        da_index = self._data.length() - 1
        while da_index != index:
            if self._data[da_index] is not None:
                self._data[da_index], self._data[da_index - 1] = self._data[da_index - 1], self._data[da_index]
                da_index -= 1
            if self._data[da_index] is None:
                da_index -= 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes value at specific index
        Reduces capacity if less than 1/4 space being used
        Will not reduce below 10
        """
        # invalid index
        if index < 0 or index > self.length():
            raise DynamicArrayException

        # empty array
        if self._size == 0:
            raise DynamicArrayException

        # resize to 10
        if self.length() * 2 < 10 and self.get_capacity() > 10:
            if self.length() / self.get_capacity() < 0.25:
                self.resize(10)

        # resize to twice the size of length
        if self.length() * 2 > 10:
            if self.length() / self.get_capacity() < 0.25:
                new_capacity = self.length() * 2
                self.resize(new_capacity)

        da_index = index
        # if last index
        if self._size - 1 == index:
            self._size -= 1
            return

        # shifts vals to the right takes off end
        while da_index != self._size - 1:
            self.set_at_index(da_index, self.get_at_index(da_index + 1))
            da_index += 1
            if da_index == self._data.length() - 1:
                self.set_at_index(da_index, None)
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a new array that contains a 'slice' of the original array
        """

        new_arr = DynamicArray()
        # invalid index
        if start_index < 0 or start_index >= self.length():
            raise DynamicArrayException

        # negative size
        if size < 0:
            raise DynamicArrayException

        # not enough indices
        if start_index + size > self.length():
            raise DynamicArrayException

        if size == 0:
            return new_arr

        index = start_index
        stop_index = start_index + size
        # appends values to new arr
        while index != stop_index:
            value = self.get_at_index(index)
            new_arr.append(value)
            index += 1
        return new_arr

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Merges two arrays into one array
        """

        index = 0
        while index != second_da.length():
            self.append(second_da.get_at_index(index))
            index += 1

    def map(self, map_func) -> "DynamicArray":
        """
        Returns new array with values of the function passed
        """
        new_arr = DynamicArray()
        index = 0
        # gets val, applies func, appends
        while index != self.length():
            value = self.get_at_index(index)
            mapped_val = map_func(value)
            new_arr.append(mapped_val)
            index += 1
        return new_arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        Returns a filtered new array
        Values are filtered by a passed function
        """

        new_arr = DynamicArray()
        index = 0
        # gets value, changes val to T or F, appends if true
        while index != self.length():
            value = self.get_at_index(index)
            filtered_val = filter_func(value)
            if filtered_val is True:
                new_arr.append(self.get_at_index(index))
            index += 1
        return new_arr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Returns a reduced object
        The object value is derived from a passed function
        """
        # if no items
        if self.length() == 0:
            return initializer

        # sets initializer if not passed
        if initializer is None:
            initializer = self.get_at_index(0)
            index = 1
        else:
            index = 0

        # gets value, reduces and adjusts initializer
        while index != self.length():
            value = self.get_at_index(index)
            reduced_val = reduce_func(initializer, value)
            initializer = reduced_val
            index += 1
        return initializer


def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Returns a new array with the most occurring objects
    Also returns frequency of objects
    Array must be ordered
    """

    new_arr = DynamicArray()
    # if arr is one item
    if arr.length() == 1:
        new_arr.append(arr[0])
        return new_arr, 1

    # loop counts the highest frequency
    max_index = arr.length() - 1
    index = 0
    counter = 1
    frequency = 0
    while index != max_index:
        if arr[index] == arr[index + 1]:
            counter += 1
        # if occurrence ends, reset counter
        if arr[index] != arr[index + 1]:
            counter = 1
        # sets the highest frequency
        if counter >= frequency:
            frequency = counter
        index += 1

    # if one occurence of items
    if frequency == 1:
        for item in arr:
            new_arr.append(item)
        return new_arr, frequency

    # loop appends highest frequency numbers
    counter = 1
    max_index = arr.length() - 1
    index = 0
    while index != max_index:
        if arr[index] == arr[index + 1]:
            counter += 1
        # if occurrence end reset values
        if arr[index] != arr[index + 1]:
            counter = 1
        if counter == frequency:
            new_arr.append(arr[index])
        index += 1
    return new_arr, frequency

# ------------------- BASIC TESTING -----------------------------------------
if __name__ == "__main__":
    print("\n# resize - example 1")
    da = DynamicArray()
    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()
    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)
    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)
    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)
    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())
    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)
    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)
    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)
    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)
    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())
    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())
    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)
    # print("\n# slice example 1")
    # da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    # da_slice = da.slice(1, 3)
    # print(da, da_slice, sep="\n")
    # da_slice.remove_at_index(0)
    # print(da, da_slice, sep="\n")
    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")
    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)
    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)
    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))
    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))
    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))
    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))
    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))
    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )
    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")
    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
