import os, requests
from opencc import OpenCC
cc = OpenCC('t2s') 

TOKEN = ""
HEAD  = {"Authorization": f"Bearer {TOKEN}"}

# Proxy setting
PROXIES = {
    "https": "http://127.0.0.1:7890",   # Clash HTTP 
    # "https": "socks5h://127.0.0.1:7891",  #  SOCKS5
}


playlists, url = [], "https://api.spotify.com/v1/me/playlists?limit=50"
while url:
    r = requests.get(url, headers=HEAD, 
                     #proxies=PROXIES,
                       timeout=15)
    r.raise_for_status()
    data = r.json()
    playlists += data["items"]
    url = data.get("next")

print(f"发现 {len(playlists)} 个歌单")

for pl in playlists:
    pl_id   = pl["id"]
    pl_name = pl["name"].replace("/", "_")        
    print(f"  ➜ 正在处理 «{pl_name}» …")

    tracks, url = [], f"https://api.spotify.com/v1/playlists/{pl_id}/tracks?limit=100&fields=items(track(name,artists(name))),next"
    while url:
        r = requests.get(url, headers=HEAD, 
                        #proxies=PROXIES,
                           timeout=15)
        r.raise_for_status()
        data = r.json()
        for item in data["items"]:
            t = item["track"]
            title   = cc.convert(t["name"])
            artist  = " / ".join(cc.convert(a["name"]) for a in t["artists"])
            tracks.append(f"{title} - {artist}")
        url = data.get("next")

    with open(f"{pl_name}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(tracks))
    print(f"    已写 {len(tracks):>3} 首 → {pl_name}.txt")

print("全部完成！")