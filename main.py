from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import folium
import openai
app = Flask(__name__)

app.secret_key = os.getenv("KEY")
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'
mysql = MySQL(app)

openai.api_key = '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'

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #I had a SQL server access problem with my device, so I used a demo value to show results
        if username == "test" and password == "test":
            session['loggedin'] = True
            session['id'] = None  
            session['username'] = username  
            return redirect(url_for('home'))
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('home'))
            else:

                msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    else:
        return "You are not logged in. Please log in first."

@app.route('/pythonlogin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/user_profile/maps')
def maps():
    map = folium.Map(
        location = [45.52336,-122.6750])
    return map._repr_html_()
def fetch_recommendations():
    prompt = "Provide personalized recommendations for international students staying off campus near Georgia State University. The response must be in specific bullet points starting from the time a student arrives on campus to finding suitable accommodations, understanding local bills and contract terms, setting up essential banking services, and accessing additional resources."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,  
        n=5,  
        stop=None,
    )
    recommendations = response.choices
    formatted_recommendations = [rec['text'] for rec in recommendations]

    return formatted_recommendations

@app.route('/show_recommendations')
def show_recommendations():

    recommendations = fetch_recommendations()
    print(recommendations);
    return render_template('home.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
