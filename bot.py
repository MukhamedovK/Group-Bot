import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import *

from datetime import timedelta


logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "6012331540:AAEF0G8In-SwLfNRrf8z9cHpx4BdXWm4TKE"

bot = Bot(token=BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot)

warnings = 0


#START COMMAND
@dp.message_handler(commands=['start'])
async def start_bot(message: Message):
    if message.chat.type in ["supergroup", "group"]:
        await message.answer("Hi, I'm a group guard!")
        await message.answer("My commands: \n\n/mute - mute the user\n/warn - warn the user\n/ban - block the user")
    else:
        await message.answer("Hello Bro!\nAdd me to the group and give everyone a ban :)")


#MUTE COMMAND
@dp.message_handler(commands=['mute'], is_chat_admin=True)
async def mute_bot(message: Message):
    if message.chat.type in ["supergroup", "group"]:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_id = message.chat.id

            perm = ChatPermissions(
                can_send_messages=False
            )

            mute_time = message.date + timedelta(minutes=int(message.text.split(' ').pop(1)))

            await bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=perm,
                until_date=mute_time
            )
            await message.answer(f"<b><pre>{message.reply_to_message.from_user.mention}</pre></b> is muted until <i><u>{mute_time}!</u></i>")


#UNMUTE COMMAND
@dp.message_handler(commands=['unmute'], is_chat_admin=True)
async def unmute_bot(message: Message):
    if message.chat.type in ["supergroup", "group"]:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_id = message.chat.id

            perm = ChatPermissions(
                can_send_messages=True
            )

            await bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=perm,
            )
            await message.answer(f"<b><pre>{message.reply_to_message.from_user.mention}</pre></b> is unmuted")


#BAN COMMAND
@dp.message_handler(commands=['ban'], is_chat_admin=True)
async def ban_bot(message: Message):
    if message.chat.type in ["supergroup", "group"]:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_id = message.chat.id

            await bot.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

            await message.reply(f"<b><pre>{message.reply_to_message.from_user.mention}</pre></b> is banned! Bye, Bye!)")


#UNBAN COMMAND
@dp.message_handler(commands=['unban'], is_chat_admin=True)
async def unban_bot(message: Message):
    if message.chat.type in ["supergroup", "group"]:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_id = message.chat.id

            await bot.unban_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

            await message.reply(f"<b><pre>{message.reply_to_message.from_user.mention}</pre></b> is unbanned!")


#WARN COMMAND
@dp.message_handler(commands=['warn'])
async def warn_bot(message: Message):
    global warnings

    if message.chat.type in ["supergroup", "group"]:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_id = message.chat.id

            if warnings >= 2:
                perm = ChatPermissions(
                    can_send_messages=False
                )
                
                await bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=perm,
                    until_date=message.date + timedelta(minutes=30)
                )
                await message.reply(f"<b><pre>{message.reply_to_message.from_user.mention}</pre></b> is muted at <i><u>30 minutes</u></i>, becouse he/she have <b>3</b>/3 warnings!")
            else:
                warnings += 1
                await message.reply(f"<b><pre>{message.reply_to_message.from_user.mention}</pre></b> you have (<b>{warnings}</b>/3) warnings")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
