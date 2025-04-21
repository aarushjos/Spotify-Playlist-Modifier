import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENT_ID",
                                               client_secret="YOUR_CLIENT_SECRET",
                                               redirect_uri="http://localhost:1234",
                                               scope="playlist-modify-public playlist-modify-private user-top-read"))


def get_top_tracks(limit,time_range):
    tracks=[]
    for offset in range(0,limit,50):
        result=sp.current_user_top_tracks(50,offset,time_range)
        tracks.extend([item["id"] for item in result["items"]])
    return tracks

def get_all_tracks(playlist_id):
    tracks=[]
    offset=0
    while True:
        results=sp.playlist_items(playlist_id,limit=100,offset=offset)
        items=results["items"]
        if not items:
            break
        tracks.extend(items)
        offset+=len(items)
    return tracks

def remove_tracks(sp,playlist_id,remove_uris):
    if remove_uris:
        for i in range(0, len(remove_not_in_top), 100):
            sp.playlist_remove_all_occurrences_of_items(playlist_id, remove_not_in_top[i:i+100])
        print(f"✅ Removed {len(remove_not_in_top)} tracks.")
    else:
        print("No tracks to remove.")


playlist_id="YOUR_PLAYLIST_ID"
all_tracks=get_all_tracks(playlist_id)
top_tracks=get_top_tracks(2000,time_range='long_term')
all_tracks.sort(key=lambda  x:x["added_at"],reverse=True)

x=int(input("How many recently added tracks do u wanna keep?"))

tracks_to_keep=all_tracks[:x]
tracks_to_remove=all_tracks[x:]
remove_tracks(sp,playlist_id,tracks_to_remove)

#BACKUP OF REMOVED TRACKS
import json

# Backup file name
backup_file = "removed_tracks_backup.json"

# Store removed track info before deleting
removed_tracks_info = [{"name": track["track"]["name"], "uri": track["track"]["uri"]} for track in tracks_to_remove]

# Save to a file
with open(backup_file, "w") as f:
    json.dump(removed_tracks_info, f, indent=4)

print(f"Backup created! {len(removed_tracks_info)} tracks saved in {backup_file}.")

remove_uris=[item["track"]["uri"] for item in tracks_to_remove if item["track"]]

# #REMOVED ALL TRACKS ONLY KEEPING 387 RECENT ONES
remove_tracks(sp,playlist_id,remove_uris)


#REMOVES ALL THE TRACKS FROM 200-387 NOT IN MY MOST LISTENED TO
remove_not_in_top=[]
for i in range(0,int(x)):
    track_data=all_tracks[i]["track"]
    track_name=track_data["name"]
    track_id=track_data["id"]
    track_uri=track_data["uri"]

    if track_id not in top_tracks:
        print(f"Tracks to be removed:\n{track_name}: {track_uri}")
        remove_not_in_top.append(track_uri)

remove_tracks(sp,playlist_id,remove_not_in_top)

