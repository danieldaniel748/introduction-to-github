from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi ke MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Ganti dengan alamat host MySQL Anda
        user='daniel',       # Ganti dengan username MySQL Anda
        password='Password2@',  # Ganti dengan password MySQL Anda
        database='ticketing_system'  # Nama database
    )
    return connection

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tickets', methods=['GET', 'POST'])
def ticket_list():
    if request.method == 'POST':
        # Ambil data dari form
        title = request.form['title']
        description = request.form['description']
        
        # Masukkan data ke dalam database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO tickets (title, description) VALUES (%s, %s)', (title, description))
        connection.commit()  # Simpan perubahan
        cursor.close()
        connection.close()

        return redirect(url_for('ticket_list'))
    
    # Ambil semua tiket dari database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tickets')
    tickets = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('tickets.html', tickets=tickets)

if __name__ == '__main__':
    print("Running Flask server on http://127.0.0.1:5000/")
    app.run(port=5000, debug=True)

