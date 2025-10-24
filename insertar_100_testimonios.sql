-- ============================================================================
-- INSERTAR 100 TESTIMONIOS PARA DRA. SHIRLEY RAMÍREZ
-- Base de Datos: drashirley (MySQL/Railway)
-- Estructura: patient_name, patient_initials, testimonial_text, rating, approved, created_at, display_date
-- ============================================================================

USE drashirley;

-- Limpiar tabla de testimonios primero (OPCIONAL - Comentar si no quieres borrar los existentes)
-- DELETE FROM testimonials WHERE id > 0;

-- Insertar 100 testimonios con la estructura correcta
INSERT INTO testimonials (patient_name, patient_initials, testimonial_text, rating, approved, created_at, display_date) VALUES
('María González', 'MG', 'La Dra. Shirley es excepcional. Me acompañó durante todo mi embarazo y el parto fue maravilloso. Súper recomendada!', 5, 1, NOW() - INTERVAL 30 DAY, DATE(NOW() - INTERVAL 30 DAY)),
('Ana Rodríguez', 'AR', 'Excelente profesional, muy atenta y cariñosa. Me dio mucha confianza durante mi control prenatal.', 5, 1, NOW() - INTERVAL 28 DAY, DATE(NOW() - INTERVAL 28 DAY)),
('Carmen Martínez', 'CM', 'La mejor ginecóloga que he tenido. Explica todo con detalle y te hace sentir cómoda.', 5, 1, NOW() - INTERVAL 26 DAY, DATE(NOW() - INTERVAL 26 DAY)),
('Laura Pérez', 'LP', 'Mi bebé nació sano gracias a su excelente cuidado. Eternamente agradecida con la doctora.', 5, 1, NOW() - INTERVAL 24 DAY, DATE(NOW() - INTERVAL 24 DAY)),
('Patricia López', 'PL', 'Muy profesional y humana. Me ayudó mucho durante mi primer embarazo.', 5, 1, NOW() - INTERVAL 22 DAY, DATE(NOW() - INTERVAL 22 DAY)),
('Isabel Fernández', 'IF', 'La doctora Shirley es maravillosa! Siempre disponible para aclarar dudas.', 5, 1, NOW() - INTERVAL 20 DAY, DATE(NOW() - INTERVAL 20 DAY)),
('Rosa Sánchez', 'RS', 'Excelente atención, trato cálido y profesional. Totalmente recomendada.', 5, 1, NOW() - INTERVAL 18 DAY, DATE(NOW() - INTERVAL 18 DAY)),
('Claudia Ramírez', 'CR', 'Me acompañó en mis 3 embarazos. Es como de la familia ya!', 5, 1, NOW() - INTERVAL 16 DAY, DATE(NOW() - INTERVAL 16 DAY)),
('Diana Torres', 'DT', 'La mejor decisión fue elegir a la Dra. Shirley para mi parto. Todo salió perfecto.', 5, 1, NOW() - INTERVAL 14 DAY, DATE(NOW() - INTERVAL 14 DAY)),
('Sofía Morales', 'SM', 'Muy paciente y comprensiva. Me explicó todo paso a paso durante mi embarazo.', 5, 1, NOW() - INTERVAL 12 DAY, DATE(NOW() - INTERVAL 12 DAY)),

('Lucía Castro', 'LC', 'Excelente doctora, muy atenta a cada detalle. Mi bebé nació sano y fuerte.', 5, 1, NOW() - INTERVAL 10 DAY, DATE(NOW() - INTERVAL 10 DAY)),
('Valeria Ruiz', 'VR', 'La recomiendo 100%. Es una profesional excepcional y muy cariñosa.', 5, 1, NOW() - INTERVAL 9 DAY, DATE(NOW() - INTERVAL 9 DAY)),
('Andrea Jiménez', 'AJ', 'Me dio mucha seguridad durante todo el proceso. Súper recomendada!', 5, 1, NOW() - INTERVAL 8 DAY, DATE(NOW() - INTERVAL 8 DAY)),
('Gabriela Herrera', 'GH', 'La doctora más preparada y humana que conozco. Gracias por todo!', 5, 1, NOW() - INTERVAL 7 DAY, DATE(NOW() - INTERVAL 7 DAY)),
('Natalia Vargas', 'NV', 'Excelente en todo sentido. Mi familia completa se atiende con ella.', 5, 1, NOW() - INTERVAL 6 DAY, DATE(NOW() - INTERVAL 6 DAY)),
('Carolina Mendoza', 'CM', 'Muy profesional, instalaciones limpias y modernas. Todo excelente.', 5, 1, NOW() - INTERVAL 5 DAY, DATE(NOW() - INTERVAL 5 DAY)),
('Daniela Ortiz', 'DO', 'Me sentí muy cuidada durante mi embarazo de alto riesgo. Infinitas gracias!', 5, 1, NOW() - INTERVAL 4 DAY, DATE(NOW() - INTERVAL 4 DAY)),
('Paola Silva', 'PS', 'La mejor ginecóloga de República Dominicana sin duda. Altamente recomendada.', 5, 1, NOW() - INTERVAL 3 DAY, DATE(NOW() - INTERVAL 3 DAY)),
('Mónica Reyes', 'MR', 'Excelente trato, muy profesional y siempre puntual en las citas.', 5, 1, NOW() - INTERVAL 2 DAY, DATE(NOW() - INTERVAL 2 DAY)),
('Alejandra Cruz', 'AC', 'Me acompañó en el mejor momento de mi vida. Gracias Dra. Shirley!', 5, 1, NOW() - INTERVAL 1 DAY, DATE(NOW() - INTERVAL 1 DAY)),

('Fernanda Díaz', 'FD', 'Súper recomendada! Es una doctora excepcional y muy empática.', 5, 1, NOW(), DATE(NOW())),
('Julia Santos', 'JS', 'Mi segunda bebé nació con ella y todo fue perfecto. Gracias!', 5, 1, NOW() - INTERVAL 60 DAY, DATE(NOW() - INTERVAL 60 DAY)),
('Adriana Flores', 'AF', 'Excelente doctora, muy profesional y atenta. La recomiendo.', 5, 1, NOW() - INTERVAL 58 DAY, DATE(NOW() - INTERVAL 58 DAY)),
('Mariana Gil', 'MG', 'Me dio mucha confianza desde la primera consulta. Súper recomendada.', 5, 1, NOW() - INTERVAL 56 DAY, DATE(NOW() - INTERVAL 56 DAY)),
('Victoria Navarro', 'VN', 'La mejor experiencia durante mi embarazo. Doctora excepcional!', 5, 1, NOW() - INTERVAL 54 DAY, DATE(NOW() - INTERVAL 54 DAY)),
('Camila Romero', 'CR', 'Muy profesional, cariñosa y siempre disponible. La mejor!', 5, 1, NOW() - INTERVAL 52 DAY, DATE(NOW() - INTERVAL 52 DAY)),
('Elena Guzmán', 'EG', 'Excelente atención prenatal. Mi bebé y yo estamos muy bien gracias a ella.', 5, 1, NOW() - INTERVAL 50 DAY, DATE(NOW() - INTERVAL 50 DAY)),
('Sandra Medina', 'SM', 'La recomiendo ampliamente. Es una doctora con mucho conocimiento.', 5, 1, NOW() - INTERVAL 48 DAY, DATE(NOW() - INTERVAL 48 DAY)),
('Cristina Ramos', 'CR', 'Me acompañó durante todo mi embarazo gemelar. Todo salió perfecto!', 5, 1, NOW() - INTERVAL 46 DAY, DATE(NOW() - INTERVAL 46 DAY)),
('Beatriz Acosta', 'BA', 'Excelente profesional, muy dedicada y cariñosa con sus pacientes.', 5, 1, NOW() - INTERVAL 44 DAY, DATE(NOW() - INTERVAL 44 DAY)),

('Teresa Vega', 'TV', 'La mejor decisión fue atenderme con la Dra. Shirley. Súper recomendada!', 5, 1, NOW() - INTERVAL 42 DAY, DATE(NOW() - INTERVAL 42 DAY)),
('Liliana Molina', 'LM', 'Muy profesional y humana. Me explicó todo con mucha paciencia.', 5, 1, NOW() - INTERVAL 40 DAY, DATE(NOW() - INTERVAL 40 DAY)),
('Cecilia Rojas', 'CR', 'Excelente doctora! Mi familia completa la adora.', 5, 1, NOW() - INTERVAL 38 DAY, DATE(NOW() - INTERVAL 38 DAY)),
('Gloria Campos', 'GC', 'Me dio mucha seguridad durante mi primer embarazo. Gracias doctora!', 5, 1, NOW() - INTERVAL 36 DAY, DATE(NOW() - INTERVAL 36 DAY)),
('Ángela Parra', 'AP', 'La mejor ginecóloga que he tenido. Muy profesional y cariñosa.', 5, 1, NOW() - INTERVAL 34 DAY, DATE(NOW() - INTERVAL 34 DAY)),
('Silvia Núñez', 'SN', 'Excelente atención, instalaciones modernas y trato excepcional.', 5, 1, NOW() - INTERVAL 32 DAY, DATE(NOW() - INTERVAL 32 DAY)),
('Rocío Peña', 'RP', 'Me acompañó en los 9 meses más importantes de mi vida. Gracias!', 4, 1, NOW() - INTERVAL 31 DAY, DATE(NOW() - INTERVAL 31 DAY)),
('Verónica Luna', 'VL', 'Muy buena doctora, atenta y profesional. La recomiendo.', 4, 1, NOW() - INTERVAL 29 DAY, DATE(NOW() - INTERVAL 29 DAY)),
('Lorena Ríos', 'LR', 'Excelente servicio y atención personalizada. Muy satisfecha.', 5, 1, NOW() - INTERVAL 27 DAY, DATE(NOW() - INTERVAL 27 DAY)),
('Pilar Soto', 'PS', 'La mejor ginecóloga de la zona. Súper recomendada!', 5, 1, NOW() - INTERVAL 25 DAY, DATE(NOW() - INTERVAL 25 DAY)),

('Raquel Benítez', 'RB', 'Me dio mucha confianza y seguridad durante todo el proceso.', 5, 1, NOW() - INTERVAL 23 DAY, DATE(NOW() - INTERVAL 23 DAY)),
('Miriam Fuentes', 'MF', 'Excelente profesional, muy preparada y actualizada.', 5, 1, NOW() - INTERVAL 21 DAY, DATE(NOW() - INTERVAL 21 DAY)),
('Susana Cortés', 'SC', 'La doctora más cariñosa y profesional que conozco.', 5, 1, NOW() - INTERVAL 19 DAY, DATE(NOW() - INTERVAL 19 DAY)),
('Irene Cabrera', 'IC', 'Mi bebé nació sano gracias a sus excelentes cuidados.', 5, 1, NOW() - INTERVAL 17 DAY, DATE(NOW() - INTERVAL 17 DAY)),
('Paula Iglesias', 'PI', 'Muy recomendada! Es una doctora excepcional en todos los sentidos.', 5, 1, NOW() - INTERVAL 15 DAY, DATE(NOW() - INTERVAL 15 DAY)),
('Alicia Duarte', 'AD', 'Excelente atención y seguimiento durante todo mi embarazo.', 5, 1, NOW() - INTERVAL 13 DAY, DATE(NOW() - INTERVAL 13 DAY)),
('Estela Mora', 'EM', 'La mejor experiencia en mi control prenatal. Gracias doctora!', 5, 1, NOW() - INTERVAL 11 DAY, DATE(NOW() - INTERVAL 11 DAY)),
('Mercedes Salas', 'MS', 'Muy profesional y humana. Siempre dispuesta a ayudar.', 4, 1, NOW() - INTERVAL 10 DAY, DATE(NOW() - INTERVAL 10 DAY)),
('Yolanda Carrillo', 'YC', 'Excelente doctora, muy dedicada y cariñosa con las pacientes.', 5, 1, NOW() - INTERVAL 9 DAY, DATE(NOW() - INTERVAL 9 DAY)),
('Blanca Aguilar', 'BA', 'La recomiendo al 100%. Es una profesional excepcional.', 5, 1, NOW() - INTERVAL 8 DAY, DATE(NOW() - INTERVAL 8 DAY)),

('Dolores Marín', 'DM', 'Me acompañó en mi embarazo de gemelas. Todo perfecto!', 5, 1, NOW() - INTERVAL 7 DAY, DATE(NOW() - INTERVAL 7 DAY)),
('Amparo Serrano', 'AS', 'Muy buena doctora, atenta y profesional. Totalmente recomendada.', 5, 1, NOW() - INTERVAL 6 DAY, DATE(NOW() - INTERVAL 6 DAY)),
('Inmaculada León', 'IL', 'Excelente en todo sentido. La mejor decisión fue elegirla.', 5, 1, NOW() - INTERVAL 5 DAY, DATE(NOW() - INTERVAL 5 DAY)),
('Remedios Vidal', 'RV', 'Me dio mucha confianza desde la primera consulta.', 5, 1, NOW() - INTERVAL 4 DAY, DATE(NOW() - INTERVAL 4 DAY)),
('Consuelo Pascual', 'CP', 'La mejor ginecóloga! Muy profesional y cariñosa.', 5, 1, NOW() - INTERVAL 3 DAY, DATE(NOW() - INTERVAL 3 DAY)),
('Encarna Rubio', 'ER', 'Excelente atención prenatal y parto sin complicaciones. Gracias!', 5, 1, NOW() - INTERVAL 2 DAY, DATE(NOW() - INTERVAL 2 DAY)),
('Montserrat Soler', 'MS', 'Muy recomendada! Es una doctora excepcional.', 5, 1, NOW() - INTERVAL 1 DAY, DATE(NOW() - INTERVAL 1 DAY)),
('Marisol Jiménez', 'MJ', 'La mejor experiencia durante mi embarazo. Súper profesional.', 5, 1, NOW(), DATE(NOW())),
('Nuria Delgado', 'ND', 'Excelente doctora, muy atenta y profesional en todo momento.', 5, 1, NOW() - INTERVAL 65 DAY, DATE(NOW() - INTERVAL 65 DAY)),
('Soledad Fernández', 'SF', 'Me acompañó en los momentos más importantes. Infinitas gracias!', 5, 1, NOW() - INTERVAL 63 DAY, DATE(NOW() - INTERVAL 63 DAY)),

('Rosario Méndez', 'RM', 'La mejor ginecóloga que he tenido. Totalmente recomendada.', 5, 1, NOW() - INTERVAL 61 DAY, DATE(NOW() - INTERVAL 61 DAY)),
('Pilar Castro', 'PC', 'Muy profesional y humana. Me explicó todo con mucha paciencia.', 5, 1, NOW() - INTERVAL 59 DAY, DATE(NOW() - INTERVAL 59 DAY)),
('Asunción Torres', 'AT', 'Excelente atención y seguimiento durante todo el embarazo.', 5, 1, NOW() - INTERVAL 57 DAY, DATE(NOW() - INTERVAL 57 DAY)),
('Luisa Herrera', 'LH', 'La recomiendo ampliamente. Es una doctora excepcional.', 5, 1, NOW() - INTERVAL 55 DAY, DATE(NOW() - INTERVAL 55 DAY)),
('Josefa Vargas', 'JV', 'Me dio mucha seguridad y confianza durante todo el proceso.', 4, 1, NOW() - INTERVAL 53 DAY, DATE(NOW() - INTERVAL 53 DAY)),
('Francisca Mendoza', 'FM', 'Excelente profesional, muy dedicada y cariñosa.', 5, 1, NOW() - INTERVAL 51 DAY, DATE(NOW() - INTERVAL 51 DAY)),
('Antonia Ortiz', 'AO', 'La mejor experiencia en mi control prenatal. Gracias!', 5, 1, NOW() - INTERVAL 49 DAY, DATE(NOW() - INTERVAL 49 DAY)),
('Catalina Silva', 'CS', 'Muy buena doctora, atenta y profesional. La recomiendo.', 5, 1, NOW() - INTERVAL 47 DAY, DATE(NOW() - INTERVAL 47 DAY)),
('Esperanza Reyes', 'ER', 'Excelente en todo sentido. Mi bebé nació sano y fuerte.', 5, 1, NOW() - INTERVAL 45 DAY, DATE(NOW() - INTERVAL 45 DAY)),
('Fátima Cruz', 'FC', 'La mejor ginecóloga de la zona. Súper recomendada!', 5, 1, NOW() - INTERVAL 43 DAY, DATE(NOW() - INTERVAL 43 DAY)),

('Marina Díaz', 'MD', 'Me acompañó durante todo mi embarazo. Doctora excepcional!', 5, 1, NOW() - INTERVAL 41 DAY, DATE(NOW() - INTERVAL 41 DAY)),
('Begoña Santos', 'BS', 'Muy profesional y humana. La recomiendo al 100%.', 5, 1, NOW() - INTERVAL 39 DAY, DATE(NOW() - INTERVAL 39 DAY)),
('Aitana Flores', 'AF', 'Excelente atención prenatal y parto perfecto. Gracias doctora!', 5, 1, NOW() - INTERVAL 37 DAY, DATE(NOW() - INTERVAL 37 DAY)),
('Celia Gil', 'CG', 'La mejor decisión fue atenderme con ella. Súper recomendada!', 5, 1, NOW() - INTERVAL 35 DAY, DATE(NOW() - INTERVAL 35 DAY)),
('Noelia Navarro', 'NN', 'Muy buena doctora, atenta y profesional en todo momento.', 4, 1, NOW() - INTERVAL 33 DAY, DATE(NOW() - INTERVAL 33 DAY)),
('Lidia Romero', 'LR', 'Excelente profesional, muy dedicada y cariñosa con pacientes.', 5, 1, NOW() - INTERVAL 31 DAY, DATE(NOW() - INTERVAL 31 DAY)),
('Tamara Guzmán', 'TG', 'Me dio mucha confianza durante mi primer embarazo.', 5, 1, NOW() - INTERVAL 30 DAY, DATE(NOW() - INTERVAL 30 DAY)),
('Mireia Medina', 'MM', 'La mejor ginecóloga que conozco. Totalmente recomendada.', 5, 1, NOW() - INTERVAL 28 DAY, DATE(NOW() - INTERVAL 28 DAY)),
('Azucena Ramos', 'AR', 'Excelente atención y seguimiento. Muy satisfecha.', 5, 1, NOW() - INTERVAL 26 DAY, DATE(NOW() - INTERVAL 26 DAY)),
('Sonia Acosta', 'SA', 'La recomiendo ampliamente. Es una doctora excepcional.', 5, 1, NOW() - INTERVAL 24 DAY, DATE(NOW() - INTERVAL 24 DAY)),

('Leticia Vega', 'LV', 'Me acompañó en los 9 meses más importantes. Gracias!', 5, 1, NOW() - INTERVAL 22 DAY, DATE(NOW() - INTERVAL 22 DAY)),
('Eva Molina', 'EM', 'Muy profesional y humana. Excelente en todo sentido.', 5, 1, NOW() - INTERVAL 20 DAY, DATE(NOW() - INTERVAL 20 DAY)),
('Marta Rojas', 'MR', 'La mejor experiencia durante mi embarazo. Súper doctora!', 5, 1, NOW() - INTERVAL 18 DAY, DATE(NOW() - INTERVAL 18 DAY)),
('Ainhoa Campos', 'AC', 'Excelente profesional, muy atenta y cariñosa.', 5, 1, NOW() - INTERVAL 16 DAY, DATE(NOW() - INTERVAL 16 DAY)),
('Almudena Parra', 'AP', 'Me dio mucha seguridad y confianza. La recomiendo.', 5, 1, NOW() - INTERVAL 14 DAY, DATE(NOW() - INTERVAL 14 DAY)),
('Carla Núñez', 'CN', 'La mejor ginecóloga! Muy profesional y dedicada.', 5, 1, NOW() - INTERVAL 12 DAY, DATE(NOW() - INTERVAL 12 DAY)),
('Elisa Peña', 'EP', 'Excelente atención prenatal. Mi bebé nació perfecto!', 5, 1, NOW() - INTERVAL 10 DAY, DATE(NOW() - INTERVAL 10 DAY)),
('Loreto Luna', 'LL', 'Muy buena doctora, atenta y profesional. Recomendada!', 4, 1, NOW() - INTERVAL 9 DAY, DATE(NOW() - INTERVAL 9 DAY)),
('Sara Ríos', 'SR', 'La recomiendo al 100%. Es una profesional excepcional.', 5, 1, NOW() - INTERVAL 8 DAY, DATE(NOW() - INTERVAL 8 DAY)),
('Inés Soto', 'IS', 'Me acompañó durante todo el proceso. Infinitas gracias!', 5, 1, NOW() - INTERVAL 7 DAY, DATE(NOW() - INTERVAL 7 DAY)),

('Alba Benítez', 'AB', 'Excelente doctora, muy preparada y actualizada.', 5, 1, NOW() - INTERVAL 6 DAY, DATE(NOW() - INTERVAL 6 DAY)),
('Nerea Fuentes', 'NF', 'La mejor experiencia en mi control prenatal.', 5, 1, NOW() - INTERVAL 5 DAY, DATE(NOW() - INTERVAL 5 DAY)),
('Clara Cortés', 'CC', 'Muy profesional y humana. Súper recomendada!', 5, 1, NOW() - INTERVAL 4 DAY, DATE(NOW() - INTERVAL 4 DAY)),
('Emma Cabrera', 'EC', 'Excelente atención y seguimiento durante embarazo.', 5, 1, NOW() - INTERVAL 3 DAY, DATE(NOW() - INTERVAL 3 DAY)),
('Olivia Iglesias', 'OI', 'La mejor ginecóloga! Me dio mucha confianza.', 5, 1, NOW() - INTERVAL 2 DAY, DATE(NOW() - INTERVAL 2 DAY)),
('Luna Duarte', 'LD', 'Muy buena doctora, atenta y profesional. La recomiendo.', 5, 1, NOW() - INTERVAL 1 DAY, DATE(NOW() - INTERVAL 1 DAY)),
('Martina Mora', 'MM', 'Excelente en todo sentido. Totalmente recomendada!', 5, 1, NOW(), DATE(NOW())),
('Valentina Salas', 'VS', 'Me acompañó en el mejor momento de mi vida. Gracias!', 5, 1, NOW() - INTERVAL 70 DAY, DATE(NOW() - INTERVAL 70 DAY)),
('Luciana Carrillo', 'LC', 'La mejor decisión fue elegir a la Dra. Shirley.', 5, 1, NOW() - INTERVAL 68 DAY, DATE(NOW() - INTERVAL 68 DAY)),
('Isabela Aguilar', 'IA', 'Excelente profesional, muy dedicada y cariñosa.', 5, 1, NOW() - INTERVAL 66 DAY, DATE(NOW() - INTERVAL 66 DAY));

-- ============================================================================
-- VERIFICAR LOS INSERTS
-- ============================================================================

SELECT COUNT(*) as total_testimonios FROM testimonials;
SELECT COUNT(*) as aprobados FROM testimonials WHERE approved = 1;

SELECT 'Script ejecutado correctamente. 100 testimonios insertados!' AS Resultado;

-- Mostrar algunos ejemplos
SELECT id, patient_name, patient_initials, LEFT(testimonial_text, 50) as testimonio_preview, rating, approved 
FROM testimonials 
ORDER BY id DESC 
LIMIT 10;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
