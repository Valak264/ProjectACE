from __future__ import print_function
import cloudmersive_virus_api_client, discord, os, json, requests
from cloudmersive_virus_api_client.rest import ApiException
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)

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
    config = cloudmersive_virus_api_client.Configuration()
    config.api_key['Apikey'] = os.getenv('CLOUDMERSIVE_API_KEY')
    api_instance = cloudmersive_virus_api_client.ScanApi(cloudmersive_virus_api_client.ApiClient(config))
    input = 'temp_file'

    try:
        api_response = api_instance.scan_file_advanced(input, allow_executables=False, allow_invalid_files = False, allow_scripts = False, allow_macros = False)
        string = str(api_response)
        json_to_dict = string.replace("'", '"')
        json_to_dict = json_to_dict.replace("True", "true")
        json_to_dict = json_to_dict.replace("False", "false")
        json_to_dict = json_to_dict.replace("None", "\"None\"")
        json_to_dict = json.loads(json_to_dict)
        
        if os.path.exists("temp_file"):
            os.remove("temp_file")
            print("File dihapus !")
        else:
            print("File tidak ditemukan !")
        return json_to_dict


    except ApiException as e:
        print("ERROR : ", e)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=SERVER)
    print(
        f'{client.user} terhubung dengan server berikut:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    attachment = message.attachments
    if len(attachment) == 1:
        await message.reply("PERHATIAN ! File sedang dipindai. Mohon jangan unduh file ini sampai pemindaian selesai")
        await download_file(attachment[0])
        result = await scanning_file()
        
        if result['clean_result']:
            await message.channel.send("File Aman !")
        else:
            await message.channel.send("File mencurigakan ! Jangan diunduh !")

client.run(TOKEN)