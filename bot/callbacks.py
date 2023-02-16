from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helper_fns.helper import USER_DATA
from helper_fns.doprax import get_bots, get_resources, bot_action
from helper_fns.helper import savetoken


############Variables##############
sudo_users = eval(Config.SUDO_USERS)



############CallBack##############
@Client.on_callback_query()
async def newbt(client, callback_query):
        txt = callback_query.data
        user_id = callback_query.message.chat.id
        print(txt)
        await callback_query.message.delete()
        
        
        if txt.startswith("checkbot-"):
            datam = txt.split("-")
            user_name = datam[-1]
            cookies = USER_DATA()[user_id]['gtoken'][user_name]['cookies']
            bots = USER_DATA()[user_id]['gtoken'][user_name]['bots']
            if not len(bots):
                await client.send_message(chat_id=user_id, text=f"❗No bots found, you need to refresh bots first.")
                return
            GITS_Names = []
            n = 1
            for bot_data in bots:
                datam = f"{str(n)}. {str(bot_data[0])}"
                keyboard = [InlineKeyboardButton(datam, callback_data=f"bot-{str(n-1)}-{str(user_name)}")]
                GITS_Names.append(keyboard)
                n = n + 1
            await client.send_message(chat_id=user_id,
                                            text=f'⏺️Choose Bot', reply_markup=InlineKeyboardMarkup(GITS_Names))
            return
        
        
        
        if txt.startswith("addbot-"):
            reply = await client.send_message(chat_id=user_id, text="⏳Connecting Please Wait...")
            datam = txt.split("-")
            user_name = datam[-1]
            cookies = USER_DATA()[user_id]['gtoken'][user_name]['cookies']
            bots_data = await get_bots(cookies, user_name, reply)
            if not bots_data:
                return
            try:
                await reply.delete()
            except:
                pass
            try:
                all_bots = []
                bot_msg = ""
                for bot in bots_data:
                    bot_name = bot['title']
                    bot_code = bot['projekt_code']
                    bot_url = bot['node']
                    bot_msg += f"⭕Bot Name: {str(bot_name)}\n"
                    all_bots.append([bot_name, bot_code, bot_url])
                if not len(all_bots):
                    await client.send_message(chat_id=user_id, text=f"❗No bots found.\n\n\n{str(bots_data)}")
                    return
                await savetoken(user_id, {'cookies': cookies, 'bots': all_bots}, user_name)
                await client.send_message(chat_id=user_id, text=f"✅Bots Refreshed Successfully.\n\n\n{str(bot_msg)}")
                return
            except Exception as e:
                await client.send_message(chat_id=user_id, text=f"❗Error: {str(e)}\n\n{str(bots_data)}")
                return
            
        if txt.startswith("bot-"):
            reply = await client.send_message(chat_id=user_id, text="⏳Connecting Please Wait...")
            datam = txt.split("-")
            user_name = datam[-1]
            bot_index = int(datam[1])
            cookies = USER_DATA()[user_id]['gtoken'][user_name]['cookies']
            bots = USER_DATA()[user_id]['gtoken'][user_name]['bots']
            if not len(bots):
                await client.send_message(chat_id=user_id, text=f"❗No bots found, you need to refresh bots first.")
                return
            selected_bot = bots[bot_index]
            bot_name = selected_bot[0]
            bot_code = selected_bot[1]
            bot_url = selected_bot[2]
            bot_data = await get_resources(bot_code, bot_url, cookies, user_name, reply)
            if not bot_data:
                return
            try:
                await reply.delete()
            except:
                pass
            try:
                ram = bot_data[0]['ram_mb']
                cpu = bot_data[0]['cpu_vcpu']
                status = bot_data[0]['status']
                if status=="running":
                    status = "🟢Running"
                    keyboard = [[
                                    InlineKeyboardButton(
                                        f'🔴Stop Bot',
                                        callback_data=f"botaction-0-{str(bot_index)}-{str(user_name)}")
                                ]]
                else:
                    if status=="not running":
                        status = "🔴Not Running"
                    else:
                        status = f"🟡 {str(status).capitalize()}"
                    keyboard = [[
                                    InlineKeyboardButton(
                                        f'🟢Start Bot',
                                        callback_data=f"botaction-1-{str(bot_index)}-{str(user_name)}")
                                ]]
                text = f"Bot Name: {str(bot_name)}\nStatus: {str(status)}\nRam: {str(ram)} mb\nCpu: {str(cpu)}"
            except Exception as e:
                await client.send_message(chat_id=user_id, text=f"❗Error: {str(e)}\n\n{str(bot_data)}")
                return
            await client.send_message(chat_id=user_id,
                                text=text,reply_markup=InlineKeyboardMarkup(
                            keyboard
                        ))
            return
    
    
        if txt.startswith("botaction-"):
            reply = await client.send_message(chat_id=user_id, text="⏳Connecting Please Wait...")
            datam = txt.split("-")
            user_name = datam[-1]
            bot_index = int(datam[2])
            cookies = USER_DATA()[user_id]['gtoken'][user_name]['cookies']
            bots = USER_DATA()[user_id]['gtoken'][user_name]['bots']
            if not len(bots):
                await client.send_message(chat_id=user_id, text=f"❗No bots found, you need to refresh bots first.")
                return
            selected_bot = bots[bot_index]
            bot_name = selected_bot[0]
            bot_code = selected_bot[1]
            bot_url = selected_bot[2]
            if datam[1]=="0":
                data = {"operation":"stop"}
            else:
                data = {"operation":"build_run"}
            action_data = await bot_action(data, bot_code, bot_url, cookies, user_name, reply)
            if not action_data:
                return
            try:
                await reply.delete()
            except:
                pass
            try:
                await client.send_message(chat_id=user_id, text=f"{str(action_data['msg'])}")
            except:
                await client.send_message(chat_id=user_id, text=f"{str(action_data)}")
            return
        
        return