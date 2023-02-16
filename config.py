from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv
from os.path import exists
from logging import StreamHandler, getLogger, basicConfig, ERROR, DEBUG, INFO
from logging.handlers import RotatingFileHandler
from requests import get

def dw_file(url, filename):
        r = get(url, allow_redirects=True, stream=True)
        with open(filename, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=1024 * 10):
                        if chunk:
                                fd.write(chunk)
        return


###############------Download_Config------###############
CONFIG_FILE_URL = getenv("CONFIG_FILE_URL", False)
if CONFIG_FILE_URL and str(CONFIG_FILE_URL).startswith("http"):
    dw_file(str(CONFIG_FILE_URL), "config.env")


if exists('config.env'):
  load_dotenv('config.env')

###############------Logging------###############
if exists("Logging.txt"):
    with open("Logging.txt", "r+") as f_d:
        f_d.truncate(0)


basicConfig(
    level=INFO,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "Logging.txt", maxBytes=50000000, backupCount=10, encoding="utf-8"
        ),
        StreamHandler(),
    ],
)

getLogger("pyrogram").setLevel(ERROR)

        
        
def get_mongo_data(MONGODB_URI, BOT_USERNAME, id, colz):
        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[BOT_USERNAME]
        col = mongo_db[colz]
        print("🔶Getting Data From Database")
        item_details = col.find({"id" : id})
        data = False
        for item in item_details:
                        data = item.get('data')
        if data:
            print("🟢Data Found In Database")
            return data
        else:
            print("🟡Data Not Found In Database")
            return "{}"


class Config:
    API_ID = int(getenv("API_ID",""))
    API_HASH = getenv("API_HASH","")
    TOKEN = getenv("TOKEN","")
    SUDO_USERS = getenv("SUDO_USERS","")
    CREDIT = getenv("CREDIT","")
    MONGODB_URI = getenv("MONGODB_URI","")
    BOT_USERNAME = getenv("BOT_USERNAME","")
    CHANNEL_USERNAME = getenv("CHANNEL_USERNAME", "")
    User_Data = get_mongo_data(MONGODB_URI, BOT_USERNAME, CREDIT, "User_Data")
    LOGGER = getLogger()