import re
import os
from . import cache
from . import paths

parantheseImportRegex = r"import.*\((.|\n)*?\)"
qouteImportRegex = r"import.*\"(.*)\""


# Get import key words by active cursors
def get_words(view):
    words = []

    for cursor in view.sel():
        word = view.substr(view.word(cursor)).strip()
        if bool(re.match("^[a-zA-Z0-9]+$", word)):
            words.append(word)

    return words


# e.g, utf8 to unicode/utf8 based on given paths
def get_full_word_names(view, searchablePaths, words):
    fullWordNames = []
    currentProjectPath = get_currect_project_path(view)

    for w in words:
        fullWord = full_word_name(view, w, searchablePaths)
        if not fullWord:
            continue

        if isinstance(fullWord, str):
            fullWord = fullWord.strip("/")
        else:
            for i, w in enumerate(fullWord):
                fullWord[i] = w.strip("/")

        fullWordNames.append(fullWord)

    return fullWordNames


# Full import name(s): e.g, utf8 to unicode/utf8, fmt to fmt, based on given paths
# If coundn't find word in given paths returns False
# Returns array if finds multiple modules with same name
# Returns string if finds a module name
# Returns false if no module found
def full_word_name(view, word, paths):
    currentProjectPath = get_currect_project_path(view)
    paths = [
        os.path.expanduser(p) for p in paths if p != "" and p != currentProjectPath
    ]
    fullWords = []

    words = check_full_word_name_recursive_in_path(
        view, word, currentProjectPath, currentProjectPath
    )
    if len(words) != 0:
        fullWords += words

    for path in paths:
        words = check_full_word_name_in_cache(view, word, path, currentProjectPath)
        if len(words) != 0:
            fullWords += words
            if len(fullWords) == 1:
                return fullWords[0]
            return fullWords

    for path in paths:
        words = check_full_word_name_recursive_in_path(
            view, word, path, currentProjectPath
        )
        if len(words) != 0:
            fullWords += words
            if len(fullWords) == 1:
                return fullWords[0]
            return fullWords

    return False


# Checks for full word name in cached file
def check_full_word_name_in_cache(view, word, path, currentProjectPath):
    words = []

    for itemPath in cache.get_cache_file(path):
        itemPath = itemPath.strip()

        if not os.path.exists(itemPath):
            continue

        directoryPath = itemPath

        if "/testdata" in directoryPath or "vendor/" in directoryPath:
            continue

        directory = directoryPath.replace(path.rstrip("/") + "/", "")
        directory = re.sub("@.*$", "", directory)

        if word != directory.split("/")[-1]:
            continue

        moduleName = get_project_module_name_if_in_path(view, path)

        if moduleName != "":
            words.append(moduleName + "/" + directory.replace(path.rstrip("/"), ""))
            continue

        words.append(directory)

    return words


# Checks for full word name in path non recursively
def check_full_word_name_in_path(view, word, path, currentProjectPath):
    for item in os.listdir(path):
        if os.path.isfile(item):
            continue

        directory = item

        if word != directory:
            continue

        moduleName = get_project_module_name_if_in_path(view, path)

        if moduleName != "":
            return moduleName + "/" + word

        return word

    return ""


# Checks for full word name in path recursively
# Returns array of name(s)
def check_full_word_name_recursive_in_path(view, word, path, currentProjectPath):
    words = []

    for itemPath in os.walk(path):
        if os.path.isfile(itemPath[0]):
            continue

        directoryPath = itemPath[0]

        if "/testdata" in directoryPath or "vendor/" in directoryPath:
            continue

        directory = directoryPath.replace(path.rstrip("/") + "/", "")
        directory = re.sub("@.*$", "", directory)

        if word != directory.split("/")[-1]:
            continue

        moduleName = get_project_module_name_if_in_path(view, path)

        if moduleName != "":
            words.append(moduleName + "/" + directory.replace(path.rstrip("/"), ""))
            continue

        words.append(directory)

    return words


# if path is opened project, return project module name
def get_project_module_name_if_in_path(view, path):
    currentProjectPath = get_currect_project_path(view)

    if currentProjectPath not in path:
        return ""

    return get_project_module_name(currentProjectPath)


# Returns opened project path
def get_currect_project_path(view):
    sublimeVariables = sublime_variables(view)

    if "folder" in sublimeVariables:
        return sublimeVariables["folder"]
    return ""


# Returns sublimetext env variables
def sublime_variables(view):
    return view.window().extract_variables()


# Removes words that are already imported.
def filter_imported_words(view, words):
    if not has_import_key_word(view):
        return words

    filteredWords = []
    importedWords = get_imported_words(view)

    for word in words:
        isAlreadyImported = False

        for importedWord in importedWords:
            if word == importedWord.split("/")[-1]:
                isAlreadyImported = True
            else:
                isAlreadyImported = isAlreadyImported or False

        if not isAlreadyImported:
            filteredWords.append(word)

    return filteredWords


# Append given words to imports
def import_words(view, edit, words):
    if len(words) == 0:
        return

    if has_import_key_word(view):
        words += get_imported_words(view)

    page_imports(view, edit, words)


# Pages imports these words
def page_imports(view, edit, words):
    words = unique(words)
    packageViewRegion = view.find("package.*$", 0)
    packageStatement = view.substr(packageViewRegion)

    remove_all_imports(view, edit)

    if len(words) == 0:
        return

    replacable = packageStatement + "\n\n" + get_import_string(words)
    view.replace(edit, packageViewRegion, replacable)


# Returns region of import in page
def get_import_view_region(view):
    return view.find(qouteImportRegex, 0) or view.find(parantheseImportRegex, 0)


# Removes all of the imported keywords of page
def remove_all_imports(view, edit):
    if not has_import_key_word(view):
        return

    replaceViewRegion = get_import_view_region(view)
    packageStatement = view.substr(view.find("package.*$", 0))
    view.replace(edit, replaceViewRegion, "")
    view.replace(edit, view.find("package.*\n\n", 0), packageStatement)


# Returns a string of imports
def get_import_string(words):
    importString = ""

    if len(words) == 0:
        return importString
    elif len(words) == 1:
        importString += 'import "' + words[0] + '"'
    else:
        words = separate_imports(words)
        importString += "import ("
        for w in words:
            if w == "":
                importString += "\n"
            else:
                importString += '\n\t"' + w + '"'
        importString += "\n)"

    return importString


# separetes imports of standard go library from another places
def separate_imports(words):
    GOROOT = paths.get_GOROOT() + "/src"
    standardLibs = []
    anotherLibs = []

    for w in words:
        if os.path.isdir(GOROOT + "/" + w):
            standardLibs.append(w)
        else:
            anotherLibs.append(w)

    standardLibs.sort()
    anotherLibs.sort()

    if len(standardLibs) == 0:
        return anotherLibs
    if len(anotherLibs) == 0:
        return standardLibs

    return standardLibs + [""] + anotherLibs


# Get project module name based on go.mod
def get_project_module_name(projectPath):
    path = os.path.expanduser(projectPath)
    goModPath = path + "/" + "go.mod"

    if not (os.path.exists(goModPath) and os.path.isfile(goModPath)):
        return ""

    with open(goModPath, "r") as f:
        line = f.readline()
        if bool(re.match("module.*", line)):
            return re.findall("module.*", line)[0].split(" ")[-1]

    return ""


# Get imported words of page
def get_imported_words(view):
    if not has_import_key_word(view):
        return []

    importString = view.substr(get_import_view_region(view))

    words = re.findall(r"\"(.+)\"", importString)
    if "import" in words:
        words.remove("import")

    return words


# Determine page has any importes
def has_import_key_word(view):
    return bool(view.find("import", 0))


# Removes specified import keywords from page
def erase_imports(view, edit, unusedWords):
    if len(unusedWords) == 0:
        return

    remainedWords = []
    imported_words = get_imported_words(view)

    for iw in imported_words:
        if iw not in unusedWords:
            remainedWords.append(iw)

    page_imports(view, edit, remainedWords)


# Returns unused specified import keywords
def get_unused_words(view, words):
    unusedWords = []

    for fullWord in words:
        w = fullWord
        if "/" in w:
            w = fullWord.split("/")[-1]
        regions = view.find_all(w + "\.", 0)

        if len(regions) == 0:
            unusedWords.append(fullWord)
            continue

        found = False

        for region in regions:
            line = view.substr(view.line(region))
            if "//" in line:
                found = found or False
            elif "import " in line:
                found = found or False
            elif '"' + w in line:
                found = found or False
            else:
                found = True

        if not found:
            unusedWords.append(fullWord)

    return unusedWords


# Unique items of the list
def unique(listArg):
    return list(set(listArg))


# path does not contain testdata or vendor or ...
def path_is_valid(path):
    notValids = [
        "/testdata",
        "vendor/",
        'cache/download',
    ];

    for notValid in notValids:
        if notValid in path:
            return False

    return True
