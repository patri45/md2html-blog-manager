from database import DataBase
import tool
class Search:
    def __init__(self,data:DataBase):
        self.CMD = "?"
        self.sub_commands={"1":self._search_theme,
                           "2": self._search_topic,
                           "3": self._search_title,
                           }

        self.tool = tool.Tool()
        self.data=data

    def run(self,user_input:str):
        c=user_input.lower()
        result=""

        if self._is_sub_cmds_in(c):
            sub_cmd=c[1]
            if self._is_keyword_in(c):
                keyword = c[3:]
                result=self.sub_commands[sub_cmd](keyword)
        else:
            if self._is_keyword_in(c,1):
                keyword = c[1:]
                result=self._search_all(keyword)

        return result

    def _search_theme(self,keyword:str):
        result=self._search_keyword_in_(keyword,0)
        return result

    def _search_topic(self,keyword:str):
        result=self._search_keyword_in_(keyword,1)
        return result

    def _search_title(self,keyword:str):
        result=self._search_keyword_in_(keyword,2)
        return result

    def _search_all(self,keyword:str):
        result=self._search_keyword_in_(keyword,-1)
        return result

    def _is_sub_cmds_in(self,c:str):
        result = len(c) >= 3 and c[2] == "." and c[1] in self.sub_commands
        return result

    def _is_keyword_in(self,c:str,cmd_length:int=3):
        result = len(c)-c.count("/")-cmd_length>0
        if result==False:
            print("no keyword")
        return result

    def _search_keyword_in_(self, keyword:str, layer_num:int):
        if layer_num != -1:
            result = self.data.get_file_by_keyword_and_layer(keyword, layer_num)
        else:
            result = self.data.get_file_by_keyword(keyword)

        if result != []:
            file = self.tool.getfile_by_number(result)
            file_path = self.data.get_path_by(file)
            print(file + " is got")
            return file_path
        else:
            print("Sorry,no match...")
            return ""
