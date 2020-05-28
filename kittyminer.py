import discord
from discord import Embed, Emoji
from discord.ext.commands import Bot
from discord.utils import get

import os
import dotenv
from dotenv import load_dotenv

import sqlite3
import random
#-----------------------------MAIN------------------------------#
bot = Bot(command_prefix=".mc ")



#For bot owner use only!!! Make fresh database if not already existing
def make_db():
    #Connecting to database
    conn = sqlite3.connect("KittyMiner.db")

    #Creating the tables
    conn.execute("CREATE TABLE IF NOT EXISTS Profiles(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,username VARCHAR(40),purplecat INT, bluecat INT)")

    #Closing the connection
    conn.close()


#Allows user to claim a card
@bot.command(pass_context=True)
async def claim(ctx):
    #Picking the rarity based on the weights
    rarities = ["white","blue","green","orange","red","pink","purple"]
    weights = [0.5,0.3,0.1,0.05,0.03,0.01,0.005]
    rarity = random.choices(rarities, weights, k=1)



    #Choosing a card in the chosen rarity tier.
    if rarity[0] == "white":
        print("white")
        rand_type = random.choice(["wood","stone"])
        type = rand_type

        added_amount = random.randint(5,10)

    elif rarity[0] == "blue":
        print("blue")
    elif rarity[0] == "green":
        print("green")
    elif rarity[0] == "orange":
        print("orange")
    elif rarity[0] == "red":
        print("red")
    elif rarity[0] == "pink":
        print("pink")
    elif rarity[0] == "purple":
        print("purple")



    ## Database stuff
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("MineCards.db")
    cursor = conn.cursor()

    #Finding the amount of cards in the player's inventory
    cursor.execute("SELECT "+type+" FROM Profiles WHERE Username = '" + str(ctx.message.author) + "'")
    result = cursor.fetchall()

    old_amount = result[0][0]



    #Calculating the new total of the type of card
    if rarity[0] == "white":
        new_amount = old_amount + added_amount
        card = str(added_amount) + "x " + type
    elif rarity[0] == "blue":
        print("blue")
    elif rarity[0] == "green":
        print("green")
    elif rarity[0] == "orange":
        print("orange")
    elif rarity[0] == "red":
        print("red")
    elif rarity[0] == "pink":
        print("pink")
    elif rarity[0] == "purple":
        print("purple")



    #Updating values
    sql = "UPDATE Profiles SET " + type + " = " + str(new_amount) + " WHERE username = '" + str(ctx.message.author) + "'"

    cursor.execute(sql)     #Updating
    conn.commit()           #Saving the entry


    #Closing the connections
    cursor.close()
    conn.close()



    ##Embed display
    embed = discord.Embed(title="You picked up a new card!", color=0x00fff0)
    embed.add_field(name="Card:", value=card, inline=False)
    embed.add_field(name="Total:", value=new_amount, inline=False)
    await ctx.message.channel.send(embed=embed)



#Displays different tiers of cards in order of most common to least common
@bot.command(pass_context=True)
async def tiers(ctx):
    embed = discord.Embed(title="Card Tiers:", color=0x00fff0)
    embed.add_field(name="Most Common -> Least Common", value="<:white:715571455370199101> White\n<:blue:715573192185610341> Blue\n<:green:715573216130629682> Green\n<:orange:715573223965851668> Orange\n<:red:715573238004056084> Red\n<:pink:715573244916400279> Pink\n<:purple:715573253808062555> Purple", inline=False)
    await ctx.message.channel.send(embed=embed)



#Makes a new profile for a new user
@bot.command(pass_context=True)
async def newprofile(ctx):
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("MineCards.db")
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
        sql = "INSERT INTO Profiles (username,stone,wood) VALUES (?,?,?)"


        values = [str(ctx.message.author),0,0]

        #Connecting to database and creating a cursor to navigate the database
        conn = sqlite3.connect("MineCards.db")
        cursor = conn.cursor()

        cursor.execute(sql,values) #Inserting the data
        conn.commit()           #Saving the entry

        #Closing the connections
        cursor.close()
        conn.close()

        await ctx.message.channel.send("New profile created. To view your profile, do .minecards profile")


    #Do nothing if username was found
    else:
        await ctx.message.channel.send("You already have a profile!")



#Shows the user's inventory
@bot.command(pass_context=True)
async def inventory(ctx):
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("MineCards.db")
    cursor = conn.cursor()

    #Check if username is already in the Profiles table
    cursor.execute("SELECT wood,stone FROM Profiles WHERE username = '" + str(ctx.message.author) + "'")

    result = cursor.fetchall()

    inv = []

    for row in result:
        inv.append(row)

    #Closing the connections
    cursor.close()
    conn.close()


    #Creating embed
    wood = inv[0][0]
    stone = inv[0][1]

    embed = discord.Embed(title="Inventory:", color=0x7C8ED0)
    embed.add_field(name="Username:", value=ctx.message.author, inline=False)
    embed.add_field(name="Wood:", value=wood, inline=False)
    embed.add_field(name="Stone:", value=stone, inline=False)


    await ctx.message.channel.send(embed=embed)



#Shows the user's profile
@bot.command(pass_context=True)
async def profile(ctx):
    embed = discord.Embed(title="Profile:", color=0x7C8ED0)
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.add_field(name="Username:", value=ctx.message.author, inline=False)

    await ctx.message.channel.send(embed=embed)




#-------------------------TOKEN---------------------------------#
load_dotenv()
token = os.getenv("TOKEN")

bot.run(token)
