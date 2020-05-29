import discord
from discord import Embed, Emoji
from discord.ext.commands import Bot
from discord.utils import get
from discord.ext import commands

import os
import dotenv
from dotenv import load_dotenv

import sqlite3
import random
#-----------------------------MAIN------------------------------#
bot = Bot(command_prefix=".cat ")

bot.remove_command("help")



#For bot owner use only!!! Make fresh database if not already existing
def make_db():
    #Connecting to database
    conn = sqlite3.connect("KittyMiner.db")

    #Creating the tables
    conn.execute("CREATE TABLE IF NOT EXISTS Profiles(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,username VARCHAR(40),whitecat INT, bluecat INT, greencat INT, orangecat INT, redcat INT, pinkcat INT, purplecat INT)")

    #Closing the connection
    conn.close()



#Allows user to claim a card
@bot.command(pass_context=True,aliases=["m"])
@commands.cooldown(1, 15, commands.BucketType.user)
async def mine(ctx):
    #Picking the rarity based on the weights
    rarities = ["white","blue","green","orange","red","pink","purple"]
    weights = [0.5,0.3,0.1,0.05,0.03,0.01,0.005]
    rarity = random.choices(rarities, weights, k=1)



    #Choosing a card in the chosen rarity tier.
    if rarity[0] == "white":
        '''
        This is the code to use if there is more than 1 cat in a rarity

        rand_type = random.choice(["cat1","cat2"])
        type = rand_type
        '''

        type = "whitecat"
        emoji = "<:whitecat:715949337007489096>"
        added_amount = random.randint(6,8)

    elif rarity[0] == "blue":
        type = "bluecat"
        emoji = "<:bluecat:715949337208684585>"
        added_amount = random.randint(5,8)

    elif rarity[0] == "green":
        type = "greencat"
        emoji = "<:greencat:715949337196101634>"
        added_amount = random.randint(4,7)

    elif rarity[0] == "orange":
        type = "orangecat"
        emoji = "<:orangecat:715949337338708090>"
        added_amount = random.randint(3,6)

    elif rarity[0] == "red":
        type = "redcat"
        emoji = "<:redcat:715949337393233980>"
        added_amount = random.randint(3,5)

    elif rarity[0] == "pink":
        type = "pinkcat"
        emoji = "<:pinkcat:715949337607274497>"
        added_amount = random.randint(3,4)

    elif rarity[0] == "purple":
        type = "purplecat"
        emoji = "<:purplecat:715949337208815627>"
        added_amount = random.randint(2,4)



    ## Database stuff
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Finding the amount of cards in the player's inventory
    cursor.execute("SELECT "+type+" FROM Profiles WHERE Username = '" + str(ctx.message.author) + "'")
    result = cursor.fetchall()

    old_amount = result[0][0]



    #Calculating the new total of the type of card
    new_amount = old_amount + added_amount
    card = str(added_amount) + "x " + emoji + type



    #Updating values
    sql = "UPDATE Profiles SET " + type + " = " + str(new_amount) + " WHERE username = '" + str(ctx.message.author) + "'"

    cursor.execute(sql)     #Updating
    conn.commit()           #Saving the entry


    #Closing the connections
    cursor.close()
    conn.close()



    ##Embed display
    embed = discord.Embed(title="You picked up a new cat!", color=0x00fff0)
    embed.add_field(name="Cat:", value=card, inline=False)
    embed.add_field(name="Total:", value=new_amount, inline=False)
    await ctx.message.channel.send(embed=embed)



#mine cooldown handler
@mine.error
async def info_error(ctx,error):
    await ctx.message.channel.send("Miner on cooldown, please wait "+ str(round(error.retry_after,1)) +" seconds.")



#Displays different tiers of cards in order of most common to least common
@bot.command(pass_context=True)
async def tiers(ctx):
    embed = discord.Embed(title="Cat Tiers:", color=0x00fff0)
    embed.add_field(name="Most Common -> Least Common", value="<:white:715571455370199101> White\n<:blue:715573192185610341> Blue\n<:green:715573216130629682> Green\n<:orange:715573223965851668> Orange\n<:red:715573238004056084> Red\n<:pink:715573244916400279> Pink\n<:purple:715573253808062555> Purple", inline=False)
    await ctx.message.channel.send(embed=embed)



#Makes a new profile for a new user
@bot.command(pass_context=True)
async def newprofile(ctx):
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Check if username is already in the Profiles table
    cursor.execute("SELECT Username FROM Profiles WHERE Username = '" + str(ctx.message.author) + "'")

    result = cursor.fetchall()

    returned = ""

    for row in result:
        returned = row

    if returned == "":
        found = False
    else:
        found = True

    #Closing the connections
    cursor.close()
    conn.close()



    #Creating a new profile if the username wasn't found
    if found == False:
        #sql INSERT, and values to be inserted
        sql = "INSERT INTO Profiles (username,whitecat,bluecat,greencat,orangecat,redcat,pinkcat,purplecat) VALUES (?,?,?,?,?,?,?,?)"


        values = [str(ctx.message.author),0,0,0,0,0,0,0]

        #Connecting to database and creating a cursor to navigate the database
        conn = sqlite3.connect("KittyMiner.db")
        cursor = conn.cursor()

        cursor.execute(sql,values) #Inserting the data
        conn.commit()           #Saving the entry

        #Closing the connections
        cursor.close()
        conn.close()

        await ctx.message.channel.send("New profile created. To view your profile, do .cat profile")


    #Do nothing if username was found
    else:
        await ctx.message.channel.send("You already have a profile!")



#Shows the user's inventory
@bot.command(pass_context=True,aliases=["inv"])
async def inventory(ctx):
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Check if username is already in the Profiles table
    cursor.execute("SELECT whitecat,bluecat,greencat,orangecat,redcat,pinkcat,purplecat FROM Profiles WHERE username = '" + str(ctx.message.author) + "'")

    result = cursor.fetchall()

    inv = []

    for row in result:
        inv.append(row)

    #Closing the connections
    cursor.close()
    conn.close()


    #Creating embed
    embed = discord.Embed(title="Inventory:", color=0x7C8ED0)
    embed.add_field(name="Username:", value=ctx.message.author, inline=False)
    embed.add_field(name="Cats:", value="<:whitecat:715949337007489096> White Cats: " + str(inv[0][0]) + "\n<:bluecat:715949337208684585> Blue Cats: " + str(inv[0][1]) + "\n<:greencat:715949337196101634> Green Cats: " + str(inv[0][2]) + "\n<:orangecat:715949337338708090> Orange Cats: " + str(inv[0][3]) + "\n<:redcat:715949337393233980> Red Cats: " + str(inv[0][4]) + "\n<:pinkcat:715949337607274497> Pink Cats: " + str(inv[0][5]) + "\n<:purplecat:715949337208815627> Purple Cats: "+ str(inv[0][6]), inline=False)

    await ctx.message.channel.send(embed=embed)



#Shows the user's profile
@bot.command(pass_context=True,aliases=["p"])
async def profile(ctx):
    embed = discord.Embed(title="Profile:", color=0x7C8ED0)
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.add_field(name="Username:", value=ctx.message.author, inline=False)

    await ctx.message.channel.send(embed=embed)



#Shows commands
@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Commands:", color=0x7C8ED0)
    embed.add_field(name="Info:", value="newprofile\nprofile (p)\ntiers", inline=False)
    embed.add_field(name="Game:", value="mine (m)\ninventory (inv)", inline=False)

    await ctx.message.channel.send(embed=embed)



#-------------------------TOKEN---------------------------------#
load_dotenv()
token = os.getenv("TOKEN")

bot.run(token)
