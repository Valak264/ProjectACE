import vt, requests, discord, os, json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
VT_APIKEY = os.getenv('VT_API_KEY')

intent = discord.Intents.default()
intent.message_content = True
intent.messages = True

discord_client = discord.Client(intents=intent)

async def download_file(url):
    response = requests.get(url)
    f = open("temp_file", "wb")
    f.write(response.content)
    f.close()
    if f.closed:
        print("File telah ditutup !")
    else:
        print("Error ! File tidak bisa ditutup !")
        exit()

async def scanning_file():
    client = vt.Client(VT_APIKEY)
    with open("temp_file", "rb") as f:
        analysis = await client.scan_file_async(f)
        f.close()
        if f.closed:
            if os.path.exists("temp_file"):
                os.remove("temp_file")
            print("File telah ditutup dan dihapus ! Mohon tunggu sampai ")
        else:
            print("Error ! File tidak ditemukan !")
            exit()
    
    while True:
        obj = await client.get_object_async("/analyses/{}", analysis.id)
        # print("Analysis status : ", obj.status)
        if obj.status == "completed":
            print("Status Analisa : ", obj.status)
            await client.close_async()
            return obj
        
@discord_client.event
async def on_ready():
    guild = discord.utils.get(discord_client.guilds, name=SERVER)
    print(
        f'{discord_client.user} terhubung dengan server berikut:\n'
        f'{guild.name}(id: {guild.id})'
    )

@discord_client.event
async def on_message(message):
    attachment = message.attachments
    if len(attachment) == 1:
        url = str(attachment[0])
        await download_file(url)
        scan = await scanning_file()
        str_scan = str(scan.stats)
        convert = str_scan.replace("'",'"')
        json_format = json.loads(convert)
        if json_format["malicious"] >= 4:
            print("File Berbahaya")
        else:
            print("File Aman")

discord_client.run(TOKEN)