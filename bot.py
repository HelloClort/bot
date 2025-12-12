from quarry.net.client import ClientFactory, SpawningClient
from twisted.internet import reactor
import time, threading

SERVER_IP = "JollyMan.aternos.me"
SERVER_PORT = 32899
USERNAME = "AFK_Bot"  # cracked username

# Optional: minor movement to bypass AFK kick
MINOR_MOVE_INTERVAL = 300  # seconds between small movements

class AFKClient(SpawningClient):
    def player_joined(self):
        # Player spawned, start minor AFK loop
        self._start_afk_loop()

    def _start_afk_loop(self):
        def loop():
            while True:
                try:
                    self.rotation.yaw += 0.01
                    self.rotation.pitch += 0.0
                except Exception:
                    pass
                time.sleep(MINOR_MOVE_INTERVAL)
        t = threading.Thread(target=loop)
        t.daemon = True
        t.start()

class AFKFactory(ClientFactory):
    protocol = AFKClient

def connect():
    try:
        factory = AFKFactory()
        print(f"Connecting to {SERVER_IP}:{SERVER_PORT} as {USERNAME}...")
        factory.connect(SERVER_IP, SERVER_PORT, username=USERNAME)
        reactor.run()
    except Exception as e:
        print(f"Disconnected, retrying in 10 seconds... {e}")
        time.sleep(10)
        connect()  # Auto-reconnect

if __name__ == "__main__":
    connect()
