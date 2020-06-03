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
bot = Bot(command_prefix="cat ")

bot.remove_command("help")

#Dict of all the cat emojis
cat_emoji = {
            "whitecat":"<:whitecat:715949337007489096>",
            "bluecat":"<:bluecat:715949337208684585>",
            "greencat":"<:greencat:715949337196101634>",
            "orangecat":"<:orangecat:715949337338708090>",
            "redcat":"<:redcat:715949337393233980>",
            "pinkcat":"<:pinkcat:715949337607274497>",
            "purplecat":"<:purplecat:715949337208815627>",
            }

#Dict of cat exp values
cat_exp = {
            "whitecat":2,
            "bluecat":4,
            "greencat":8,
            "orangecat":16,
            "redcat":32,
            "pinkcat":64,
            "purplecat":128,
            }



#For bot owner use only!!! Make fresh database if not already existing
def make_db():
    #Connecting to database
    conn = sqlite3.connect("KittyMiner.db")

    #Creating the tables
    conn.execute("CREATE TABLE IF NOT EXISTS Profiles(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,userid VARCHAR(40),level INT,exp REAL,whitecat INT, bluecat INT, greencat INT, orangecat INT, redcat INT, pinkcat INT, purplecat INT)")

    #Closing the connection
    conn.close()



#Allows user to claim a card
@bot.command(pass_context=True,aliases=["m"])
@commands.cooldown(1, 5, commands.BucketType.user)
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
        added_amount = random.randint(6,8)

    elif rarity[0] == "blue":
        type = "bluecat"
        added_amount = random.randint(5,8)

    elif rarity[0] == "green":
        type = "greencat"
        added_amount = random.randint(4,7)

    elif rarity[0] == "orange":
        type = "orangecat"
        added_amount = random.randint(3,6)

    elif rarity[0] == "red":
        type = "redcat"
        added_amount = random.randint(3,5)

    elif rarity[0] == "pink":
        type = "pinkcat"
        added_amount = random.randint(3,4)

    elif rarity[0] == "purple":
        type = "purplecat"
        added_amount = random.randint(2,4)


    ## Database stuff
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Finding the amount of cards in the player's inventory
    cursor.execute("SELECT "+type+",exp FROM Profiles WHERE userid = '" + str(ctx.message.author.id) + "'")
    result = cursor.fetchall()

    old_amount = result[0][0]
    old_exp = result[0][1]

    #Calculating the new total of the type of card
    new_amount = old_amount + added_amount
    new_exp = old_exp + cat_exp[type]

    levelup = False
    if new_exp >= 100:
        #Finding the amount of levels
        cursor.execute("SELECT level FROM Profiles WHERE userid = '" + str(ctx.message.author.id) + "'")
        result_level = cursor.fetchall()
        new_level = result_level[0][0] + 1

        sql = "UPDATE Profiles SET level = "+str(new_level)+" WHERE userid = '" + str(ctx.message.author.id) + "'"
        cursor.execute(sql)     #Updating
        conn.commit()           #Saving the entry

        new_exp -= 100
        levelup = True




    card = str(added_amount) + "x " + cat_emoji[type] + type + " (+"+str(cat_exp[type])+" exp)"


    #Updating values
    sql = "UPDATE Profiles SET " + type + " = " + str(new_amount) + ", exp = "+str(new_exp)+" WHERE userid = '" + str(ctx.message.author.id) + "'"

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

    if levelup == True:
        ##Embed display
        embed = discord.Embed(title="Level Up!", color=0x00fff0)
        embed.add_field(name="Level: ", value=new_level, inline=False)
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
    cursor.execute("SELECT userid FROM Profiles WHERE userid = '" + str(ctx.message.author.id) + "'")

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
        sql = "INSERT INTO Profiles (userid,level,exp,whitecat,bluecat,greencat,orangecat,redcat,pinkcat,purplecat) VALUES (?,?,?,?,?,?,?,?,?,?)"


        values = [str(ctx.message.author.id),1,0,0,0,0,0,0,0,0]

        #Connecting to database and creating a cursor to navigate the database
        conn = sqlite3.connect("KittyMiner.db")
        cursor = conn.cursor()

        cursor.execute(sql,values) #Inserting the data
        conn.commit()           #Saving the entry

        #Closing the connections
        cursor.close()
        conn.close()

        await ctx.message.channel.send("New profile created. To view your profile, do 'cat profile'. To see a list of commands, do 'cat help'.")


    #Do nothing if username was found
    else:
        await ctx.message.channel.send("You already have a profile!")



#Shows the user's inventory
@bot.command(pass_context=True,aliases=["inv"])
async def inventory(ctx):
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Selecting all cat types from table
    cursor.execute("SELECT whitecat,bluecat,greencat,orangecat,redcat,pinkcat,purplecat FROM Profiles WHERE userid = '" + str(ctx.message.author.id) + "'")

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
    embed.add_field(name="Cats:", value=cat_emoji["whitecat"]+" White Cats: " + str(inv[0][0]) + "\n"+cat_emoji["bluecat"]+" Blue Cats: " + str(inv[0][1]) + "\n"+cat_emoji["greencat"]+"Green Cats: " + str(inv[0][2]) + "\n"+cat_emoji["orangecat"]+" Orange Cats: " + str(inv[0][3]) + "\n"+cat_emoji["redcat"]+" Red Cats: " + str(inv[0][4]) + "\n"+cat_emoji["pinkcat"]+" Pink Cats: " + str(inv[0][5]) + "\n"+cat_emoji["purplecat"]+" Purple Cats: "+ str(inv[0][6]), inline=False)

    await ctx.message.channel.send(embed=embed)



#Shows the user's profile
@bot.command(pass_context=True,aliases=["p"])
async def profile(ctx):
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Selecting all cat types from table
    cursor.execute("SELECT level,exp FROM Profiles WHERE userid = '" + str(ctx.message.author.id) + "'")

    result = cursor.fetchall()

    selected = []

    for row in result:
        selected.append(row)

    #Closing the connections
    cursor.close()
    conn.close()



    embed = discord.Embed(title="Profile:", color=0x7C8ED0)
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.add_field(name="Username:", value=ctx.message.author, inline=False)
    embed.add_field(name="Level:", value=selected[0][0], inline=False)
    embed.add_field(name="Exp:", value=selected[0][1], inline=False)

    await ctx.message.channel.send(embed=embed)



#profile error handler
@profile.error
async def info_error(ctx,error):
    await ctx.message.channel.send("Welcome to Kitty Miner! To get started, type 'cat newprofile'. To see a list of commands, type 'cat help'.")



#Shows commands
@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Commands:", color=0x7C8ED0)
    embed.add_field(name="Info:", value="newprofile\nprofile (p)\ntiers", inline=False)
    embed.add_field(name="Game:", value="mine (m)\ninventory (inv)\nrecipes\ncraft\ntrade", inline=False)

    await ctx.message.channel.send(embed=embed)



#Shows crafting recipe
@bot.command(pass_context=True)
async def recipes(ctx):
    embed = discord.Embed(title="Recipes:", color=0x7C8ED0)
    embed.add_field(name="Cats:", value="[blue] 5 whitecat -> 1 bluecat\n[green] 5 bluecat -> 1 greencat\n[orange] 5 greencat -> 1 orangecat\n[red] 4 orangecat -> 1 redcat\n[pink] 4 redcat -> 1 pinkcat\n[purple] 4 pinkcat -> 1 purplecat", inline=False)

    await ctx.message.channel.send(embed=embed)



#Crafting cats
@bot.command(pass_context=True)
async def craft(ctx, recipe):
    recipe = recipe.lower()



    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Check if username is already in the Profiles table
    cursor.execute("SELECT whitecat,bluecat,greencat,orangecat,redcat,pinkcat,purplecat FROM Profiles WHERE userid = '" + str(ctx.message.author.id) + "'")

    result = cursor.fetchall()

    inv = []

    for row in result:
        inv.append(row)



    if recipe == "blue":
        component = "whitecat"
        crafted = "bluecat"
        num_needed = 5
    elif recipe == "green":
        component = "bluecat"
        crafted = "greencat"
        num_needed = 5
    elif recipe == "orange":
        component = "greencat"
        crafted = "orangecat"
        num_needed = 5
    elif recipe == "red":
        component = "orangecat"
        crafted = "redcat"
        num_needed = 4
    elif recipe == "pink":
        component = "redcat"
        crafted = "pinkcat"
        num_needed = 4
    elif recipe == "purple":
        component = "pinkcat"
        crafted = "purplecat"
        num_needed = 4
    else:
        await ctx.message.channel.send("What are you trying to craft? (cat craft recipeID)")



    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Check if username is already in the Profiles table
    cursor.execute("SELECT " + component + "," + crafted + " FROM Profiles WHERE userid = '" + str(ctx.message.author.id) + "'")

    result = cursor.fetchall()

    inv = []

    for row in result:
        inv.append(row)


    cont = True
    #checking if the user has enough of the components
    if inv[0][0] < num_needed:
        await ctx.message.channel.send("You dont have enough " + component + "s!")
        cont = False
    else:
        component_final = inv[0][0]-num_needed
        crafted_final = inv[0][1]+1



    if cont == True:
        sql = "UPDATE Profiles SET " + component + " = " + str(component_final) + "," + crafted + " = " + str(crafted_final) + " WHERE userid = '" + str(ctx.message.author.id) + "'"

        cursor.execute(sql)     #Updating
        conn.commit()           #Saving the entry


        embed = discord.Embed(title="You successfully crafted an item!", color=0x7C8ED0)
        embed.add_field(name="Username:", value=ctx.message.author, inline=False)
        embed.add_field(name="Crafted:", value= crafted + " x1", inline=False)

        await ctx.message.channel.send(embed=embed)


    #Closing the connections
    cursor.close()
    conn.close()



#craft error handler
@craft.error
async def info_error(ctx,error):
    await ctx.message.channel.send("What are you trying to craft? (cat craft recipeID)")



#Trading cats between players
@bot.command(pass_context=True)
async def trade(ctx,player,tcat,amount):

    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("KittyMiner.db")
    cursor = conn.cursor()

    #Get how many of tcat the message author has
    cursor.execute("SELECT " + tcat + " FROM Profiles WHERE userid = '" + str(ctx.message.author.id) + "'")

    result = cursor.fetchall()

    giver_inv = []

    for row in result:
        giver_inv.append(row)


    if int(giver_inv[0][0]) < int(amount):
        await ctx.message.channel.send("You dont have enough to be able to trade.")
    elif str(ctx.message.author.id) == str(player[3:-1]):
        await ctx.message.channel.send("You can't trade with yourself!")
    else:
        #Get how many of tcat the reciever has
        cursor.execute("SELECT " + tcat + " FROM Profiles WHERE userid = '" + str(player[3:-1]) + "'")

        result = cursor.fetchall()

        reciever_inv = []

        for row in result:
            reciever_inv.append(row)


        #Calculating new totals
        giv_new_total = int(giver_inv[0][0]) - int(amount)
        rec_new_total = int(reciever_inv[0][0]) + int(amount)


        giv_sql = "UPDATE Profiles SET " + tcat + " = " + str(giv_new_total) + " WHERE userid = '" + str(ctx.message.author.id) + "'"
        rec_sql = "UPDATE Profiles SET " + tcat + " = " + str(rec_new_total) + " WHERE userid = '" + str(player[3:-1]) + "'"

        cursor.execute(giv_sql)     #Updating
        cursor.execute(rec_sql)
        conn.commit()           #Saving the entry



        #Setting the url for the cat image
        if tcat == "whitecat":
            caturl = "https://cdn.discordapp.com/emojis/715949337007489096.png?v=1"
        elif tcat == "bluecat":
            caturl = "https://cdn.discordapp.com/emojis/715949337208684585.png?v=1"
        elif tcat == "greencat":
            caturl = "https://cdn.discordapp.com/emojis/715949337196101634.png?v=1"
        elif tcat == "orangecat":
            caturl = "https://cdn.discordapp.com/emojis/715949337338708090.png?v=1"
        elif tcat == "redcat":
            caturl = "https://cdn.discordapp.com/emojis/715949337393233980.png?v=1"
        elif tcat == "pinkcat":
            caturl = "https://cdn.discordapp.com/emojis/715949337607274497.png?v=1"
        elif tcat == "purplecat":
            caturl = "https://cdn.discordapp.com/emojis/715949337208815627.png?v=1"


        #Making embed
        embed = discord.Embed(title="Trade Successful!", color=0x7C8ED0)
        embed.set_thumbnail(url=caturl)
        embed.add_field(name="Kitty Giver:", value=ctx.message.author, inline=False)
        embed.add_field(name="Kitty Traded:", value=tcat + " x" + str(amount), inline=False)

        await ctx.message.channel.send(embed=embed)



    #Closing the connections
    cursor.close()
    conn.close()



#trade error handler
@trade.error
async def info_error(ctx,error):
    await ctx.message.channel.send("Invalid command. Do 'cat trade @username cattype amount'.\nMake sure the other person has a profile made (cat newprofile)")





#-------------------------TOKEN---------------------------------#
load_dotenv()
token = os.getenv("TOKEN")

bot.run(token)
