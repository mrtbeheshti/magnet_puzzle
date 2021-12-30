from Table import Table as T
from time import time

src_dir = 'input3_method2.txt'
f = open(src_dir)
x, y = map(int, f.readline().split())
rows_positive = list(map(int, f.readline().split()))
rows_negative = list(map(int, f.readline().split()))
columns_positive = list(map(int, f.readline().split()))
columns_negative = list(map(int, f.readline().split()))
table = []
while (row := f.readline()):
    table.append(list(map(int, row.split())))
f.close()
table = T(rows_negative, columns_negative, rows_positive, columns_positive,
          table)
start_time = time()
table.solve(0)
end_time = time()
table.print_table()
print(f"running time: {end_time-start_time}")