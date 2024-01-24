# Library
import discord
import random
import csv
from datetime import datetime

''' PARAMETERS ''' 
# BOT TOKEN (PUT THE TOKEN IN "")
var_bot_token = ""
# DISCORD SERVER ID (REPLACE 0 BY THE ID)
var_bot_server = 0
# RADIO CHANNEL ID (REPLACE 0 BY THE ID)
# WARNING !! THE BOT WILL DELETE PREVIOUS MESSAGES, BE SURE TO MAKE A NEW CHANNEL IF YOU DON'T WANT TO LOST MESSAGES
var_bot_channel = 0
# LOG CHANNEL ID (REPLACE 0 BY THE ID)
var_log_channel = 0
# CRACKLING FREQUENCY (0 -> 10)
var_gresillement = 3
# CRACKLING NOISES
liste_gresillement = ["shkkkk", "ksssss", "zzzzz"]
# JUMP FREQUENCY (0 -> 10)
var_jump = 3
# CSV LOG FILE (NON MODIFIED MESSAGES)
var_log_csv = 'data/logs.csv'
# CSV MESSAGE DATA FILE (MODIFIED MESSAGES)
var_messages_csv = 'data/messages.csv'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def create_log_csv(message):
    with open(var_log_csv, mode='a', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message.author.name, message.content])

def save_modified_message(modified_message, message):
    with open(var_messages_csv, mode='a', newline='') as messages_file:
        messages_writer = csv.writer(messages_file)
        messages_writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message.author.name, modified_message, 'FALSE'])

def create_log_embed(message):
    embed = discord.Embed(title=f"{message.author.name}#{message.author.discriminator} ({message.author.id})", description=f"{message.content}\nSent on {message.created_at}")
    return embed

def add_gresillement_and_jump(phrase, var_gresillement, var_jump, liste_gresillement):
    phrase_modifiee = ""
    for char in phrase:
        if random.uniform(0, 100) < var_gresillement:
            char = char + random.choice(liste_gresillement)
        if random.uniform(0, 100) < var_jump:
            char = "\_"
        phrase_modifiee += char
    return phrase_modifiee

@client.event
async def on_ready():
    channel = client.get_channel(var_bot_channel)
    await channel.purge()
    with open(var_messages_csv, mode='w', newline='') as messages_file:
        messages_file.seek(0)
        messages_file.truncate()


@client.event
async def on_message(message):
    try:
        if message.guild.id == var_bot_server and message.channel.id == var_bot_channel and message.author != client.user:
            await message.delete()
            modified_message = add_gresillement_and_jump(message.content, var_gresillement, var_jump, liste_gresillement)
            embed = discord.Embed(title="Radio Message", description=modified_message)
            await message.channel.send(embed=embed)
            await client.get_channel(var_log_channel).send(embed=create_log_embed(message))
            create_log_csv(message)
            save_modified_message(modified_message, message)
    except:
        if message.author != client.user and isinstance(message.channel, discord.DMChannel):
            if message.author in client.get_guild(var_bot_server).members:
                modified_message = add_gresillement_and_jump(message.content, var_gresillement, var_jump, liste_gresillement)
                embed = discord.Embed(title="Radio Message", description=modified_message)
                await client.get_channel(var_bot_channel).send(embed=embed)
                await client.get_channel(var_log_channel).send(embed=create_log_embed(message))
                create_log_csv(message)
                save_modified_message(modified_message, message)

client.run(var_bot_token)
