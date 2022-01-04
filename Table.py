import time
from Magnet import Magnet

plus = '+'
minus = '-'
empty = '0'


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
            self.table.append(empty * len(self.columns_negative))

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
                     == self.table[i][j + 1])) and (self.table[i][j] != empty):
                    return False
        return True

    def is_complete(self):
        for i in range(len(self.rows_positive)):
            if self.rows_positive[i]:
                return False
        return True

    def add_to_table(self, magnet):
        positive_row = self.table[magnet.positive_pos['x']]
        positive_row = positive_row[:magnet.
                                    positive_pos['y']] + plus + positive_row[
                                        magnet.positive_pos['y'] + 1:]
        self.table[magnet.positive_pos['x']] = positive_row
        negative_row = self.table[magnet.negative_pos['x']]
        negative_row = negative_row[:magnet.
                                    negative_pos['y']] + minus + negative_row[
                                        magnet.negative_pos['y'] + 1:]
        self.table[magnet.negative_pos['x']] = negative_row

    def remove_from_table(self, magnet):
        positive_row = self.table[magnet.positive_pos['x']]
        positive_row = positive_row[:magnet.
                                    positive_pos['y']] + empty + positive_row[
                                        magnet.positive_pos['y'] + 1:]
        self.table[magnet.positive_pos['x']] = positive_row
        negative_row = self.table[magnet.negative_pos['x']]
        negative_row = negative_row[:magnet.
                                    negative_pos['y']] + empty + negative_row[
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
                if self.is_empty_pair((pair[0], i), (pair[1], i)):
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
                cell2[1]] != empty:
            return False
        return True

    def get_actions_sorted(self, possible_magnets):
        if (len(possible_magnets) > 1):
            MRV_list = sorted(
                possible_magnets,
                key=lambda x: self.rows_positive[x.positive_pos[
                    'x']] + self.columns_positive[x.positive_pos[
                        'y']] + self.rows_negative[x.negative_pos[
                            'x']] + self.columns_negative[x.negative_pos['y']])
            last_magnet = MRV_list[-1]
            LCV = []
            for i in range(
                    4, self.rows_positive[last_magnet.positive_pos['x']] +
                    self.columns_positive[last_magnet.positive_pos['y']] +
                    self.rows_negative[last_magnet.negative_pos['x']] +
                    self.columns_negative[last_magnet.negative_pos['y']] + 1):
                l = list(
                    filter(
                        lambda x: self.rows_positive[x.positive_pos[
                            'x']] + self.columns_positive[x.positive_pos['y']]
                        + self.rows_negative[x.negative_pos['x']] + self.
                        columns_negative[x.negative_pos['y']] == i, MRV_list))
                l.sort(key=self.get_cv, reverse=True)
                LCV += l
            return LCV
        else:
            return possible_magnets

    def get_cv(self, magnet):
        self.add_magnet(magnet)
        possibles = len(self.get_possible_magnets())
        self.remove_magnet(magnet)
        return possibles

    def forward_checking(self, possible_magnets):
        possible_positives_in_row = [0] * len(self.rows_positive)
        possible_negatives_in_row = [0] * len(self.rows_negative)
        possible_positives_in_column = [0] * len(self.columns_positive)
        possible_negatives_in_column = [0] * len(self.columns_negative)
        for magnet in possible_magnets:
            possible_positives_in_row[magnet.positive_pos['x']] += 1
            possible_negatives_in_row[magnet.negative_pos['x']] += 1
            possible_positives_in_column[magnet.positive_pos['y']] += 1
            possible_negatives_in_column[magnet.negative_pos['y']] += 1
        for i in range(len(self.rows_negative)):
            if self.rows_negative[i] > possible_negatives_in_row[
                    i] or self.rows_positive[i] > possible_positives_in_row[i]:
                return False
        for j in range(len(self.columns_negative)):
            if self.columns_negative[j] > possible_negatives_in_column[
                    j] or self.columns_positive[
                        j] > possible_positives_in_column[j]:
                return False
        return True

    def solve(self, depth):
        if self.is_complete() and self.is_consistent():
            return True
        possible_magnets = self.get_possible_magnets()
        if depth % 3 == 1:
            if not self.forward_checking(possible_magnets):
                return False
        MRV_Asc = self.get_actions_sorted(possible_magnets)
        for magnet in MRV_Asc:
            self.add_magnet(magnet)
            solved = self.solve(depth + 1)
            if not solved:
                self.remove_magnet(magnet)
            else:
                return True
        return False

    def print_table(self):
        for row in self.table:
            print(f"{row}")
