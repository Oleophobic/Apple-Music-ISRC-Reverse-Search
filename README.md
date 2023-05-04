# Apple-Music-ISRC-Reverse-Search for catalog IDs (Track ID.py) - Then get TTML Lyrics from the song ID (Google Lyrics.py)



This is my first script, with the help of AI (Chat GPT &amp; Google BARD)
a python script which allows you to read ALAC files for metadata related to individual track ISRCs
First reads the current folder for .m4a files then reads files for ISRCs, this will then take your Auth and Media Tokens then reverse seacrch for coresponding song IDs
ID's are writen to a text file named metadata.txt with the coresponding file name.
Running Google Lyrics.py will get lyrics in a .json TTML format.

From there other scripts can be made to use Apple Musics extensive API for relevent song or album information 
https://developer.apple.com/documentation/applemusicapi/



Account required, extract Bearer and Media User Token from the we by inspecting cookies.
Place the relevent auths inside the files


This is my first working code ive ever made, feedback if any will be appreciated.
