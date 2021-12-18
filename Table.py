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
        self.colum_pairs = []
        for j in table[0]:
            self.colum_pairs.append([])
        for i in range(len(table)):
            for j in range(len(table[i])):
                if table[i][j] != 0:
                    if j < len(table[0]) - 1 and table[i][j] == table[i][j +
                                                                         1]:
                        self.row_pairs[i].append((j, j + 1))
                        table[i][j], table[i][j + 1] = 0, 0
                    elif i < len(table) - 1 and table[i][j] == table[i + 1][j]:
                        self.colum_pairs[j].append((i, i + 1))
                        table[i][j], table[i + 1][j] = 0, 0
        self.magnets = []

    def add_magnet(self, p_x, p_y, n_x, n_y):
        if self.rows_negative[n_x] > 0 and self.columns_negative[
                n_y] > 0 and self.rows_positive[
                    p_x] > 0 and self.columns_positive[p_y]:
            new_m = Magnet(p_x, p_y, n_x, n_y)
            self.magnets.append(new_m)
            if p_x == n_x:
                self.row_pairs[p_x].remove((p_y, n_y) if p_y < n_y else (n_y,
                                                                         p_y))
            else:
                self.colum_pairs[p_y].remove((p_x,
                                              n_x) if p_x < n_x else (n_x,
                                                                      p_x))
            self.rows_negative[n_x] -= 1
            self.columns_negative[n_y] -= 1
            self.rows_positive[p_x] -= 1
            self.columns_positive[p_y] -= 1
            return 1
        else:
            return 0

    def remove_magnet(self, p_x, p_y, n_x, n_y):
        for magnet in self.magnets:
            if magnet.positive_pos['x'] == p_x and magnet.positive_pos[
                    'y'] == p_y and magnet.negative_pos[
                        'x'] == n_x and magnet.negative_pos['y'] == n_y:
                self.magnets.remove(magnet)
                if p_x == n_x:
                    self.row_pairs[p_x].append((p_y,
                                                n_y) if p_y < n_y else (n_y,
                                                                        p_y))
                else:
                    self.colum_pairs[p_y].append((p_x,
                                                  n_x) if p_x < n_x else (n_x,
                                                                          p_x))
                self.rows_negative[n_x] += 1
                self.columns_negative[n_y] += 1
                self.rows_positive[p_x] += 1
                self.columns_positive[p_y] += 1
                return 1
        return 0
