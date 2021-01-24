import os
import tool

class DataBase:
    def __init__(self):
        self.BLOG_MD_ROOT = "f:/blog_markdown"
        self.BLOG_MD_CONTENT_ROOT = self.BLOG_MD_ROOT + "/content"

        self.files_path_dict = {}
        self.files_structure_dict = {}
        self.files_layers_dict = []

        self.tool=tool.Tool()

        self.layers=0

    def load(self):
        self._load_files_in_content()
        self._classify_topics_by_layers_in()
        self._initialize_content_structure()
        self.layers=len(self.files_layers_dict)

    def _load_files_in_content(self):
        self.files_path_dict.clear()  # 暂时用于重新初始化，待升级
        for root, dirs, files in os.walk(self.BLOG_MD_CONTENT_ROOT):
            for d in dirs:
                self.files_path_dict[d] = os.path.join(root, d).replace('\\', '/')
            for f in files:
                f_name = f.split('.')[0]
                self.files_path_dict[f_name] = os.path.join(root, f_name).replace('\\', '/')

    def _classify_topics_by_layers_in(self):
        self.files_layers_dict = []  # 暂时用于重新初始化，待升级
        for name, path in self.files_path_dict.items():
            dir_num = path.replace(self.BLOG_MD_CONTENT_ROOT, '').count('/')
            self._initialize_if_childList_is_null_of(dir_num - 1, self.files_layers_dict)
            self.files_layers_dict[dir_num - 1].append(name)

    def _initialize_content_structure(self):
        self.files_structure_dict.clear()  # 暂时用于重新初始化，待升级
        for name, path in self.files_path_dict.items():
            file_layer_path = path.replace(self.BLOG_MD_CONTENT_ROOT, '').split(".")[0]
            file_layer_path = file_layer_path.strip("/")
            file_layer_list = file_layer_path.split("/")
            self._structure_file_in_dict_by(file_layer_list, self.files_structure_dict)
        # print(self.content_structure_dict)

    def _structure_file_in_dict_by(self, file_layer_list, d):
        for layer in range(len(file_layer_list)):
            if layer == 0:
                if file_layer_list[0] not in d.keys():
                    d[file_layer_list[0]] = {}
            elif layer == 1:
                if file_layer_list[1] not in d[file_layer_list[0]].keys():
                    d[file_layer_list[0]][file_layer_list[1]] = []
            elif layer == 2:
                if file_layer_list[2] not in d[file_layer_list[0]][file_layer_list[1]]:
                    d[file_layer_list[0]][file_layer_list[1]].append(file_layer_list[2])

    def _initialize_if_childList_is_null_of(self, index, parent_list):
        while True:
            if index > len(parent_list) - 1:
                parent_list.append([])
            else:
                break

    def get_path_by(self,file_name:str):
        return self.files_path_dict[file_name]

    def is_file_in_layer(self,file_name:str,layer_num:int):
        return file_name in self.files_layers_dict[layer_num]

    def get_file_by_keyword_and_layer(self,keyword:str,layer_num:int):
        result=[]
        if self.is_num_in_layer(layer_num):
            for file_name in self.files_layers_dict[layer_num]:
                if keyword.lower() in file_name.lower():
                    result.append(file_name)
        return result

    def get_file_by_keyword(self,keyword:str):
        result=[]
        for layer_num in range(self.layers):
            for file_name in self.files_layers_dict[layer_num]:
                if keyword.lower() in file_name.lower():
                    result.append(file_name)
        return result

    def is_num_in_layer(self,layer_num):
        return 0 <= layer_num <= self.layers-1

    def get_all_files(self):
        return list(self.files_path_dict.keys())

    def get_themes(self):
        result = self.files_layers_dict[0] if self.layers >= 1 else []
        return result

    def get_topics(self):
        result = self.files_layers_dict[1] if self.layers >= 2 else []
        return result

    def get_titles(self):
        result=self.files_layers_dict[2] if self.layers>=3 else []
        return result

    def get_topics_in(self,theme:str):
        result = list(self.files_structure_dict[theme].keys()) if self.layers >= 1 and theme in self.files_structure_dict else []
        return result

    def get_titles_in(self,theme:str,topic:str):
        if self.layers >= 2 and theme in self.files_structure_dict and topic in self.files_structure_dict[theme]:
            result = self.files_structure_dict[theme][topic]
        else:
            result = []
        return result

    def get_path_list_of(self, file_name):
        path=self.get_path_by(file_name)
        path_refined = path.replace(self.BLOG_MD_CONTENT_ROOT+"/", "")
        return path_refined.split("/")

    def get_files_in_target_path_by(self, path_list:list):
        result = []
        path_num = len(path_list)
        if path_list != []:  # 判断是否为根目录
            if path_num > 2:  # 判断是否超过目录层级限制
                print("exceed layer limit")
            elif path_num == 2:  # 判断是否为topic
                if path_list[0] in self.get_themes() and path_list[1] in self.get_topics_in(path_list[0]):  # 判断是否存在topic
                    result = self.get_titles_in(path_list[0],path_list[1])
            else:  # 判断是否为theme
                if path_list[0] in self.get_themes(): # 判断是否存在theme
                    result = self.get_topics_in(path_list[0])
        else:
            result = self.get_themes()
        return result

    def auto_file_completion_by_layer(self, file_keyword, layer:int):
        result = ""
        possible_results_list = self.get_file_by_keyword_and_layer(file_keyword,layer)

        if len(possible_results_list) > 1:
            file = self.tool.getfile_by_number(possible_results_list)
            # print(file)
            if file != "":
                result = file
        elif len(possible_results_list) == 1:
            result = possible_results_list[0]
        else:
            print("Sorry,no match...")
        return result

    def auto_file_completion_by_parentPath(self, file_keyword, parent_path_list):
        result = ""
        possible_results_list = []
        files = self.get_files_in_target_path_by(parent_path_list)
        if files != []:
            for file in files:
                if file_keyword.lower() in file.lower():
                    possible_results_list.append(file)

        if len(possible_results_list) > 1:
            file = self.tool.getfile_by_number(possible_results_list)
            # print(file)
            if file != "":
                result = file
        elif len(possible_results_list) == 1:
            result = possible_results_list[0]
        else:
            print("Sorry,no match...")
        return result

    def auto_path_completion(self, input_layer_list):
        result = []
        possible_path_list = []  # 储存每个子目录可能的结果
        i_list = input_layer_list

        i_index = 0
        while i_index <= len(i_list) - 1:
            i_file = i_list[i_index]
            self.tool.initialize_if_childList_is_null_of(i_index, possible_path_list)  # 根据index初始化列表中的子列表，避免index报错
            if i_index == 0:
                files = self.get_themes()
            elif i_index == 1:
                files = self.get_topics_in(result[0])  # 子目录需要在父目录中
            elif i_index == 2:
                files = self.get_titles_in(result[0],result[1])  # 子目录需要在父目录中
            for file in files:
                if i_file.lower() in file.lower():
                    possible_path_list[i_index].append(file)  # 将可能的结果添加到possible path list

            if len(possible_path_list[i_index]) > 1:  # 当目录可能结果大于1时，列出可能结果，用户进行选择
                file = self.tool.getfile_by_number(possible_path_list[i_index])
                # print(file)
                if file != "":
                    result.append(file)
            elif len(possible_path_list[i_index]) == 1:  # 当目录可能结果等于1时，直接添加结果
                result.append(possible_path_list[i_index][0])
            else:  # 当目录可能结果为0时，打印找到的父目录
                print("Sorry,no match...")
                if result != []:
                    result_str = " ,".join(result)
                    print("Existed parent directory: " + result_str)
                else:
                    print("No parent directory found")
                result = []
                break
            i_index += 1
            # print(result)

        return result

# a=DataBase()
# a.load()
# print(a.get_themes())
# print(a.files_path_dict)
# print(a.files_layers_dict)