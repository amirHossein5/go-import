import sublime
import sublime_plugin
import os
from . import paths
from . import utils
from . import cache


def plugin_loaded():
    GOROOT = paths.get_GOROOT() + "/src"
    GOMODCACHE = paths.get_GOMODCACHE() + "/cache/download"

    for path in [GOROOT, GOMODCACHE]:
        if path == "" or not os.path.exists(path):
            return
        cache.cache_directory_paths_of_path(path)


class GoImportCommand(sublime_plugin.TextCommand):
    def run(self, edit, args=None):
        if "Go" not in self.view.syntax().name:
            return

        if args and "words" in args:
            utils.import_words(self.view, edit, args["words"])
            return

        words = utils.filter_imported_words(self.view, utils.get_words(self.view))

        if len(words) == 0:
            sublime.status_message("GoImport: already imported.")
            return

        words = utils.get_full_word_names(self.view, self.get_searchable_paths(), words)

        if len(words) == 0:
            sublime.status_message("GoImport: keyword not found")
            return

        absoluteWords = [w for w in words if isinstance(w, str)]
        utils.import_words(self.view, edit, absoluteWords)
        sublime.status_message("GoImport: imported!")

        self.importList = [w for w in words if not isinstance(w, str)]
        self.show_quick_panel()

    # User selects intended import from panel
    def show_quick_panel(self):
        if len(self.importList) == 0:
            return
        sublime.active_window().show_quick_panel(
            self.importList[0], self.user_selected_import
        )

    def user_selected_import(self, index):
        if index == -1:
            return
        if len(self.importList) == 0:
            return

        self.view.run_command(
            "go_import", {"args": {"words": [self.importList[0][index]]}}
        )
        self.importList.pop(0)

        if len(self.importList) != 0:
            self.show_quick_panel()

    # Returns paths for searching import keywords
    def get_searchable_paths(self):
        searchablePaths = [
            utils.get_currect_project_path(self.view),
            paths.get_GOROOT() + "/src",
            paths.get_GOMODCACHE() + "/cache/download",
        ]
        return [p for p in searchablePaths if p]


class GoImportEraseUnusedCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if "Go" not in self.view.syntax().name:
            return

        unusedWords = utils.get_unused_words(
            self.view, utils.get_imported_words(self.view)
        )

        if len(unusedWords) == 0:
            sublime.status_message("GoImport: no unused import found.")
            return

        utils.erase_imports(self.view, edit, unusedWords)
        sublime.status_message("GoImport: erased!")
