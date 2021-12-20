import time
from Magnet import Magnet


class Table:
    def __init__(self, rows_negative, columns_negative, rows_positive,
                 columns_positive, table):
        self.rows_negative = rows_negative
        self.columns_negative = columns_negative
        self.rows_positive = rows_positive
        self.columns_positive = columns_positive
        self.row_pairs = []
        for i in table:
            self.row_pairs.append([])
        self.column_pairs = []
        for j in table[0]:
            self.column_pairs.append([])
        for i in range(len(table)):
            for j in range(len(table[i])):
                if table[i][j] != 0:
                    if j < len(table[0]) - 1 and table[i][j] == table[i][j +
                                                                         1]:
                        self.row_pairs[i].append((j, j + 1))
                        table[i][j], table[i][j + 1] = 0, 0
                    elif i < len(table) - 1 and table[i][j] == table[i + 1][j]:
                        self.column_pairs[j].append((i, i + 1))
                        table[i][j], table[i + 1][j] = 0, 0
        self.magnets = []
        self.table = []
        for i in range(len(self.rows_negative)):
            self.table.append('0' * len(self.columns_negative))

    def add_magnet(self, magnet):
        p_x, p_y = magnet.positive_pos['x'], magnet.positive_pos['y']
        n_x, n_y = magnet.negative_pos['x'], magnet.negative_pos['y']
        self.magnets.append(magnet)
        self.add_to_table(magnet)
        self.rows_negative[n_x] -= 1
        self.columns_negative[n_y] -= 1
        self.rows_positive[p_x] -= 1
        self.columns_positive[p_y] -= 1

    def remove_magnet(self, magnet):
        p_x, p_y = magnet.positive_pos['x'], magnet.positive_pos['y']
        n_x, n_y = magnet.negative_pos['x'], magnet.negative_pos['y']
        self.magnets.remove(magnet)
        self.remove_from_table(magnet)
        self.rows_negative[n_x] += 1
        self.columns_negative[n_y] += 1
        self.rows_positive[p_x] += 1
        self.columns_positive[p_y] += 1

    def is_consistent(self):
        for i in range(len(self.rows_negative)):
            if self.rows_negative[i] < 0 or self.rows_positive[i] < 0:
                return False
        for i in range(len(self.columns_negative)):
            if self.columns_negative[i] < 0 or self.columns_positive[i] < 0:
                return False
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if ((i > 0 and self.table[i][j] == self.table[i - 1][j]) or
                    (i < len(self.table) - 1
                     and self.table[i][j] == self.table[i + 1][j]) or
                    (j > 0 and self.table[i][j] == self.table[i][j - 1]) or
                    (j < len(self.table[i]) - 1 and self.table[i][j]
                     == self.table[i][j + 1])) and (self.table[i][j] != '0'):
                    return False
        return True

    def is_complete(self):
        for i in range(len(self.rows_positive)):
            if self.rows_positive[i] or self.rows_negative[i]:
                return False
        for i in range(len(self.rows_positive)):
            if self.columns_positive[i] or self.columns_negative[i]:
                return False
        return True

    def add_to_table(self, magnet):
        positive_row = self.table[magnet.positive_pos['x']]
        positive_row = positive_row[:magnet.
                                    positive_pos['y']] + '+' + positive_row[
                                        magnet.positive_pos['y'] + 1:]
        self.table[magnet.positive_pos['x']] = positive_row
        negative_row = self.table[magnet.negative_pos['x']]
        negative_row = negative_row[:magnet.
                                    negative_pos['y']] + '-' + negative_row[
                                        magnet.negative_pos['y'] + 1:]
        self.table[magnet.negative_pos['x']] = negative_row

    def remove_from_table(self, magnet):
        positive_row = self.table[magnet.positive_pos['x']]
        positive_row = positive_row[:magnet.
                                    positive_pos['y']] + '0' + positive_row[
                                        magnet.positive_pos['y'] + 1:]
        self.table[magnet.positive_pos['x']] = positive_row
        negative_row = self.table[magnet.negative_pos['x']]
        negative_row = negative_row[:magnet.
                                    negative_pos['y']] + '0' + negative_row[
                                        magnet.negative_pos['y'] + 1:]
        self.table[magnet.negative_pos['x']] = negative_row

    def get_possible_magnets(self):
        possible_magnets = []
        for i in range(len(self.row_pairs)):
            for pair in self.row_pairs[i]:
                if self.is_empty_pair((i, pair[0]), (i, pair[1])):
                    magnet = Magnet(i, pair[0], i, pair[1])
                    self.add_magnet(magnet)
                    if self.is_consistent():
                        possible_magnets.append(self.magnets[-1])
                    self.remove_magnet(magnet)
                    magnet = Magnet(i, pair[1], i, pair[0])
                    self.add_magnet(magnet)
                    if self.is_consistent():
                        possible_magnets.append(self.magnets[-1])
                    self.remove_magnet(magnet)

        for i in range(len(self.column_pairs)):
            for pair in self.column_pairs[i]:
                if self.is_empty_pair((pair[0],i), (pair[1],i)):
                    magnet = Magnet(pair[0], i, pair[1], i)
                    self.add_magnet(magnet)
                    if self.is_consistent():
                        possible_magnets.append(self.magnets[-1])
                    self.remove_magnet(magnet)

                    magnet = Magnet(pair[1], i, pair[0], i)
                    self.add_magnet(magnet)
                    if self.is_consistent():
                        possible_magnets.append(self.magnets[-1])
                    self.remove_magnet(magnet)
        return possible_magnets

    def is_empty_pair(self, cell1, cell2):
        if self.table[cell1[0]][cell1[1]] != '0' and self.table[cell2[0]][
                cell2[1]] != '0':
            return False
        return True

    def print_table(self):
        for row in self.table:
            print(f"{row}")

    def solve(self, step):
        if self.is_complete() and self.is_consistent():
            return True
        possible_magnets = self.get_possible_magnets()
        for magnet in possible_magnets:
            self.add_magnet(magnet)
            solved = self.solve(step + 1)
            if not solved:
                self.remove_magnet(magnet)
            else:
                return True
        return False
