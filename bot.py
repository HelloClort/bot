from twisted.internet import reactor
from quarry.net.client import ClientFactory, ClientProtocol
from quarry.net.auth import OfflineProfile
import time
import threading

# ===== CONFIG =====
SERVER_IP = "JollyMan.aternos.me"
SERVER_PORT = 32899
USERNAME = "AFK_Bot"
RECONNECT_DELAY = 5      # seconds
MOVE_INTERVAL = 60       # seconds
# ==================


class AFKProtocol(ClientProtocol):
    def player_joined(self):
        print("Spawned in world")

        def anti_afk():
            while True:
                try:
                    # Send a tiny position packet (no real movement)
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
                except Exception as e:
                    print("AFK loop error:", e)
                    break
                time.sleep(MOVE_INTERVAL)

        threading.Thread(target=anti_afk, daemon=True).start()

    def connection_lost(self, reason):
        print("Disconnected:", reason)
        reactor.stop()
        reconnect()


class AFKFactory(ClientFactory):
    protocol = AFKProtocol


def reconnect():
    print(f"Reconnecting in {RECONNECT_DELAY}s...")
    time.sleep(RECONNECT_DELAY)
    start_bot()


def start_bot():
    profile = OfflineProfile(USERNAME)
    factory = AFKFactory(profile)
    factory.connect(SERVER_IP, SERVER_PORT)
    reactor.run()


if __name__ == "__main__":
    start_bot()
