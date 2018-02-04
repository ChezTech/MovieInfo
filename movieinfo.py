import sys
import os
import re
from collections import namedtuple
import secrets
import requests
import json
import functools

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

            mainMovieName, movieNameSuffix = getMovieNameParts(entry.name)
            print(f"   main movie name: {mainMovieName} suffix: {movieNameSuffix}")

            movieInfo = fetchMovieInfo(mainMovieName)
            if movieInfo is None:
                continue

            print(f"   info: {movieInfo.title}, {movieInfo.originalTitle}, {movieInfo.releaseDate}")

            newName = getNewName(movieInfo, movieNameSuffix)
            print(f"   {newName}")


def getNewName(movieInfo, movieNameSuffix):
    year = movieInfo.releaseDate[0:4]
    return f"{movieInfo.title} ({year}){movieNameSuffix}"


def getMovieNameParts(movieName):
    """Get the main movie name, as well as the remaining parts"""

    # Trim the movie name down to just the main part of the name
    # up until a '-', '[', '(', or the extension
    # if no match, then the whole movieName
    match = re.search(r'(.*?)(?=\s*[([.-])|(.+)', movieName)
    # if match:
    #     print(f"**{match.group()}**")
    # else:
    #     print(f"##{movieName}##")
    mainName = match.group()
    suffixName = movieName[len(mainName):]

    return mainName, suffixName


@functools.lru_cache(maxsize=500)
def fetchMovieInfo(movieName):
    url = "https://api.themoviedb.org/3/search/movie"

    payload = {"api_key": secrets.apiKey, "query": movieName}

    response = requests.request("GET", url, params=payload)

    if (response.status_code != 200):
        print(f"   ***Unable to get info for: {movieName}")
        print(f"   Status Code: {response.status_code}")
        print(response.headers)
        return None

    # print(response.text)

    return findNameMatch(movieName,  response.json()['results'])


def doesMovieMatch(o, movieName):
    if movieName == o["title"]:
        return True
    if movieName == o["original_title"]:
        return True
    return False


def findNameMatch(movieName, results):
    matchedNames = list(filter(lambda o: doesMovieMatch(o, movieName), results))
    infos = list(map(lambda o: MovieInfo(title=o["title"], originalTitle=o["original_title"], releaseDate=o["release_date"]), matchedNames))

    if len(infos) == 1:
        return infos[0]

    if len(infos) > 1:
        for info in infos:
            print(f"   possibility: {info.title}, {info.originalTitle}, {info.releaseDate}")

    # TODO: looser movie match, maybe just name contains, or check popularity, or vote_count?

    return None


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
