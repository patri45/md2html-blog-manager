import os, time
import tool


class Cancel(Exception): pass


class Quit(Exception):
    def __str__(self):
        return ("quit...")


class BlogManager:
    def __init__(self):
        self.BLOG_MD_ROOT = "f:/blog_markdown"
        self.BLOG_MD_CONTENT_ROOT = self.BLOG_MD_ROOT + "/content"

        self.BASIC_COMMANDS = {
            "": ["raise Cancel"],
            "q": ["raise Quit"],
            "c": ["os.system('cls')"],
            "ll": ["self._show_files_in_user_path()"],
            "l": ["self._show_user_path()"],
            "la": ["self._show_content_structure()"],
            "lf": ["self._show_content_themes()"],
            "ls": ["self._show_content_topics()"],
            "lt": ["self._show_content_titles()"],
        }
        self.OPERATION_COMMANDS = {"~": ["self._search_mode()"],
                                   "+": ["self._add_mode()"],
                                   "?": ["self._search_mode()"],
                                   ">": ["self._enter_dir_mode()"],
                                   "/": ["self._open_file_mode()"],
                                   }
        self.SEARCH_COMMANDS = {"a.": ["layer_num = -1"],
                                "f.": ["layer_num = 0"],
                                "s.": ["layer_num = 1"],
                                "t.": ["layer_num = 2"],
                                }
        self.HINTS = {"add": [],
                      }

        self.tool = tool.Tool()

        self.content_files_path_dict = {}
        self.content_structure_dict = {}
        self.topics_in_layers = []

        self.mode = None
        self.user_input = ""
        self.user_path = []
        self.user_got_file_path = ""

    def _initialize(self):
        self._load_files_in_content()
        self._classify_topics_by_layers_in()
        self._initialize_content_structure()

    def _load_files_in_content(self):
        self.content_files_path_dict.clear()  # 暂时用于重新初始化，待升级
        for root, dirs, files in os.walk(self.BLOG_MD_CONTENT_ROOT):
            for d in dirs:
                self.content_files_path_dict[d] = os.path.join(root, d).replace('\\', '/')
            for f in files:
                f_name = f.split('.')[0]
                self.content_files_path_dict[f_name] = os.path.join(root, f_name).replace('\\', '/')

    def _classify_topics_by_layers_in(self):
        self.topics_in_layers = []  # 暂时用于重新初始化，待升级
        for name, path in self.content_files_path_dict.items():
            dir_num = path.replace(self.BLOG_MD_CONTENT_ROOT, '').count('/')
            self.tool.initialize_if_childList_is_null_of(dir_num - 1, self.topics_in_layers)
            self.topics_in_layers[dir_num - 1].append(name)

    def _initialize_content_structure(self):
        self.content_structure_dict.clear()  # 暂时用于重新初始化，待升级
        for name, path in self.content_files_path_dict.items():
            file_layer_path = path.replace(self.BLOG_MD_CONTENT_ROOT, '').split(".")[0]
            file_layer_path = file_layer_path.strip("/")
            file_layer_list = file_layer_path.split("/")
            self._structure_file_in_dict_by(file_layer_list, self.content_structure_dict)
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

    def _show_content_structure(self):
        for theme in self.content_structure_dict.keys():
            print(theme + " >> ", end="")
            for topic in self.content_structure_dict[theme].keys():
                print(topic + ", ", end="")
            print(end="\n")
        print()

    def _show_content_themes(self):
        print("Themes >> ", end="")
        files = " | ".join(self.topics_in_layers[0])
        print(files)

    def _show_content_topics(self):
        print("Topics >> ", end="")
        files = " | ".join(self.topics_in_layers[1])
        print(files)

    def _show_content_titles(self):
        print("Titles >> ", end="")
        files = " | ".join(self.topics_in_layers[2])
        print(files)

    def _show_files_in_user_path(self):
        print("Local files >> ", end="")
        result = self._get_files_in_target_path_by(self.user_path)
        files = " | ".join(result)
        print(files)

    def _show_user_path(self):
        print("Path >> ", end="")
        if self.user_path != []:
            dirs = " / ".join(self.user_path)
            print(dirs)
        else:
            print("ROOT")

    def run(self):
        self._initialize()
        self._show_content_structure()
        print("Blog Manager start...")
        hints = "hints: + 添加 | ? 搜索 | c 清屏| q 退出"
        try:
            while True:
                try:
                    self._input_command("请输入指令:")
                except Cancel:
                    pass
        except Quit:
            print("Blog Manager closed...")

    def _execute_command(self, commands):
        for command in commands:
            exec(command)

    def _input_command(self, prompt):
        self.user_input = input(prompt)
        c = self.user_input.lower()
        if c in self.BASIC_COMMANDS:
            self._execute_command(self.BASIC_COMMANDS[c])
        elif c[0] in self.OPERATION_COMMANDS:
            self._execute_command(self.OPERATION_COMMANDS[c[0]])
        else:
            print("no command...")

    def _input_number(self, prompt):
        while True:
            self.user_input = input(prompt)
            c = self.user_input
            if self.tool.is_int(c):
                break
            elif c == "":
                raise Cancel
            else:
                print("input is not number")

    def _search_mode(self):
        hints = "hints: a. all | f. themes | s. topics | t. titles"
        c = self.user_input.lower()
        search_layer = -1
        search_keyword = ""
        is_search = False

        if len(c) >= 3 and c[2] == ".":  # 判断是否有副指令
            sub_command = c[1]
            if len(c) - 3 > 0:  # 判断是否有文件名
                search_keyword = c[3:]
                if sub_command == "f":  # ?f. 一级搜索 在theme中搜索title
                    search_layer = 0
                    is_search = True
                elif sub_command == "s":  # ?s. 二级搜索 在topic中搜索title
                    search_layer = 1
                    is_search = True
                elif sub_command == "t":  # ?t. 三级搜索 在title中搜索title
                    search_layer = 2
                    is_search = True
                else:
                    print("no sub command")
            else:
                print("no search file name")
        else:  # ? 默认创建 没有副指令
            if len(c) - 1 > 0:  # 判断是否有文件名
                search_keyword = c[1:]
                is_search = True
            else:
                print("no search file name")

        if is_search:  # 判断是否满足进行搜索的条件
            result = self._search_keyword_in_(search_keyword, search_layer)
            if result != []:
                file = self._getfile_by_number(result)
                file_path = self.content_files_path_dict[file]
                self.user_got_file_path = file_path
                print(file + " is got")
                # self.tool.open_file(file_path)
                # self._openfile_by_number(result)
            else:
                print("Sorry,no match...")

    def _search_keyword_in_(self, keyword, layer_num=-1):
        result = []
        if layer_num != -1:
            if layer_num <= len(self.topics_in_layers) - 1:
                for file_name in self.topics_in_layers[layer_num]:
                    if keyword in file_name.lower():
                        result.append(file_name)
        else:
            for layer in self.topics_in_layers:
                for file_name in layer:
                    if keyword in file_name.lower():
                        result.append(file_name)
        return result

    def _print_result_by_number(self, result):
        index = 0
        for title in result:
            index += 1
            print(str(index) + ". " + title)

    def _open_file_mode(self):
        c = self.user_input.lower()
        c_slash_num = c.count("/")
        if c_slash_num <= 3:  # 判断输入路径是否超过 theme topic title 的限制
            if len(c) == 2 and c[-1] == "?":  # /?. 打开got文件
                file_path = self.user_got_file_path
                if file_path != "":
                    file_name = file_path.split("/")[-1]
                    if file_name not in self.topics_in_layers[0] and file_name not in self.topics_in_layers[
                        1]:  # theme topic无文件，不能打开
                        print("open title " + file_name)
                        time.sleep(1)
                        self.tool.open_file(file_path + ".md")
                    else:
                        print("cannot open theme or topic")
                else:
                    print("you got no file")
            elif len(c) >= 3 and c[2] == ".":  # 判断是否有副指令
                sub_command = c[1]
                if len(c) - 3 > 0:  # 判断是否有文件名
                    file_name = c[3:]
                    if sub_command == "l":  # /l. 打开本地文件 在user path直接打开
                        if self.user_path != [] and len(self.user_path) != 1:  # theme topic 无文件，不能打开
                            completed_file_name = self._auto_file_completion(file_name, self.user_path)
                            if completed_file_name != "":
                                parent_path = "/".join(self.user_path)
                                file_path = self.BLOG_MD_CONTENT_ROOT + "/" + parent_path + "/" + completed_file_name + ".md"
                                print("open " + file_path)
                                time.sleep(1)
                                self.tool.open_file(file_path)
                        else:
                            print("cannot open theme or topic")
                    elif sub_command == "t":  # /t. 打开title文件
                        result = self._auto_layers_completion(file_name, 2)
                        if result != "":
                            file_path = self.content_files_path_dict[result]
                            # print(file_path)
                            print("open title " + result)
                            time.sleep(1)
                            self.tool.open_file(file_path + ".md")
                    else:
                        print("no sub command")
                else:
                    print("no open file name")
            else:  # / 默认打开文件 直接根据标准目录输入打开
                words_without_slashes = len(c) - c_slash_num
                if c_slash_num <= 2 and words_without_slashes > 0:
                    print("cannot open theme or topic")
                elif c_slash_num == 3 and words_without_slashes > 0:
                    input_layer_list = c[1:].split("/")
                    result = self._auto_path_completion(input_layer_list)
                    if result != []:
                        completed_input_path = "/".join(result)
                        file_path = str(self.BLOG_MD_CONTENT_ROOT + "/" + completed_input_path + ".md")
                        # print(file_path)
                        print("open " + completed_input_path)
                        time.sleep(1)
                        self.tool.open_file(file_path)
                else:
                    print("no open file name")

        else:
            print("exceed layer limit")

    def _judge_is_dir(self, layer_num):
        result = True
        if layer_num >= 2:
            print("You cannot enter file")
            result = False
        return result

    def _enter_dir_mode(self):
        c = self.user_input.lower()

        if c.count("/") <= 1:  # 判断输入路径是否超过 theme topic 的限制
            if len(c) == 3 and c[1:] == "..":  # >.. 进入父目录的父目录 根据user path直接进入
                if self.user_path == [] or len(self.user_path) == 1 or len(self.user_path) == 2:
                    self.user_path = []
                else:
                    self.user_path = self.user_path[:-2]
                path = " / ".join(self.user_path)
                print("enter " + path)
            elif len(c) == 2 and c[-1] == ".":  # >. 进入父目录 根据user path直接进入
                if self.user_path == [] or len(self.user_path) == 1:
                    self.user_path = []
                else:
                    self.user_path = self.user_path[:-1]
                path = " / ".join(self.user_path)
                print("enter " + path)
            elif len(c) == 2 and c[-1] == "?":  # >? 进入got目录
                file_path = self.user_got_file_path
                if file_path != "":
                    file_path_list = file_path.replace(self.BLOG_MD_CONTENT_ROOT + "/", "").split("/")
                    if len(file_path_list) <= 2:
                        self.user_path = file_path_list
                        path = " / ".join(file_path_list)
                        print("enter " + path)
                    else:
                        print("cannot enter file")
                else:
                    print("you got no file")

            elif len(c) >= 3 and c[2] == ".":  # 判断是否有副指令
                sub_command = c[1]
                if len(c) - 3 > 0:  # 判断是否有文件名
                    file_name = c[3:]
                    if sub_command == "l":  # >l. 进入当前目录下级文档 在user path直接进入
                        result = self._auto_file_completion(file_name, self.user_path)
                        if result != "" and result not in self.topics_in_layers[2]:
                            self.user_path.append(result)
                            path = " / ".join(self.user_path)
                            print("enter " + path)
                        else:
                            print("cannot enter file")
                    elif sub_command == "f":  # >f. 进入theme文档
                        print(file_name)
                        result = self._auto_layers_completion(file_name, 0)
                        if result != "":
                            self.user_path = self._get_path_list_of(result)
                            path = " / ".join(self.user_path)
                            print("enter " + path)
                    elif sub_command == "s":  # >s. 进入topic文档
                        file_name = c[3:]
                        result = self._auto_layers_completion(file_name, 1)
                        if result != "":
                            self.user_path = self._get_path_list_of(result)
                            path = " / ".join(self.user_path)
                            print("enter " + path)
                    else:
                        print("no sub command")
                else:
                    print("no enter dir name")
            else:  # > 默认进入目录 直接根据标准目录格式输入进入
                if len(c) >= 2:
                    input_layer_list = c[1:].split("/")
                    result = self._auto_path_completion(input_layer_list)
                    if result != []:
                        self.user_path = result
                        path = " / ".join(self.user_path)
                        print("enter " + path)
                else:
                    print("no enter dir name")

        else:
            print("cannot enter file")

    def _get_path_list_of(self, file_name):
        path = self.content_files_path_dict[file_name].replace(self.BLOG_MD_CONTENT_ROOT, "")
        result = path.split("/")
        return result

    def _get_files_in_target_path_by(self, path_list):
        result = []
        path_num = len(path_list)
        if path_list != []:  # 判断是否为根目录
            if path_num > 2:  # 判断是否超过目录层级限制
                print("exceed layer limit")
            elif path_num == 2:  # 判断是否为topic
                if path_list[0] in self.content_structure_dict.keys() and path_list[1] in self.content_structure_dict[path_list[0]].keys():  # 判断是否存在topic
                    result = self.content_structure_dict[path_list[0]][path_list[1]]
            else:  # 判断是否为theme
                if path_list[0] in self.content_structure_dict.keys():  # 判断是否存在theme
                    result = self.content_structure_dict[path_list[0]]
        else:
            result = self.topics_in_layers[0]
        return result

    def _auto_layers_completion(self, file_name, layer):
        result = ""
        possible_results_list = []
        files = self.topics_in_layers[int(layer)]

        for file in files:
            if file_name.lower() in file.lower():
                possible_results_list.append(file)  # 将可能的结果添加到possible path list

        if len(possible_results_list) > 1:
            file = self._getfile_by_number(possible_results_list)
            # print(file)
            if file != "":
                result = file
        elif len(possible_results_list) == 1:
            result = possible_results_list[0]
        else:
            print("Sorry,no match...")
        return result

    def _auto_file_completion(self, file_name, parent_path_list):
        result = ""
        possible_results_list = []
        files = self._get_files_in_target_path_by(parent_path_list)
        if files != []:
            for file in files:
                if file_name.lower() in file.lower():
                    possible_results_list.append(file)

        if len(possible_results_list) > 1:
            file = self._getfile_by_number(possible_results_list)
            # print(file)
            if file != "":
                result = file
        elif len(possible_results_list) == 1:
            result = possible_results_list[0]
        else:
            print("Sorry,no match...")
        return result

    def _auto_path_completion(self, input_layer_list):
        result = []
        possible_path_list = []  # 储存每个子目录可能的结果
        i_list = input_layer_list

        i_index = 0
        while i_index <= len(i_list) - 1:
            i_file = i_list[i_index]
            self.tool.initialize_if_childList_is_null_of(i_index, possible_path_list)  # 根据index初始化列表中的子列表，避免index报错
            if i_index == 0:
                files = self.topics_in_layers[0]
            elif i_index == 1:
                files = self.content_structure_dict[result[0]].keys()  # 子目录需要在父目录中
            elif i_index == 2:
                files = self.content_structure_dict[result[0]][result[1]]  # 子目录需要在父目录中
            for file in files:
                if i_file.lower() in file.lower():
                    possible_path_list[i_index].append(file)  # 将可能的结果添加到possible path list

            if len(possible_path_list[i_index]) > 1:  # 当目录可能结果大于1时，列出可能结果，用户进行选择
                file = self._getfile_by_number(possible_path_list[i_index])
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

    def _create_file(self, path_list):
        theme_path = ""
        topic_path = ""
        title_path = ""

        theme_path = self.BLOG_MD_CONTENT_ROOT + "/" + path_list[0]
        if len(path_list) >= 2:
            topic_path = self.BLOG_MD_CONTENT_ROOT + "/" + path_list[0] + "/" + path_list[1]
            if len(path_list) > 2:
                title_path = self.BLOG_MD_CONTENT_ROOT + "/" + path_list[0] + "/" + path_list[1] + "/" + path_list[
                    2] + ".md"

        if not os.path.isdir(theme_path):  # 无theme时创建theme文件夹和文件
            os.makedirs(theme_path)
            print("add theme " + path_list[0] + "... Done!")
        if topic_path != "" and not os.path.isdir(topic_path):  # 无theme时创建topic文件夹和文件
            os.makedirs(topic_path)
            print("add topic " + path_list[1] + "... Done!")
        if title_path != "" and not os.path.isfile(title_path):  # 无title时创建title文件
            f = open(title_path, mode="w", encoding="utf-8")
            f.close()
            print("add title " + path_list[2] + "... Done!")

    def _add_mode(self):
        c = self.user_input
        is_created = False

        if c.count("/") <= 2:  # 判断输入路径是否超过 theme topic title 的限制
            if len(c) >= 3 and c[2] == ".":  # 判断是否有副指令
                sub_command = c[1]
                if len(c) - 3 > 0:  # 判断是否有文件名
                    if sub_command == "f":  # +f. 强制创建 创建输入路径中所有不存在的文件夹和文件
                        dirs_list = c[3:].split("/")
                        self._create_file(dirs_list)
                        is_created = True
                    elif sub_command == "l":  # +l. 本地创建 在user path直接创建
                        dirs_newFile = c[3:].split("/")
                        dirs_list = []
                        dirs_list.extend(self.user_path)
                        dirs_list.extend(dirs_newFile)
                        self._create_file(dirs_list)
                        is_created = True
                    else:
                        print("no sub command")
                else:
                    print("no add file name")
            else:  # + 默认创建 没有副指令
                if len(c) - 1 > 0:
                    dirs_list = []
                    if c.count("/") > 0:  # 创建topic或者title，需要对路径进行自动补全
                        dirs_newFile = c[1:].lower().split("/")
                        input_layer_list = dirs_newFile[:-1]
                        parent_dir_list = self._auto_path_completion(input_layer_list)
                        if parent_dir_list != []:
                            dirs_list.extend(parent_dir_list)
                            dirs_list.append(c[1:].split("/")[-1])
                            self._create_file(dirs_list)
                            is_created = True
                    else:  # 创建theme，不需要对路径进行自动补全
                        dirs_list.append(self.user_input[1:])
                        self._create_file(dirs_list)
                        is_created = True
                else:
                    print("no add file name")

        else:
            print("exceed layer limit")

        if is_created:
            self._initialize()
            pass

    def _getfile_by_number(self, result_list):
        result = ""
        self._print_result_by_number(result_list)
        self._input_number("请输入序号:")
        c = self.user_input
        if 0 < int(c) <= len(result_list):
            result = result_list[int(c) - 1]
        return result


blogManager = BlogManager()
blogManager.run()
