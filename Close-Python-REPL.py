import sublime
import sublime_plugin


class ClosePyReplCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        # print(view.name())
        sheet = view.window().active_sheet()
        if view.window().num_groups() == 2:
            returnWindow = view.window().get_sheet_index(sheet)[1]
            # print("returnWindow = %s" % (returnWindow))
            view.window().run_command('focus_group', {
                "group": 1
            })
            view.window().run_command('set_layout', {
                "cols": [0.0, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1]]
            })
            close_all_sublime_pythons()
            # view.window().run_command('close')
            view.window().run_command(
                'select_by_index', {"index": returnWindow})


def close_all_sublime_pythons():
    import os

    def process_list():

        class Process():
            def __init__(self, name, pid, ppid):
                self.name = name
                self.pid = pid
                self.ppid = ppid
                self.parent = None
                self.children = []

            def kill(self):
                try:
                    os.kill(self.pid, 9)
                    print('Process %s killed' % (self.pid))
                except:
                    print('Could not kill process %s' % (self.pid))

        process_map = [
            [
                entry
                for entry
                in line.split(' ') if entry.strip()
            ]
            for line
            in os.popen(
                'wmic process get Caption,ParentProcessId,ProcessId'
            ).readlines()
            if line.strip()
        ]
        processes = [
            Process(name=' '.join(line[:-2]),
                    pid=int(line[-1]),
                    ppid=int(line[-2]))
            for line
            in process_map[1:]
        ]
        for process in processes:
            if process.ppid != process.pid:
                parents = [
                    parent for parent in processes
                    if parent.pid == process.ppid
                ]
                if len(parents) > 1:
                    raise Exception('Error with finding parent process:\n'
                                    'More than 1 parent process found:\n'
                                    '%s' % ([err.__dict__ for err in parents]))
                elif len(parents) == 1:
                    process.parent = parents[0]
                    process.parent.children.append(process)

        return processes

    def find_processes(tree, name=None, pid=None):
        if name and pid:
            return [
                process for process in tree
                if process.name == name and process.pid == pid
            ]
        elif name:
            return [
                process for process in tree
                if process.name == name
            ]
        elif pid:
            return [
                process for process in tree
                if process.pid == pid
            ]
        else:
            return [process for process in tree]

    sublime_apps = find_processes(
        tree=process_list(), name='sublime_text.exe'
    )
    for sublime_app in sublime_apps:
        plugin_hosts = find_processes(
            tree=sublime_app.children, name='plugin_host.exe'
        )
        for plugin_host in plugin_hosts:
            pythons = find_processes(
                tree=plugin_host.children, name='python.exe'
            )
            for python in pythons:
                print('Closing:\n'
                      '%s' % (python))
                python.kill()
