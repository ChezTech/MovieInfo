# MovieInfo
Adds info about movies

# Purpose
I have a bunch of movies in folders. I didn't put the year in the filenames. This is handy for all the various media organizers out there.

I didn't want to take the 30 min to do it manually, so I figured I'd spend a few horus to write an app that'd do it for me automatically.

So this app/script will list all the filenames in a folder, go out to https://www.themoviedb.org to get the year for that movie and append the year to the filename.

E.g. `"Bull Durham.mkv"` ==> `"Bull Durham (1988).mkv"`

# Development Environment
Here's what I'm using, should work anywhere.
* Windows 10
* VS Code 64-bit
  * Python extension
* Python 3.6.4
  * `pip install requests`
