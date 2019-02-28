import sublime
import sublime_plugin


class PyReplCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.window().run_command('set_layout', {
            "cols": [0.0, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1]]
        })
        view.window().run_command('build')
        # segment 1 and 2 are equivalent but segment 1 changes original view's focus
        # after moving repl to new group
        # segment 1
        # view.window().run_command('carry_file_to_pane', {"direction": "right"})
        # segment 2
        view.window().run_command('travel_to_pane', {"direction": "right"})
        view.window().run_command('travel_to_pane', {"direction": "left"})
        view.window().run_command('move_to_neighboring_group')
        screen_fraction = 1 / (view.window().num_groups())
        view.window().run_command('zoom_pane', {"fraction": screen_fraction})
