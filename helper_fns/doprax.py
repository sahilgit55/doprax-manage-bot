from aiohttp import ClientSession
from string import ascii_lowercase, digits
from random import choices
from asyncio import sleep
from asyncio import create_task

def gen_random_string(k):
    return str(''.join(choices(ascii_lowercase + digits, k=k)))

update_id_list = []

async def msg_time_updater(updater_time, reply, updater_id, raw_text):
    await sleep(1)
    initial_updater_time = updater_time
    while True:
        if updater_time>0 and updater_id in update_id_list:
            text= f"{raw_text}\n\n⏳Timeout in {str(updater_time)} secs"
            try:
                if initial_updater_time!=updater_time:
                        print("updating message")
                        await reply.edit(text)
            except Exception as e:
                print(f"error in updating message {str(e)}")
        else:
            print("updater time completed")
            break
        await sleep(9)
        updater_time = updater_time - 10
    return


async def clear_update_list(update_id, task):
    if update_id in update_id_list:
        update_id_list.remove(update_id)
    await stop_tash(task)
    return

async def stop_tash(t):
    try:
        t.cancelled()
    except Exception as e:
        print(e)
    return


async def get_bots(cookies, user_name, reply):
        headers = {
            "Host": "www.doprax.com",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.136 Mobile Safari/537.36",
            "x-requested-with": "idm.internet.download.manager.plus",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": f"https://www.doprax.com/u/{str(user_name)}/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en,en-IN;q=0.9,en-US;q=0.8",
            "cookie": f"{str(cookies)}"
        }
        timeout = 120
        async with ClientSession() as session:
            update_id = gen_random_string(10)
            update_id_list.append(update_id)
            task1 = create_task(msg_time_updater(timeout, reply, update_id, "⏳Connecting Please Wait..."))
            try:
                bots_data = await session.get(url="https://www.doprax.com/api/v1/projects/", headers=headers, timeout=timeout)
            except:
                await clear_update_list(update_id, task1)
                await sleep(1)
                await reply.edit(f"❗Connection Failed.")
                return False
            await clear_update_list(update_id, task1)
            try:
                return await bots_data.json()
            except Exception as e:
                await reply.edit(f"❗Error: {str(e)}")
                return False
            


async def get_resources(bot_code, bot_url, cookies, user_name, reply):
        headers = {
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.136 Mobile Safari/537.36",
    "x-requested-with": "idm.internet.download.manager.plus",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": f"{str(bot_url).strip('/')}/{str(user_name)}/projects/{str(bot_code)}/deploy/",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en,en-IN;q=0.9,en-US;q=0.8",
    "cookie": f"{str(cookies)}"
  }
        timeout = 120
        async with ClientSession() as session:
            update_id = gen_random_string(10)
            update_id_list.append(update_id)
            task1 = create_task(msg_time_updater(timeout, reply, update_id, "⏳Connecting Please Wait..."))
            url = f"{str(bot_url).strip('/')}/api/v1/projects/{str(bot_code)}/resources/?environment=sandbox"
            print(url)
            try:
                bot_data = await session.get(url=url, headers=headers, timeout=timeout)
            except:
                await clear_update_list(update_id, task1)
                await sleep(1)
                await reply.edit(f"❗Connection Failed.")
                return False
            await clear_update_list(update_id, task1)
            try:
                return await bot_data.json()
            except Exception as e:
                await reply.edit(f"❗Error: {str(e)}")
                return False
            

async def bot_action(data, bot_code, bot_url, cookies, user_name, reply):
        headers = {
    "content-length": f"{str(len(str(data)))}",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.136 Mobile Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "origin": f"{str(bot_url).strip('/')}",
    "x-requested-with": "idm.internet.download.manager.plus",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": f"{str(bot_url).strip('/')}/{str(user_name)}/projects/{str(bot_code)}/deploy/",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en,en-IN;q=0.9,en-US;q=0.8",
    "cookie": f"{str(cookies)}"
  }
        timeout = 120
        async with ClientSession() as session:
            update_id = gen_random_string(10)
            update_id_list.append(update_id)
            task1 = create_task(msg_time_updater(timeout, reply, update_id, "⏳Connecting Please Wait..."))
            url = f"{str(bot_url).strip('/')}/api/v1/projects/{str(bot_code)}/deploy/main/"
            print(url)
            try:
                bot_data = await session.post(url=url, headers=headers, json=data, timeout=timeout)
            except:
                await clear_update_list(update_id, task1)
                await sleep(1)
                await reply.edit(f"❗Connection Failed.")
                return False
            await clear_update_list(update_id, task1)
            try:
                return await bot_data.json()
            except Exception as e:
                await reply.edit(f"❗Error: {str(e)}")
                return False