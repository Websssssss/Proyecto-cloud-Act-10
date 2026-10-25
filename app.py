from flask import Flask, request, render_template, render_template_string, session, redirect, url_for
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def inicializar_bd():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # ESTA LÍNEA SOLUCIONA EL ERROR: Borra la tabla vieja para crearla bien
        cur.execute('DROP TABLE IF EXISTS usuarios CASCADE;')
        
        cur.execute('''
            CREATE TABLE usuarios (
                id SERIAL PRIMARY KEY,
                usuario VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                nombre VARCHAR(100) NOT NULL
            )
        ''')
        cur.execute('SELECT COUNT(*) FROM usuarios')
        if cur.fetchone()[0] == 0:
            cur.execute('''
                INSERT INTO usuarios (usuario, password_hash, nombre) VALUES
                ('test1', '12345', 'Juan Perez'),
                ('test2', '12345', 'Maria Gomez')
            ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error inicializando la base de datos: {e}")

# 1. Ruta principal que muestra tu página web moderna (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# 2. Ruta de inicio de sesión (Login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        user = request.form['usuario']
        pwd = request.form['password']
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT password_hash, nombre FROM usuarios WHERE usuario = %s', (user,))
            res = cur.fetchone()
            cur.close()
            conn.close()

            if res and pwd == res[0]:
                session['nombre'] = res[1]
                return redirect(url_for('bienvenida'))
            else:
                error = 'Credenciales inválidas'
        except Exception as e:
            error = f'Error: {e}'
            
    # Plantilla interna sencilla para el login del laboratorio
    html_login = """
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Login Lab</title></head>
    <body style="font-family: Arial; display: grid; place-items: center; height: 100vh; background: #f9f7f0;">
      <div style="background: white; padding: 30px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <h2>Iniciar Sesión (Lab)</h2>
        <form method="POST">
            Usuario: <br><input type="text" name="usuario" required style="width: 100%; padding: 8px; margin: 8px 0;"><br>
            Clave: <br><input type="password" name="password" required style="width: 100%; padding: 8px; margin: 8px 0;"><br><br>
            <button type="submit" style="width: 100%; padding: 10px; background: #eb7446; color: white; border: none; font-weight: bold; cursor: pointer;">Entrar</button>
        </form>
        <p style="color:red; text-align:center;">{{ error }}</p>
        <p style="text-align:center;"><a href="/">Volver al inicio</a></p>
      </div>
    </body>
    </html>
    """
    return render_template_string(html_login, error=error)

@app.route('/bienvenida')
def bienvenida():
    if 'nombre' not in session:
        return redirect(url_for('login'))
    return f"""
    <div style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1>¡Bienvenido, {session['nombre']}!</h1>
        <p>Sesión validada correctamente con PostgreSQL en Blitz Cloud.</p>
        <a href="/">Ir a la página principal</a>
    </div>
    """

if __name__ == '__main__':
    if os.getenv('DATABASE_URL'):
        inicializar_bd()
    app.run(host='0.0.0.0', port=5000)