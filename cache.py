import os

def cache_directory_paths_of_path(path):
    cacheFilePath = generate_file_path(path)

    with open(cacheFilePath, 'w') as file:
        for itemPath in os.walk(path):
            if os.path.isfile(itemPath[0]):
                continue

            directoryPath = itemPath[0]
            if "/testdata" in directoryPath:
                continue

            file.write(directoryPath+"\n")


def get_cache_file(path):
    filePath = generate_file_path(path)
    if not os.path.exists(filePath):
        return []
    return open(filePath, 'r')


def generate_file_name(path):
    return path.replace('/', '.').strip('.')+'.cache'


def generate_file_path(path):
    return os.path.dirname(__file__)+'/'+generate_file_name(path)
