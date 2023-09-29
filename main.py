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
            exit()
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

        elif ans.lower().strip() == "4":
            print("\033[1;34;40mStarting to collect!⚙️\033[0;40m")
            n = 0
            data = DB.fetch()
            accounts = [data[key]["phone_number"] for key in data.keys()]
            for account in accounts:
                s = await collect_daily(account)
                n+=s
                print(f"\033[1;34;40mFinished \033[1;32;40m{account}\033[1;34;40m, collected \033[1;32;40m{s}\033[1;34;40m Points!\033[0;40m")
            print(f"\033[1;34;40mFinished✅, collected \033[1;32;40m{n}\033[1;34;40m points from \033[1;32;40m{len(data.keys())}\033[0;40m")
            
            
asyncio.run(main())