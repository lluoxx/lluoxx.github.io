from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

LINKS_FILE = 'links.json'
SECRET_KEY = '1667'

DEFAULT_LINKS = [
    {"label": "Help & Documentation", "url": "https://fr.lowkey.nichesite.org/help.txt"},
    {"label": "File Server Root", "url": "https://fr.lowkey.nichesite.org/"}
]

def read_links():
    if not os.path.exists(LINKS_FILE):
        write_links(DEFAULT_LINKS)
        return DEFAULT_LINKS
    with open(LINKS_FILE, 'r') as f:
        return json.load(f)

def write_links(links):
    with open(LINKS_FILE, 'w') as f:
        json.dump(links, f, indent=2)

def check_auth(req):
    return req.headers.get('X-Key') == SECRET_KEY

@app.route('/links', methods=['GET'])
def get_links():
    return jsonify(read_links())

@app.route('/links', methods=['POST'])
def add_link():
    if not check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    if not data or not data.get('label') or not data.get('url'):
        return jsonify({'error': 'Missing label or url'}), 400
    links = read_links()
    links.append({'label': data['label'], 'url': data['url']})
    write_links(links)
    return jsonify({'ok': True})

@app.route('/links/<int:index>', methods=['DELETE'])
def delete_link(index):
    if not check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    links = read_links()
    if index < 0 or index >= len(links):
        return jsonify({'error': 'Index out of range'}), 400
    links.pop(index)
    write_links(links)
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
