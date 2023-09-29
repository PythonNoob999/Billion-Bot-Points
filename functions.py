from pyrogram import Client
from pyrogram.errors import BadRequest, SessionPasswordNeeded
from utils import msg
from database import DB
import asyncio
import re

creds = DB.get_creds()
answer = "\033[1;32;40m>> "

async def add_account():
    password=""
    print(msg["ask_phone_number"])
    phone_number = input(answer)
    if phone_number.startswith("+") and phone_number[1:].isdigit():
        app = Client(phone_number, creds[0], creds[1])
        try:
            await app.connect()
            sent_code = await app.send_code(phone_number)
            print(msg["ask_code"])
            code = input(answer)
            do_it = True
            try:
    	        await app.sign_in(phone_number=phone_number, phone_code_hash=sent_code.phone_code_hash, phone_code=code)
            except BadRequest:
    	        print("\033[1;34;40mCode Invalid!!, type it again")
    	        code = input(answer)
    	        while True:
    	            try:
    	                print("\033[1;34;40mChecking Code💬\033[0;40m")
    	                await app.sign_in(phone_number=phone_number, phone_code_hash=sent_code.phone_code_hash, phone_code=code)
    	                print('\033[1;34;40mCorrect Code✅\033[0;40m')
    	                break
    	            except BadRequest:
    	                print("\033[1;34;40mCode Invalid!!, type it again")
    	                code = input(answer)
    	            except SessionPasswordNeeded:
    	                break
    	            except Exception as e:
    	                print(e)
    	                do_it=False
    	                break
    	            
            except SessionPasswordNeeded:
    	        while True:
        	       try:
        	           print('\033[1;34;40mChecking Password🔑\033[0;40m')
        	           await app.check_password(password)
        	           break
        	       except BadRequest as e:
        	            if e.ID == "PASSWORD_HASH_INVALID":
        	                print(msg["ask_password"])
        	                password = input(answer) 
        	            else:
        	                print(e.ID)
        	                do_it=False
        	                break
        	       except Exception as e:
        	            do_it=False
        	            break

            if do_it:
                 session_string = ""
                 if not DB.check_exist(phone_number):
                     session_string = await app.export_session_string()
                 print("\033[1;34;40mJoining Channels⚙️\033[1;34;40m")
                 await join_chats(app)
                 try:
                     await app.disconnect()
                 except:
                     pass
                
                 DB.add_account(phone_number, password, session_string)
                 print(f"\033[1;34;40mSigned in to {phone_number} Successfully✅\033[0;40m")
            else:
                 print("\033[1;34;40mFailed to login❗\033[0;40m")
        except Exception as e:
            print(e)
            print(msg["phone_number_invalid"])
    else:
    	print(msg["phone_number_invalid"])


async def get_last_message(app):
    async for message in app.get_chat_history("EEOBOT"):
        return message

async def send_command(app, command):
    try:
        await app.send_message("EEOBOT", command)
        await asyncio.sleep(1.5)
    except:
        pass
        
async def click_button(app, message, index):
    try:
        await message.click(index)
    except:
        pass
    await asyncio.sleep(1)
    
async def join_chats(app, chats=["https://t.me/+vVntQPBqfbFkMDc0", "https://t.me/+SPTrcs3tJqhlMDVi", "https://t.me/+vEqyo7gWbB4xZTYy", "https://t.me/+PrvCMD0_rKqw9TXV"]):
    for chat in chats:
        try:
            await app.join_chat(chat)
            await asyncio.sleep(0.5)
        except:
            pass
            
async def get_chats(keyboard):
    links = []
    for row in keyboard:
        for button in row:
            if button.url is not None:
                if button.url.replace("https://t.me/", "").startswith("+"):
                    links.append(button.url)
                else:
                    links.append(button.url.replace("https://t.me/", ""))
    return links

async def get_finish_button_index(app, keyboard):
    n = -1
    cont = True
    for row in keyboard:
        if cont:
            for button in row:
                n+=1
                if button.text.strip() == "تحقق":
                    cont=False
                    break
        else:
            break
    return n
    
def get_count_from_message(text):
    pattern = r'\{(\d{2,3})\}'
    matches = re.findall(pattern, text)
    for matched in matches:
        return int(matched)
        break

async def collect_points(account):
    app = Client(account)
    n = 0
    try:
        await app.connect()
        await send_command(app, "/start")
        msg = await get_last_message(app)
        await click_button(app, msg, 2)
        msg = await get_last_message(app)
        await click_button(app, msg, 1)
        await asyncio.sleep(3)
        msg = await get_last_message(app)
        links = await get_chats(msg.reply_markup.inline_keyboard)
        await join_chats(app, links)
        index = await get_finish_button_index(app, msg.reply_markup.inline_keyboard)
        await click_button(app, msg, index)
        await asyncio.sleep(1.5)
        msg = await get_last_message(app)
        n += get_count_from_message(msg.text)
    except Exception as e:
        print(e)
        
    try:
        await app.disconnect()
    except:
        pass
    return n

async def collect_daily(account):
    app = Client(account)
    try:
        await app.connect()
    except:
        pass
        
    await send_command(app, "/start")
    msg = await get_last_message(app)
    await click_button(app, msg, 6)
    await asyncio.sleep(1)
    msg = await get_last_message(app)
    if "10" in msg.text:
        return 10
    else:
        return 0
        
    try:
        await app.disconnect()
    except:
        pass    