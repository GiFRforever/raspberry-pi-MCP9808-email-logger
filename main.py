import readtemp
import sendmail
import time
from datetime import date, datetime
import os

if __name__ != "__main__":
    raise Exception("This script should not be imported")

today: date = date.today()

if (dir_wip := os.listdir("WIP")) != []:
    for file in dir_wip:
        if file != today:
            sendmail.SendMail().send_mail(f"WIP/{file}")

while True:
    teplota: float = readtemp.MCP9808().read_temp()
    now: datetime = datetime.now()
    print(f"{now} - {teplota}")
    if int(now.isoformat(timespec="minutes")[14:16]) % 5 == 0:  # every 5 minutes
        with open(f"WIP/{today}", "a") as f:
            f.write(
                f"""{now.strftime("%H:%M")};{str(round(teplota, 2)).replace(".", ",")}"""
            )

    if now.isoformat(timespec="minutes") == "00:00":
        sendmail.SendMail().send_mail(f"WIP/{today}")
        os.rename(f"WIP/{today}", f"LOGGED/{today}")
        today = date.today()
        with open(f"WIP/{today}", "w") as f:
            f.write("Time;Temperature")
    time.sleep(5)
