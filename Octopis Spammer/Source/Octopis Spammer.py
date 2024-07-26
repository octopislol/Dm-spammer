import discord
import asyncio
import aiohttp

# Read bot tokens from tokens.txt
def read_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = file.readlines()
    return [token.strip() for token in tokens]

# Send DM using a bot token
async def send_dm(token, user_id, message, count, emoji=None, emoji_count=0):
    intents = discord.Intents.default()
    intents.messages = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            user = await client.fetch_user(user_id)
            emoji_str = emoji * emoji_count if emoji else ""
            full_message = message + emoji_str
            for _ in range(count):
                await user.send(full_message)
            print(f"[+] Sent {count} DMs to user {user_id}.")
        except Exception as e:
            print(f"[-] Error sending DM: {e}")
        finally:
            await client.close()

    try:
        await client.start(token)
    except Exception as e:
        print(f"[-] Error starting bot with token {token}: {e}")

# Send message to a server channel
async def send_to_channel(token, server_id, channel_id, message, count, ping_everyone):
    intents = discord.Intents.default()
    intents.messages = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            guild = client.get_guild(server_id)
            if guild is None:
                raise Exception("Guild not found. Check server ID.")
            channel = guild.get_channel(channel_id)
            if channel is None:
                raise Exception("Channel not found. Check channel ID.")
            if ping_everyone:
                message = "@everyone " + message
            for _ in range(count):
                await channel.send(message)
            print(f"[+] Sent {count} messages to channel {channel_id} in server {server_id}.")
        except Exception as e:
            print(f"[-] Error sending message to channel: {e}")
        finally:
            await client.close()

    try:
        await client.start(token)
    except Exception as e:
        print(f"[-] Error starting bot with token {token}: {e}")

# Change the username of a bot
async def change_username(token, new_username):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            await client.user.edit(username=new_username)
            print(f"[+] Username changed to '{new_username}'")
        except Exception as e:
            print(f"[-] Error changing username: {e}")
        finally:
            await client.close()

    try:
        await client.start(token)
    except Exception as e:
        print(f"[-] Error starting bot with token {token}: {e}")

# Change the profile picture of a bot
async def change_profile_picture(token, image_url):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        await client.user.edit(avatar=image_data)
                        print(f"[+] Profile picture updated successfully.")
                    else:
                        print(f"[-] Failed to fetch image from URL.")
        except Exception as e:
            print(f"[-] Error changing profile picture: {e}")
        finally:
            await client.close()

    try:
        await client.start(token)
    except Exception as e:
        print(f"[-] Error starting bot with token {token}: {e}")

# Main function to get inputs and perform actions
async def main():
    tokens = read_tokens('tokens.txt')

    while True:
        print("1: Dm                                2: Change Username  3: Send to Server  4: Change Profile  5: Exit")
        choice = input("Please enter your choice: ")

        if choice == '1':
            user_id = int(input("User ID: "))
            message = input("Message: ")
            count = int(input("How Many: "))

            emoji_choice = input("Include Emoji? (y/n): ").strip().lower()
            emoji = None
            emoji_count = 0
            if emoji_choice == 'y':
                emoji = input("Enter Emoji: ")
                emoji_count = int(input("Number of Emojis (1-10): "))
                if emoji_count < 1 or emoji_count > 10:
                    print("Invalid number of emojis. Setting to 0.")
                    emoji_count = 0

            tasks = []
            for token in tokens:
                tasks.append(send_dm(token, user_id, message, count, emoji, emoji_count))

            await asyncio.gather(*tasks)
        elif choice == '2':
            new_username = input("New Username: ")

            tasks = []
            for token in tokens:
                tasks.append(change_username(token, new_username))

            await asyncio.gather(*tasks)
        elif choice == '3':
            server_id = int(input("Server ID: "))
            channel_id = int(input("Channel ID: "))
            message = input("Message: ")
            count = int(input("How Many? (1-100): "))

            if count < 1 or count > 100:
                print("Invalid number of messages. Setting to 1.")
                count = 1

            ping_everyone = input("Ping Everyone? (y/n): ").strip().lower() == 'y'

            tasks = []
            for token in tokens:
                tasks.append(send_to_channel(token, server_id, channel_id, message, count, ping_everyone))

            await asyncio.gather(*tasks)
        elif choice == '4':
            image_url = input("Image URL: ")

            tasks = []
            for token in tokens:
                tasks.append(change_profile_picture(token, image_url))

            await asyncio.gather(*tasks)
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    asyncio.run(main())
