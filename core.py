import subprocess


def get_status():
    res = subprocess.run(["systemctl", "is-active", "tom_discord.service"], stdout=subprocess.PIPE, text=True)
    print(res.returncode)
    if res.returncode == 0:
        return "🟢Alive"
    else:
        return "🔴Dead"
