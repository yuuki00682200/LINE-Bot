import requests
import urllib
import bs4

class Web:
    def __init__(self):
        self.host = "http://jpnrdb.com"
        self.rdblist = "/pic/legend_rdb.gif"

    def get_red_list(self, name):
        url = f"{self.host}/search.php?mode=key&q={name}"
        html = requests.get(url)

        soup = bs4.BeautifulSoup(html.content, "lxml")
        list = soup.find("table", {"class":"table_kekka"})
        results = map(lambda x:x.a, list.find_all("td", {"class":"list", "width":"30%"}))
        results = filter(lambda x:bool(x), results)
        texts = map(lambda x:(x.text, f"{self.host}/search.php{x.get('href')}"), results)
        return texts

    def get_red(self, name):
        texts = self.get_red_list(name)
        next_url = dict(texts)[name]
        html = requests.get(next_url)
        soup = bs4.BeautifulSoup(html.content, "lxml")
        map_ = soup.find("div", {"style":"border:1px #cccccc solid"})
        map_url = f"{self.host}{map_.find('img').get('src')[1:]}"
        return map_url

if __name__ == "__main__":
    M = Web()
    res = M.get_red("カネコトタテグモ")
    print(res)

