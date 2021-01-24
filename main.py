import tool,database
import basic_commands,hint_commands,search_commands,enter_commands,open_commands,add_commands
from sys_exceptions import Quit,Cancel

class BlogManager:
    def __init__(self):
        self.tool = None
        self.data = None
        self.basic_cmds=None
        self.hint_cmds=None
        self.search_cmds=None
        self.enter_cmds=None
        self.add_cmds=None

        self.user_input = ""
        self.user_path = []
        self.user_got_file_path = ""

    def _initialize(self):
        self.tool = tool.Tool()
        self.data = database.DataBase()
        self.data.load()
        self.basic_cmds = basic_commands.BasicCommands(self.data)
        self.hint_cmds = hint_commands.Hint()
        self.search_cmds = search_commands.Search(self.data)
        self.enter_cmds = enter_commands.Enter(self.data)
        self.open_cmds = open_commands.Open(self.data)
        self.add_cmds = add_commands.Add(self.data)

    def run(self):
        self._initialize()

        self.basic_cmds._look_content_structure()
        print()
        print("Blog Manager start...")
        try:
            while True:
                try:
                    self._input_command("请输入指令:")
                except Cancel:
                    pass
                print()
        except Quit:
            print("Blog Manager closed...")

    def _input_command(self, prompt):
        self.user_input = input(prompt)
        c = self.user_input.lower()
        if c in self.basic_cmds.CMDS:
            self.user_path=self.basic_cmds.run(self.user_input,self.user_path)
        elif c[0] == self.hint_cmds.CMD:
            self.hint_cmds.run(self.user_input)
        elif c[0] == self.search_cmds.CMD:
            result=self.search_cmds.run(self.user_input)
            if result!="":
                self.user_got_file_path=result
            #print(self.user_got_file_path)
        elif c[0] == self.enter_cmds.CMD:
            self.user_path = self.enter_cmds.run(self.user_input,self.user_path,self.user_got_file_path)
            #print(self.user_path)
        elif c[0] == self.open_cmds.CMD:
            self.open_cmds.run(self.user_input, self.user_path, self.user_got_file_path)
        elif c[0] == self.add_cmds.CMD:
            self.add_cmds.run(self.user_input, self.user_path)
        else:
            print("no command...")

blogManager = BlogManager()
blogManager.run()
