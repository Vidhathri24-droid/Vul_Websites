from flask import Flask, request, render_template, render_template_string
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
        input = request.form['input']
        result = os.popen(f" {input} ").read()
        return render_template_string('<pre>{{ result }}</pre>', result=result)

if __name__ == "__main__":
        app.run(debug=True)
