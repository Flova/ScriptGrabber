import requests
import re
import os
import json


text = ""


def import_data():
    urls = []
    # Change config.json your JSON filename
    config = json.load(open("config.json", "r"))
    for index, page in enumerate(config["pages"]):
        urls.append([page["url"], page["local"]])
    return urls


def main():
    pages = import_data()
    print("---- Searching on " + str(len(pages)) + " sources ----")
    for url in pages:
        r = requests.get(url[0])
        links = re.findall('".*?.pdf"', r.text)
        letzter_slash = len(url[0])
        for index, zeichen in enumerate(url[0]):
            if(zeichen == "/" and index > 7):
                letzter_slash = index
        url_mod = url[0][0:letzter_slash]
        lokal = url[1]
        for link in links:
            if "http" == link[1:5]:
                dokument_url = link[1:-1]
            else:
                dokument_url = url_mod + "/" + link[1:-1]
            datei_name = dokument_url.rsplit('/', 1)[1]
            if not os.path.isfile(lokal + datei_name):
                print("Downloading " + dokument_url)
                rb = requests.get(dokument_url, allow_redirects=True)
                open(lokal + datei_name, 'wb').write(rb.content)


if __name__ == "__main__":
    main()
    print("-----Finished-----")
