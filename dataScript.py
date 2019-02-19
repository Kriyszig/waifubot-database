import requests
from bs4 import BeautifulSoup
from pprint import pprint
import time

def scraper(cnt, CharacterList):
    url = 'https://myanimelist.net/character.php?limit=' + str(cnt)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('a'):
        hlurl = link.get('href')
        if(hlurl == None):
            continue
        if(hlurl.find("/character/") > -1):
            if hlurl.strip() in CharacterList:
                continue
            CharacterList.append(hlurl.strip())


if __name__ == "__main__":
    try:
        fin = open('cleandata.csv', 'r')
        done = fin.readlines()
        fin.close()
        CharacterList = []
        for element in done:
            breakdown = element.split(',')
            CharacterList.append('https://myanimelist.net/character/' + breakdown[0] + '/' + breakdown[1].replace(' ','_'))
        cnt = (len(CharacterList)//50)*50
        done = len(CharacterList)
        while(True):
            scraper(cnt, CharacterList)
            # pprint(characterList)
            # print(len(characterList))
            for character in CharacterList[done:]:
                # print(character)
                pos1 = character.find('/character/')
                pos2 = (pos1 + 11 + character[(pos1 + 11):].find("/"))
                characterId = character[(pos1 + 11):pos2]
                # print(characterId)
                field = "https://api.jikan.moe/v3/character/" + str(characterId) + "/pictures"
                response = requests.get(field)
                data = response.json()
                # pprint(data)
                # print(data['pictures'][0]['large'])
                if('pictures' in data and len(data['pictures']) > 0):
                    outf = open('cleandata.csv', 'a')
                    outf.write(characterId + "," + character[pos2 + 1:].replace('_', ' ') + "," + data['pictures'][0]['large'] + '\n')
                    outf.close()
                else:
                    outf = open('unknownWaifu.csv', 'a')
                    outf.write(character + '\n')
                    outf.close()
                time.sleep(2)
                done += 1
                print(done)
            cnt += 50
    except KeyboardInterrupt:
        print(cnt)
    finally:
        print(cnt)
