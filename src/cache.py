import os
import tempfile
import datetime


# when using optimizeCaching on cache_directory_paths_of_path function, it won't
# cache again until X days later from file modification date.
RECACHE_AFTER_DAYS = 5


# Writes(caches) directory names of the given path into tmp file
# optimizeCaching if be true it caches file if not cached recently and tmp file not be empty.
def cache_directory_paths_of_path(path, optimizeCaching=False):
    if optimizeCaching:
        cachedFilePath = generate_file_path(path)
        if cached_recently(cachedFilePath) and os.stat(cachedFilePath).st_size != 0:
            return

    cacheFilePath = generate_file_path(path)

    with open(cacheFilePath, "w") as file:
        for itemPath in os.walk(path):
            if os.path.isfile(itemPath[0]):
                continue

            directoryPath = itemPath[0]
            from . import utils

            if not utils.path_is_valid(directoryPath):
                continue

            file.write(directoryPath + "\n")


def cached_recently(cachedFilePath):
    if not os.path.exists(cachedFilePath):
        return False

    modifiedDate = datetime.datetime.fromtimestamp(os.path.getmtime(cachedFilePath))
    cacheAfterDate = datetime.datetime.today() + datetime.timedelta(
        days=RECACHE_AFTER_DAYS
    )

    return modifiedDate < cacheAfterDate


def get_cache_file(path):
    filePath = generate_file_path(path)
    if not os.path.exists(filePath):
        return []
    return open(filePath, "r")


def generate_file_name(path):
    return path.replace("/", ".").strip(".") + ".tmp"


def generate_file_path(path):
    return tempfile.gettempdir() + "/" + generate_file_name(path)
