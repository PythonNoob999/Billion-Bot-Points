import subprocess
from database import DB
from utils import msg
from functions import *
import time
import asyncio
subprocess.run("clear", shell=True)

print(msg["start"])
time.sleep(0.7)
print(msg["creds"])
time.sleep(0.7)

total_points = 0

async def main():
    global total_points
    while True:
        print(msg["options"])
        time.sleep(0.25)
        ans = input("\033[1;32;40m>> ")
        if ans.lower().strip() == "exit":
            break
        elif ans.lower().strip() == "1":
            await add_account()
        elif ans.lower().strip() == "2":
            accs = DB.fetch()
            print(f"\033[1;34;40mYou have {len([key for key in accs.keys()])} accounts\033[0;40m")
        elif ans.lower().strip() == "3":
            points = 0
            print('\033[1;34;40mType the amount of tries for each account to collect point\033[0;40m')
            num = 0
            amount_of_tries = int(input('\033[1;32;40m>> '))
            data = DB.fetch()
            accounts = [data[key]["phone_number"] for key in data.keys()]
            print("\033[1;34;40mCollecting process begin🕥, take a cup of coffee☕\033[0;40m")
            for account in accounts:
                while num < amount_of_tries:
                    points += await collect_points(account)
                    num+=1
            print("\033[1;34;40mFinished✅\033[0;40m")
            print(msg['finished_order'].format(points))
            
asyncio.run(main())