import os
import requests
import json

# Define the root directory
root_dir = "./"

# Loop through all subfolders and files
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        # Check if the file is named "metadata.txt"
        if file == "metadata.txt":
            # Read the track IDs and filenames from the file
            with open(os.path.join(subdir, file), "r") as f:
                lines = f.readlines()

            track_info = []
            for line in lines:
                if not line.startswith("#"):
                    track_id, filename = line.split()[0], line.split("# from file: ")[1].strip()
                    track_info.append((track_id, filename))

            # Make requests for each track ID
            for track_id, filename in track_info:
                print(f"Fetching info for track {track_id}...")
                url = f"https://amp-api.music.apple.com/v1/catalog/us/songs/{track_id}"
                headers = {
                    "User-Agent": "iPhone",
                    "Media-User-Token": "YOUR AUTH HERE",
                    "Authorization": "Bearer YOUR AUTH HERE"
                }
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    track_info = response.json()["data"][0]
                    track_number = track_info["attributes"]["trackNumber"]
                    track_name = track_info["attributes"]["name"]
                    print(f"Track {track_id}: {track_number}. {track_name}")
                    lyrics_url = f"https://amp-api.music.apple.com/v1/catalog/nz/songs/{track_id}/lyrics"
                    lyrics_response = requests.get(lyrics_url, headers=headers)

                    if lyrics_response.status_code == 200:
                        # Write the lyrics content to a file named after the track number and name in the same folder
                        with open(os.path.join(subdir, f"{track_number}. {track_name}.json"), "w") as f:
                            json.dump(lyrics_response.json(), f, indent=4)
                    else:
                        print(f"Lyrics not found for track {track_id}")
                else:
                    print(f"Track info not found for track {track_id}")
