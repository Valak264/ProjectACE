import vt, requests, discord, os, time
from dotenv import load_dotenv

load_dotenv()

# TOKEN = os.getenv('DISCORD_TOKEN')
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
            print("File closed !")
        else:
            print("Error ! File not closing !")
            exit()
    
    while True:
        obj = client.get_object("/analyses/{}", analysis.id)
        print("Analysis status : ", obj.status)
        if obj.status == "completed":
            print("Stats : ", obj.stats)
        time.sleep(30)

@discord_client.event
async def on_ready():
    guild = discord.utils.get(discord_client.guilds, name=SERVER)
    print(
        f'{discord_client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )