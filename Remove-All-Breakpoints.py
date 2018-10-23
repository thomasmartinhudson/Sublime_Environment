import sublime
import sublime_plugin


class RemoveAllBreakpointsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        # print ("Function Running")
        Instance_Count = len(view.find_all('import pdb'))+1
        for i in range(1, Instance_Count):
            # print ("Removing Breakpoint %s" % (i))
            # print ("%s" % (view.line(view.find('import pdb; pdb.set_trace\(\)',0))))
            # print ("Removing Data from %s" % (view.line(view.find('import pdb; pdb.set_trace\(\)',0))))
            self.view.erase(edit, view.full_line(
                view.find('import pdb', 0)))
            self.view.erase(edit, view.full_line(
                view.find('pdb.set_trace\(\)', 0)))
