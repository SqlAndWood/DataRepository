import os


def main():
    pass


def locateFiles(dl, fileType):

    from os import listdir

    list_of_files = [f for f in listdir(dl) if not f.startswith('.') if not f.startswith('~') if f.endswith(fileType)]

    sorted(list_of_files, key=str.lower)

    return list_of_files


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            if not f.startswith('~'):
                yield f


if __name__ == "__main__":
    main()
