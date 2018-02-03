import sys
import os
import re

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

            # if alreadyHasYearInName(entry.name):
            #     print("   already has a year")
            #     continue

            getMainMovieName(entry.name)

    
def getMainMovieName(movieName):
    # Trim the movie name down to just the main part of the name
    # up until a '-', '[', '(', or the extension
    match = re.search(r'(.*?)(?=\s*[([.-])|(.+)', movieName)
    if match:
        print(f"**{match.group()}**")
    else:
        print(f"##{movieName}##")
    

def fetchMovieInfo(movieName):
    pass

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
