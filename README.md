# Actividad 10: Despliegue Cloud con Flask & PostgreSQL

## 👥 Integrantes del Equipo
* Gonzales Cuaresma Alondra Yamileth | 2312461 
* Morales Apolinario, Anyeli María  | 2312227 
* Ruiz Victorio, Paola Rosmery | 2312213 
* Hernandez Carrillo, Jerko Khaleb | 2220847 
* Haji Taira, Yasmin Akemi | 2310089 
* Maquen Caisan, Fabian | 2311685


---

## 🚀 Descripción del Proyecto
Este repositorio contiene el código fuente y la configuración necesaria para desplegar una aplicación web desarrollada en Flask y conectada a una base de datos PostgreSQL. Todo el entorno está empaquetado en contenedores Docker y alojado con alta disponibilidad en la plataforma PaaS Blitz Cloud.

## 🛠️ Tecnologías Utilizadas
- **Backend:** Python 3.9, Flask
- **Base de Datos:** PostgreSQL 17 (Instancia en la nube)
- **Virtualización:** Docker
- **Frontend:** HTML5, CSS3
- **Infraestructura Cloud:** Blitz Cloud

## 📂 Estructura del Proyecto
```text
Proyecto cloud Act 10/
├── app.py                 # Lógica principal, rutas y conexión a la BD
├── requirements.txt       # Dependencias de Python (Flask, psycopg2-binary)
├── Dockerfile             # Configuración de la imagen del contenedor
├── README.md              # Documentación del proyecto
├── templates/             
│   └── index.html         # Interfaz principal y vistas
└── static/                
    └── styles.css         # Estilos visuales