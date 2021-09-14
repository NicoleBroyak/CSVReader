from os import sep
import sys
import csv
import os

csvlist = []
num_changes = len(sys.argv) - 3
index = 0
err = 0
try:
    with open(f"{sys.argv[1]}", newline="\n") as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            csvlist.append(row)
except OSError as error:
    print("Wrong file name, try again with files available below")
    print(os.listdir())
    err = 1
if not err:
    for index in range(0,num_changes):
        change = sys.argv[index + 3].split(sep=",")
        csvlist[int(change[0])][int(change[1])] = change[2]
    with open(f'{sys.argv[2]}', mode='w') as file:
        for rows in csvlist:
            csv_write = csv.writer(file, delimiter=',')
            csv_write.writerow(rows)
    print(f"File {sys.argv[1]} updated "
          f"successfully and saved as {sys.argv[2]}")