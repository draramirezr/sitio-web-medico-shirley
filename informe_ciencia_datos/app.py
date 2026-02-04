"""
Aplicación Flask - Informe: Perfil Profesional del Científico de Datos
Autor: [Tu nombre]
Fecha: 25 de Enero, 2026
"""

from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# Datos del informe
ROLES_DATA = {
    'cientifico_datos': {
        'nombre': 'Científico de Datos',
        'nombre_ingles': 'Data Scientist',
        'descripcion': 'Profesional especializado en extraer conocimiento e insights de datos complejos mediante técnicas estadísticas, machine learning y programación avanzada.',
        'habilidades': [
            'Estadística avanzada y probabilidad',
            'Machine Learning y Deep Learning',
            'Programación (Python, R, SQL)',
            'Visualización de datos',
            'Comunicación de resultados',
            'Pensamiento analítico',
            'Conocimiento del negocio'
        ],
        'herramientas': [
            'Python (scikit-learn, TensorFlow, PyTorch)',
            'R (tidyverse, caret)',
            'Jupyter Notebooks',
            'SQL y NoSQL',
            'Git/GitHub',
            'Tableau, Power BI',
            'Cloud (AWS, GCP, Azure)'
        ],
        'responsabilidades': [
            'Diseñar y desarrollar modelos predictivos',
            'Realizar análisis estadísticos complejos',
            'Crear algoritmos de machine learning',
            'Investigar y aplicar nuevas técnicas de IA',
            'Presentar insights a stakeholders',
            'Definir métricas y KPIs estratégicos',
            'Colaborar con equipos multidisciplinarios'
        ],
        'formacion': [
            'Maestría o Doctorado en Ciencias de Datos, Estadística, Matemáticas, Física o Ingeniería',
            'Conocimientos profundos en matemáticas y estadística',
            'Experiencia en investigación científica (deseable)'
        ],
        'salario_promedio': '$80,000 - $150,000 USD/año',
        'color': '#4CAF50'
    },
    'analista_datos': {
        'nombre': 'Analista de Datos',
        'nombre_ingles': 'Data Analyst',
        'descripcion': 'Profesional enfocado en interpretar datos existentes, crear reportes y dashboards para apoyar decisiones de negocio.',
        'habilidades': [
            'SQL y consultas de bases de datos',
            'Excel avanzado',
            'Visualización de datos (Tableau, Power BI)',
            'Estadística descriptiva',
            'Interpretación de datos',
            'Comunicación de resultados',
            'Conocimiento del negocio'
        ],
        'herramientas': [
            'SQL (MySQL, PostgreSQL)',
            'Excel / Google Sheets',
            'Tableau / Power BI',
            'Python básico (Pandas, Matplotlib)',
            'Google Analytics',
            'Looker, Metabase',
            'ETL básico'
        ],
        'responsabilidades': [
            'Crear reportes y dashboards',
            'Analizar tendencias y patrones',
            'Limpiar y preparar datos',
            'Generar insights para el negocio',
            'Monitorear KPIs',
            'Responder preguntas de negocio con datos',
            'Automatizar reportes recurrentes'
        ],
        'formacion': [
            'Licenciatura en Administración, Economía, Ingeniería o afines',
            'Conocimientos básicos de estadística',
            'Cursos o certificaciones en análisis de datos'
        ],
        'salario_promedio': '$45,000 - $85,000 USD/año',
        'color': '#2196F3'
    },
    'ingeniero_datos': {
        'nombre': 'Ingeniero de Datos',
        'nombre_ingles': 'Data Engineer',
        'descripcion': 'Profesional especializado en diseñar, construir y mantener la infraestructura de datos que permite el análisis a gran escala.',
        'habilidades': [
            'Programación avanzada (Python, Java, Scala)',
            'Bases de datos SQL y NoSQL',
            'Big Data (Hadoop, Spark)',
            'ETL/ELT pipelines',
            'Cloud computing',
            'Arquitectura de sistemas',
            'DevOps y CI/CD'
        ],
        'herramientas': [
            'Apache Spark, Hadoop',
            'Airflow, Luigi (orquestación)',
            'Kafka, RabbitMQ (streaming)',
            'Docker, Kubernetes',
            'AWS (S3, Redshift, EMR)',
            'GCP (BigQuery, Dataflow)',
            'MongoDB, Cassandra, Redis'
        ],
        'responsabilidades': [
            'Diseñar arquitecturas de datos escalables',
            'Construir pipelines de datos (ETL/ELT)',
            'Optimizar consultas y bases de datos',
            'Implementar data warehouses y data lakes',
            'Asegurar calidad y disponibilidad de datos',
            'Automatizar procesos de ingesta de datos',
            'Colaborar con científicos y analistas de datos'
        ],
        'formacion': [
            'Licenciatura en Ingeniería de Software, Ciencias de la Computación o afines',
            'Conocimientos sólidos en programación y sistemas',
            'Experiencia en arquitectura de software'
        ],
        'salario_promedio': '$70,000 - $140,000 USD/año',
        'color': '#FF9800'
    }
}

@app.route('/')
def index():
    """Página principal del informe"""
    return render_template('index.html', 
                         roles=ROLES_DATA,
                         fecha_actual=datetime.now().strftime('%d de %B de %Y'))

@app.route('/comparacion')
def comparacion():
    """Página de comparación detallada"""
    return render_template('comparacion.html', 
                         roles=ROLES_DATA,
                         fecha_actual=datetime.now().strftime('%d de %B de %Y'))

@app.route('/perfil/<rol>')
def perfil_rol(rol):
    """Perfil detallado de un rol específico"""
    if rol not in ROLES_DATA:
        return "Rol no encontrado", 404
    
    return render_template('perfil.html', 
                         rol=rol,
                         datos=ROLES_DATA[rol],
                         fecha_actual=datetime.now().strftime('%d de %B de %Y'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
