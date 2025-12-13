from twisted.internet import reactor
from quarry.net.client import ClientFactory, ClientProtocol
from quarry.net.auth import OfflineProfile
import time
import threading

# ========= CONFIG =========
SERVER_IP = "JollyMan.aternos.me"
SERVER_PORT = 32899
USERNAME = "AFK_Bot"
# ==========================


class AFKProtocol(ClientProtocol):
    def connection_made(self):
        super().connection_made()
        print("Connected to server")

    def player_joined(self):
        print("Spawned in world")

        def anti_afk():
            while True:
                try:
                    # Just stay alive, quarry handles keepalive automatically
                    pass
                except:
                    pass
                time.sleep(60)

        threading.Thread(target=anti_afk, daemon=True).start()


class AFKFactory(ClientFactory):
    protocol = AFKProtocol


def main():
    profile = OfflineProfile(USERNAME)
    factory = AFKFactory(profile)
    factory.connect(SERVER_IP, SERVER_PORT)
    reactor.run()


if __name__ == "__main__":
    main()
