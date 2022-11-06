import subprocess
from pymemcache.client import base
import threading


class cache:

    def __init__(self, name):
        self.name = name
        self.client = base.Client(('127.0.0.1', 11211))

    def get(self):
        result = self.client.get(self.name)
        return result

    def set(self, value):
        self.client.set(self.name, value)


class discord_status:

    def __init__(self):
        self.status = cache('status')

    def run_check_status(self):
        threading.Timer(10.0, self.run_check_status).start()
        print("work")
        res = subprocess.run(["systemctl", "is-active", "tom_discord.service"], stdout=subprocess.PIPE, text=True)
        if res.returncode == 0:
            self.status.set("Alive")
        else:
            self.status.set("Dead")
        print(self.status.get())

    def get_status(self):
        if 'Alive' in str(self.status.get()):
            print("Alive")
            return "🟢Alive"
        elif 'Dead' in str(self.status.get()):
            print("Dead")
            return "🔴Dead"
        else:
            print("Not found")
            return "Not found"