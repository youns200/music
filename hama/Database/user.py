from typing import Dict, List, Union

from hama import db

userdb = db.user


async def is_served_user(user_id: int) -> bool:
    user = await userdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_user() -> list:
    user = userdb.find({"user_id": {"$gt": 0}})
    if not user:
        return []
    user_list = []
    for user in await user.to_list(length=1000000000):
        user_list.append(user)
    return user_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await userdb.insert_one({"user_id": user_id})

