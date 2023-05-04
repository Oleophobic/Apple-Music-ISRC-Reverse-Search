import os
import requests
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4

# function to get the track ID for a given ISRC code using the Apple Music API
def get_track_id(isrc):
    url = "https://api.music.apple.com/v1/catalog/nz/songs"
    headers = {
        "Authorization": "Bearer YOUR AUTH HERE",
        "Media-User-Token": "YOUR AUTH HERE",
        "User-Agent": "iPhone"
    }
    params = {
        "filter[isrc]": isrc
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json().get("data")
        if data:
            track_id = data[0].get("id")
            return track_id
    print(f"Track ID not found for {isrc}")
    return None

# get the current directory
dir_path = os.getcwd()

# loop through each file in the directory and its subdirectories
for root, dirs, files in os.walk(dir_path):
    # check if there are any .m4a files in this directory
    if any(filename.endswith(".m4a") for filename in files):
        # create a text file to write the metadata to in the same folder as the .m4a files
        output_path = os.path.join(root, "metadata.txt")
        with open(output_path, "w", encoding="utf-8") as file:
            for filename in files:
                # check if the file is an ALAC .m4a file
                if filename.endswith(".m4a"):
                    # get the full file path and load the metadata
                    filepath = os.path.join(root, filename)
                    try:
                        audio = EasyID3(filepath)
                    except:
                        try:
                            audio = MP4(filepath)
                        except:
                            print("Error loading metadata for file:", filepath)
                            continue

                    # get the value of the "----:com.apple.iTunes:ISRC:" field
                    if "----:com.apple.iTunes:ISRC" in audio:
                        isrc_value = str(audio["----:com.apple.iTunes:ISRC"][0])
                        # extract the text after "----:com.apple.iTunes:ISRC:b" and remove the "'" symbol from it
                        if "b" in isrc_value:
                            text_after_b = isrc_value.split("b", 1)[1].replace("'", "")
                            # get the track ID for this ISRC code using the Apple Music API
                            track_id = get_track_id(text_after_b)
                            if track_id:
                                # write the track ID to the text file, with a space before the file comment
                                file.write(track_id + " # from file: " + filename)
                                file.write("\n")
                                print(f"Successfully found Track ID for {text_after_b}")
                            else:
                                # write the ISRC code and message to the text file
                                file.write(f"{text_after_b} Track ID not found")
                                file.write("\n")

# print a message indicating that the script has finished running
print("Script has finished running.")
