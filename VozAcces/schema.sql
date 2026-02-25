-- Script de creación de base de datos para el proyecto VoiceAudit
-- Este script define la estructura básica para la gestión de usuarios y auditoría de accesos.

-- Tabla: usuarios_voz
-- Almacena la información de identificación de los usuarios del sistema.
CREATE TABLE IF NOT EXISTS usuarios_voz (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    passphrase_text TEXT NOT NULL
);

-- Tabla: log_accesos_voz
-- Registra cada intento de acceso al sistema para fines de auditoría.
CREATE TABLE IF NOT EXISTS log_accesos_voz (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios_voz(id) ON DELETE CASCADE,
    fecha TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resultado_json JSONB
);

-- Justificación teórica del uso de JSONB para auditoría:
/*
   De acuerdo con la teoría de Bases de Datos Objeto-Relacionales de PostgreSQL, 
   el uso del tipo JSONB para la columna 'detalles' en una tabla de auditoría (logs) 
   es preferible a una estructura de múltiples columnas opcionales (NULLs) por las siguientes razones:

   1. Flexibilidad de Esquema (Schema-less): Las auditorías a menudo requieren capturar datos 
      heterogéneos que dependen del tipo de evento (IP, navegador, ubicación, parámetros de voz, etc.). 
      JSONB permite almacenar cualquier estructura sin necesidad de alterar la tabla cada vez que 
      se añade un nuevo tipo de metadatos.

   2. Eficiencia de Almacenamiento: El uso de múltiples columnas que terminan siendo mayoritariamente 
      NULL desperdicia espacio en el mapa de bits de nulos de la fila. JSONB almacena los datos 
      de forma binaria y jerárquica, ocupando espacio solo para la información realmente presente.

   3. Integridad y Rendimiento: JSONB soporta indexación GIN (Generalized Inverted Index), lo que 
      permite realizar búsquedas rápidas dentro de los documentos JSON sin penalizar el rendimiento 
      como lo haría una búsqueda de texto plano.

   4. Evolución del Sistema: En el contexto de VoiceAudit, los detalles del análisis de voz pueden 
      cambiar con nuevas versiones de algoritmos. JSONB nos permite mantener la compatibilidad 
      hacia atrás sin migraciones de esquema costosas.
*/
