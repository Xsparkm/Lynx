import requests 
import discord
from discord.ext import commands
import animec
from animec import anicore


class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def anime(self,ctx,*,name):
        r = anicore.Anime(name)
        desc = r.description
        desc2 = desc[0:500]

        em = discord.Embed(title= f":white_flower: | {r.name}",description=desc2,color=discord.Colour.blue())
        em.add_field(name="Status",value=f":ribbon: | {r.status}",inline=False)
        em.add_field(name="Genres",value=f":white_flower: | {r.genres}",inline=False)        
        em.add_field(name="Episodes",value=f":film_frames: | {r.episodes}",inline=False)
        em.add_field(name="Rating",value=f":scroll: | {r.rating}",inline=False)
        em.add_field(name="Ranking",value=f":medal: | {r.ranked}",inline=False)
        em.add_field(name="Popularity",value=f"{r.popularity}",inline=False)
        em.add_field(name="Favorites",value=f":thumbsup: | {r.favorites}",inline=False)
        em.add_field(name="Type",value=f":tv: | {r.type}",inline=False)
        em.add_field(name="Producer",value=f":film_frames: | {r.producers}",inline=False)
        em.set_thumbnail(url=r.poster)
        await ctx.send(embed =em)

    @commands.command()     
    async def quote(self,ctx):
        response = requests.get("https://animechan.vercel.app/api/random")
        data = response.json()
        em = discord.Embed(title="Anime Quote",description=data['quote'],color=discord.Colour.blue())
        em.set_footer(text=f"{data['character']}, {data['anime']}")
        await ctx.send(embed=em)

    @commands.command()
    async def character(self,ctx,*,charecter: str):
        char = animec.Charsearch(charecter)
        await ctx.send(char.image_url)


async def setup(client):
    await client.add_cog(Anime(client))
