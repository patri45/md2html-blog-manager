import os
from database import DataBase
from sys_exceptions import Quit,Cancel

class BasicCommands:
    def __init__(self,data:DataBase):
        self.CMDS= {
            "": self._cancel_input,
            "q": self._quit_software,
            "c": self._clear_screen,
            "ll": self._look_files_in_user_path,
            "l": self._look_user_path,
            "la": self._look_content_structure,
            "l1": self._look_content_themes,
            "l2": self._look_content_topics,
            "l3": self._look_content_titles,
            "r": self._open_root_dir,
        }

        self.data=data
        self.user_path=None

    def run(self,user_input,user_path:list):
        c = user_input.lower()
        self.user_path=user_path
        self.CMDS[c]()
        return self.user_path

    def _cancel_input(self):
        raise Cancel

    def _quit_software(self):
        raise Quit

    def _clear_screen(self):
        os.system('cls')

    def _look_content_structure(self):
        for theme in self.data.get_themes():
            theme_fmt="{:<20} >> ".format(theme)
            print(theme_fmt, end="")
            for topic in self.data.get_child_files_in(theme):
                print(topic + " | ", end="")
            print(end="\n")

    def _look_content_themes(self):
        print("Themes >> ")
        files = " | ".join(self.data.get_themes())
        print(files)

    def _look_content_topics(self):
        print("Topics >> ")
        files = " | ".join(self.data.get_topics())
        print(files)

    def _look_content_titles(self):
        print("Titles >> ")
        files = " | ".join(self.data.get_titles())
        print(files)

    def _look_files_in_user_path(self):
        print("Local files >> ")
        result = self.data.get_child_files_in(self.user_path[-1]) if self.user_path != [] else self.data.get_child_files_in(
            'root')
        files = " | ".join(result)
        print(files)

    def _look_user_path(self):
        print("Path >> ")
        if self.user_path != []:
            dirs = " / ".join(self.user_path)
            print(dirs)
        else:
            print("ROOT")

    def _open_root_dir(self):
        os.startfile(os.path.realpath(self.data.BLOG_MD_CONTENT_ROOT))
        print("open blog markdown dir")