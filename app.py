import os.path
import youtube_dl
from flask import Flask, send_file, render_template, request, redirect, url_for, send_from_directory, make_response
app = Flask(__name__,template_folder='template')

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def util(defUrl):
    # getting a get request from client
    #url = request.args.get(defUrl)

    # function call for downloding
    mp3_file_name = get_mp3(defUrl)

    # sending file as response
    resp = make_response(
        send_file("./song.mp3", mimetype='audio/wav', as_attachment=True, attachment_filename="audio.mp3"))

    return resp


def get_mp3(url):
    # gets video information from url
    video_info = youtube_dl.YoutubeDL().extract_info(
        url, download=False
    )
    file_name = "song.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': file_name,
        # conversion
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    # downloads song with above parameters
    with youtube_dl.YoutubeDL(options) as download:
        download.download([url])

    return file_name


@app.route('/hello', methods=['POST'])
def hello():
    defUrl = request.form.get('name')    

    if defUrl:
        print('Request for hello page received with name=%s' % defUrl)
        #return send_file("/tmp/output.mp3",as_attachment=True)
        return util(defUrl)
        #return render_template('hello.html', name = defUrl)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return render_template('index.html')

if __name__ == '__main__':
    app.run()

