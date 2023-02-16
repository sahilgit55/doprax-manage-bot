from config import Config
from db_handler import Database

db = Database()

############Variables##############
User_Data = eval(Config.User_Data)
CREDIT = Config.CREDIT


############Helper Functions##############
def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result



def get_human_size(num):
    base = 1024.0
    sufix_list = ['B','KB','MB','GB','TB','PB','EB','ZB', 'YB']
    for unit in sufix_list:
        if abs(num) < base:
            return f"{round(num, 2)} {unit}"
        num /= base


##########Save Token###############
def USER_DATA():
    return User_Data

##########Save Token###############
async def savetoken(user_id, token, user):
    try:
        if user_id not in User_Data:
            User_Data[user_id] = {}
            User_Data[user_id]['gtoken'] = {}
            User_Data[user_id]['gtoken'][user] = token
        else:
            User_Data[user_id]['gtoken'][user] = token
        data = await db.add_datam(str(User_Data), CREDIT, "User_Data")
        return data
    except Exception as e:
        print(e)
        return False

##########Delete Token###############
async def deletetoken(user_id, user):
        try:
            del User_Data[user_id]['gtoken'][user]
            data = await db.add_datam(str(User_Data), CREDIT, "User_Data")
            print("🔶Token Deleted Successfully")
            return data
        except Exception as e:
            print("🔶Failed To Delete Token")
            print(e)
            return False
