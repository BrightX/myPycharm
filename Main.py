from flask import Flask, request
from flask import render_template
from music import MusicDownload
app = Flask(__name__)


@app.route('/')
def ku_zhu():
    song_input = request.args.get('song_input')
    md = MusicDownload(song_input)
    song_list = md.run()
    return render_template("index.html", context=song_list)


@app.route('/parase_url')
def parase_url():
    hash = request.args.get('hash')
    id = request.args.get('id')

    title = request.args.get('title')
    md = MusicDownload()
    download_url = md.download_url(hash, id)
    return render_template("download_url.html", context=(title, download_url))


if __name__ == '__main__':
    app.run()
