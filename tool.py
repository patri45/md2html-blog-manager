import os

class Tool:
    def initialize_if_childList_is_null_of(self, index, parent_list):
        while True:
            if index > len(parent_list) - 1:
                parent_list.append([])
            else:
                break

    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def open_file(self, file_path):
        os.system('"' + file_path + '"')