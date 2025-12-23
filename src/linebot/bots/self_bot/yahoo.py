import requests
import bs4
import datetime
import random


class Yahoo:
    def __init__(self):
        pass

    def get_url(self, city: str) -> str:
        sUrl = f'https://weather.yahoo.co.jp/weather/search/?p={city}'
        sHtml = requests.get(sUrl)
        sSoup = bs4.BeautifulSoup(sHtml.text, 'html.parser')
        sTbody = sSoup.find('tbody').find_all('tr')
        sCity = random.choice(sTbody)
        return 'https:' + sCity.find('a').get('href')

    def get_weather(self, city: str) -> (str, dict):
        url = self.get_url(city)
        html = requests.get(url)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        name = soup.find('div', {'id': 'cat-pass'}).find_all('a')[3]
        weather = [n.text for n in soup.find_all('small')[9:20]]
        weather = weather[weather.index("天気")+1:weather.index("天気")+9]
        times = ['0時', '3時', '6時', '9時', '12時', '15時', '18時', '21時']
        result = dict(zip(times, weather))
        return name.text, result

    def get_train(self, st: str, en: str) -> str:
        dnow = datetime.datetime.now()
        day = dnow.strftime('%M')
        m1 = day[0]
        m2 = day[1]
        url = f'https://transit.yahoo.co.jp/search/result?flatlon=&fromgid=&from=;:;&tlatlon=&togid=&to=:;:&viacode=&via=&viacode=&via=&viacode=&via=&y=%Y&m=%m&d=%d&hh=%H&m2={m2}&m1={m1}&type=1&ticket=ic&expkind=1&ws=3&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1&kw=:;:'.replace(
            ':;:',
            en).replace(
            ';:;',
            st)
        url = dnow.strftime(url)
        html = requests.get(url)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        time = soup.find('dl', class_='routeSummary')
        result = ''
        for t in time:
            try:
                result += t.find('span').text if 'ルート' not in t.find('span').text else ''
            except BaseException:
                pass
        data = soup.find('div', class_='routeDetail')
        for d in data:
            try:
                result += d.text.strip() if '地図' not in d.text else ''
            except BaseException:
                pass

        result = result.replace(
            'ホテル',
            '').replace(
            '[line]',
            '').replace(
            '[train]',
            '').replace(
                '[arr]',
                '').replace(
                    '[dep]',
            '')
        return result

    def get_news(self) -> list:
        url = 'https://news.yahoo.co.jp'
        html = requests.get(url)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        topics = soup.find('ul', class_='topicsList_main')
        links = list(map(lambda a: a.find('a').get('href'), topics))
        result = list()
        for link in links:
            html = requests.get(link)
            soup = bs4.BeautifulSoup(html.text, 'html.parser')
            title = soup.find(
                'h2', class_='tpcNews_title').text.strip().replace(
                '\u3000', '')
            body = soup.find(
                'p', class_='tpcNews_summary').text.replace(
                '\u3000', '')
            result.append((title, body))
        return result


if __name__ == '__main__':
    pass
