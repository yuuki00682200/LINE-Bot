import requests
import random
import urllib
import base64
import json
import bs4


class WebData:
    def __init__(self):
        pass

    def get_genre_with_maimai(self) -> dict:
        url = 'https://w.atwiki.jp/simai/pages/32.html'
        html = requests.get(url).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tbodys = soup.find_all('table')
        genres = {}
        for tbody in tbodys:
            genre = tbody.find_all('tr')
            genres[genre[0].text.strip()] = genre[1:]
        return genres

    def get_music_with_maimai(self,
                              keyword: str) -> str:
        genres = self.get_genre_with_maimai()
        result = {}
        for genre, value in genres.items():
            if keyword in genre:
                for val in value:
                    tag = val.find('a')
                    if tag:
                        name = tag.text
                        href = tag.get('href')
                        result[name] = f'https:{href}#MASTER'
        return result

    def get_musicinfo_with_maimai(self, genre: str,
                                  title: str) -> str:
        genres = self.get_music_with_maimai(genre)
        url = ''
        for name, value in genres.items():
            if name.startswith(title):
                url = value
        html = requests.get(url).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        divlist = soup.find_all('div')
        result = ''
        bpm = soup.find('td', {'style': 'text-align:center;'}).text
        for div in divlist:
            data = div.text
            if data:
                if data.strip().startswith(f'({bpm})'):
                    index = divlist.index(div)

        for data in divlist[index:]:
            if data.text:
                if data.text.strip().endswith('E'):
                    break
                result += data.text
        return result

    def image_to_url(self, path: str) -> str:
        clid = 'e31111dc4015e1b'
        api_key = 'f39558875d630b3dd42c58421e5bb4c01d69d57a'
        url = 'https://api.imgur.com/3/upload.json'
        headers = {'Authorization': f'Client-ID {clid}'}
        data = {
            'key': api_key,
            'image': base64.b64encode(open(path, 'rb').read()),
            'type': 'base64',
            'name': path,
            'title': path
        }
        res = requests.post(url, headers=headers, data=data)
        return res.json()['data']['link']

    def save_video_with_xvideo(self, url: str) -> (str, str):
        html = requests.get(url).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        duration = soup.find('span', class_='duration').text
        script = soup.find_all('script')
        links = str(script[7]).split('\n')
        link = ''
        for i in links:
            if "html5player.setVideoUrlLow('" in i:
                link += i
        video = link.split("'")[1]
        return video, duration

    def get_short_url(self, url: str) -> str:
        params = (
            ('action', 'shortURL'),
            ('input_url', url),
        )

        response = requests.get('https://kuku.lu/index.php', params=params)

        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        get = soup.find('div', {'style': 'padding-bottom:10px;color:black;'})
        return get.text

    def get_image_with_google(self, text: str) -> (bool, str):
        keyword = urllib.parse.quote(text)
        url = "https://www.google.com/search?hl=jp&q=" + \
            keyword + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }
        html = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        elems = soup.select('.rg_meta.notranslate')
        elem = random.choice(elems)
        elem = elem.contents[0].replace('"', '').split(',')
        elemdict = {}
        for e in elem:
            num = e.find(':')
            elemdict[e[0:num]] = e[num + 1:]
        url = elemdict['ou']
        gif = False
        if '.gif' in url:
            gif = True
        return gif, url

    def get_lyric(self, title: str) -> (str, str, str, str):

        sUrl = 'https://utaten.com/search/=/show_artists=1/layout_search_text=%s/layout_search_type=title/' % title
        sResultResponce = requests.get(sUrl)
        sHtml = sResultResponce.text
        sSoup = bs4.BeautifulSoup(sHtml, 'html.parser')
        list__main = sSoup.find('p', class_='searchResult__title')
        topResult = list__main.find('a').attrs['href']

        url = 'https://utaten.com/%s' % topResult

        res = requests.get(url)
        html = res.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        name = soup.find_all("span", {"class": "movieTtl_mainTxt"})[0].ing

        lyrics = soup.find('div', class_='hiragana')
        rt_list = lyrics.find_all('span', class_='rt')

        for rt in rt_list:
            rt.extract()

        a = soup.find('a', class_='lnk_gaugeLst_youtubeLink')
        movurl = 'https://utaten.com' + a.attrs['href']

        movRes = requests.get(movurl)
        movSoup = bs4.BeautifulSoup(movRes.text, 'html.parser')
        src = movSoup.find_all('iframe')[1]
        youtubeUrl = src.attrs['src'].replace(
            'www.youtube.com', 'youtu.be').replace('/embed', '')

        lyric = lyrics.get_text().strip()
        return lyric, youtubeUrl, url, name


if __name__ == '__main__':
    M = WebData()
    print(M.get_musicinfo_with_maimai('SEGA', 'awake'))
