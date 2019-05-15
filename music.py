import requests
import re
import json


class MusicDownload(object):
    base_url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery112407507331082826529_1536909176399" \
               "&keyword={}&page=1&pagesize=50&userid=-1&clientver=" \
               "&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1536909176401"

    down_url = "http://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191046558493281196833_1536907165442"\
              "&hash={}&album_id={}&_=1536907165443"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    # 初始化对象

    def __init__(self, song_name=None):
        self.song_name = song_name
        # 定义歌曲序号
        self.n = 1
        # 定义歌曲序号列表
        self.nlist = []
        self.parase_url = None

    # 音乐下载程序入口
    def run(self):
        if self.song_name is None:
            self.parase_url = self.base_url.replace('{}', '')
        else:
            if self.song_name.strip() == "":
                self.parase_url = self.base_url.replace('{}', '')
            else:
                self.parase_url = self.base_url.format(self.song_name)
        song_list = self._parase_page(self.parase_url)
        return song_list
    # 解析歌曲搜索页面

    def _parase_page(self, url):
        song_list = []
        respons = requests.get(url, headers=self.headers)
        text = respons.content.decode('utf-8')
        json_text = re.sub('jQuery112407507331082826529_1536909176399.*"lists":', '', text)
        rel_text = re.sub(',"chinesecount".*', '', json_text)
        if self.song_name is None:
            rel_text = re.sub(',"correctiontype".*', '', json_text)
        else:
            if self.song_name.strip() == "":
                rel_text = re.sub(',"correctiontype".*', '', json_text)
        list_text = json.loads(rel_text, encoding='utf-8')
        for dic in list_text:
            self.nlist.append(str(self.n))
            title = dic['FileName']
            hash = dic['FileHash']
            id = dic['AlbumID']
            duration = dic['Duration']
            seconds = duration % 60
            if seconds == "0":
                seconds = "00"
            if 0 < seconds < 10:
                seconds = "0"+str(seconds)
            album_name = "《"+re.sub('[<em> | </em>]', '', dic['AlbumName'])+"》"
            if len(album_name) > 25:
                album_name = album_name[0:25]+'...'
            if dic['AlbumID'] == "":
                album_name = "无"
            title = re.sub('[<em> | </em>]', '', title)
            if len(title) > 25:
                title = title[0:25]+'...'
            song_dic = (self.n, title, album_name, str(duration // 60)+":"+str(seconds), hash, id)
            song_list.append(song_dic)
            self.n += 1
        return song_list
    # 解析歌曲地址

    def download_url(self, request_hash, request_id):
        url = self.down_url.format(request_hash, request_id)
        respons = requests.get(url, headers=self.headers)
        text = respons.content.decode('utf-8')
        text = text.replace('\\', '')
        download_url = text[text.index("http://fs"):text.index("authors")-3]  # 歌曲地址
        return download_url
