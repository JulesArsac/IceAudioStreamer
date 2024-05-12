import json
import os.path

import Ice
import sys
import Demo
import sqlite3
import vlc
import socket
from threading import Timer
import threading
from datetime import datetime, timedelta


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        ip_address = s.getsockname()[0]
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None


global localIp
localIp = get_local_ip()


class PrinterI(Demo.Printer):
    global streamingLinks
    streamingLinks = {}
    global playerInstances
    playerInstances = {}
    global clientStates
    clientStates = {}
    global playersAges
    playersAges = {}
    global vlc_instance
    vlc_instance = vlc.Instance('--no-xlib', '--network-caching=0')

    def startStream(self, player):
        player.play()

    def playMusic(self, s, current):
        global streamingLinks
        global playerInstances
        global clientStates
        global vlc_instance
        global playersAges

        print(f"Got request to play {s}")
        con = sqlite3.connect('songs.db')
        cur = con.cursor()
        cur.execute(f"select path from songs where queryName = '{s}'")
        rows = cur.fetchone()
        if rows is None:
            print("Song not found.")
            return None
        path = rows[0]
        con.close()
        clientIp = current.con.getInfo().remoteAddress
        clientIp = clientIp.replace("::ffff:", "")

        print(f"Request from {clientIp}")

        if clientIp not in playersAges:
            playersAges[clientIp] = datetime.now()
        lastPlayerAge = playersAges[clientIp]
        currentTime = datetime.now()
        difference = currentTime - lastPlayerAge
        secondsSinceLastRenew = difference.total_seconds()
        print(f"Seconds since last renew: {secondsSinceLastRenew}")
        if secondsSinceLastRenew > 100:
            print("Renewing player instance")
            player = playerInstances[clientIp]
            t = threading.Thread(target=self.deletePlayerForClient, args=(player, clientIp,))
            t.start()
            playerInstances[clientIp] = vlc_instance.media_player_new()
            playersAges[clientIp] = datetime.now()

        if clientIp not in playerInstances:
            print("Creating new player instance")
            playerInstances[clientIp] = vlc_instance.media_player_new()
        player = playerInstances[clientIp]
        if clientIp not in streamingLinks:
            print("Creating new streaming link")
            streamingLinks[clientIp] = f"rtsp://{get_local_ip()}:8554/{clientIp}"
        url = streamingLinks[clientIp]
        media = vlc_instance.media_new_path(path)
        options = f":sout=#transcode{{acodec=mpga,ab=128,channels=2,samplerate=44100}}:rtp{{mux=ts,sdp={url}}}"
        media.add_option(options)
        if player.is_playing():
            print("Player was already playing, stopping it first.")
            t = threading.Thread(target=lambda: player.pause())
            t.start()
        player.set_media(media)

        timerDelay = 0.0
        media.parse()
        duration_ms = media.get_duration()
        print(f"Duration: {duration_ms}")

        info = Demo.StreamingInfo()
        info.url = url
        info.duration = duration_ms
        info.clientIP = clientIp

        clientStates[clientIp] = "playing"

        t = Timer(timerDelay, self.startStream, [player])
        t.start()
        print(f"Playing {s} on {url}")
        return info

    def doesSongExist(self, title, current):
        con = sqlite3.connect('songs.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM songs WHERE queryName = '{title}'")
        rows = cur.fetchall()
        con.close()
        return len(rows) > 0


    def stopMusic(self, current):
        global playerInstances
        global clientStates
        clientIp = current.con.getInfo().remoteAddress
        clientIp = clientIp.replace("::ffff:", "")
        if clientIp in playerInstances:
            print(f"Stopping player for {clientIp}")
            clientStates[clientIp] = "stopped"
            player = playerInstances[clientIp]
            t = threading.Thread(target=self.deletePlayerForClient, args=(player, clientIp,))
            t.start()

    def playPauseMusic(self, current):
        global playerInstances
        global clientStates
        bufferdelay = 2000
        clientIp = current.con.getInfo().remoteAddress
        clientIp = clientIp.replace("::ffff:", "")
        print(f"Play/Pause request from {clientIp}")
        if clientIp in playerInstances and clientIp in clientStates:
            if clientStates[clientIp] == "playing":
                player = playerInstances[clientIp]
                player.pause()
                clientStates[clientIp] = "paused"
                return 0
            elif clientStates[clientIp] == "paused":
                player = playerInstances[clientIp]
                player.set_time(player.get_time() - bufferdelay)
                media = player.get_media()
                media.parse()
                remaining = media.get_duration() - player.get_time()
                player.play()
                clientStates[clientIp] = "playing"
                return remaining

    def deletePlayerForClient(self, player, clientIp):
        global playerInstances
        player.stop()
        player.release()

    def getSongList(self, current):
        con = sqlite3.connect('songs.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM songs")
        rows = cur.fetchall()

        results = []
        for row in rows:
            result_dict = {}
            for idx, col in enumerate(cur.description):
                result_dict[col[0]] = row[idx]
            results.append(result_dict)

        json_string = json.dumps(results)
        con.close()
        return json_string

    def getSearchByTitle(self, title, current=None):
        con = sqlite3.connect('songs.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM songs WHERE title LIKE '%{title}%'")
        rows = cur.fetchall()

        results = []
        for row in rows:
            result_dict = {}
            for idx, col in enumerate(cur.description):
                result_dict[col[0]] = row[idx]
            results.append(result_dict)

        json_string = json.dumps(results)
        con.close()
        return json_string

    def getSearchByAuthor(self, author, current=None):
        con = sqlite3.connect('songs.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM songs WHERE author LIKE '%{author}%'")
        rows = cur.fetchall()

        results = []
        for row in rows:
            result_dict = {}
            for idx, col in enumerate(cur.description):
                result_dict[col[0]] = row[idx]
            results.append(result_dict)

        json_string = json.dumps(results)
        con.close()
        return json_string

    def changeSongTitle(self, title, newTitle, current=None):
        print(f"Changing title from {title} to {newTitle}")
        con = sqlite3.connect('songs.db')
        cur = con.cursor()
        cur.execute(f"select path from songs where title = '{title}'")
        path = cur.fetchone()[0]
        os.rename(path, path.replace(title, newTitle))
        cur.execute(f"UPDATE songs SET title = '{newTitle}' WHERE title = '{title}'")
        cur.execute(f"UPDATE songs SET path = '{path.replace(title, newTitle)}' WHERE title = '{newTitle}'")
        con.commit()
        con.close()

    def changeSongAuthor(self, title, newAuthor, current=None):
        con = sqlite3.connect('songs.db')
        cur = con.cursor()
        cur.execute(f"UPDATE songs SET author = '{newAuthor}' WHERE title = '{title}'")
        con.commit()
        con.close()

    def deleteSong(self, title, current=None):
        con = sqlite3.connect('songs.db')
        cur = con.cursor()
        cur.execute(f"select path from songs where title = '{title}'")
        path = cur.fetchone()[0]
        os.remove(path)
        cur.execute(f"DELETE FROM songs WHERE title = '{title}'")
        con.commit()
        con.close()


class FileTransferI(Demo.FileTransfer):
    songsfolder = "songs/"

    def sendFile(self, data, title, current=None):
        print(f"Completing transfer for {title}")
        if (data is None):
            return

        pathTofile = self.songsfolder + title

        if (not os.path.isfile(pathTofile)):
            with open(pathTofile, 'wb') as f:
                f.write(data)

            print(f"File {title} uploaded successfully.")
            title = title.split(".")[0]
            con = sqlite3.connect('songs.db')
            cur = con.cursor()
            cur.execute(f"INSERT INTO songs (title, path) VALUES ('{title}', '{pathTofile}')")
            con.commit()
        else:
            print(f"File {title} already exists.")


props = Ice.createProperties(sys.argv)
props.setProperty("Ice.MessageSizeMax", "0")
# props.setProperty("Ice.Trace.Network", "2")
id = Ice.InitializationData()
id.properties = props
communicator = Ice.initialize(id)

adapter = communicator.createObjectAdapterWithEndpoints("SimplePrinterAdapter", "default -p 10000")
printer = PrinterI()
adapter.add(printer, communicator.stringToIdentity("SimplePrinter"))
adapter.activate()
print("Printer server started")

file_transfer_adapter = communicator.createObjectAdapterWithEndpoints("FileTransferAdapter", "default -p 10001")
file_transfer = FileTransferI()
file_transfer_adapter.add(file_transfer, communicator.stringToIdentity("FileTransfer"))
file_transfer_adapter.activate()
print("FileTransfer server started")

print("Server ip: " + localIp)

communicator.waitForShutdown()
