import vlc
import time

RADIO_URL = "http://stream.radioparadise.com/mp3-192"

instance = vlc.Instance()
player = instance.media_player_new()

media = instance.media_new(RADIO_URL)
player.set_media(media)

print('Starting playback')
player.play()

# Wait for the stream to initialize
time.sleep(2)

# Keep the program alive to listen
input("Press Enter to stop...\n")
player.stop()