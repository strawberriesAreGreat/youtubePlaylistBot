# bot.py
import os
import discord
from dotenv import load_dotenv
import pandas as pd
from urllib.parse import urlparse
import re
#from playlistAdder import addSongsToPlaylist
import playlistAdder
import pickle


limit=10000

def parseSongIDs(msg):

    regEx =(r'(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))')
    url = re.findall(regEx,msg)
    return [x[len(x)-2] for x in url]


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('ytbot'):
        cmd = message.content.split()[1]

        if cmd == 'scan':
          allSongs = []
          def is_command (msg): # Checking if the message is a command call
            if len(msg.content) == 0:
                return False
            elif msg.content.split()[0] == 'scan':
                return True
            else:
                return False
          async for msg in message.channel.history(limit=10000):
            if msg.author != client.user:
                if not is_command(msg):
                    if "https://www.youtube" in msg.content:
                        url = parseSongIDs(msg.content)
                        for i in url:
                            allSongs.append(i)
        ytAddSongs(allSongs)
        await message.channel.send('playlist has been updated: https://youtube.com/playlist?list=PLmkt3aL7fnXVyoZpk2TTrkJEL4sGXU9Ap');



    elif "https://www.youtube" in message.content:
        ytAddSongs(parseSongIDs(message.content))
        await message.channel.send('playlist has been updated: https://youtube.com/playlist?list=PLmkt3aL7fnXVyoZpk2TTrkJEL4sGXU9Ap');


def ytAddSongs(list):
    if os.path.getsize('playlist') > 0:
        with open('playlist','rb') as f:
            playist_ids = pickle.load(f)
    else:
        playist_ids = set();
    for song in list:
        #if song in playist_ids:
            #print ("Song already found in the playlist")
        if song not in playist_ids:
            #print ("Adding song to youtube playlist")
            if __name__ == '__main__':
                youtube = playlistAdder.get_authenticated_service()
                playlistAdder.add_video_to_playlist(youtube,song,"PLmkt3aL7fnXVyoZpk2TTrkJEL4sGXU9Ap")
            playist_ids.add(song)
    with open('playlist', 'wb') as fp:
        pickle.dump(playist_ids, fp)
    print("playlist updated")

client.run(TOKEN)
