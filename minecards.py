import discord
from discord.utils import get

import os
import dotenv
from dotenv import load_dotenv

import sqlite3
import random


#only activate this if new table added or old database deleted
def make_db():
    #Connecting to database
    conn = sqlite3.connect("MineCards.db")

    #Creating the tables
    conn.execute("CREATE TABLE IF NOT EXISTS Cards(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name VARCHAR(20),category VARCHAR(10))")
    conn.execute("CREATE TABLE IF NOT EXISTS Profiles(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,username VARCHAR(40),stone INT, wood INT)")

    #Closing the connection
    conn.close()



def claim_card():
    rand_card = random.randint(1,2)
    common = random.randint(2,5)
    if rand_card == 1:
        card = "+" + str(common) + " Stone"
    elif rand_card == 2:
        card = "+" + str(common) + " Wood"
    else:
        print("CLAIM FAILED! BEEP BOOP BUG FOUND!")

    return card



def new_profile(user):
    #Connecting to database and creating a cursor to navigate the database
    conn = sqlite3.connect("MineCards.db")
    cursor = conn.cursor()

    #Check if username is already in the Profiles table
    cursor.execute("SELECT Username FROM Profiles WHERE Username = '" + user + "'")

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


        values = [user,0,0]

        #Connecting to database and creating a cursor to navigate the database
        conn = sqlite3.connect("MineCards.db")
        cursor = conn.cursor()

        cursor.execute(sql,values) #Inserting the data
        conn.commit()           #Saving the entry

        #Closing the connections
        cursor.close()
        conn.close()

        return found

    #Do nothing if username was found
    else:
        return found


### --------------------- MAIN --------------------- ###
client = discord.Client()

load_dotenv()
token = os.getenv("TOKEN")

@client.event
async def on_message(message):
    message.content = message.content.lower()

    #Prevents bot from seeing own messages
    if message.author == client.user:
        return

    ### Main ###
    if message.content.startswith(".minecards") or message.content.startswith(".mc"):
        if "claim" in message.content:
            card = claim_card()

            embed = discord.Embed(title="You picked up a new card!", color=0x00fff0)
            embed.add_field(name="Card:", value=card, inline=False)
            await message.channel.send(embed=embed)



        #Allow user to view their profile
        elif "profile" in message.content:
            await message.channel.send("PROFILE PLACEHOLDER")


        #Make a new profile for user
        elif "new" in message.content:
            user = str(message.author)
            existing = new_profile(user)

            if existing == True:
                await message.channel.send("You already have a profile!")
            else:
                await message.channel.send("New profile created. To view your profile, do .minecards profile")


        #Invalid command
        else:
            await message.channel.send("Invalid command, to see a list of commands do .minecards help")

        #if str(message.author) == "AnimatorOfSouls#2980":


client.run(token)
