import random as rand
from typing import List, Optional

class CuckooHash:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.tables = [[None] * init_size for _ in range(2)]

    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return rand.randint(0, self.table_size - 1)

    def get_table_contents(self) -> List[List[Optional[int]]]:
        return self.tables

    def insert(self, key: int) -> bool:
        position, table_id = key, 0
        for _ in range(self.CYCLE_THRESHOLD):
            pos = self.hash_func(position, table_id)
            position, self.tables[table_id][pos] = self.tables[table_id][pos], position
            if position is None:
                return True
            table_id = 1 - table_id
        return False

    def lookup(self, key: int) -> bool:
        return any(self.tables[i][self.hash_func(key, i)] == key for i in range(2))

    def delete(self, key: int) -> None:
        for i in range(2):
            pos = self.hash_func(key, i)
            if self.tables[i][pos] == key:
                self.tables[i][pos] = None
                return

    def rehash(self, new_table_size: int) -> None:
        self.__num_rehashes += 1
        self.table_size = new_table_size
        old_elements = [key for table in self.tables for key in table if key is not None]
        self.tables = [[None] * new_table_size for _ in range(2)]
        for key in old_elements:
            self.insert(key)
