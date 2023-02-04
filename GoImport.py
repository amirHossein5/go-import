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

        words = utils.get_full_word_names(
            self.view, self.get_searchable_paths(), words
        )

        if len(words) == 0:
            sublime.status_message("GoImport: keyword not found")
            return

        utils.import_words(self.view, edit, words)
        sublime.status_message("GoImport: imported!")

    # Returns paths for searching import keywords
    def get_searchable_paths(self):
        paths = [
            utils.get_currect_project_path(self.view),
            get_GOROOT().rstrip('/')+'/src',
            get_GOMODCACHE().rstrip('/')+'/cache/download',
        ]
        return [p for p in paths if p]


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


def get_GOROOT():
    GOROOT = ''

    settings = sublime.load_settings('GoImport.sublime-settings')
    GOROOT = settings.get('GOROOT')

    if not GOROOT or GOROOT == '':
        return "/usr/lib/go"
    return GOROOT


def get_GOMODCACHE():
    GOMODCACHE = ''

    settings = sublime.load_settings('GoImport.sublime-settings')
    GOMODCACHE = settings.get('GOMODCACHE')

    if not GOMODCACHE or GOMODCACHE == '':
        return "~/go/pkg/mod"
    return GOMODCACHE
