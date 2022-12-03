import vt, json, discord, os
from dotenv import load_dotenv

#Memuat file .env
load_dotenv()

#Mengambil Token Bot dan Nama Server Discord 
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

# async def scan_and_get_obj(url):
#     vt_client = vt.Client("19a17669220145bd0afac5597644dc574f8e12b9a6fb447e595bb5cdb05a0af7")
#     analysis = await vt_client.scan_url_async(url)
#     url_id = vt.url_id(url)
#     url_obj = await vt_client.get_object_async("/urls/{}", url_id)
#     await vt_client.close_async()
#     return url_obj.last_analysis_stats
    

#Inisialisasi Discord Client agar terhubung dengan Discord API
discord_client = discord.Client()

@discord_client.event
async def on_ready():
    guild = discord.utils.get(discord_client.guilds, name=SERVER)
    print(
        f'{discord_client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@discord_client.event
async def on_message(message):
    attachment = message.attachments
    stringified_url = str(attachment[0])
    print(stringified_url)

discord_client.run(TOKEN)