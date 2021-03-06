import sublime, sublime_plugin
import os
from . import converter


def _open_file(window, filename):
    if window.num_groups() > 1:
        window.focus_group((window.active_group() + 1) % window.num_groups())

    window.open_file(filename)


class OpenRelatedCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        current_file = view.file_name()
        found = False
        non_existing_files = []

        settings = view.settings()
        plugin_settings = settings.get('open_related', {})

        for patterns in plugin_settings.get('patterns', []):
            for file in converter.create(patterns, sublime.platform()).convert(current_file):
                if os.path.exists(file):
                    _open_file(self.window, file)
                    found = True
                else:
                    non_existing_files.append(file)
            if found:
                return

        if non_existing_files and plugin_settings.get('create_new_if_not_exist', False):
            file_path = non_existing_files[0]
            directory, filename = os.path.split(file_path)
            try:
                os.makedirs(directory)
            except OSError:
                if not os.path.isdir(directory):
                    raise
            _open_file(self.window, file_path)

        sublime.status_message("Cannot find related file!")

    def is_enabled(self):
        view = self.window.active_view()
        return bool(view and view.file_name())

    def description(self):
        return "Open related file."
