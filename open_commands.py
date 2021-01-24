import os
from database import DataBase
import tool

class Open:
    def __init__(self,data:DataBase):
        self.CMD = "/"
        self.abbr_commands={"?":self._open_got_file,
                            }
        self.sub_commands={"l":self._open_local_file,
                           "3": self._open_title,
                           }

        self.tool = tool.Tool()
        self.data=data
        self.user_path=None
        self.user_got_file_path=None

    def run(self,user_input,user_path,user_got_file_path):
        c=user_input.lower()
        self.user_path=user_path
        self.user_got_file_path=user_got_file_path

        if self._is_abbr_cmds_in(c):
            abbr_cmd=c[1:]
            self.abbr_commands[abbr_cmd]()
        elif self._is_sub_cmds_in(c):
            sub_cmd=c[1]
            if self._is_keyword_in(c[1:],2):
                keyword = c[3:]
                self.sub_commands[sub_cmd](keyword)
        else:
            if self._is_keyword_in(c[1:],0):
                if self._is_in_layer(c[1:], [2]):
                    keyword = c[1:]
                    self._open_path(keyword)

    def _open_got_file(self):
        file_path = self.user_got_file_path
        if file_path != "":
            file_path_list = file_path.replace(self.data.BLOG_MD_CONTENT_ROOT+"/", "").split("/")
            if self._is_file(len(file_path_list)) and os.path.exists(os.path.realpath(file_path+".md")):  # theme topic无文件，不能打开
                self._print_open(file_path_list[-1],file_path)
        else:
            print("you didn't get file")

    def _open_local_file(self,keyword:str):
        if self._is_file(len(self.user_path)+1):  # theme topic 无文件，不能打开
            result = self.data.auto_file_completion_by_parentPath(keyword, self.user_path)
            if result != "":
                parent_path = "/".join(self.user_path)
                file_path = self.data.BLOG_MD_CONTENT_ROOT + "/" + parent_path + "/" + result
                self._print_open(result,file_path)

    def _open_title(self,keyword:str):
        result = self.data.auto_file_completion_by_layer(keyword, 2)
        if result != "":
            file_path = self.data.get_path_by(result)
            self._print_open(result,file_path)

    def _open_path(self,keyword:str):
        input_layer_list = keyword.split("/")
        result = self.data.auto_path_completion(input_layer_list)
        if result != []:
            completed_input_path = "/".join(result)
            file_path = self.data.BLOG_MD_CONTENT_ROOT + "/" + completed_input_path
            self._print_open(result[-1],file_path)

    def _print_open(self,file_name,file_path):
        self.tool.open_file(file_path + ".md")
        print("open title " + file_name)

    def _is_in_layer(self,c:str,aim_layers:list):
        result = c.count("/") in aim_layers
        if result == False:
            print("wrong file layer")
        return result

    def _is_abbr_cmds_in(self,c:str):
        result= c[1:] in self.abbr_commands
        return result

    def _is_sub_cmds_in(self,c:str):
        result= len(c)>=3 and c[2]=="." and c[1] in self.sub_commands
        return result

    def _is_keyword_in(self,c:str,cmd_length:int=3):
        result = len(c)-c.count("/")-cmd_length>0
        if result==False:
            print("no keyword")
        return result

    def _is_file(self, layer_num:int):
        result = True
        if layer_num <= 2:
            print("You cannot open dir")
            result = False
        return result