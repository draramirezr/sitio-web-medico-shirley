#!/usr/bin/env python3
"""Script para insertar datos iniciales en la base de datos Railway"""
import pymysql
import os

# Connection string
MYSQL_URL = "mysql://root:koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX@turntable.proxy.rlwy.net:33872/drashirley"

print("🔌 Conectando a MySQL Railway...")
conn = pymysql.connect(
    host='turntable.proxy.rlwy.net',
    port=33872,
    user='root',
    password='koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX',
    database='drashirley',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()

print("✅ Conexión exitosa\n")

# Verificar si ya existen datos
cursor.execute('SELECT COUNT(*) as count FROM services')
count = cursor.fetchone()['count']
print(f"📊 Servicios existentes: {count}")

if count > 0:
    print("⚠️ Ya hay servicios en la base de datos")
    respuesta = input("¿Quieres eliminar los existentes y reinsertar? (s/n): ")
    if respuesta.lower() == 's':
        cursor.execute('DELETE FROM services')
        print("🗑️ Servicios eliminados")
    else:
        print("❌ Operación cancelada")
        conn.close()
        exit()

print("\n📝 Insertando servicios...")

# Servicios de ejemplo
services = [
    ('Consulta Ginecológica', 'Consulta ginecológica\nPapanicolau\nColposcopia/biopsias\nCirugías ginecológicas\nIrregularidad menstrual\nGenotipificación y manejo del virus de papiloma humano\nManejo del síndrome de ovario poliquístico\nPlanificación familiar\nMenopausia y climaterio', 'fas fa-female', 'Consultar', '45 min'),
    ('Consulta Obstétrica', 'Consulta de obstetricia\nConsulta preconcepcional\nControl prenatal\nSeguimiento de embarazo de alto riesgo\nPartos y cesáreas\nAsesoría en lactancia materna', 'fas fa-baby', 'Consultar', '60 min'),
    ('Ecografías', 'Estudios de imagen para diagnóstico y seguimiento del embarazo y condiciones ginecológicas.', 'fas fa-heartbeat', 'Consultar', '30 min'),
    ('Cirugía Ginecológica', 'Procedimientos quirúrgicos especializados en ginecología con técnicas avanzadas.', 'fas fa-cut', 'Consultar', 'Variable'),
    ('Planificación Familiar', 'Asesoría sobre métodos anticonceptivos y planificación reproductiva personalizada.', 'fas fa-calendar-check', 'Consultar', '30 min'),
    ('Tratamientos Estéticos Ginecológicos', 'Tecnología láser de última generación para rejuvenecimiento vaginal, blanqueamiento genital, corrección de cicatrices y más. Click para ver todos los tratamientos disponibles.', 'fas fa-wand-magic-sparkles', 'Ver Tratamientos', 'Variable')
]

cursor.executemany('''
    INSERT INTO services (name, description, icon, price_range, duration) 
    VALUES (%s, %s, %s, %s, %s)
''', services)

print(f"✅ {cursor.rowcount} servicios insertados")

# Insertar testimonios
print("\n📝 Insertando testimonios...")
testimonials = [
    ('María González', 'M.G.', 'La Dra. Shirley es una excelente profesional. Su atención es muy cuidadosa y me hizo sentir cómoda durante toda la consulta.', 5),
    ('Ana Rodríguez', 'A.R.', 'Durante mi embarazo recibí un excelente cuidado prenatal. La doctora siempre estuvo disponible para resolver mis dudas.', 5),
    ('Carmen López', 'C.L.', 'Gracias a la Dra. Shirley tuve un parto seguro y sin complicaciones. Su profesionalismo y calidez humana son excepcionales.', 5),
    ('Lucía Martínez', 'L.M.', 'Me realizó una cirugía ginecológica y todo salió perfecto. Su seguimiento postoperatorio fue impecable.', 5),
    ('Isabel Fernández', 'I.F.', 'Excelente doctora, muy profesional y empática. Me ayudó mucho en mi tratamiento hormonal.', 5)
]

cursor.executemany('''
    INSERT INTO testimonials (patient_name, patient_initials, testimonial_text, rating, approved) 
    VALUES (%s, %s, %s, %s, 1)
''', testimonials)

print(f"✅ {cursor.rowcount} testimonios insertados")

# Insertar tratamientos estéticos
print("\n📝 Insertando tratamientos estéticos...")
aesthetic_treatments = [
    ('Rejuvenecimiento vaginal', 'Mejora la elasticidad y tonicidad del canal vaginal.\nReduce la sequedad y mejora la lubricación natural.', 'fas fa-magic'),
    ('Blanqueamiento genital', 'Aclara la pigmentación de la vulva, periné o zona anal.\nUnifica el tono de la piel íntima.', 'fas fa-sun'),
    ('Tensado o lifting vulvar', 'Mejora la apariencia externa de los labios mayores y menores.', 'fas fa-compress-arrows-alt'),
    ('Corrección de cicatrices de episiotomía o desgarros', 'Mejora estética y funcional de cicatrices perineales.', 'fas fa-band-aid'),
]

cursor.executemany('''
    INSERT INTO aesthetic_treatments (name, description, icon) 
    VALUES (%s, %s, %s)
''', aesthetic_treatments)

print(f"✅ {cursor.rowcount} tratamientos estéticos insertados")

# Commit
conn.commit()
conn.close()

print("\n✅✅✅ DATOS INSERTADOS CORRECTAMENTE ✅✅✅")
print("\n🔄 Ahora reinicia el servidor Flask y prueba /servicios")






