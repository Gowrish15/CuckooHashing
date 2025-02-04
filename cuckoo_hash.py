# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		print("Table is ",self.tables)
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		cycle = 0
		while self.tables[cycle%2][self.hash_func(key,cycle%2)] is not None and cycle <= self.CYCLE_THRESHOLD:
			temp = self.tables[cycle%2][self.hash_func(key,cycle%2)]
			self.tables[cycle%2][self.hash_func(key,cycle%2)] = key
			key = temp
			cycle = cycle+1
		if cycle >= 10: 
			return False
		self.tables[cycle%2][self.hash_func(key,cycle%2)] = key
		return True
		

	def lookup(self, key: int) -> bool:
		# TODO
		return any(self.tables[table_id][self.hash_func(key, table_id)] == key for table_id in range(2))
		

	def delete(self, key: int) -> None:
		# TODO
		for i in range(2):
			pos = self.hash_func(key, i)
			if self.tables[i][pos] == key:
				self.tables[i][pos] = None
				return

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO
		old_elements = []
		for table in self.tables:
			for key in table:
				if key is not None:
					old_elements.append(key)
		
		self.tables = [[None]* new_table_size for _ in range(2)]
  	
		for key in old_elements:
			self.insert(key)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


