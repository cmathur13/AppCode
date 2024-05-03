import requests
from flask import Flask, render_template
from flask_caching import Cache

app = Flask(__name__)
cache = Cache()
app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects")
@cache.cached(timeout=60) # 43200 = 12 tuntia
def get_repos():
    api_url = "https://api.github.com/users/alexanderritik/repos"
    response = requests.get(api_url).json()
    repos = []
    for data in response:
        if 'ohtu' not in data['name']:
            if 'minitex' not in data['name']:
                repo = {}
                repo['name'] = data['name'].replace("-", " ").title()
                repo['description'] = data['description']
                repo['language'] = data['language']
                repo['topics'] = data['topics']
                repo['html_url'] = data['html_url']
                repo['updated_at'] = data['updated_at']
                repos.append(repo)
    return render_template("projects.html", repos=repos)
