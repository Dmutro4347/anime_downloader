import requests
import json
import re
from bs4 import BeautifulSoup


def get_hash(link_to_anime):
    html_code = requests.get(link_to_anime).text
    hash_pattern = re.compile(r'\b[0-9a-f]{40}\b')
    hash_match = hash_pattern.search(html_code)
    
    return hash_match.group(0)


def get_anime_code(link_to_anime):
    pattern = r"https://anitube\.in\.ua/(\d+)-"
    match = re.search(pattern, link_to_anime)

    return match.group(1)


def get_episodes_numbers(link_to_anime):
    soup = BeautifulSoup(requests.get(link_to_anime).text, "lxml")

    strong_tags = soup.find_all('strong')

    for tag in strong_tags:
        if 'Серій:' in tag.text:
            series_info = tag.next_sibling.strip()
            num_episodes = series_info.split(' ')[0]
            return int(num_episodes)

def get_link_to_anime(url_to_get_episodes_links, episodes_number, episodes_offset=0):
    data_dict = json.loads(requests.get(url_to_get_episodes_links).text)

    soup = BeautifulSoup(data_dict["response"], "lxml")
    data = soup.find("div", class_="playlists-videos").find_all("li")[episodes_offset:episodes_number]

    links_to_episodes = []
    name_of_episodes = []

    for i in data:
        links_to_episodes.append(i.get("data-file"))
    for i in data:
        name_of_episodes.append(i.text)


    return links_to_episodes, name_of_episodes


def get_url_to_download_episodes(links_to_episodes):
    url_to_download_episodes = []
    for i in links_to_episodes:
        player_link = "https://jk19ocmjeoyql3tj.ashdi.vip/content/stream/serials/"
        pattern = f"{player_link}(.*)"

        match = re.search(pattern, requests.get(i).text)

        end_link = match.group(1)
        end_link = end_link.replace('screen.jpg",', '')
        link_to_download_anime = f"{player_link}{end_link}hls/720"
        url_to_download_episodes.append(link_to_download_anime)
    
    # print(url_to_download_episodes)
    return url_to_download_episodes


def download_episodes(url_to_download_episodes, name_of_episodes):
        for i in range(0, len(url_to_download_episodes)):
            episode_name = name_of_episodes[i]
            url = url_to_download_episodes[i]
            if requests.get(f"{url}/segment1.ps").status_code != 404:
                ending = "ps"
            else:
                ending = "ts"

            video = requests.get(f"{url}/segment1.{ending}").content

            with open(f"{episode_name}.mp4", "wb") as fl:
                fl.write(video)


            for n in range(2, 290):
                video = requests.get(f"{url}/segment{n}.{ending}").content

                with open(f"{episode_name}.mp4", "ab") as fl:
                    fl.write(video)

            print(f"Done {episode_name}")


def main():
    url_to_anime = "https://anitube.in.ua/2875-ncal-d-pershiy-etap.html"
    data = {
        "news_id": get_anime_code(url_to_anime),
        "user_hash": get_hash(url_to_anime)
    }


    url_to_get_episodes_links = f"https://anitube.in.ua/engine/ajax/playlists.php?news_id={data["news_id"]}&xfield=playlist&user_hash={data["user_hash"]}"

    episodes_number = get_episodes_numbers(url_to_anime)
    links_to_episodes, name_of_episodes = get_link_to_anime(url_to_get_episodes_links, episodes_number, 16)
    url_to_download_episodes = get_url_to_download_episodes(links_to_episodes)
    download_episodes(url_to_download_episodes, name_of_episodes)

if __name__ == "__main__":
    main()

