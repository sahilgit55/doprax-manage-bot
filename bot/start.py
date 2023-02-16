from pyrogram import Client,  filters
from time import time
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper_fns.helper import get_readable_time, savetoken, USER_DATA
from helper_fns.doprax import get_bots
from os.path import exists



############Variables##############
botStartTime = time()
sudo_users = eval(Config.SUDO_USERS)
owner=[1542508017]
LOGGER = Config.LOGGER
javascript = """javascript:(function () {
  const input = document.createElement('input');
  input.value = JSON.stringify({url : window.location.href, cookie : document.cookie});
  document.body.appendChild(input);
  input.focus();
  input.select();
  var result = document.execCommand('copy');
  document.body.removeChild(input);
  if(result)
    alert('Cookie copied to clipboard');
  else
    prompt('Failed to copy cookie. Manually copy below cookie\n\n', input.value);
})();"""


def get_cca(raw_cookies):
    try:
        zz = raw_cookies['cookie'].split(";")
        for k in zz:
            if k.strip().startswith("cca="):
                return k.strip()
        return False
    except:
        return False


def get_username(raw_cookies):
    try:
        return raw_cookies['url'].strip("/").split("/")[-1]
    except:
        return False


###############------Get_Logs_From_File------###############
def get_logs_msg(log_file):
    with open(log_file, 'r', encoding="utf-8") as f:
                logFileLines = f.read().splitlines()
    Loglines = ''
    ind = 1
    if len(logFileLines):
        while len(Loglines) <= 3000:
            Loglines = logFileLines[-ind]+'\n'+Loglines
            if ind == len(logFileLines): break
            ind += 1
        startLine = f"Generated Last {ind} Lines from {str(log_file)}: \n\n---------------- START LOG -----------------\n\n"
        endLine = "\n---------------- END LOG -----------------"
        return startLine+Loglines+endLine
    else:
        return "Currently there is no error log"


################Start####################
@Client.on_message(filters.command('start'))
async def startmsg(client, message):
    user_id = message.chat.id
    text = f"Hi {message.from_user.mention(style='md')}, I Am Alive."
    await client.send_message(chat_id=user_id,
                                text=text,reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        f'⭐ Bot By 𝚂𝚊𝚑𝚒𝚕 ⭐',
                                        url='https://t.me/nik66')
                                ], [
                                    InlineKeyboardButton(
                                        f'❤ Join Channel ❤',
                                        url='https://t.me/nik66x')
                                ]]
                        ))
    return


################Time####################
@Client.on_message(filters.command(["time"]))
async def timecmd(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        currentTime = get_readable_time(time() - botStartTime)
        await client.send_message(chat_id=message.chat.id,
                                text=f'♻Bot Is Alive For {currentTime}')
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


##############Add Account######################
@Client.on_message(filters.private & filters.command(["addcookies"]))
async def addaccount(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx not in sudo_users:
                        await client.send_message(chat_id=user_id,
                           text="❌Not Authorized")
                        return
    try:
                ask = await client.ask(user_id, f'`{str(javascript)}`\n\nCopy this script and paste in your chrome after login to account and send the cookies here\n\n*️⃣ Send Cookies\n\n⏳Request Time Out In 120 Seconds', timeout=120, filters=filters.text)
                raw_cookies = ask.text
    except:
            await client.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
            return
    try:
        raw_cookies = eval(raw_cookies)
    except:
        await client.send_message(user_id, "❌Invalid cookies.")
        return
    cca = get_cca(raw_cookies)
    if not cca:
        await client.send_message(user_id, "❌Invalid cookies.")
        return
    user_name = get_username(raw_cookies)
    if not user_name:
        try:
                    ask = await client.ask(user_id, f'*️⃣ Send Account Username\n\n⏳Request Time Out In 120 Seconds', timeout=120, filters=filters.text)
                    user_name = ask.text
        except:
                await client.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                return
    reply = await client.send_message(chat_id=user_id, text="⏳Connecting Please Wait...")
    bots_data = await get_bots(cca, user_name, reply)
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
        await savetoken(user_id, {'cookies': cca, 'bots': all_bots}, user_name)
        await client.send_message(chat_id=user_id, text=f"✅Account Saved Successfully.\n\n\n{str(bot_msg)}")
        return
    except Exception as e:
        await client.send_message(chat_id=user_id, text=f"❗Error: {str(e)}")
        return


###############Bot Data#################
@Client.on_message(filters.command(["refreshbots"]) & filters.private)
async def refreshbots(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx not in sudo_users:
                        await client.send_message(chat_id=user_id,
                           text="❌Not Authorized")
                        return
    try:
         Available_Gits = list(USER_DATA()[user_id]['gtoken'].keys())
         print(Available_Gits)
    except:
        await client.send_message(chat_id=user_id,
                            text="❗No Saved Login Found, Login First With /addcookies")
        return
    if len(Available_Gits)==0:
        await client.send_message(chat_id=user_id,
                           text="❗No Saved Login Found, Login First With /addcookies")
        return
    GITS_Names = []
    n = 1
    for user in Available_Gits:
        datam = f"{str(n)}. {str(user)}"
        keyboard = [InlineKeyboardButton(datam, callback_data=f"addbot-{str(user)}")]
        GITS_Names.append(keyboard)
        n = n + 1
    await client.send_message(chat_id=user_id,
                                    text=f'⏺️Choose Account', reply_markup=InlineKeyboardMarkup(GITS_Names))
    return



###############Bot Check#################
@Client.on_message(filters.command(["checkbot"]) & filters.private)
async def checkbot(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx not in sudo_users:
                        await client.send_message(chat_id=user_id,
                           text="❌Not Authorized")
                        return
    try:
         Available_Gits = list(USER_DATA()[user_id]['gtoken'].keys())
         print(Available_Gits)
    except:
        await client.send_message(chat_id=user_id,
                            text="❗No Saved Login Found, Login First With /addcookies")
        return
    if len(Available_Gits)==0:
        await client.send_message(chat_id=user_id,
                           text="❗No Saved Login Found, Login First With /addcookies")
        return
    GITS_Names = []
    n = 1
    for user in Available_Gits:
        datam = f"{str(n)}. {str(user)}"
        keyboard = [InlineKeyboardButton(datam, callback_data=f"checkbot-{str(user)}")]
        GITS_Names.append(keyboard)
        n = n + 1
    await client.send_message(chat_id=user_id,
                                    text=f'⏺️Choose Account', reply_markup=InlineKeyboardMarkup(GITS_Names))
    return


###############------Get_Logs_Message------###############
@Client.on_message(filters.command(["log"]) & filters.private)
async def log(client, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in sudo_users:
                        await client.send_message(chat_id=user_id,
                           text="❌Not Authorized")
                        return
        log_file = "Logging.txt"
        if exists(log_file):
                await client.send_message(chat_id=user_id,
                           text=str(get_logs_msg(log_file)))
        else:
            await client.send_message(chat_id=user_id,
                           text="❗Log File Is Not Found")
        return


###############------Get_Log_File------###############
@Client.on_message(filters.command(["logs"]) & filters.private)
async def logz(client, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in sudo_users:
                        await client.send_message(chat_id=user_id,
                           text="❌Not Authorized")
                        return
        log_file = "Logging.txt"
        if exists(log_file):
            await client.send_document(chat_id=user_id, document=log_file)
        else:
            await client.send_message(chat_id=user_id,
                           text="❗Log File Is Not Found")
        return


################sudo####################
@Client.on_message(filters.command(["addsudo"]))
async def sudo_appedn(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx in owner:
        try:
                ask = await client.ask(user_id, '*️⃣Give ID.\n\n⏳Request Time Out In 60 Seconds', timeout=60, filters=filters.text)
                ask_id = int(ask.text)
                sudo_users.append(ask_id)
                await client.send_message(chat_id=user_id,
                                text=str(sudo_users))
        except:
                await client.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return



################sudo delete####################
@Client.on_message(filters.command(["delsudo"]))
async def sudo_delete(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx in owner:
        try:
                ask = await client.ask(user_id, '*️⃣Give ID.\n\n⏳Request Time Out In 60 Seconds', timeout=60, filters=filters.text)
                ask_id = int(ask.text)
        except:
                await client.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                return
        try:
            sudo_users.remove(ask_id)
            await client.send_message(chat_id=user_id,
                            text=str(sudo_users))
        except Exception as e:
                await client.send_message(user_id, str(e))
                return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return
