from database import DataBase
import tool

class Enter:
    def __init__(self,data:DataBase):
        self.CMD = ">"
        self.abbr_commands={"..":self._enter_parent_parent_dir,
                            ".":self._enter_parent_dir,
                            "?":self._enter_got_dir,
                            }
        self.sub_commands={"l":self._enter_local_dir,
                           "1": self._enter_theme,
                           "2": self._enter_topic,
                           }

        self.tool = tool.Tool()
        self.data=data
        self.user_path=None
        self.user_got_file_path=None

    def run(self,user_input,user_path,user_got_file_path):
        c=user_input.lower()
        self.user_path=user_path
        self.user_got_file_path=user_got_file_path

        if self._is_in_layer(c,[0,1]):
            if self._is_abbr_cmds_in(c):
                abbr_cmd=c[1:]
                self.abbr_commands[abbr_cmd]()
            elif self._is_sub_cmds_in(c):
                sub_cmd=c[1]
                if self._is_keyword_in(c):
                    keyword = c[3:]
                    self.sub_commands[sub_cmd](keyword)
            else:
                if self._is_keyword_in(c,1):
                    keyword = c[1:]
                    self._enter_path(keyword)

        return self.user_path

    def _enter_parent_parent_dir(self):
        if self.user_path == [] or len(self.user_path) == 1 or len(self.user_path) == 2:
            self.user_path = []
        else:
            self.user_path = self.user_path[:-2]
        self._print_enter()

    def _enter_parent_dir(self):
        if self.user_path == [] or len(self.user_path) == 1:
            self.user_path = []
        else:
            self.user_path = self.user_path[:-1]
        self._print_enter()

    def _enter_got_dir(self):
        file_path = self.user_got_file_path
        if file_path != "":
            file_path_list = file_path.replace(self.data.BLOG_MD_CONTENT_ROOT + "/", "").split("/")
            if self._is_dir(len(file_path_list)):
                self.user_path = file_path_list
                self._print_enter()
        else:
            print("you didn't get file")

    def _enter_local_dir(self,keyword:str):
        if self._is_dir(len(self.user_path)+1):
            result = self.data.auto_file_completion_by_parentPath(keyword, self.user_path)
            if result != "":
                self.user_path.append(result)
                self._print_enter()

    def _enter_theme(self,keyword:str):
        result = self.data.auto_file_completion_by_layer(keyword, 0)
        if result != "":
            self.user_path = self.data.get_path_list_of(result)
            self._print_enter()

    def _enter_topic(self,keyword:str):
        result = self.data.auto_file_completion_by_layer(keyword, 1)
        if result != "":
            self.user_path = self.data.get_path_list_of(result)
            self._print_enter()

    def _enter_path(self,keyword:str):
        input_layer_list = keyword.split("/")
        result = self.data.auto_path_completion(input_layer_list)
        if result != []:
            self.user_path = result
            self._print_enter()

    def _print_enter(self):
        path = " / ".join(self.user_path)
        print("enter " + path)


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

    def _is_dir(self, layer_num:int):
        result = True
        if layer_num >= 3:
            print("You cannot enter file")
            result = False
        return result