import sys
import json
import os
import pickle


class Base:

    def __init__(self):
        self.error = 0
        self.no_of_changes()
        self.src_file_type_check()
        self.dst_file_type_check()

    def no_of_changes(self):
        self.num_changes = len(sys.argv) - 3
        if self.num_changes < 1:
            self.error = 1
            return None
        return self.num_changes

    def src_subclass_init(self, file_type):
        if file_type == 'csv':
            self.src_file = Csv()
            self.src_file.file_name = sys.argv[1]
        elif file_type == 'json':
            self.src_file = Json()
            self.src_file.file_name = sys.argv[1]
        elif file_type == 'pickle':
            self.src_file = Pickle()
            self.src_file.file_name = sys.argv[1]
            self.src_file.pickle_read()
        else:
            self.dst_file = None
            self.error = 1

    def dst_subclass_init(self, file_type):
        if file_type == 'csv':
            self.dst_file = Csv()
            self.dst_file.file_name = sys.argv[2]
        elif file_type == 'json':
            self.dst_file = Json()
            self.dst_file.file_name = sys.argv[2]
        elif file_type == 'pickle':
            self.dst_file = Pickle()
            self.dst_file.file_name = sys.argv[2]
            self.dst_file.pickle_write()
        else:
            self.dst_file = None
            self.error = 1        

    def src_file_type_check(self):
        try:
            self.src_file_type = sys.argv[1][sys.argv[1].find('.') + 1:].lower()
            self.src_subclass_init(self.src_file_type)
        except IndexError:
            self.error = 1

    def dst_file_type_check(self):
        try:
            self.dst_file_type = sys.argv[2][sys.argv[2].find('.') + 1:].lower()
            self.dst_subclass_init(self.dst_file_type)
        except IndexError:
            self.error = 1

    def error_print(self):
        print("Wrong file name or type, try again with files available below")
        print(os.listdir())


class Csv(Base):
    def __init__(self):
        pass

class Json(Base):
    def __init__(self):
        pass

class Pickle(Base):
    
    def __init__(self):
        pass

    def pickle_mode(self):
        if self.file_name == sys.argv[1]:
            self.mode = 'rb'
        else:
            self.mode = 'wb'

    def pickle_read(self):
        with open(self.file_name, self.mode) as file:
            self.unpickled = pickle.loads(file.read())
            print(self.unpickled)

    def write_as_json(self):
        self.unpickled_json = json.dumps(self.unpickled)
        print(self.unpickled_json)
        with open(sys.argv[2], 'w') as file:
            file.write(self.unpickled_json)

    def write_as_csv(self):
        pass

    def write_as_pickle(self):
        with open(self.file_name, self.mode) as file:
            self.pickled = pickle.dumps(file.read())
"""
listsss = [['a', 'b', 'c'],['z', 'y', 'x']]
with open('pickle.pickle', 'wb') as file:
    pickledlist = pickle.dumps(listsss)
    file.write(pickledlist)
with open('pickle.pickle', 'rb') as file:
    unpickled = pickle.loads(file.read())
    print(unpickled)
"""
base = Base()
if not base.error:
    if base.src_file_type == 'json':
        base.dst_file.write_as_json()
    elif base.src_file_type == 'csv':
        base.dst_file.write_as_csv()
    else:
        base.dst_file.write_as_pickle()
"""
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
"""