import sublime
import os


# Returns path of go standard library
def get_std_library_path():
    return get_GOROOT() + '/src'

def get_GOROOT():
    GOROOT = ""

    settings = sublime.load_settings("GoImport.sublime-settings")
    GOROOT = settings.get("GOROOT")

    if not GOROOT or GOROOT == "":
        return "/usr/lib/go"
    return os.path.expanduser(GOROOT).rstrip("/")


def get_GOMODCACHE():
    GOMODCACHE = ""

    settings = sublime.load_settings("GoImport.sublime-settings")
    GOMODCACHE = settings.get("GOMODCACHE")

    if not GOMODCACHE or GOMODCACHE == "":
        return "~/go/pkg/mod"
    return os.path.expanduser(GOMODCACHE).rstrip("/")
