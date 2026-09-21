#--- START OF FILE main.py ---

import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp , asyncio , random
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from xC4 import EnC_AEs, EnC_Uid, DEc_AEs, DeCode_PackEt # Explicitly imported for Clan Info
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
from emote_handler import load_emotes_from_file, get_menu_pages # <-- Updated Import

#EMOTES BY PARAHEX X CODEX
# FIXED BY WINTER ❄️ 


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# Load Emotes from emotes.json (New System)
# emote_aliases = Command ke liye dict
# categorized_emotes_data = Menu Display ke liye dict
emote_aliases, categorized_emotes_data = load_emotes_from_file("emotes.json")

# VariabLes dyli 
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False

# --- ESPAM & BOT VARIABLES ---
espam_on = False
active_squad_players = set()
bot_uid = None

# --- NEW LAG & SPAM VARIABLES ---
lag_running = False
spam_request_running = False
#------------------------------------------#
 
####################################

#Clan-info-by-clan-id
def Get_clan_info(clan_id):
    try:
        url = f"https://get-clan-info.vercel.app/get_clan_info?clan_id={clan_id}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            msg = f""" 
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
▶▶▶▶GUILD DETAILS◀◀◀◀
Achievements: {data['achievements']}\n\n
Balance : {fix_num(data['balance'])}\n\n
Clan Name : {data['clan_name']}\n\n
Expire Time : {fix_num(data['guild_details']['expire_time'])}\n\n
Members Online : {fix_num(data['guild_details']['members_online'])}\n\n
Regional : {data['guild_details']['regional']}\n\n
Reward Time : {fix_num(data['guild_details']['reward_time'])}\n\n
Total Members : {fix_num(data['guild_details']['total_members'])}\n\n
ID : {fix_num(data['id'])}\n\n
Last Active : {fix_num(data['last_active'])}\n\n
Level : {fix_num(data['level'])}\n\n
Rank : {fix_num(data['rank'])}\n\n
Region : {data['region']}\n\n
Score : {fix_num(data['score'])}\n\n
Timestamp1 : {fix_num(data['timestamp1'])}\n\n
Timestamp2 : {fix_num(data['timestamp2'])}\n\n
Welcome Message: {data['welcome_message']}\n\n
XP: {fix_num(data['xp'])}\n\n
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
[FFB300][b][c]MADE BY SPIDEERIO YT
            """
            return msg
        else:
            msg = """
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
Failed to get info, please try again later!!

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
[FFB300][b][c]MADE BY SPIDEERIO YT
            """
            return msg
    except:
        pass
#GET INFO BY PLAYER ID
def get_player_info(player_id):
    url = f"https://like2.vercel.app/player-info?uid={player_id}&server={server2}&key={key2}"
    response = requests.get(url)
    print(response)    
    if response.status_code == 200:
        try:
            r = response.json()
            return {
                "Account Booyah Pass": f"{r.get('booyah_pass_level', 'N/A')}",
                "Account Create": f"{r.get('createAt', 'N/A')}",
                "Account Level": f"{r.get('level', 'N/A')}",
                "Account Likes": f" {r.get('likes', 'N/A')}",
                "Name": f"{r.get('nickname', 'N/A')}",
                "UID": f" {r.get('accid', 'N/A')}",
                "Account Region": f"{r.get('region', 'N/A')}",
                }
        except ValueError as e:
            pass
            return {
                "error": "Invalid JSON response"
            }
    else:
        pass
        return {
            "error": f"Failed to fetch data: {response.status_code}"
        }
#CHAT WITH AI
def talk_with_ai(question):
    url = f"https://gemini-api-api-v2.vercel.app/prince/api/v1/ask?key=prince&ask={question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        msg = data["message"]["content"]
        return msg
    else:
        return "An error occurred while connecting to the server."
#SPAM REQUESTS
def spam_requests(player_id):
    # This URL now correctly points to the Flask app you provided
    url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
    try:
        res = requests.get(url, timeout=20) # Added a timeout
        if res.status_code == 200:
            data = res.json()
            # Return a more descriptive message based on the API's JSON response
            return f"API Status: Success [{data.get('success_count', 0)}] Failed [{data.get('failed_count', 0)}]"
        else:
            # Return the error status from the API
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle cases where the API isn't running or is unreachable
        print(f"Could not connect to spam API: {e}")
        return "Failed to connect to spam API."
####################################

# ** NEW INFO FUNCTION using the new API **
def newinfo(uid):
    # Base URL without parameters
    url = "https://like2.vercel.app/player-info"
    # Parameters dictionary - this is the robust way to do it
    params = {
        'uid': uid,
        'server': server2,  # Hardcoded to bd as requested
        'key': key2
    }
    try:
        # Pass the parameters to requests.get()
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the expected data structure is in the response
            if "basicInfo" in data:
                return {"status": "ok", "data": data}
            else:
                # The API returned 200, but the data is not what we expect (e.g., error message in JSON)
                return {"status": "error", "message": data.get("error", "Invalid ID or data not found.")}
        else:
            # The API returned an error status code (e.g., 404, 500)
            try:
                # Try to get a specific error message from the API's response
                error_msg = response.json().get('error', f"API returned status {response.status_code}")
                return {"status": "error", "message": error_msg}
            except ValueError:
                # If the error response is not JSON
                return {"status": "error", "message": f"API returned status {response.status_code}"}

    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., timeout, no connection)
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except ValueError: 
        # Handle cases where the response is not valid JSON
        return {"status": "error", "message": "Invalid JSON response from API."}

	
#ADDING-100-LIKES-IN-24H
def send_likes(uid):
    try:
        likes_api_response = requests.get(
             f"https://yourlikeapi/like?uid={uid}&server_name={server2}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS_TOKEN}",
             timeout=15
             )
      
      
        if likes_api_response.status_code != 200:
            return f"""
[C][B][FF0000]━━━━━
[FFFFFF]Like API Error!
Status Code: {likes_api_response.status_code}
Please check if the uid is correct.
━━━━━
"""

        api_json_response = likes_api_response.json()

        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # ✅ Success
            return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Likes Status:

[00FF00]Likes Sent Successfully!

[FFFFFF]Player Name : [00FF00]{player_name}  
[FFFFFF]Likes Added : [00FF00]{likes_added}  
[FFFFFF]Likes Before : [00FF00]{likes_before}  
[FFFFFF]Likes After : [00FF00]{likes_after}  
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Subscribe: [FFFFFF]SPIDEERIO YT [00FF00]!!
"""
        elif status == 2 or likes_before == likes_after:
            # 🚫 Already claimed / Maxed
            return f"""
[C][B][FF0000]━━━━━━━━━━━━

[FFFFFF]No Likes Sent!

[FF0000]You have already taken likes with this UID.
Try again after 24 hours.

[FFFFFF]Player Name : [FF0000]{player_name}  
[FFFFFF]Likes Before : [FF0000]{likes_before}  
[FFFFFF]Likes After : [FF0000]{likes_after}  
[C][B][FF0000]━━━━━━━━━━━━
"""
        else:
            # ❓ Unexpected case
            return f"""
[C][B][FF0000]━━━━━━━━━━━━
[FFFFFF]Unexpected Response!
Something went wrong.

Please try again or contact support.
━━━━━━━━━━━━
"""

    except requests.exceptions.RequestException:
        return """
[C][B][FF0000]━━━━━
[FFFFFF]Like API Connection Failed!
Is the API server (app.py) running?
━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]An unexpected error occurred:
[FF0000]{str(e)}
━━━━━
"""
####################################
#CHECK ACCOUNT IS BANNED

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB55"}

# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)


async def send_emote_menu_background(chat_type, uid, chat_id, key, iv, whisper_writer, online_writer):
    """
    Ye function background mein chalega aur list bhejega.
    """
    pages = get_menu_pages(categorized_emotes_data)
    
    for page in pages:
        try:
            # Message bhejo
            P = await SEndMsG(chat_type, page, uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            
            # 1.5 second ka delay taaki spam kick na mile aur message sequence me jaye
            await asyncio.sleep(1) 
        except Exception as e:
            print(f"Menu sending error: {e}")
            break


async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

# --- PLAYER INFO LOGIC (FIXED KEYS & DATE) ---
async def fetch_player_info_crowx(uid):
    url = f"https://crowx64-info-api.vercel.app/info?uid={uid}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200: return None
                data = await response.json()
                
                # Extract Data
                acc = data.get("AccountInfo") or {}
                guild = data.get("GuildInfo") or {}
                social = data.get("socialinfo") or {}
                
                # Internal Date Formatter (Crash Proof)
                def get_date(ts):
                    try:
                        import datetime
                        # Agar Timestamp string hai to int banao
                        if ts:
                            return datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d')
                    except:
                        pass
                    return "N/A"

                # Dictionary with SIMPLE KEYS
                return {
                    "name": str(acc.get("AccountName", "N/A")),
                    "uid": str(acc.get("accountId", "0")),
                    "level": str(acc.get("AccountLevel", "0")),
                    "likes": str(acc.get("AccountLikes", "0")),
                    "exp": str(acc.get("AccountEXP", "0")),
                    "region": str(acc.get("AccountRegion", "N/A")),
                    "br_pts": str(acc.get("BrRankPoint", "0")),
                    "cs_pts": "0" if str(acc.get("CsRankPoint")) == "None" else str(acc.get("CsRankPoint", "0")),
                    "g_name": str(guild.get("GuildName", "No Guild")),
                    "bio": str(social.get("signature", "No Bio")),
                    "login": get_date(acc.get("releaseVersion")), # Key is 'login'
                    "created": get_date(acc.get("showType")) # Key is 'created'
                }
    except Exception as e:
        print(f"API Error: {e}")
        return None

# --- CLAN INFO LOGIC START ---
async def fetch_leader_name_async(uid, token):
    if not uid: return "N/A"
    url = "https://clientbp.ggblueshark.com/GetPlayerPersonalShow"
    try:
        uid_hex = await EnC_Uid(int(uid), 'Uid')
        raw_hex = f"08{uid_hex}1007"
        encrypted_hex = await EnC_AEs(raw_hex)
        data_bytes = bytes.fromhex(encrypted_hex)
        
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; SM-A505F Build/QP1A.190711.020)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": "OB55",
            "X-GA": "v1 1",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data_bytes, headers=headers, ssl=False) as response:
                if response.status == 200:
                    content = await response.read()
                    resp_hex = content.hex()
                    final_json_str = None
                    try:
                        dec_hex = await DEc_AEs(resp_hex)
                        final_json_str = await DeCode_PackEt(dec_hex)
                    except:
                        try: final_json_str = await DeCode_PackEt(resp_hex)
                        except: return "Parse Error"

                    if final_json_str:
                        p_data = json.loads(final_json_str)
                        root = p_data.get('1', {}).get('data', p_data)
                        name = root.get('3', {}).get('data')
                        return name if name else "Unknown"
    except:
        return "Error"
    return "N/A"

async def get_clan_info_full(clan_id, token):
    try:
        # 1. Prepare Request
        uid_hex = await EnC_Uid(int(clan_id), 'Uid')
        raw_payload = f"08{uid_hex}"
        encrypted_payload = await EnC_AEs(raw_payload)
        data_bytes = bytes.fromhex(encrypted_payload)

        url = "https://clientbp.ggblueshark.com/GetClanInfoByClanID"
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; SM-A505F Build/QP1A.190711.020)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": "OB55",
            "X-GA": "v1 1",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

        # 2. Send Request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data_bytes, headers=headers, ssl=False) as response:
                if response.status != 200:
                    return f"❌ API Error: {response.status}"
                
                content = await response.read()
                resp_hex = content.hex()
                
                # 3. Decrypt
                final_json_str = None
                try:
                    decrypted_hex = await DEc_AEs(resp_hex)
                    final_json_str = await DeCode_PackEt(decrypted_hex)
                except:
                    try: final_json_str = await DeCode_PackEt(resp_hex)
                    except: return "❌ Failed to decode clan data."

                if final_json_str:
                    data = json.loads(final_json_str)
                    
                    # 4. Parse Data
                    raw_field1 = data.get('1', {}).get('data')
                    root = raw_field1 if isinstance(raw_field1, dict) else data
                    
                    c_name = root.get('2', {}).get('data', 'N/A')
                    c_id = root.get('1', {}).get('data', 'N/A')
                    c_lvl = root.get('5', {}).get('data', '0')
                    c_glory = root.get('39', {}).get('data', '0')
                    c_mem = root.get('7', {}).get('data', '0')
                    c_max = root.get('6', {}).get('data', '0')
                    c_slogan = root.get('12', {}).get('data', root.get('3', {}).get('data', 'No Message'))
                    
                    # Entry Type
                    type_code = root.get('9', {}).get('data')
                    entry_type = "🔴 Closed" if type_code == 0 else "🟡 Approval" if type_code == 1 else "🟢 Auto" if type_code == 2 else "Unknown"

                    # 5. Fetch Leader Name
                    leader_uid = root.get('4', {}).get('data')
                    leader_name = await fetch_leader_name_async(leader_uid, token)

                    # 6. Format Message
                    msg = f"""
[B][C][FF0000]╔════ CLAN INFO ════╗
[FFFF00]Name : [FFFFFF]{c_name}
[FFFF00]ID   : [FFFFFF]{c_id}
[FFFF00]Lvl  : [FFFFFF]{c_lvl}
[FFFF00]Type : [FFFFFF]{entry_type}
[FFFF00]Glory: [FF00FF]{c_glory}
[FFFF00]Mems : [00FF00]{c_mem}/{c_max}
[FFFF00]Lead : [00FFFF]{leader_name}
[FFFF00]Msg  : [FFFFFF]{c_slogan}
[B][C][FF0000]╚═══════════════════╝
"""
                    return msg
                else:
                    return "❌ Empty Data Received."

    except Exception as e:
        return f"❌ System Error: {str(e)}"
# --- CLAN INFO LOGIC END ---


async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    """Safely send message with retry mechanism"""
    global whisper_writer, online_writer
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            # Ensure writer exists before writing
            if whisper_writer:
                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except Exception as e:
            print(f"Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    return False

# --- ESPAM LOOP FUNCTION ---
async def run_espam_loop(online_writer, whisper_writer, key, iv, region):
    global espam_on, active_squad_players, emote_aliases, bot_uid
    
    all_emote_ids = list(emote_aliases.values())
    
    if not all_emote_ids:
        print("Error: Emotes list is empty!")
        return

    print("🔥 Espam Loop Started! (Waiting for completion)")
    
    while espam_on:
        try:
            # Random Emote Select
            random_emote = random.choice(all_emote_ids)
            emote_int = int(random_emote)
            
            # Target List: Active Players + Bot Khud
            targets = list(active_squad_players)
            if bot_uid and bot_uid not in targets:
                targets.append(bot_uid)

            if not targets:
                await asyncio.sleep(1)
                continue
            
            # Ek baar sabko emote bhejo
            for target_uid in targets:
                H = await Emote_k(target_uid, emote_int, key, iv, region)
                if online_writer:
                    online_writer.write(H)
                    await online_writer.drain()
                await asyncio.sleep(0.05) 

            # YAHAN CHANGE KIYA HAI:
            # Pehle 5 sec tha, ab 6.5 sec kiya hai taaki emote poora khatam ho
            # Tabhi naya aayega "bina ruke"
            await asyncio.sleep(6.5)

        except Exception as e:
            print(f"Espam Error: {e}")
            await asyncio.sleep(2)

async def lag_team_loop(team_code, key, iv, region, chat_type, uid, chat_id):
    """Rapid join/leave loop to create lag - Runs for 15 Seconds Only"""
    global lag_running, whisper_writer, online_writer
    
    start_time = time.time() # Start timer
    duration = 15 # Seconds
    count = 0
    
    print(f"[+] Lag Attack Started on Team: {team_code} for 15s")
    
    while lag_running and (time.time() - start_time < duration):
        try:
            # Join the team
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            if online_writer:
                online_writer.write(join_packet)
                await online_writer.drain()
            
            # Ultra fast delay
            await asyncio.sleep(0.01) 
            
            # Leave the team
            leave_packet = await ExiT(None, key, iv)
            if online_writer:
                online_writer.write(leave_packet)
                await online_writer.drain()
            
            count += 1
            # Thoda delay taaki script crash na ho
            await asyncio.sleep(0.02)
            
        except Exception as e:
            print(f"Error in lag loop: {e}")
            await asyncio.sleep(0.1)
            
    # Loop khatam hone ke baad (ya to 15s poore hue ya /stop dabaya)
    lag_running = False
    
    # Agar time poora hone par ruka hai, to "Completed" message bhejo
    if time.time() - start_time >= duration:
        print(f"[-] Lag Attack Auto-Stopped (Time Up). Cycles: {count}")
        finish_msg = f"[B][C][00FF00]✅ Lag Attack Completed!\nTarget: {team_code}\nCycles: {count}"
        try:
            P = await SEndMsG(chat_type, finish_msg, uid, chat_id, key, iv)
            if whisper_writer and online_writer:
                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        except:
            pass

async def spam_request_loop(target_list, count_limit, key, iv, region, chat_type, uid, chat_id):
    """
    Advanced Spam Loop:
    - Handles Single UID or Team List
    - Custom Count
    - Proper Status Messages
    """
    global spam_request_running, whisper_writer, online_writer
    
    current_count = 0
    total_targets = len(target_list)
    
    # 1. Processing Message
    process_msg = f"[B][C][FFFF00]⚙️ Processing Request...\nTargets: {total_targets}\nCount: {count_limit}"
    try:
        P = await SEndMsG(chat_type, process_msg, uid, chat_id, key, iv)
        if whisper_writer: await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    except: pass
    
    await asyncio.sleep(1) # Thoda delay taaki message dikhe

    # 2. Started Message
    start_msg = f"[B][C][FF0000]🚀 Attack Started!\nSending {count_limit} requests to {total_targets} players."
    try:
        P = await SEndMsG(chat_type, start_msg, uid, chat_id, key, iv)
        if whisper_writer: await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    except: pass

    # Main Loop
    while spam_request_running and current_count < count_limit:
        try:
            # Step A: Squad banao
            PAc = await OpEnSq(key, iv, region)
            if online_writer:
                online_writer.write(PAc)
                await online_writer.drain()
            
            await asyncio.sleep(0.2) 
            
            # Step B: List me jitne log hain sabko invite bhejo (Ek hi squad me)
            for target in target_list:
                try:
                    # Invite Packet
                    V = await SEnd_InV(5, int(target), key, iv, region)
                    if online_writer:
                        online_writer.write(V)
                        await online_writer.drain()
                    await asyncio.sleep(0.1) # Fast invite
                except: continue

            # Step C: Squad leave karo
            E = await ExiT(None, key, iv)
            if online_writer:
                online_writer.write(E)
                await online_writer.drain()
            
            current_count += 1
            print(f"Spam Cycle {current_count}/{count_limit} Completed.")
            
            await asyncio.sleep(0.4) # Delay before next cycle
            
        except Exception as e:
            print(f"Error in spam loop: {e}")
            await asyncio.sleep(0.5)

    # 3. Finished Message
    spam_request_running = False
    finish_msg = f"[B][C][00FF00]✅ Task Finished!\nTotal Requests Sent: {current_count}"
    try:
        P = await SEndMsG(chat_type, finish_msg, uid, chat_id, key, iv)
        if whisper_writer: await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    except: pass



# --- BADGE LOGIC START ---
BADGE_VALUES = {
    "s1": 1048576,    # Craftland
    "s2": 32768,      # V-Badge
    "s3": 2048,       # Moderator
    "s4": 64,         # Small V-Badge
    "s5": 262144      # Pro Badge
}

async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    """Send join request with specific badge"""
    # Random Avatar helper
    avatar_id = random.choice([902050001, 902050002, 902050003, 902039016, 902050004])
    
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] BADGE BOT",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56, 97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: avatar_id,
            26: "",
            28: "",
            31: {
                1: 1,
                2: badge_value
            },
            32: badge_value,
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {2: 1, 3: 1}
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind": packet_type = '0514'
    elif region.lower() == "bd": packet_type = "0519"
    else: packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)

async def handle_badge_command_logic(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type, whisper_writer, online_writer):
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Usage: {cmd} (uid)\nExample: {cmd} 123456789"
        P = await SEndMsG(chat_type, error_msg, uid, chat_id, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        return

    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)

    if not target_uid.isdigit():
        return

    # 1. Processing Msg
    msg = f"[B][C][FFFF00]⚙️ Sending {cmd} Request to {target_uid}..."
    P = await SEndMsG(chat_type, msg, uid, chat_id, key, iv)
    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

    try:
        # 2. Leave current squad first (Reset state)
        leave = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave)
        await asyncio.sleep(0.5)

        # 3. Send Badge Join Request (5 times fast)
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        for _ in range(5):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(0.1)

        # 4. Success Msg
        final_msg = f"[B][C][00FF00]✅ Sent {cmd} Request!\nTarget: {target_uid}\nBadge Value: {badge_value}"
        P = await SEndMsG(chat_type, final_msg, uid, chat_id, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        
        # Cleanup
        await asyncio.sleep(1)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave)

    except Exception as e:
        print(f"Badge Error: {e}")
# --- BADGE LOGIC END ---



async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave, bot_uid
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break
                
                if data2.hex().startswith('0500') and len(data2.hex()) > 400:
                    try:
                        print(data2.hex()[10:])
                        print("📩 Group Info/Invite Detected...")
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        print(packet)
                        packet = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)

                        # 2. LOBBY (SQUAD) JOIN KARO (Ye naya hai)
                        # Jaise hi invite accept hoga ya info milegi, bot squad me ghus jayega
                        if SQuAD_CoDe:
                            print(f"🚀 Auto-Joining Squad Lobby: {SQuAD_CoDe}")
                            EM = await GenJoinSquadsPacket(SQuAD_CoDe, key, iv)
                            online_writer.write(EM) 
                            await online_writer.drain()
                            
                            # Emote spam ke liye owner ko list me daal do
                            active_squad_players.add(OwNer_UiD)

                        message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot ! '
                        P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)

                    except:
                        if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                            try:
                                print(data2.hex()[10:])
                                packet = await DeCode_PackEt(data2.hex()[10:])
                                print(packet)
                                packet = json.loads(packet)
                                OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                                JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)


                                message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot ! \n\n{get_random_color()}- Commands : @a {xMsGFixinG('player_uid')} {xMsGFixinG('909000001')}\n\n[00FF00]Dev : @{xMsGFixinG('Spideerio')}'
                                P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                            except:
                                pass

            online_writer.close() ; await online_writer.wait_closed() ; online_writer = None

        except Exception as e: print(f"- ErroR With {ip}:{port} - {e}") ; online_writer = None
        await asyncio.sleep(reconnect_delay)

# ==========================================================
#      TRICK: BACKGROUND TASK FOR FRIEND REQUESTS
# ==========================================================
async def Background_Friend_Worker(target_uid, action, chat_type, uid, chat_id, key, iv, jwt_token, whisper_writer, online_writer):
    # 1. Processing Message (Turant Bhejo)
    if action == 'add':
        msg_wait = f"[B][C]🔄 [FFD700]Processing Request...\n[FFFFFF]UID: {target_uid}"
    else:
        msg_wait = f"[B][C]🔄 [FFD700]Processing Removal...\n[FFFFFF]UID: {target_uid}"
        
    try:
        # Message bhej ke turant aage badho
        P = await SEndMsG(chat_type, msg_wait, uid, chat_id, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    except Exception as e:
        print(f"Error Sending Wait Msg: {e}")

    # 2. API Call (Background me - Bot rukega nahi)
    try:
        loop = asyncio.get_event_loop()
        # Ye line magic hai, ye request ko alag thread me chalayegi
        status_code, code_msg = await loop.run_in_executor(None, Friend_Action_API, target_uid, jwt_token, action)
    except Exception as e:
        print(f"API Failed: {e}")
        status_code = 500

    # 3. Final Message Prepare Karo
    final_msg = ""
    if action == 'add':
        if status_code == 200:
            final_msg = f"[B][C]✅ [00FF00]Friend Request Sent Successfully!\n[FFFFFF]Target: {target_uid}"
        elif status_code == 400:
            final_msg = f"[B][C]⚠️ [FFA500]Failed: Already Friends or\nRequest Already Sent."
        elif status_code == 404:
            final_msg = f"[B][C]❌ [FF0000]Failed: UID Not Found."
        else:
            final_msg = f"[B][C]❌ [FF0000]Action Failed!\nStatus: {status_code}"
    else: # remove
        if status_code == 200:
            final_msg = f"[B][C]✅ [00FF00]Successfully Removed Friend!\n[FFFFFF]UID: {target_uid}"
        elif status_code == 400:
            final_msg = f"[B][C]❌ [FF0000]Failed: Player Not Found\nin Friend List."
        else:
            final_msg = f"[B][C]❌ [FF0000]Action Failed!\nStatus: {status_code}"

    # 4. Final Message Bhejo (Ab connection zinda hoga)
    try:
        await asyncio.sleep(0.5) # Thoda sa saans lene do bot ko
        P = await SEndMsG(chat_type, final_msg, uid, chat_id, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    except Exception as e:
        print(f"Error Sending Final Msg: {e}")

async def send_repeated_emote(uid, emote_id, count, key, iv, region, online_writer):
    """
    Ye function background mein emote ko repeat karega.
    Gap: 0.3 Seconds
    """
    try:
        # Loop jitni baar user ne bola (e.g. 5, 10, 20)
        for i in range(count):
            # Emote Packet Bhejo
            H = await Emote_k(uid, emote_id, key, iv, region)
            if online_writer:
                online_writer.write(H)
                await online_writer.drain()
            
            # Fast Delay (Glitch Effect)
            await asyncio.sleep(0.13)
            
        print(f"✅ Repeated Emote Finished: {count} times")
    except Exception as e:
        print(f"Repeater Error: {e}")


async def send_team_emote_task(target_uids, emote_id, count, key, iv, region, online_writer):
    """
    Background task to send emotes to a list of players (Team).
    Handles both single time and repeated loops.
    """
    try:
        # Loop for the repeat count (e.g., 10, 20 times)
        for i in range(count):
            # Loop through each player in the team
            for target in target_uids:
                try:
                    H = await Emote_k(int(target), emote_id, key, iv, region)
                    if online_writer:
                        online_writer.write(H)
                        await online_writer.drain()
                    # Tiny delay between players to prevent packet loss
                    await asyncio.sleep(0.02) 
                except: continue
            
            # Delay between cycles (Fast but visible)
            await asyncio.sleep(0.15)
            
    except Exception as e:
        print(f"Team Emote Task Error: {e}")

async def auto_rings_emote_dual(sender_uid, key, iv, region):
    """
    Sends 'The Rings' emote (909050009) to both the sender and the bot.
    """
    global bot_uid, online_writer
    try:
        rings_emote_id = 909050009
        
        # 1. Send Emote to Sender (Jisne invite kiya/Code diya)
        H1 = await Emote_k(int(sender_uid), rings_emote_id, key, iv, region)
        if online_writer:
            online_writer.write(H1)
            await online_writer.drain()
        
        await asyncio.sleep(0.3) # Thoda delay taaki sync dikhe
        
        # 2. Send Emote to Bot itself (Dual effect ke liye)
        if bot_uid:
            H2 = await Emote_k(int(bot_uid), rings_emote_id, key, iv, region)
            if online_writer:
                online_writer.write(H2)
                await online_writer.drain()
                
        print(f"💍 Dual Rings Emote Triggered with {sender_uid}")
        
    except Exception as e:
        print(f"Dual Emote Error: {e}")



async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, jwt_token, reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    # Yahan saare globals ek saath hone chahiye
    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, espam_on, active_squad_players
    global lag_running, spam_request_running # <--- YE LINE ADD KARO
    
    # Use globally loaded emote aliases
    global normal_aliases, evo_aliases, emote_aliases

    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                
                if data.hex().startswith("120000"):

                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except:
                        response = None


                    if response:
                        # Har message karne wale ko active list me dalo
                        if uid not in active_squad_players:
                            active_squad_players.add(uid)
                            # print(f"Added to Espam List: {uid}")

                        # Raw message cleaning for commands
                        raw_input_lower = inPuTMsG.strip().lower()
                        cleaned_alias = raw_input_lower.replace(' ', '')
                        
                        # --- PM AUTO JOIN (BACKUP FEATURE) ---
                        if (XX == 1 or XX == 2) and inPuTMsG.isdigit() and len(inPuTMsG) > 6:
                            print(f"📨 Team Code Received: {inPuTMsG}")
                            
                            # 1. Join Team
                            EM = await GenJoinSquadsPacket(inPuTMsG , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
                            
                            # 2. Send Message
                            ok_msg = f"[B][C][00FF00]Joining Team: {inPuTMsG}..."
                            P = await SEndMsG(XX , ok_msg , uid , chat_id , key , iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            # 3. TRIGGER DUAL EMOTE (Added Logic)
                            # 1.5 second wait karenge taaki bot lobby me enter ho jaye fir emote kare
                            await asyncio.sleep(1.5)
                            asyncio.create_task(auto_rings_emote_dual(uid, key, iv, region))

                        # --- ELIST COMMAND (BACKGROUND MODE) ---
                        elif inPuTMsG == 'elist':
                            print(f"Sending Emote List to {uid} (Background)")
                            asyncio.create_task(send_emote_menu_background(
                                response.Data.chat_type, 
                                uid, 
                                chat_id, 
                                key, 
                                iv, 
                                whisper_writer, 
                                online_writer
                            ))

                        # --- ESPAM START COMMAND ---
                        elif inPuTMsG == 'spam':
                            if not espam_on:
                                espam_on = True
                                active_squad_players.add(uid)
                                asyncio.create_task(run_espam_loop(online_writer, whisper_writer, key, iv, region))
                                msg = "[B][C][00FF00]✅ Random Emote Spam STARTED!\n(Bot + Squad)"
                                P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                        # --- ESPAM STOP COMMAND ---
                        # --- ESPAM STOP COMMAND ---
                        elif inPuTMsG == 'stop':
                            if espam_on:
                                espam_on = False
                                active_squad_players.clear()
                            
                            # Yahan koi global line nahi honi chahiye
                            if lag_running: lag_running = False
                            if spam_request_running: spam_request_running = False

                            msg = "[B][C][FF0000]⛔ All Tasks STOPPED!"
                            P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                        # --- DIRECT NAME EMOTE TRIGGER (UPDATED FOR TEAM) ---
                        # Agar upar wala koi command nahi tha, tabhi emote check karo
                        else:
                            # 1. Input Clean karo
                            raw_msg = inPuTMsG.strip().lower()
                            
                            # "!e" hatao agar hai to
                            if raw_msg.startswith('!e '): raw_msg = raw_msg.replace('!e ', '')
                            elif raw_msg.startswith('!e'): raw_msg = raw_msg.replace('!e', '')
                            
                            parts = raw_msg.split()
                            if not parts: continue 

                            emote_name = parts[0]
                            
                            # Check karo Emote List mein
                            if emote_name in emote_aliases:
                                try:
                                    # Private Chat Check
                                    try:
                                        dd = chatdata['5']['data']['16']
                                        # Private me bas normal reply ya ignore
                                    except KeyError: 
                                        # Squad Chat Detected
                                        emote_id_int = emote_aliases[emote_name]
                                        
                                        # Default Values
                                        target_uids = [uid] # Default: Sender only
                                        repeat_count = 1
                                        
                                        # Parse arguments (Example: "p90 t 10", "lol 5", "lol t")
                                        if len(parts) > 1:
                                            for part in parts[1:]:
                                                if part == 't':
                                                    # 't' detected: Target = Team
                                                    if active_squad_players:
                                                        target_uids = list(active_squad_players)
                                                        # Add bot itself to the fun if not in list
                                                        if bot_uid and bot_uid not in target_uids:
                                                            target_uids.append(bot_uid)
                                                elif part.isdigit():
                                                    # Number detected: Count
                                                    repeat_count = int(part)
                                        
                                        # Safety Limit
                                        if repeat_count > 100: repeat_count = 100

                                        # Execute Logic (Background Task)
                                        # Ab chahe 1 baar ho ya 100 baar, single player ho ya team
                                        # Hum new helper function use karenge jo sab handle karega
                                        asyncio.create_task(send_team_emote_task(
                                            target_uids, 
                                            emote_id_int, 
                                            repeat_count, 
                                            key, 
                                            iv, 
                                            region, 
                                            online_writer
                                        ))
                                            
                                except Exception as e:
                                    print(f"Emote Logic Error: {e}")

                        # --- ESPAM STOP COMMAND (/spam/) ---
                        if inPuTMsG == 'stop':
                            # Stop Emote Spam
                            if espam_on:
                                espam_on = False
                                active_squad_players.clear()
                            
                            # Stop Lag Loop
                            if lag_running:
                                lag_running = False
                                
                            # Stop Request Spam
                            if spam_request_running:
                                spam_request_running = False

                            msg = "[B][C][FF0000]⛔ All Tasks (Spam/Lag/Requests) STOPPED!"
                            P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                        # --- LAG TEAM COMMAND ---
                        if inPuTMsG.startswith('lag'):
                            try:
                                # Command format: lag 1234567
                                team_code = inPuTMsG.replace('lag', '').strip()
                                if team_code.isdigit() and len(team_code) > 5:
                                    if not lag_running:
                                        lag_running = True
                                        # Message: Process Started
                                        start_msg = f"[B][C][FF0000]☠️ Lag Attack Started!\nTarget: {team_code}\nDuration: 15 Seconds..."
                                        P = await SEndMsG(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                        
                                        # Start Loop with extra args for message handling
                                        asyncio.create_task(lag_team_loop(team_code, key, iv, region, response.Data.chat_type, uid, chat_id))
                                    else:
                                        msg = "[B][C][FFFF00]⚠️ Lag Loop is already running!"
                                        P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    msg = "[B][C][FFFF00]❌ Invalid Code! Use: lag <teamcode>"
                                    P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except Exception as e:
                                print(f"Lag Command Error: {e}")

                        # --- ADVANCED SPAM REQUEST COMMAND ---
                        if inPuTMsG.startswith('spm'):
                            try:
                                # Format: spm <uid/t> <count>
                                # Example: spm 123456 20  OR  spm t 50
                                
                                parts = inPuTMsG.split()
                                target_input = parts[1] if len(parts) > 1 else None
                                count_input = int(parts[2]) if len(parts) > 2 else 30 # Default 30
                                
                                target_list = []
                                
                                if target_input:
                                    if target_input.lower() == 't':
                                        # Target is TEAM (active players in chat)
                                        if active_squad_players:
                                            target_list = list(active_squad_players)
                                            # Bot khud ko spam na kare agar list me hai
                                            if bot_uid in target_list: target_list.remove(bot_uid)
                                        else:
                                            # Agar koi list me nahi hai
                                            msg = "[B][C][FF0000]❌ No active players found for 't' option!"
                                            P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                            continue 
                                    elif target_input.isdigit():
                                        # Target is Single UID
                                        target_list = [target_input]
                                    else:
                                        msg = "[B][C][FFFF00]❌ Invalid ID! Use: spm <uid> or spm t"
                                        P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                        continue

                                    # Start Logic
                                    if not spam_request_running:
                                        if target_list:
                                            spam_request_running = True
                                            # Loop start kar rahe hain nayi list ke saath
                                            asyncio.create_task(spam_request_loop(target_list, count_input, key, iv, region, response.Data.chat_type, uid, chat_id))
                                    else:
                                        msg = "[B][C][FFFF00]⚠️ Spam Task is already running!"
                                        P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    msg = "[B][C][FFFF00]❌ Usage: spm <uid/t> <count>"
                                    P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except Exception as e:
                                print(f"Spm Command Error: {e}")


# --- START OF FILE main.py (Inside TcPChaT loop) ---

                        # --- FORCE START COMMAND (/start) ---
                        if inPuTMsG.startswith('/start '):
                            try:
                                # 1. Command Parse karo (Bilkul aapke logic jaisa)
                                parts = inPuTMsG.split()
                                if len(parts) < 2:
                                    msg = "[B][C][FF0000]Please provide a team code."
                                    P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    continue

                                team_code = parts[1]
                                
                                # Count Logic (Default 20, Max 50)
                                spam_count = 20
                                if len(parts) > 2 and parts[2].isdigit():
                                    spam_count = int(parts[2])
                                if spam_count > 50:
                                    spam_count = 50

                                # 2. Joining Message
                                msg_join = f"[B][C][FFA500]Joining lobby to force start..."
                                P = await SEndMsG(response.Data.chat_type, msg_join, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                                # 3. Join Team (join_teamcode equivalent)
                                join_pkt = await GenJoinSquadsPacket(team_code, key, iv)
                                if online_writer:
                                    online_writer.write(join_pkt)
                                    await online_writer.drain()
                                
                                # 4. Wait 2 Seconds (Ye zaroori hai sync ke liye - Aapke code se liya)
                                await asyncio.sleep(2)

                                # 5. Spamming Start Message
                                msg_spam = f"[B][C][FF0000]Spamming start command {spam_count} times!"
                                P = await SEndMsG(response.Data.chat_type, msg_spam, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                                # 6. Start Packet Generate (start_autooo equivalent)
                                # Note: 'region' variable pass kiya hai taaki server reject na kare
                                start_pkt = await Start_Game_Packet(key, iv, region)

                                # 7. Spam Loop (Aapke logic: Send -> sleep 0.2)
                                for _ in range(spam_count):
                                    if online_writer:
                                        online_writer.write(start_pkt)
                                        await online_writer.drain()
                                    await asyncio.sleep(0.2) # 0.2s delay as per your logic

                                # 8. Leave Team (leave_s equivalent)
                                leave_pkt = await ExiT(None, key, iv)
                                if online_writer:
                                    online_writer.write(leave_pkt)
                                    await online_writer.drain()

                                # 9. Finished Message
                                done_msg = f"[B][C][00FF00]Force start process finished."
                                P = await SEndMsG(response.Data.chat_type, done_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except Exception as e:
                                print(f"Start Command Error: {e}")


                        # --- नया इमोट लॉजिक ---
                        if cleaned_alias in emote_aliases:
                            try:
                                # यह जांचें कि यह निजी चैट तो नहीं है
                                dd = chatdata['5']['data']['16']
                                message = f"[B][C]{get_random_color()}\n\nयह कमांड केवल स्क्वाड में उपलब्ध है!\n\n"
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except KeyError: # इसका मतलब है कि यह स्क्वाड चैट है
                                print(f"उपनाम '{cleaned_alias}' UID {uid} द्वारा स्क्वाड चैट में ट्रिगर किया गया।")
                                try:
                                    emote_id_str = emote_aliases[cleaned_alias]
                                    emote_id_int = int(emote_id_str)

                                    # इमोट पैकेट भेजें, जो उस खिलाड़ी को लक्षित करता है जिसने कमांड भेजा है
                                    H = await Emote_k(uid, emote_id_int, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                except (ValueError, KeyError) as e:
                                    print(f"इमोट उपनाम '{cleaned_alias}' को संसाधित करते समय त्रुटि: {e}")
                                except Exception as e:
                                    print(f"इमोट भेजते समय एक अप्रत्याशित त्रुटि हुई: {e}")
                            continue # अगले संदेश पर जाएं

                        if inPuTMsG.startswith(("5")):
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                message = f"[B][C]{get_random_color()}\n\nAccepT My Invitation FasT\n\n"
                                P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                                PAc = await OpEnSq(key , iv,region)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , PAc)
                                C = await cHSq(5, uid ,key, iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , C)
                                V = await SEnd_InV(5 , uid , key , iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , V)
                                E = await ExiT(None , key , iv)
                                await asyncio.sleep(3)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , E)
                            except:
                                print('msg in squad')



                        if inPuTMsG.startswith('/x/'):
                            CodE = inPuTMsG.split('/x/')[1]
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                EM = await GenJoinSquadsPacket(CodE , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)


                            except:
                                print('msg in squad')

                        if inPuTMsG.startswith('solo'):
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)

# --- ADD FRIEND COMMAND ---
                        # =====================================================
                        #              FRIEND REQUEST COMMAND (add)
                        # =====================================================
                        # =====================================================
                        #              FRIEND REQUEST COMMAND (add)
                        # =====================================================
                        # =====================================================
                        #              FRIEND REQUEST COMMAND (add)
                        # =====================================================
                        # =====================================================
                        #              FRIEND REQUEST COMMAND (add)
                        # =====================================================
# =====================================================
                        #              ADD FRIEND COMMAND (add)
                        # =====================================================
                        if inPuTMsG.startswith('add '):
                            try:
                                target_uid = inPuTMsG.split(' ')[1].strip()
                                
                                cur_type = response.Data.chat_type
                                cur_uid = uid
                                cur_cid = chat_id
                                
                                if target_uid.isdigit() and len(target_uid) > 5:
                                    
                                    # 1. PROCESSING MESSAGE
                                    msg_proc = f"[B][C]🔄 [FFD700]Adding Friend...\n[FFFFFF]UID: {target_uid}"
                                    P = await SEndMsG(cur_type, msg_proc, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    await asyncio.sleep(0.3)
                                    
                                    # 2. CALL API (Pass JWT Token)
                                    loop = asyncio.get_event_loop()
                                    # Note: 'ToKen' variable comes from TcPChaT
                                    result = await loop.run_in_executor(None, Friend_Action_API_Remote, target_uid, 'add', jwt_token)
                                    
                                    # 3. HANDLE RESPONSE
                                    is_success = result.get("success", False)
                                    api_msg = result.get("message", "Unknown Error")

                                    if is_success:
                                        final_msg = f"[B][C]✅ [00FF00]Friend Request Sent!\n[FFFFFF]UID: {target_uid}\nStatus: Success"
                                    else:
                                        # Handle errors (Already friend, list full, etc)
                                        final_msg = f"[B][C]❌ [FF0000]Failed to Add!\n[FFFFFF]Reason: {api_msg}"

                                    # 4. SEND FINAL STATUS
                                    P = await SEndMsG(cur_type, final_msg, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                else:
                                    err = "[B][C]❌ [FF0000]Invalid UID Format!"
                                    P = await SEndMsG(cur_type, err, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            
                            except Exception as e:
                                print(f"Add Error: {e}")

                        # =====================================================
                        #              REMOVE FRIEND COMMAND (remove)
                        # =====================================================
                        if inPuTMsG.startswith('remove '):
                            try:
                                target_uid = inPuTMsG.split(' ')[1].strip()

                                cur_type = response.Data.chat_type
                                cur_uid = uid
                                cur_cid = chat_id
                                
                                if target_uid.isdigit() and len(target_uid) > 5:
                                    
                                    # 1. PROCESSING MESSAGE
                                    msg_proc = f"[B][C]🔄 [FFD700]Removing Friend...\n[FFFFFF]UID: {target_uid}"
                                    P = await SEndMsG(cur_type, msg_proc, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    await asyncio.sleep(0.3)
                                    
                                    # 2. CALL API
                                    loop = asyncio.get_event_loop()
                                    result = await loop.run_in_executor(None, Friend_Action_API_Remote, target_uid, 'remove', jwt_token)
                                    
                                    # 3. HANDLE RESPONSE
                                    is_success = result.get("success", False)
                                    api_msg = result.get("message", "Unknown Error")

                                    if is_success:
                                        final_msg = f"[B][C]✅ [00FF00]Friend Removed!\n[FFFFFF]UID: {target_uid}\nStatus: Success"
                                    else:
                                        final_msg = f"[B][C]❌ [FF0000]Removal Failed!\n[FFFFFF]Reason: {api_msg}"

                                    # 4. SEND FINAL STATUS
                                    P = await SEndMsG(cur_type, final_msg, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                                else:
                                    err = "[B][C]❌ [FF0000]Invalid UID Format!"
                                    P = await SEndMsG(cur_type, err, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except Exception as e:
                                print(f"Remove Error: {e}")


                        # =====================================================
                        #              GUILD JOIN COMMAND (guild)
                        # =====================================================
                        # =====================================================
                        #              GUILD JOIN COMMAND (guild)
                        # =====================================================
                        if inPuTMsG.startswith('guild '):
                            try:
                                target_guild_id = inPuTMsG.split(' ')[1].strip()

                                # Current Chat Details
                                cur_type = response.Data.chat_type
                                cur_uid = uid
                                cur_cid = chat_id

                                if target_guild_id.isdigit() and len(target_guild_id) > 5:
                                    
                                    # 1. PROCESSING MESSAGE
                                    start_msg = f"[B][C]🔄 [FFD700]Sending Request...\n[FFFFFF]Guild ID: {target_guild_id}"
                                    P = await SEndMsG(cur_type, start_msg, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    await asyncio.sleep(0.3)
                                    
                                    # 2. CALL API (Background Execution)
                                    # NOTE: Yahan 'jwt_token' use karein (jo TcPChaT argument mein hai)
                                    loop = asyncio.get_event_loop()
                                    result = await loop.run_in_executor(None, Guild_Join_API, target_guild_id, jwt_token)
                                    
                                    # 3. PARSE JSON RESPONSE (New Logic)
                                    
                                    # A. Check for JWT/Auth Errors
                                    if "error" in result:
                                        err_msg = result["error"]
                                        final_msg = f"[B][C]⚠️ [FF0000]Auth/API Error!\n[FFFFFF]Msg: {err_msg}"

                                    # B. Check for Invalid Guild (Unknown)
                                    elif result.get("clan_name") == "Unknown":
                                        final_msg = f"[B][C]❌ [FF0000]Invalid Guild ID!\n[FFFFFF]Clan Name: Unknown\nStatus: Failed"

                                    # C. Check for Success
                                    elif result.get("success") == True:
                                        c_name = result.get("clan_name", "N/A")
                                        c_lvl = result.get("clan_level", "N/A")
                                        c_reg = result.get("region", "N/A")
                                        c_msg = result.get("message", "OK")
                                        
                                        final_msg = f"[B][C]✅ [00FF00]Request Sent!\n[FFFFFF]Name: [00FF00]{c_name}\n[FFFFFF]Level: {c_lvl}\nRegion: {c_reg}\nStatus: {c_msg}"

                                    # D. General Failure (Success False but not Unknown)
                                    else:
                                        fail_msg = result.get("message", "Unknown Error")
                                        final_msg = f"[B][C]❌ [FFA500]Request Failed!\n[FFFFFF]Msg: {fail_msg}"

                                    # 4. SEND FINAL STATUS
                                    P = await SEndMsG(cur_type, final_msg, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                                else:
                                    err = "[B][C]❌ [FF0000]Invalid Guild ID!"
                                    P = await SEndMsG(cur_type, err, cur_uid, cur_cid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except Exception as e:
                                print(f"Guild Command Error: {e}")
                                # Detail error print karein taaki debug ho sake
                                import traceback
                                traceback.print_exc()
                                
                                err_msg = f"[B][C]❌ [FF0000]Bot Logic Error!\n{str(e)}"
                                P = await SEndMsG(response.Data.chat_type, err_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)


# PLAYER INFO COMMAND (/info) - KEYS MATCHED
                        if inPuTMsG.strip().startswith('/info '):
                            print(f'Processing /info command from UID: {uid}')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                err = "[B][C][FF0000]❌ Usage: /info <uid>"
                                P = await SEndMsG(response.Data.chat_type, err, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            else:
                                target_uid_info = parts[1]
                                
                                # 1. Fetch Data
                                info_data = await fetch_player_info_crowx(target_uid_info)
                                
                                if info_data:
                                    # --- PAGE 1: BASIC ---
                                    # Yahan ab info_data['uid'] use ho raha hai jo function se match karta hai
                                    msg_page1 = f"[B][C][FF0000]╔════ [DATA 1/5] ════╗\n[FFFFFF]Nick : [00FF00]{info_data['name']}\n[FFFFFF]ID : {info_data['uid']}\n[00FF00]Loading Next... ⏳"
                                    P1 = await SEndMsG(response.Data.chat_type, msg_page1, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P1)

                                    # --- PAGE 2: STATS ---
                                    await asyncio.sleep(0.3)
                                    msg_page2 = f"[B][C][FF0000]╔════ [DATA 2/5] ════╗\n[FFFFFF]Level : {info_data['level']}\n[FFFFFF]Likes : {info_data['likes']}\n[FFFFFF]Experience : {info_data['exp']}\n[00FF00]Loading Next... ⏳"
                                    P2 = await SEndMsG(response.Data.chat_type, msg_page2, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P2)

                                    # --- PAGE 3: RANKS ---
                                    await asyncio.sleep(0.3)
                                    msg_page3 = f"[B][C][FF0000]╔════ [DATA 3/5] ════╗\n[FFFFFF]BR Points : {info_data['br_pts']}\n[00FFFF]CS Points : {info_data['cs_pts']}\n[FFFFFF]Region : {info_data['region']}\n[00FF00]Loading Next... ⏳"
                                    P3 = await SEndMsG(response.Data.chat_type, msg_page3, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P3)

                                    # --- PAGE 4: SOCIAL ---
                                    await asyncio.sleep(0.3)
                                    msg_page4 = f"[B][C][FF0000]╔════ [DATA 4/5] ════╗\n[FFFFFF]Guild : [00FFFF]{info_data['g_name']}\n[FFFFFF]Bio : {info_data['bio']}\n[00FF00]Finalizing... ⏳"
                                    P4 = await SEndMsG(response.Data.chat_type, msg_page4, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P4)

                                    # --- PAGE 5: ACTIVITY ---
                                    # Yahan 'login' aur 'created' use ho raha hai (Crash fixed)
                                    await asyncio.sleep(0.3)
                                    msg_page5 = f"[B][C][FF0000]╔════ [DATA 5/5] ════╗\n[FFFFFF]Seen : {info_data['login']}\n[FFFFFF]Born : {info_data['created']}\n[B][C][FF0000]╚═══════════════════╝"
                                    P5 = await SEndMsG(response.Data.chat_type, msg_page5, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P5)
                                    
                                    print("All Info Pages Sent!")
                                else:
                                    err_msg = "[B][C][FF0000]❌ Failed to fetch info.\nCheck UID or try again."
                                    P_ERR = await SEndMsG(response.Data.chat_type, err_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_ERR)



# CLAN INFO COMMAND
                        if inPuTMsG.strip().startswith('/clan_info '):
                            print('Processing clan info command')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /clan_info <clan_id>\nExample: /clan_info 100220304\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_clan_id = parts[1]
                                
                                # Initial Msg
                                wait_msg = f"[B][C][FFFF00]🔍 Fetching Info for Guild {target_clan_id}...\n"
                                await safe_send_message(response.Data.chat_type, wait_msg, uid, chat_id, key, iv)
                                
                                # Call Async Function using Bot's Token (jwt_token is passed in TcPChaT)
                                # Note: Ensure 'jwt_token' is available in TcPChaT arguments (I added it in previous steps)
                                result_msg = await get_clan_info_full(target_clan_id, jwt_token)
                                
                                await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)


                        if inPuTMsG.strip().startswith('/s'):
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)

# --- BADGE COMMANDS (NO SLASH) ---
                        if inPuTMsG.startswith(('s1 ', 's2 ', 's3 ', 's4 ', 's5 ')):
                            cmd = inPuTMsG.split()[0] # s1, s2 etc.
                            await handle_badge_command_logic(cmd, inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type, whisper_writer, online_writer)

                        if inPuTMsG in ("hi" , "bot" , "a" , "1" , "hello" , "fan" , "help" , "/help"):
                            uid = response.Data.uid
                            chat_id = response.Data.Chat_ID

                            # ==============================
                            # PAGE 1: BASIC & EMOTES
                            # ==============================
                            msg_page1 = """[C][B][00E5FF]╔════MENU (1/4)═════╗

[8A2BE2][B]├─ ☂︎ Add 100 Likes
[CCCCCC]│    ➜ /like <uid>

[8A2BE2][B]├─ ❄︎ Auto Join Team
[CCCCCC]│    ➜ Put TeamCode in Chat

[8A2BE2][B]├─ 💀 Old Emote Menu
[CCCCCC]│    ➜ elist

[8A2BE2][B]├─ 🎭 Start Emote Spam Team
[CCCCCC]│    ➜ spam

[8A2BE2][B]└─ ⛔ Stop All Tasks
[CCCCCC]     ➜ stop

[00E5FF]╚═══════════════╝"""

                            P1 = await SEndMsG(response.Data.chat_type , msg_page1 , uid , chat_id , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P1)

                            # Wait for 1.5 Seconds
                            await asyncio.sleep(0.8)

                            # ==============================
                            # PAGE 2: ATTACKS & LOBBY
                            # ==============================
                            msg_page2 = """[C][B][00E5FF]╔════MENU (2/4)═════╗

[FF00FF][B]├─ ☠️ Lag Team (15s)
[CCCCCC]│    ➜ lag <TeamCode>

[FF00FF][B]├─ ☠️ Force To Start Match
[CCCCCC]│    ➜ /start <TeamCode>

[FF00FF][B]├─ 📨 Spam Requests (UID)
[CCCCCC]│    ➜ spm <uid> <count>

[FF00FF][B]├─ 👨‍👩‍👦 Spam Requests (Team)
[CCCCCC]│    ➜ spm t <count>

[FF00FF][B]├─ ⚡ Create 5-Man Squad
[CCCCCC]│    ➜ 5

[FF00FF][B]└─ 🎵 Leave Lobby (Solo)
[CCCCCC]     ➜ solo

[00E5FF]╚═══════════════╝"""

                            P2 = await SEndMsG(response.Data.chat_type , msg_page2 , uid , chat_id , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P2)

                            # Wait for 1.5 Seconds
                            await asyncio.sleep(0.8)

                            # ==============================
                            # PAGE 3: FRIENDS & GUILD
                            # ==============================
                            msg_page3 = """[C][B][00E5FF]╔════MENU (3/4)═════╗

[00FFEA][B]├─ 📋 Friend Request List
[CCCCCC]│    ➜ /rlist

[00FFEA][B]├─ 👥 My Friend List
[CCCCCC]│    ➜ /ls

[00FFEA][B]├─ ➕ Add Friend
[CCCCCC]│    ➜ add <uid>

[00FFEA][B]├─ ❌ Remove Friend
[CCCCCC]│    ➜ remove <uid>

[00FFEA][B]└─ 🏰 Join Guild
[CCCCCC]     ➜ guild <guild_id>

[00E5FF]╚═══════════════╝"""

                            P3 = await SEndMsG(response.Data.chat_type , msg_page3 , uid , chat_id , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P3)

                            # Wait for 1.5 Seconds
                            await asyncio.sleep(0.8)

                            # ==============================
                            # PAGE 4: BADGE REQUESTS
                            # ==============================
                            msg_page4 = """[C][B][9400FF]╔════MENU (4/4)═════╗

[00FFEA][B]├─ Craftland Badge Join
[CCCCCC]│    ➜ s1 <uid>

[00FFEA][B]├─ New V-Badge Join
[CCCCCC]│    ➜ s2 <uid>

[00FFEA][B]├─ Moderator Badge Join
[CCCCCC]│    ➜ s3 <uid>

[00FFEA][B]├─ Small V-Badge Join
[CCCCCC]│    ➜ s4 <uid>

[00FFEA][B]└─ Pro Badge Join
[CCCCCC]     ➜ s5 <uid>

               [C][B][FFB300]👑 OWNER: SKBHAI
[9400FF]━━━━━━━━━━━━━━━━━"""

                            P4 = await SEndMsG(response.Data.chat_type , msg_page4 , uid , chat_id , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P4)
                        response = None
                            
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
                    
                    	
                    	
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    global bot_uid
    
    # Nm.txt se account load karega
    try:
        with open('Cr.txt', 'r') as file:
            data = json.load(file)
            if data:
                # Pehla account uthayega
                Uid = list(data.keys())[0]
                Pw = data[Uid]
                print(f"Loaded Account: {Uid}")
            else:
                print("Error: No account found in Cr.txt")
                return None
    except Exception as e:
        print(f"Error reading Cr.txt: {e}")
        return None
    

    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: print("ErroR - InvaLid AccounT") ; return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("TarGeT AccounT => BannEd / NoT ReGisTeReD ! ") ; return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    print(UrL)
    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    bot_uid = int(TarGeT) # <--- Bot UID Set
    
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: print("ErroR - GeTinG PorTs From LoGin DaTa !") ; return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    #print(acc_name)
    print(ToKen)
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region, ToKen))
     
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))
    os.system('clear')
    print(render('WINTER', colors=['white', 'green'], align='center'))
    print('')
    #print(' - ReGioN => {region}'.format(region))
    print(f" - BoT STarTinG And OnLine on TarGet : {TarGeT} | BOT NAME : {acc_name}\n")
    print(f" - BoT sTaTus > GooD | OnLinE ! (:")    
    print(f" - Subscribe > crowx64 | Gaming ! (:")    
    await asyncio.gather(task1 , task2)
    
async def StarTinG():
    while True:
        try: await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except asyncio.TimeoutError: print("Token ExpiRed ! , ResTartinG")
        except Exception as e: print(f"ErroR TcP - {e} => ResTarTinG ...")

if __name__ == '__main__':
    asyncio.run(StarTinG())