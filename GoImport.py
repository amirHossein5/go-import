import sublime
import sublime_plugin
from . import utils


class GoImportCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if "Go" not in self.view.syntax().name:
            return

        words = utils.filter_imported_words(
            self.view, utils.get_words(self.view)
        )

        if len(words) == 0:
            sublime.status_message("GoImport: already imported.")
            return

        words = utils.get_full_word_names(self.view, words)

        if len(words) == 0:
            sublime.status_message("GoImport: keyword not found")
            return

        utils.import_words(self.view, edit, words)
        sublime.status_message("GoImport: imported!")


class GoImportEraseUnusedCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if "Go" not in self.view.syntax().name:
            return

        unusedWords = utils.get_unused_words(
            self.view, get_imported_words(self.view)
        )

        if len(unusedWords) == 0:
            sublime.status_message("GoImport: no unused import found.")
            return

        utils.erase_imports(self.view, edit, unusedWords)
        sublime.status_message("GoImport: erased!")
