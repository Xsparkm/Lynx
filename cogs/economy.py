import discord
import sqlite3
import random
from discord.ext import commands

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        db  = sqlite3.connect("database/main.sqlite")
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS main (
            user_id INTERGER, wallet INTERGER, bank INTERGER
        )''')
        print("Bot Is Online")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        author = message.author
        db  = sqlite3.connect("database/main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM main WHERE user_id = {author.id}")
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO main(user_id, wallet, bank) VALUES(?,?,?)"
            val = (message.author.id, 100, 0)
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()
    


async def setup(client):
    await client.add_cog(Economy(client))