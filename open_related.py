import sublime, sublime_plugin
import os.path
from . import converter

class OpenRelatedCommand(sublime_plugin.WindowCommand):
    def run(self):
        win = self.window
        view = win.active_view()
        current_file = view.file_name()
        found = False

        settings = view.settings()
        plugin_settings = settings.get('open_related', {})

        for patterns in plugin_settings.get('patterns', []):
            for file in converter.create(patterns, sublime.platform()).convert(current_file):
                if os.path.exists(file):
                    if win.num_groups() > 1:
                        win.focus_group((win.active_group() + 1) % win.num_groups())
                    self.window.open_file(file)
                    found = True
            if found: return

        sublime.status_message("Cannot find related file !")

    def is_enabled(self):
        return self.window.active_view() != None

    def description(self):
        return "Open related file."
