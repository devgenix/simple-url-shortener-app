from flask import Flask, render_template, request, redirect, url_for
import string
import random

app = Flask(__name__)

# In-memory storage for URLs
url_map = {}

def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url
        
        short_id = generate_short_id()
        url_map[short_id] = original_url
        
        short_url = request.host_url + short_id
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<short_id>')
def redirect_to_url(short_id):
    original_url = url_map.get(short_id)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
