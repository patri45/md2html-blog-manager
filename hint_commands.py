class Hint:
    def __init__(self):
        self.CMD = ":"
        self.abbr_commands={"?":self._hint_search,
                            ">": self._hint_enter,
                            "/": self._hint_open,
                            "+": self._hint_add,
                            }

    def run(self,user_input:str):
        c=user_input.lower()

        if len(c)>1:
            abbr_cmd=c[1:]
            if abbr_cmd in self.abbr_commands:
                self.abbr_commands[abbr_cmd]()
        else:
            self._hint_basic()

    def _print_hints(self,print_data:dict):
        fmt = "{:<4} {:<25} {:<4} {:<25}"
        c_0 = ""
        c_0_hint = ""
        c_1 = ""
        c_1_hint = ""
        data_length=len(print_data.keys())
        i=0
        counter = 0
        for c, c_hint in print_data.items():
            if counter == 0 and i==data_length-1:
                print("{:<4} {:<25}".format(c,c_hint))
            if counter == 0:
                c_0 = c
                c_0_hint = c_hint
                counter += 1
            elif counter == 1:
                c_1 = c
                c_1_hint = c_hint
                print(fmt.format(c_0, c_0_hint, c_1, c_1_hint))
                counter = 0
            i+=1

    def _hint_basic(self):
        HINTS={"<E>": "cancel input",
                "q": "quit software",
                "c": "clear screen",
                "ll": "look files in user path",
                "l": "look user path",
                "la": "look structure",
                "l1": "look themes",
                "l2": "look topics",
                "l3": "look titles",
                "r": "open root dir",
                }
        self._print_hints(HINTS)


    def _hint_search(self):
        HINTS={"?": "search all",
                "?1.": "search themes",
                "?2.": "search topics",
                "?3.": "search titles",
                }
        self._print_hints(HINTS)

    def _hint_enter(self):
        HINTS={">": "enter dir by path",
               ">..": "back to p-parent dir",
               ">.": "back to parent dir",
               ">?": "enter got dir",
               ">l.": "enter local dir",
               ">1.": "enter theme",
               ">2.": "enter topic",
                }
        self._print_hints(HINTS)

    def _hint_open(self):
        HINTS={"/": "open file by path",
               "/?": "open got file",
               "/l.": "open local file",
               "/3.": "open title",
                }
        self._print_hints(HINTS)

    def _hint_add(self):
        HINTS={"+": "add file by path",
               "+f.": "force add file",
               "+l.": "add file in local dir",
                }
        self._print_hints(HINTS)
