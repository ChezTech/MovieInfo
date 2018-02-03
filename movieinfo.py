import sys
import os
import re
from collections import namedtuple

MovieInfo = namedtuple("MovieInfo", "title originalTitle releaseDate")

def getMovieNames(path=None):
    if not os.path.isdir(path):
        print(f"Can't find folder: {path}")
        sys.exit()

    # movieNameList = os.listdir(folder)
    # print(movieNameList)

    with os.scandir(path) as it:
        for entry in it:

            print(f"\nChecking {entry.name}...")
            # print(entry.path)

            if alreadyHasYearInName(entry.name):
                print("   already has a year")
                continue

            mainMovieName = getMainMovieName(entry.name)
            print(f"   main movie name: {mainMovieName}")

            movieInfo = fetchMovieInfo(mainMovieName)
            print(f"   info: {movieInfo.title}, {movieInfo.originalTitle}, {movieInfo.releaseDate}")

    
def getMainMovieName(movieName):
    # Trim the movie name down to just the main part of the name
    # up until a '-', '[', '(', or the extension
    # if no match, then the whole movieName
    match = re.search(r'(.*?)(?=\s*[([.-])|(.+)', movieName)
    # if match:
    #     print(f"**{match.group()}**")
    # else:
    #     print(f"##{movieName}##")
    return match.group()
    

def fetchMovieInfo(movieName):
    
    return MovieInfo(title="aTitle", originalTitle="origTitle", releaseDate="2018-01-01")

def alreadyHasYearInName(movieName):
    # See if the name has a 4 digit year in parentheses
    # E.g. "Bull Durham (1988).mkv"
    return re.search(r'[(]\d{4}[)]', movieName)
    # match = re.search('[(]\d{4}[)]', movieName)
    # year = match.group()


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args)==0:
        print("Enter a directory to scan.")
        sys.exit()

    # Scan the folder, get a list of files
    getMovieNames(args[0])

    # Lookup those files to find a movie match

if __name__ == "__main__":
    main()
