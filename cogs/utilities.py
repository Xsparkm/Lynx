import discord
from discord.ext import commands

import json
import requests

class Popcat(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def car(self,ctx):
      api = 'https://api.popcat.xyz/car'
      json_data = requests.get(api).json()
      image = json_data["image"]
      title = json_data['title']
      em = discord.Embed(description=title)
      em.set_image(url = image)
      await ctx.send(embed=em)

    @commands.command()  
    async def oogway(self,ctx,*,text):
      title=text.replace(' ','+')

      url = f'https://api.popcat.xyz/oogway?text={title}'
      await ctx.send(url)

    @commands.command()  
    async def sadcat(self,ctx,*,text):
      title=text.replace(' ','+')

      url = f'https://api.popcat.xyz/sadcat?text={title}'
      await ctx.send(url) 

    @commands.command()  
    async def site(self,ctx,*,text):
      url = f'https://api.popcat.xyz/screenshot?url={text}'
      await ctx.send(url)

    @commands.command()  
    async def wanted(self,ctx,member: discord.Member = None):
      member = ctx.author if not member else member
      av= member.avatar_url_as(format='png', size=1024)
      url = f'https://api.popcat.xyz/wanted?image={av}'
      await ctx.send(url)

    @commands.command()  
    async def gun(self,ctx,member: discord.Member = None):
      member = ctx.author if not member else member
      av= member.avatar_url_as(format='png', size=1024)
      url = f'https://api.popcat.xyz/gun?image={av}'
      await ctx.send(url)

    @commands.command()  
    async def opinion(self,ctx,member: discord.Member = None):
      member = ctx.author if not member else member
      av= member.avatar_url_as(format='png', size=1024)
      url = f'https://api.popcat.xyz/opinion?image={av}'
      await ctx.send(url)

    @commands.command()  
    async def drip(self,ctx,member: discord.Member = None):
      member = ctx.author if not member else member
      av= member.avatar_url_as(format='png', size=1024)
      url = f'https://api.popcat.xyz/drip?image={av}'
      await ctx.send(url)

    @commands.command()  
    async def clown(self,ctx,member: discord.Member = None):
      member = ctx.author if not member else member
      av= member.avatar_url_as(format='png', size=1024)
      url = f'https://api.popcat.xyz/clown?image={av}'
      await ctx.send(url)

    @commands.command()  
    async def ad(self,ctx,member: discord.Member = None):
      member = ctx.author if not member else member
      av= member.avatar_url_as(format='png', size=1024)
      url = f'https://api.popcat.xyz/ad?image={av}'
      await ctx.send(url)


    @commands.command()  
    async def pat(self,ctx,member: discord.Member = None):
      member = ctx.author if not member else member
      av= member.avatar_url_as(format='png', size=1024)
      url = f'https://api.popcat.xyz/pat?image={av}'
      await ctx.send(url)

    @commands.command()
    async def lyrics(self,ctx,*,name):
      api = f'https://api.popcat.xyz/lyrics?song={name}'
      data = requests.get(api).json()
      title = data['title']
      image = data['image']
      artist = data['artist']
      lyrics = data['lyrics']

      em = discord.Embed(title=f'{title} | {artist}',description=lyrics)
      em.set_image(url= image)
      await ctx.send(embed=em)

    @commands.command()
    async def element(self,ctx,*,name):
      api = f'https://api.popcat.xyz/periodic-table?element={name}'
      data = requests.get(api).json()
      element = data['name']
      symbol = data['symbol']
      an = data['atomic_number']
      am = data['atomic_mass']
      period = data['period']
      image = data['image']
      by = data['discovered_by']
      summary = data['summary']

      em = discord.Embed(title=f'{element} | {symbol}',description={summary})
      em.add_field(name='Atomic Number',value=an)
      em.add_field(name='Atomic Mass',value=am)
      em.add_field(name='Period',value=period)
      em.add_field(name='Discovered by',value=by)
      em.set_image(url=image)
      await ctx.send(embed=em)

    @commands.command()
    async def movie(self,ctx,*,name):
      api = f'https://api.popcat.xyz/imdb?q={name}'
      data = requests.get(api).json()
      
      rating = data['rating']
      title = data['title']
      rated = data['rated']
      realease = data["released"]
      genres = data['genres']
      director = data["director"]
      writer = data['writer']
      actors = data['actors']
      plot = data['plot']
      languages = data['languages']
      awards = data['awards']
      poster = data['poster']
      type = data['type']
      boxoffice = data['boxoffice']

      em = discord.Embed(title=title,description=plot)
      em.set_image(url=poster)
      em.add_field(name='director',value=director,inline=False)
      em.add_field(name='writer(s)',value=writer,inline=False)
      em.add_field(name='Type',value=type,inline=False)
      em.add_field(name='Release',value=realease,inline=False)
      em.add_field(name='Rated',value=rated,inline=False)
      em.add_field(name='Rating',value=rating,inline=False)
      em.add_field(name='Awards',value=awards,inline=False)
      em.add_field(name='Actors',value=actors,inline=False)
      em.add_field(name='Genres',value=genres,inline=False)
      em.add_field(name='Box office',value=boxoffice,inline=False)
      em.add_field(name='Languages',value=languages,inline=False)
      await ctx.send(embed=em)
      


async def setup(client):
    await client.add_cog(Popcat(client))                                                                  