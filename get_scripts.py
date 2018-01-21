import requests
import re
import os


urls = [
        ["https://www.math.uni-hamburg.de/home/geschke/lehre.html.de", "/home/florian/Nextcloud/Documents/01 Uni/WISE 1718/Mathe/"],
        ["https://tams.informatik.uni-hamburg.de/lectures/2017ws/vorlesung/rs/uebung/index.php", "/home/florian/Nextcloud/Documents/01 Uni/WISE 1718/RS/"],
        ["https://tams.informatik.uni-hamburg.de/lectures/2017ws/vorlesung/rs/index.php?content=01-unterlagen", "/home/florian/Nextcloud/Documents/01 Uni/WISE 1718/RS/"]
    ]

#config = open("config.json","r")

text = ""


def main():
    for url in urls:
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
