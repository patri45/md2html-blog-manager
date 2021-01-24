import os
from sys_exceptions import Cancel

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
        os.startfile(os.path.realpath(file_path))

    def _print_result_by_number(self, result):
        index = 0
        for title in result:
            index += 1
            print(str(index) + ". " + title)

    def _input_number(self, prompt):
        while True:
            self.user_input = input(prompt)
            c = self.user_input
            if self.is_int(c):
                break
            elif c == "":
                raise Cancel
            else:
                print("input is not number")

    def getfile_by_number(self, result_list):
        result = ""
        self._print_result_by_number(result_list)
        self._input_number("请输入序号:")
        c = self.user_input
        if 0 < int(c) <= len(result_list):
            result = result_list[int(c) - 1]
        return result