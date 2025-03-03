from flask import Flask, render_template, request

app = Flask(__name__)


PUBLIC_CONTENT = """
<h2>Sea Turtle Soup Game</h2>
<p>The common name is a situational puzzle, or a lateral thinking puzzle.<br><br>

Horizontal thinking is a way of thinking that complements vertical thinking,<br><br>

observing and reviewing situations and developing thoughts logically is called vertical thinking.<br><br>

A way of thinking that moves around between various ideas is called horizontal thinking.<br><br><br><br>
<h2>How to play</h2></p>
<p>The process of Sea Turtle Soup Game is as follows.</p>
"""

FULL_CONTENT = """
<p>WP{**flag**}</p>
"""

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    if 'Googlebot' in user_agent:
        premium_content = FULL_CONTENT
    else:
        premium_content = ""
    return render_template('index.html', public_content=PUBLIC_CONTENT, premium_content=premium_content)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=200015)
