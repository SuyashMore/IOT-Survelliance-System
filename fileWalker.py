from os import listdir
from os.path import isfile, join


def getFilesIn(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


if __name__=="__main__":
    path = "./static/recVideos/"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    print(f"Only-Files:{files}")
    