import requests

video = requests.get(f"https://calypso.tortuga.wtf/content/stream/chest/black.lagoon.s01e07.qtv.dvo_58929/hls/720/segment1.ts").content

with open(f"7 серія.mp4", "wb") as fl:
  fl.write(video)

for n in range(2, 290):
  video = requests.get(f"https://calypso.tortuga.wtf/content/stream/chest/black.lagoon.s01e07.qtv.dvo_58929/hls/720/segment{n}.ts").content

  with open(f"7 серія.mp4", "ab") as fl:
    fl.write(video)