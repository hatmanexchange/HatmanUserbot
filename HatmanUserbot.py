from sched import scheduler
from pyrogram import Client, filters, idle
from pyrogram.raw.functions.messages import StartBot, DeleteHistory, InstallStickerSet
from pyrogram.raw.functions.help import GetUserInfo
from pyrogram.errors import * 
from pyrogram.errors import UsernameInvalid
from pyrogram.enums import ChatType, ParseMode, UserStatus
from pyrogram.raw.functions.account import UpdateNotifySettings
from pyrogram.raw.base import InputPeer
from pyrogram.raw.types import InputPeerNotifySettings, InputNotifyPeer, InputPeerChat, Message
from pyrogram.types import ChatPermissions
import asyncio
import time
import asyncio
import datetime
from multiprocessing import get_context
import os
import traceback
import requests
import validators
from pathlib import Path
from random import randint
import json
import random
import string
from random import randint
import time
ubot = Client("killersession", api_id=25047326, api_hash="9673ea812441c77e912979cd0f8a2572", lang_code="it")
ubot.start()

IDSSS, usernamesss = (ubot.get_me()).id, (ubot.get_me()).username
statusse = False
ignore = []

# Addword
class Database:
    def __init__(self, file_name: str):
        self.database = file_name
        if os.path.exists(file_name) == False:
            f = open(file_name, "a+")
            f.write(json.dumps({"word": {}, "wordr": {}, "sticker": False}))
            f.close()

    async def save(self, update: dict):
        os.remove(self.database)
        f = open(self.database, "a+")
        f.write(json.dumps(update))
        f.close()

    async def add_word(self, word: str, risposta: str):
        update = json.load(open(self.database))
        update["word"][str(word)] = risposta
        await self.save(update)
        return json.load(open(self.database))["word"][word]

    async def add_wordr(self, word: str, risposta: str):
        update = json.load(open(self.database))
        update["wordr"][str(word)] = risposta
        await self.save(update)
        return json.load(open(self.database))["wordr"][word]
word = Database("word.json")

paypal_link = None
litecoin_link = None
gruppi = []
muted_users = {}

@ubot.on_message(filters.user("self") & filters.command("help", "."))
async def help_command(client, message):
    await message.edit_text("https://telegra.ph/HatmanUserbot-01-14")

@ubot.on_message(filters.user("self") & filters.command("dev", "."))
async def creator_command(client, message):
    await message.edit_text("I am developed by @hatmanexchanger!")

@ubot.on_message(filters.user("self") & filters.command("percentage", "."))
async def percentage_command(client, message):
    # Estrai il testo del messaggio dopo il comando
    command_text = message.text.split(' ', 2)[1:]

    try:
        # Estrai i valori del numero e della percentuale
        numero = float(command_text[0])
        percentuale = float(command_text[1])

        # Calcola la percentuale
        risultato = (percentuale / 100) * numero

        # Invia la risposta
        await message.edit_text(f"{percentuale}% of {numero} is {risultato}")
    except (ValueError, IndexError):
        # Gestisce il caso in cui la conversione o l'accesso ai valori fallisce
        await message.edit_text("Right command is: .percentage [number] [percentage]")

@ubot.on_message(filters.user("self") & filters.command("addgroup", prefixes="."))
async def add_group_command(client, message):
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        gruppo_id = int(command_text)

        # Aggiungi il gruppo alla lista con un messaggio di default solo se non è già presente
        if gruppo_id not in gruppi:
            gruppi[gruppo_id] = {'intervallo': 5, 'messaggio': ""}
            await message.edit_text(f"Group {gruppo_id} added to the list.")
        else:
            await message.edit_text(f"Group is already in the list {gruppo_id}.")
    except (ValueError, IndexError):
        await message.edit_text("Right command: .addgroup [id_group]")

@ubot.on_message(filters.user("self") & filters.command("spam", "."))
async def spam_command(client, message):
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 2)[1:]
        intervallo = int(command_text[0])
        messaggio = command_text[1]

        # Imposta l'intervallo e il messaggio di spam per il gruppo specifico
        gruppo_id = message.chat.id
        gruppi[gruppo_id] = {'intervallo': intervallo, 'messaggio': messaggio}

        # Pianifica l'invio del messaggio al gruppo ogni intervallo specificato
        scheduler.every(intervallo).minutes.do(send_spam, client, gruppo_id)

        await message.edit_text(f"Spam on! i will send the message every {intervallo} minutes.")
    except (ValueError, IndexError):
        await message.edit_text("Right command: .spam [minutes] [message]")

def send_spam(client, gruppo_id):
    try:
        # Invia il messaggio di spam al gruppo specifico
        client.send_message(gruppo_id, gruppi[gruppo_id]['messaggio'])
    except Exception as e:
        print(f"error while the sending of the message in group {gruppo_id}: {e}")

@ubot.on_message(filters.user("self") & filters.command("listgroup", "."))
async def list_groups_command(client, message):
    elenco_gruppi = "\n".join([f"{gruppo_id}: {client.get_chat(gruppo_id).title}" for gruppo_id in gruppi])
    await message.edit_text(f"List of groups:\n{elenco_gruppi}")

@Client.on_message(filters.command("stopspam"))
async def stop_spam_command(client, message):
    try:
        # Interrompi la pianificazione per tutti i gruppi
        for group_id in gruppi:
            schedule.clear(f'send_spam_{group_id}')
        
        await message.edit_text("Spam stopped successfully.")
    except Exception as e:
        print(f"Error while stopping spam  {e}")
        await message.edit_text("Error while stopping spam")

@ubot.on_message(filters.user("self") & filters.command("cloud", "."))
async def save_to_cloud(client, message):
    try:
        # Estrai il messaggio a cui si sta rispondendo
        replied_message = message.reply_to_message

        # Salva il messaggio nei messaggi salvati
        await client.save_file(replied_message, file_name="")

        await message.edit_text("Message correctly saved")
    except Exception as e:
        print(f"Error while the saving of the message: {e}")

@ubot.on_message(filters.user("self") & filters.command("ppset", "."))
async def set_paypal_link(client, message):
    global paypal_link
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        link_paypal = command_text

        # Imposta il link PayPal generico
        paypal_link = link_paypal

        await message.edit_text("Link PayPal set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .ppset [link_paypal]")

@ubot.on_message(filters.user("self") & filters.command("pp", "."))
async def show_paypal_link(client, message):
    if paypal_link:
        await message.edit_text(f"Link PayPal:\n{paypal_link}")
    else:
        await message.edit_text("No link PayPal set. Use .ppset to set a link.")

ubot.on_message(filters.user("self") & filters.command("ltcset", "."))
async def set_litecoin_link(client, message):
    global litecoin_link
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        link_litecoin = command_text

        # Imposta il link Litecoin generico
        litecoin_link = link_litecoin

        await message.edit_text("Ltc address set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .ltcset [Address]")

@ubot.on_message(filters.user("self") & filters.command("ltc", "."))
async def show_litecoin_link(client, message):
    if litecoin_link:
        await message.edit_text(f"{litecoin_link}")
    else:
        await message.edit_text("No ltc address  set. Use .ltcset to set a link.")
       
@ubot.on_message(filters.user("self") & filters.command("block", "."))
async def block_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Blocca l'utente
        await client.block_user(user_id)

        await message.edit_text("User blocked.")
    except Exception as e:
        print(f"Error while blocking the user:{e}")
        await message.edit_text("Error while blocking the user.")

@ubot.on_message(filters.command("unblock", ".") & filters.reply)
async def unblock_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Sblocca l'utente
        await client.unblock_user(user_id)

        await message.edit_text("User unblocked successfully.")
    except Exception as e:
        print(f"Error while unblocking user: {e}")
        await message.edit_text("Error while unblocking user.")

# Comando per disattivare le notifiche per un utente in risposta
@ubot.on_message(filters.command("mute", ".") & filters.reply)
async def mute_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Aggiungi l'utente al dizionario dei muteati
        muted_users[user_id] = True
        
        await message.edit_text("User muted successfully.")
    except Exception as e:
        print(f"Error while muting user: {e}")
        await message.edit_text("Error while muting user.")
        
@ubot.on_message(filters.command("unmute", ".") & filters.reply)
async def unmute_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Rimuovi l'utente dal dizionario dei muteati
        muted_users.pop(user_id, None)

        await message.edit_text("User unmuted successfully.")
    except Exception as e:
        print(f"Error while unmuting user {e}")
        await message.edit_text("Error while unmuting user.")

# Handler per eliminare i messaggi degli utenti muteati
@ubot.on_message(filters.text)
async def delete_muted_messages(client, message):
    try:
        # Verifica se l'utente è muteato
        if message.from_user.id in muted_users:
            # Elimina il messaggio
            await message.delete()
    except Exception as e:
        print(f"Error while deleting muted user's message: {e}")

idle()
