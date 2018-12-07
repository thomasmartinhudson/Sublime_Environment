import sublime
import sublime_plugin


class ClosePyReplCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # view = self.view
        # # print(view.name())
        # sheet = view.window().active_sheet()
        # if view.window().num_groups() == 2:
        #     returnWindow = view.window().get_sheet_index(sheet)[1]
        #     # print("returnWindow = %s" % (returnWindow))
        #     view.window().run_command('focus_group', {
        #         "group": 1
        #     })
        #     view.window().run_command('set_layout', {
        #         "cols": [0.0, 1.0],
        #         "rows": [0.0, 1.0],
        #         "cells": [[0, 0, 1, 1]]
        #     })
        #     # view.window().run_command('close')
        #     view.window().run_command(
        #         'select_by_index', {"index": returnWindow})

        close_all_sublime_pythons()


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
                    print('Process {}: {} killed'.format(self.pid, self.name))
                except:
                    print('Could not kill process {}: {}'.format(
                        self.pid, self.name))

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

    def kill_descendants(process):
        process_id = process.pid
        process_object = process
        loop_flag = True
        while loop_flag:
            while process_object.children:
                process_object = process_object.children[0]
            process_object.kill()
            process_object = find_processes(tree=process_list(),
                                            pid=process_id)[0]
            if not process_object.children:
                process_object.kill()
                loop_flag = False

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
                kill_descendants(python)
                # console_hosts = find_processes(
                #     tree=python.children, name='conhost.exe'
                # )
                # for console_host in console_hosts:
                #     console_host.kill()
                # gits = find_processes(
                #     tree=python.children, name='git.exe'
                # )
                # for git in gits:
                #     console_hosts = find_processes(
                #         tree=git.children, name='conhost.exe'
                #     )
                #     for console_host in console_hosts:
                #         console_host.kill()
                # python.kill()
