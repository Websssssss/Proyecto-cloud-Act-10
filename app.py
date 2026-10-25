from flask import Flask, request, render_template_string, session, redirect, url_for
import psycopg2
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

HTML_LOGIN = """
<h2>Iniciar Sesión</h2>
<form method="POST">
    Usuario: <input type="text" name="usuario" required><br><br>
    Clave: <input type="password" name="password" required><br><br>
    <button type="submit">Entrar</button>
</form>
<p style="color:red;">{{ error }}</p>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        user = request.form['usuario']
        pwd = request.form['password'].encode('utf-8')
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT password_hash, nombre FROM usuarios WHERE usuario = %s', (user,))
        res = cur.fetchone()
        cur.close()
        conn.close()

        if res and bcrypt.checkpw(pwd, res[0].encode('utf-8')):
            session['nombre'] = res[1]
            return redirect(url_for('bienvenida'))
        else:
            error = 'Credenciales inválidas'
            
    return render_template_string(HTML_LOGIN, error=error)

@app.route('/bienvenida')
def bienvenida():
    if 'nombre' not in session:
        return redirect(url_for('login'))
    return f"<h1>Bienvenido, {session['nombre']}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)