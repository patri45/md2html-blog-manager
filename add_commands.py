import os
from database import DataBase
import tool


class Add:
    def __init__(self, data: DataBase):
        self.CMD = "+"
        self.sub_commands = {"l": self._add_file_in_local_dir,
                             "f": self._force_add_file_by_path,
                             }

        self.tool = tool.Tool()
        self.data = data
        self.user_path = None
        self.add_files_path_list=[]

    def run(self, user_input, user_path):
        c = user_input
        self.user_path = user_path

        if self._is_in_layer(c, [0, 1, 2]):
            if self._is_sub_cmds_in(c):
                sub_cmd = c[1]
                if self._is_keyword_in(c):
                    keyword = c[3:]
                    self.sub_commands[sub_cmd](keyword)
            else:
                if self._is_keyword_in(c, 1):
                    keyword = c[1:]
                    self._add_file_by_path(keyword)

        return self.add_files_path_list

    def _add_file_in_local_dir(self, keyword: str):
        path_list = []
        path_list.extend(self.user_path)
        path_list.append(keyword)
        self._create_file(path_list)

    def _force_add_file_by_path(self, keyword: str):
        path_list = keyword.split("/")
        if self._is_not_same_name(path_list):
            self._create_file(path_list)

    def _add_file_by_path(self, keyword: str):
        path_list = []
        if keyword.count("/") > 0:  # 创建topic或者title，需要对路径进行自动补全
            parents_list = keyword.lower().split("/")[:-1]
            parents_list_refined = self.data.auto_path_completion(parents_list)
            if parents_list_refined != []:
                path_list.extend(parents_list_refined)
                path_list.append(keyword.split("/")[-1])
                self._create_file(path_list)
        else:  # 创建theme，不需要对路径进行自动补全
            path_list.append(keyword)
            self._create_file(path_list)

    def _is_in_layer(self, c: str, aim_layers: list):
        result = c.count("/") in aim_layers
        if result == False:
            print("wrong file layer")
        return result

    def _is_abbr_cmds_in(self, c: str):
        result = c[1:] in self.abbr_commands
        return result

    def _is_sub_cmds_in(self, c: str):
        result = len(c) >= 3 and c[2] == "." and c[1] in self.sub_commands
        return result

    def _is_keyword_in(self, c: str, cmd_length: int = 3):
        result = len(c) - c.count("/") - cmd_length > 0
        if result == False:
            print("no search keyword")
        return result

    def _is_not_same_name(self,path_list:list):
        result=True
        for layer in range(len(path_list)):
            if layer==0:
                if path_list[layer] in self.data.get_topics() or path_list[layer] in self.data.get_titles():
                    print(path_list[layer]+" have same file in other layers")
                    result=False
            elif layer==1:
                if path_list[layer] in self.data.get_themes() or path_list[layer] in self.data.get_titles():
                    print(path_list[layer] + " have same file in other layers")
                    result=False
            elif layer==2:
                if path_list[layer] in self.data.get_themes() or path_list[layer] in self.data.get_topics():
                    print(path_list[layer] + " have same file in other layers")
                    result=False
        return result

    def _is_file_or_dir_not_existed(self,path):
        return bool(1-os.path.exists(os.path.realpath(path)))

    def _create_file(self, path_list):
        topic_path = ""
        title_path = ""
        theme_path = self.data.BLOG_MD_CONTENT_ROOT + "/" + path_list[0]
        if len(path_list) >= 2:
            topic_path = self.data.BLOG_MD_CONTENT_ROOT + "/" + path_list[0] + "/" + path_list[1]
            if len(path_list) > 2:
                title_path = self.data.BLOG_MD_CONTENT_ROOT + "/" + path_list[0] + "/" + path_list[1] + "/" + path_list[
                    2] + ".md"

        is_created=False
        if self._is_file_or_dir_not_existed(theme_path):  # 无theme时创建theme文件夹和文件
            os.makedirs(theme_path)
            is_created =True
            print("add theme " + path_list[0] + "... Done!")
        if topic_path != "" and self._is_file_or_dir_not_existed(topic_path):  # 无theme时创建topic文件夹和文件
            os.makedirs(topic_path)
            is_created = True
            print("add topic " + path_list[1] + "... Done! in "+path_list[0])
        if title_path != "" and self._is_file_or_dir_not_existed(title_path):  # 无title时创建title文件
            f = open(title_path, mode="w", encoding="utf-8")
            f.close()
            is_created = True
            print("add title " + path_list[2] + "... Done! in "+path_list[0]+"/"+path_list[1])

        if is_created:
            print("update database")
            self.add_files_path_list.append(path_list)
        else:
            print("file is existed")
