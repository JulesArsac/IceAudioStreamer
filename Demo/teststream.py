import sys

import Ice
import vlc
import YourModule

class AudioStreamI(YourModule.AudioStream_ice):
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new("morshu.mp3")
        print("init done")

    def play_audio(self):
        self.player.set_media(self.media)
        self.player.play()

class Server(Ice.Application):
    def run(self, argv):
        print("start run")
        adapter = self.communicator().createObjectAdapterWithEndpoints("AudioStreamAdapter", "default -p 10000")
        audio_stream = AudioStreamI()
        adapter.add(audio_stream, self.communicator().stringToIdentity("AudioStream"))
        adapter.activate()
        self.communicator().waitForShutdown()

if __name__ == "__main__":
    app = Server()
    sys.exit(app.main(sys.argv))
