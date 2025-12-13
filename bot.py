from quarry.net.client import ClientFactory, SpawningClient
from twisted.internet import reactor
import time
import threading

# -------- CONFIG --------
SERVER_IP = "JollyMan.aternos.me"
SERVER_PORT = 32899
USERNAME = "AFK_Bot"
# ------------------------

class AFKBot(SpawningClient):
    def player_joined(self):
        print("Bot joined server")

        def anti_afk():
            while True:
                try:
                    self.send_packet(
                        "player_position",
                        self.buff_type.pack(
                            "ddd?",
                            self.player.x,
                            self.player.y,
                            self.player.z,
                            True
                        )
                    )
                except:
                    pass
                time.sleep(120)

        threading.Thread(target=anti_afk, daemon=True).start()


class BotFactory(ClientFactory):
    protocol = AFKBot


def start():
    factory = BotFactory()
    factory.connect(SERVER_IP, SERVER_PORT, username=USERNAME)
    reactor.run()


if __name__ == "__main__":
    start()
