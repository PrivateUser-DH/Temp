import sqlite3
import random
from flask import Flask, request, render_template, redirect, url_for, g

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    fixed_username = "'OR' 1'='" #-----
    message = None
    message_class = ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        result = db.execute(query).fetchall()
        
        if result:
            return redirect(url_for('decode_task'))
        else:
            message = 'Invalid credentials!'
            message_class = 'error-message'
            
    return render_template('login1.html' ,fixed_username = fixed_username, message=message, message_class=message_class)

@app.route('/decode_task', methods=['GET', 'POST'])


def decode_task():
    # Generate a random binary number between 1 and 255 (8 bits)
    #random_number = random.randint(1, 4095)
    binary_value = '110000000110'
    decimal_value = 3078# Convert to binary, remove '0b' prefix
    message = None
    
    if request.method == 'POST':
        user_input = request.form['decimal_value']
        #correct_decimal = str(int(request.form['correct_decimal']))  # Convert correct answer to string
        
        # Check if the user input matches the correct decimal value
        if user_input == str(decimal_value):
            return redirect(url_for('caesar_cipher_task'))  # Redirect to the next task
        else:
            message = f'Incorrect! Try again. The binary number was {binary_value}.'

    return render_template('decode_task.html', binary_value=binary_value, message=message)

@app.route('/caesar_cipher_task', methods=['GET', 'POST'])
def caesar_cipher_task():
    shift = 3
    plaintext = "FLASKAPP"
    ciphertext = ''.join(chr(((ord(char) - 65 + shift) % 26) + 65) for char in plaintext)
    message = None

    if request.method == 'POST':
        user_input = request.form['caesar_input'].upper()
        if user_input == plaintext:
            return redirect(url_for('new_task'))  # Redirect to next task after successful cipher decode
        else:
            message = 'Incorrect! Try again.'

    return render_template('caesar_cipher.html', ciphertext=ciphertext, message=message)


@app.route('/new_task')
def new_task():
    return '<h2>New Task: This is the next task page!</h2>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
