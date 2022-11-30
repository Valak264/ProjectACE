import vt, json, discord, os
from dotenv import load_dotenv

async def scan_and_get_obj():
    vt_client = vt.Client("19a17669220145bd0afac5597644dc574f8e12b9a6fb447e595bb5cdb05a0af7")
    analysis = await vt_client.scan_url_async("http://www.virustotal.com")
    url_id = vt.url_id("http://www.virustotal.com")
    url_obj = await vt_client.get_object_async("/urls/{}", url_id)
    return url_obj.last_analysis_stats
    
#Memuat file .env
load_dotenv()

#Mengambil Token Bot dan Nama Server Discord 
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

#Inisialisasi Discord Client agar terhubung dengan Discord API
discord_client = discord.Client()

@discord_client.event
async def on_message(message):
    attached = message.attachments
    text = await scan_and_get_obj()
    print(text)

discord_client.run(TOKEN)