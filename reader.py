import sys
import json
import os
import pickle
import csv


class Base:

    def __init__(self):
        self.error = 0
        if not self.argv_check():
            if not self.src_file_type_check():
                if not self.dst_file_type_check():
                    if self.error:
                        self.error_2_print()
        self.no_of_changes_check()

    def no_of_changes_check(self):
        self.num_changes = len(sys.argv) - 3
        if self.num_changes < 1:
            self.error = 1
            print("Error [1], you didn't type any changes to the file")
            return None
        return self.num_changes

    def argv_check(self):
        if len(sys.argv) < 4:
            self.error = 1
            self.error_2_print()
            return True

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
        else:
            self.dst_file = None
            self.error = 1
            print("Error [4] Wrong output file extension")
            print("App uses only .json, .csv or .pickle extensions")


    def src_file_type_check(self):
        try:
            self.src_file_type = sys.argv[1][sys.argv[1].find('.') + 1:].lower()
            self.src_subclass_init(self.src_file_type)
        except IndexError:
            self.error = 1
            self.error_2_print()  
            return True

    def dst_file_type_check(self):
        try:
            self.dst_file_type = sys.argv[2][sys.argv[2].find('.') + 1:].lower()
            self.dst_subclass_init(self.dst_file_type)
        except IndexError:
            self.error = 1
            self.error_2_print()  
            return True

    def error_2_print(self):
        print("Error [2] Wrong file name, type or missing files in command")
        print("Try again with files available below")
        print("App uses only .json, .csv or .pickle extensions")
        for files in os.listdir():
                print(files)     

    def write_as_json(self, list):
        with open(sys.argv[2], 'w') as file:
            file.write(json.dumps(list))
        with open(sys.argv[2]) as file:
            print(f"Raw JSON after changes is:\n{file.read()}\n")


    def write_as_csv(self, list):
        with open(sys.argv[2], 'w') as file:
            for rows in list:
                csv_write = csv.writer(file, delimiter=';', lineterminator='\n')
                csv_write.writerow(rows)
        with open(sys.argv[2], 'r') as file:
            file_len = len(file.read())
        with open(sys.argv[2], 'a') as file:
            file.truncate(file_len - 1)
        with open(sys.argv[2]) as file:
            print(f"Raw CSV after changes is:\n{file.read()}\n")
            

    def write_as_pickle(self, list):
        with open(sys.argv[2], 'wb') as file:
            file.write(pickle.dumps(list))
        with open(sys.argv[2], 'rb') as file:
            print(f"Raw pickle after changes is:\n{file.read()}\n")

    def changes(self, num_changes, list):
        for index in range(0,num_changes):
            change = sys.argv[index + 3].split(sep=",")
            try:
                list[int(change[0])][int(change[1])] = change[2]
            except IndexError:
                print("Error [3], try again with corrent index numbers of change")
                print("Changes aborted")
                return None
        print(f"Changes completed\n{list}\n")
        return 1

    def write_as_selector(self):
        if self.dst_file_type == 'json':
            self.dst_file.write_as_json(base.src_file.list)
        elif self.dst_file_type == 'csv':
            self.dst_file.write_as_csv(base.src_file.list)
        else:
            self.dst_file.write_as_pickle(base.src_file.list)



class Csv(Base):
    def __init__(self):
        pass

    def read(self):
        for files in os.listdir():
            if self.file_name == files:
                with open(self.file_name, newline='\n') as file:
                    print(f"Raw CSV is:\n{file.read()}\n")
                self.list = []
                with open(self.file_name, newline='\n') as file:
                    csv_reader = csv.reader(file, delimiter=';')
                    for row in csv_reader:
                        self.list.append(row)
                print(f"Decoded csv is:\n{self.list}\n")
                return True
        return False

class Json(Base):
    def __init__(self):
        pass

    def read(self):
        for files in os.listdir():
            if self.file_name == files:
                with open(self.file_name) as file:
                    print(f"Raw json is:\n{file.read()}\n")
                with open(self.file_name, 'r') as file:
                    self.list = json.loads(file.read())
                    print(f"Decoded json is:\n{self.list}\n")
                return True
        return False
class Pickle(Base):
    
    def __init__(self):
        pass

    def read(self):
        for files in os.listdir():
            if self.file_name == files:
                with open(self.file_name, 'rb') as file:
                    print(f"Raw pickle is:\n{file.read()}\n")
                with open(self.file_name, 'rb') as file:
                    self.list = pickle.loads(file.read())
                    print(f"Decoded pickle is:\n{self.list}\n")
                return True
        return False

base = Base()
if not base.error:
    if base.src_file.read():
        if base.src_file.changes(base.num_changes, base.src_file.list):
            base.write_as_selector()
    else: base.error_2_print()