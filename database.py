import os
from collections import defaultdict
from anytree import Node


class DataBase:
    def __init__(self):
        self.BLOG_MD_ROOT = "f:/blog_markdown"
        self.BLOG_MD_CONTENT_ROOT = self.BLOG_MD_ROOT + "/content"

        self.tree = {}
        self.f_in_layers = defaultdict(list)

        self.layers = 0

    def load(self):
        self.tree['root'] = Node(self.BLOG_MD_CONTENT_ROOT)

        for root, dirs, files in os.walk(self.BLOG_MD_CONTENT_ROOT):
            for d in dirs:
                if root == self.BLOG_MD_CONTENT_ROOT:
                    self.tree[d] = Node(d, parent=self.tree['root'])
                    self.f_in_layers[0].append(d)
                else:
                    parent_dirs_list = root.split("\\")
                    parent_name = parent_dirs_list[-1]
                    self.tree[d] = Node(d, parent=self.tree[parent_name])
                    self.f_in_layers[len(parent_dirs_list) - 1].append(d)

            for f in files:
                f_name = f.split('.')[0]
                parent_dirs_list = root.split("\\")
                parent_name = parent_dirs_list[-1]
                self.tree[f_name] = Node(f_name, parent=self.tree[parent_name])
                self.f_in_layers[len(parent_dirs_list) - 1].append(f_name)

        self.layers = len(self.f_in_layers)

    def get_path_by(self, file_name: str):
        node = self.tree[file_name]
        return str(node)[7:-2]

    def is_file_in_layer(self, file_name: str, layer_num: int):
        return file_name in self.f_in_layers[layer_num]

    def get_file_by_keyword_and_layer(self, keyword: str, layer_num: int):
        result = []
        if layer_num in self.f_in_layers:
            for file_name in self.f_in_layers[layer_num]:
                if keyword.lower() in file_name.lower():
                    result.append(file_name)
        return result

    def get_file_by_keyword(self, keyword: str):
        result = []
        for files in self.f_in_layers.values():
            for file_name in files:
                if keyword.lower() in file_name.lower():
                    result.append(file_name)
        return result

    def is_num_in_layer(self, layer_num):
        return layer_num in self.f_in_layers

    def get_all_files(self):
        all_file_names = list(self.tree.keys())
        all_file_names.remove('root')
        return all_file_names

    def get_themes(self):
        return self.f_in_layers[0]

    def get_topics(self):
        return self.f_in_layers[1]

    def get_titles(self):
        return self.f_in_layers[2]

    def get_child_files_in(self, parent_dir: str):
        result = [child.name for child in self.tree[parent_dir].children]
        return result

    def get_path_list_of(self, file_name):
        path = self.get_path_by(file_name)
        path_refined = path.replace(self.BLOG_MD_CONTENT_ROOT + "/", "")
        return path_refined.split("/")

    def _process_possible_results(self,possible_results_list:list):
        result=''
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

    def auto_file_completion_by_layer(self, file_keyword:str, layer: int):
        possible_results_list = self.get_file_by_keyword_and_layer(file_keyword, layer)
        result=self._process_possible_results(possible_results_list)
        return result

    def auto_file_completion_by_parentPath(self, file_keyword:str, parent_path_list:list):
        possible_results_list = []
        files = self.get_child_files_in(parent_path_list[-1]) if parent_path_list != [] else self.get_child_files_in(
            'root')
        if files:
            for file in files:
                if file_keyword.lower() in file.lower():
                    possible_results_list.append(file)

        result = self._process_possible_results(possible_results_list)
        return result

    def auto_path_completion(self,input_layer_list:list):
        result=[]
        if input_layer_list:
            for i_index,i in enumerate(input_layer_list):
                if i_index==0:
                    completed_f=self.auto_file_completion_by_layer(i, 0)
                    if completed_f=='':
                        break
                    else:
                        result.append(completed_f)
                else:
                    completed_f=self.auto_file_completion_by_parentPath(i,result)
                    if completed_f=='':
                        break
                    else:
                        result.append(completed_f)
        else:
            print("Sorry,no input...")
        if len(result)<len(input_layer_list):
            if result:
                result_str = "/ ".join(result)
                print("Existed parent directory: " + result_str)
            else:
                print("No parent directory found")
            result=[]
        return result

    def add(self,files_path_list:list):
        for f_path_list in files_path_list:
            for index,f in enumerate(f_path_list):
                if f not in self.f_in_layers[index]:
                    self.f_in_layers[index].append(f)
                    pre_index=index-1
                    if pre_index>=0:
                        self.tree[f]=Node(f,parent=self.tree[f_path_list[pre_index]])
                    else:
                        self.tree[f] = Node(f, parent=self.tree['root'])


a = DataBase()
a.load()

#print(a.get_topics())
#print(a.get_path_list_of('kl'))

#print(a.auto_path_completion(['p','g','m']))
#print(a.get_child_files_in('Github开源项目练手'))
#print(a.auto_file_completion_by_parentPath(file_keyword='',parent_path_list=['Github开源项目练手']))
#print(a.auto_file_completion_by_layer('p',1))

# a.add([['Modeling 建模相关','Modeling 建模相关','000']])
# print(a.get_themes())
# print(a.get_topics())
# print(a.get_titles())