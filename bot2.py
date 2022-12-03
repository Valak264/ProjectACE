import vt, requests, discord, time, os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
VT_APIKEY = os.getenv('VT_API_KEY')
discord_client = discord.Client()

async def download_file(url):
    response = requests.get(url)
    f = open("temp_file", "wb")
    f.write(response.content)
    f.close()
    if f.closed:
        print("File closed !")
    else:
        print("Error ! File not closing !")
        exit()

async def scanning_file():
    client = vt.Client(VT_APIKEY)
    with open("temp_file", "rb") as f:
        analysis = await client.scan_file_async(f)
        f.close()
        if f.closed:
            if os.path.exists("temp_file"):
                os.remove("temp_file")
            print("File closed and deleted ! Wait for analysis status")
        else:
            print("Error ! File not found !")
            exit()
    
    while True:
        obj = await client.get_object_async("/analyses/{}", analysis.id)
        print("Analysis status : ", obj.status)
        if obj.status == "completed":
            print("Stats : ", obj.stats)
            await client.close_async()
            return obj
        time.sleep(30)

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
    url = str(attachment[0])
    await download_file(url)
    scan = await scanning_file()
    print(scan.stats)
    exit()

discord_client.run(TOKEN)