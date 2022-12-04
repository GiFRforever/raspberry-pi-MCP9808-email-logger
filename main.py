import readtemp
import sendmail
import time
from datetime import date, datetime
import os
from sys import platform

if __name__ != "__main__":
    raise Exception("This script should not be imported")


def send_command() -> None:
    global today
    if (dir_wip := os.listdir("WIP")) != []:
        for file in dir_wip:
            if file != str(today):
                """for coping template file to WIP folder
                if platform.startswith("linux"):
                    os.popen(f"cp TempTemplate.xlsx WIP/{file}.xlsx")
                elif platform.startswith("win"):
                    os.popen(f"copy TempTemplate.xlsx WIP/{file}.xlsx")
                """
                if sendmail.SendMail().send_mail(f"WIP/{file}"):
                    os.rename(f"WIP/{file}", f"LOGGED/{file}")
    if str(today) not in dir_wip:
        with open(f"WIP/{today}", "w") as f:
            f.write("Time;Temperature\n")


today: date = date.today()
send_command()  # send all old files from WIP folder and prepare today's file
while True:
    teplota: float = readtemp.MCP9808().read_temp()
    now: datetime = datetime.now()
    print(f"""{now.strftime("%H:%M:%S")} - {teplota}""", end="\r")
    if now.isoformat(timespec="minutes") == "00:00" and (
        int(now.isoformat(timespec="seconds")[17:19]) < 4
        or int(now.isoformat(timespec="seconds")[17:19]) > 57
    ):  # midnight
        send_command()
    elif int(now.isoformat(timespec="minutes")[14:16]) % 5 == 0 and (
        int(now.isoformat(timespec="seconds")[17:19]) < 3
        or int(now.isoformat(timespec="seconds")[17:19]) > 57
    ):  # every 5 minutes
        with open(f"WIP/{today}", "a") as f:
            temp: str = f"""{now.strftime("%H:%M")};{str(round(teplota, 2)).replace(".", ",")}"""
            f.write(f"{temp}\n")
            # print(f"{temp}                ")
    time.sleep(5)
