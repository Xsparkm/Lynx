import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import os
from os import environ
from dotenv import load_dotenv
import wolframalpha
import sqlite3
from cogs.economy import Economy
import random
    
load_dotenv()
TOKEN = environ["TOKEN"]

client = commands.Bot(command_prefix="!",intents=discord.Intents.all())
client.remove_command('help')




@client.event
async def on_ready():
  print('Bot is online')
  try:
      synced = await client.tree.sync()
      print(f'synced {len(synced)} command')
  except Exception as e:
    print(e)

  

  
@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")


@client.command(aliases=["commands", "Commands",'cmd'])
async def help(ctx):
    em = discord.Embed(title='',description="__**List of commands**__ ",color=ctx.author.color)

    em.add_field(name="Anime", value="anime, quote, character, pokemon",
    inline=False)
    em.add_field(name='Games', value='akinator, slot, coinflip, guess',
    inline=False)
    em.add_field(name='Economy', value='gamble, work, balance, deposit, withdraw',
    inline=False)
    em.add_field(name='Utilities', value='wikipedia, translate, topic, gif ')

    em.set_footer(text=f"requested by {ctx.author.name}")

    await ctx.send(embed=em)    

#databse=========

@client.command(aliases=['bal','Balance', 'BALANCE'])
async def balance(ctx, member:discord.Member = None):
    if member is None:
        member = ctx.author

    db = sqlite3.connect('database/main.sqlite')
    cursor = db.cursor()

    cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {member.id}")    
    bal = cursor.fetchone()
    try:
        wallet = bal[0]
        bank = bal[1]
    except:
        wallet = 0
        bank = 0 

    em = discord.Embed(title=f"{member.name}'s Balance",color=ctx.author.top_role.colour)
    em.add_field(name='Wallet: ',value=f'{wallet} 💵',inline=False)
    em.add_field(name='Bank: ',value=f'{bank} 💵',inline=True)
    em.add_field(name='Networth: ',value=f'{bank+wallet} 💵',inline=True)

    em.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=em)


@client.command()
async def give(ctx, member:discord.Member,amount:int):
    if member is None:
        member = ctx.author

    db = sqlite3.connect('database/main.sqlite')
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM main")    
    bal = cursor.fetchone()
    try:
        wallet = bal[1]
    except:
        wallet = wallet

        cursor.execute('UPDATE main SET wallet = ? WHERE user_id = ?', (wallet+amount , member.id))   
        cursor.execute('UPDATE main SET wallet = ? WHERE user_id = ?', (wallet-amount , ctx.author.id))   
    db.commit()

    em = discord.Embed(description=f'{ctx.author.name.title()} successfully gave {amount} to {member.name.title()} ')
    await ctx.send(embed=em)

    cursor.close()
    db.close()

@client.command()
async def work(ctx):
    member = ctx.author
    amount = random.randint(100,1000)

    db = sqlite3.connect('database/main.sqlite')
    cursor = db.cursor()

    cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")    
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = 0

    chance = [1, 4]
    if chance == 2:
        return await ctx.send(
            "You worked so hard that you got fired from your office ecks deeeeee")
    else:
        amount = random.randrange(400, 600)
        outcomes = [
            f"You worked in your office for **{amount}**",
            f"Your boss was frustrated but you worked for him and got **{amount}**",
            f"You begged your boss for **{amount}**",
            f"You killed your boss and got **{amount}** from his wallet",
            f"You got a promotion! You earned **{amount}** today :D"
        ]

    sql = ('UPDATE main SET wallet = ? WHERE user_id = ?')
    val = (wallet + int(amount), member.id)
    cursor.execute(sql, val)

    em = discord.Embed(title = random.choice(outcomes) ,color=ctx.author.top_role.colour)
    em.add_field(name='Wallet: ',value=f'{wallet + int(amount)} 💵',inline=False)
    await ctx.send(embed=em)

    db.commit()
    cursor.close()
    db.close()


@client.command()
async def gamble(ctx, amount:int=1000):
    db = sqlite3.connect('database/main.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT wallet FROM main WHERE user_id = {ctx.author.id}')
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet

    if amount<500:
        return await ctx.send('You need to bet atleast 500 💵')    
    if wallet<amount:
        return await ctx.send("You don't have enough balance")
    
    user_strike = random.randint(1,15)
    bot_strike = random.randint(5, 15)

    if user_strike > bot_strike:
        percentage = random.randint(50,100)
        amount_won = int(amount*(percentage/100))
        cursor.execute('UPDATE main SET wallet = ? WHERE user_id = ?', (wallet + amount_won, ctx.author.id))
        db.commit()
        em = discord.Embed(description=f"You Won! **{amount_won}** 💵\nPercentage: **{percentage}%**\nNew Balance: **{wallet+amount_won}** 💵",color=ctx.author.top_role.colour)
        em.set_footer(text=f"Requested by {ctx.author}")

    elif user_strike < bot_strike:
        percentage = random.randint(0,80)
        amount_lost = int(amount*(percentage/100))
        cursor.execute('UPDATE main SET wallet = ? WHERE user_id = ?', (wallet - amount_lost, ctx.author.id))
        db.commit()
        em = discord.Embed(description=f"You Lost! **{amount_lost}** 💵\nPercentage: **{percentage}%**\nNew Balance: **{wallet-amount_lost}** 💵",color=ctx.author.top_role.colour)
        em.set_footer(text=f"Requested by {ctx.author}")

    else:
        em = discord.Embed(description=f'**It was a Tie**',color=ctx.author.top_role.colour)
        em.set_footer(text=f"Requested by {ctx.author}")

    em.add_field(name=f"**{ctx.author.name.title()}**", value=f'Strikes {user_strike}')
    em.add_field(name=f"**{ctx.bot.user.name.title()}**", value=f'Strikes {bot_strike}')
    await ctx.send(embed=em)

    cursor.close()
    db.close()


@client.command()
async def deposit(ctx, amount:int):
    db = sqlite3.connect('database/main.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM main WHERE user_id = {ctx.author.id}')
    data  = cursor.fetchone()

    try:
        wallet = data[1]
        bank = data[2]
    except:
        await ctx.send("Some Error occured!")

    if wallet< amount:
        return await ctx.send("You don't have enought money too deposit")    

    else: 
        cursor.execute('UPDATE main SET bank = ? WHERE user_id = ?', (bank+amount , ctx.author.id))   
        cursor.execute('UPDATE main SET wallet = ? WHERE user_id = ?', (wallet-amount , ctx.author.id))   

        em = discord.Embed(description=f'Successfully deposited **{amount}** 💵 to your Bank account',color=ctx.author.top_role.colour)
        em.add_field(name='Wallet: ',value=f'{wallet-amount} 💵',inline=False)
        em.add_field(name='Bank: ',value=f'{bank+amount} 💵',inline=True)
        em.add_field(name='Networth: ',value=f'{bank+wallet} 💵',inline=True)

        em.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=em)
    db.commit()
    cursor.close()
    db.close()

@client.command()
async def addbal(ctx, member:discord.Member,amount:int):
    db = sqlite3.connect('database/main.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT wallet FROM main WHERE user_id = {member.id}')
    data  = cursor.fetchone()
    
    try:
        wallet = wallet[0]
    except:
        wallet = wallet
    
    cursor.execute('UPDATE main SET wallet = ? WHERE user_id = ?',(wallet+amount, member.id))
    em = discord.Embed(description=f"Successfully added {amount} to  {member.display_name()}'s account",color=ctx.author.top_role.colour)
    em.add_field(name='Wallet: ',value=f'{wallet + amount} 💵',inline=False)
    await ctx.send(embed=em)

    db.commit()
    cursor.close()
    db.close()


@client.command()
async def withdraw(ctx, amount:int):
    db = sqlite3.connect('database/main.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM main WHERE user_id = {ctx.author.id}')
    data  = cursor.fetchone()

    try:
        wallet = data[1]
        bank = data[2]
    except:
        await ctx.send("Some Error occured!")

    if bank< amount:
        return await ctx.send("You don't have enought money too withdraw")    

    else:
        cursor.execute('UPDATE main SET bank = ? WHERE user_id = ?', (bank - amount , ctx.author.id))   
        cursor.execute('UPDATE main SET wallet = ? WHERE user_id = ?', (wallet + amount , ctx.author.id))   
        
        em = discord.Embed(description=f'Successfully withdrawed {amount} to your Bank account',color=ctx.author.top_role.colour)
        em.add_field(name='Wallet: ',value=f'{wallet + amount} 💵',inline=False)
        em.add_field(name='Bank: ',value=f'{bank - amount} 💵',inline=True)
        em.add_field(name='Networth: ',value=f'{bank+wallet} 💵',inline=True) 

        em.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=em)

    db.commit()
    cursor.close()
    db.close()



#cogs======= 

@client.command()
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} has loaded')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} has unloaded')

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")



async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)

asyncio.run(main())






#rough work 

#database embed
    # embed = discord.Embed(color=discord.Color.blue , timestamp=ctx.message.created_at)
    # embed.set_author(name=f"{member.name}'s Balance", icon_url=member.avatar_url)
    # embed.add_field(name="Wallet", value= wallet)
    # embed.add_field(name="Bank", value= bank)
    # embed.set_footer(text=f"Requested by {ctx.author}", icon_url=member.avatar_url)
    # embed.set_thumbnail(url=ctx.guild.icon_url)

    # await ctx.send(embed=embed)


#     em = discord.Embed(title=f"{member.name}'s Balance",color=discord.Color.blue)
    # em.add_field(name="👛 | Wallet", value= f'{wallet} 💵')
    # em.add_field(name="🏦 | Bank", value= f'{bank} 💵')
    # em.add_field(name="💸 | Networth", value= f'{bank+wallet} 💵')

    # em.set_footer(text=f"Requested by {ctx.author}", icon_url=member.avatar_url)


    # await ctx.send(embed=em)

# 
    # try:
    #     amount = int(amount)
    # except ValueError:
    #     pass
    # if type(amount) == str:
    #     if amount.lower() == 'max' or amount.lower() == 'all':
    #         amount = int(wallet)
    # else:
    #     amount = int(amount)
#