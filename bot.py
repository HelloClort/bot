from quarry.net.client import Client, ClientFactory
from twisted.internet import reactor
import time, threading
from flask import Flask
from threading import Thread

SERVER_IP = "JollyMan.aternos.me"
SERVER_PORT = 32899
USERNAME = "AFK_Bot"  # cracked username
MINOR_MOVE_INTERVAL = 300


# Flask keep-alive
app = Flask("")
@app.route("/")
def home(): return "Bot alive!"
def run(): app.run(host="0.0.0.0", port=8080)
Thread(target=run).start()

# AFK bot
class AFKClient(Client):
    def packet_spawn(self, packet, buff=None):
        # Start minor rotation movement
        def loop():
            while True:
                try:
                    self.rotation.yaw += 0.01
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
        connect()  # auto-reconnect

if __name__ == "__main__":
    connect()
