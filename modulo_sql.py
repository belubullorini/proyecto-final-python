# Módulo encargado de manejar toda la conexión y operaciones con la base de datos.
# Acá se crea la tabla de productos y se definen las funciones para agregar, buscar,
# actualizar y eliminar registros. Este archivo se importa en el programa principal
# para mantener el código más ordenado y separado por responsabilidades.

import sqlite3

# Conexión a la base de datos (si no existe, se crea automáticamente)
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()
print("Conexión establecida exitosamente.")

# Creación de la tabla de productos si no existe.
# Acá defino todas las columnas que voy a usar en mi inventario.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        categoria TEXT
    )
''')
conexion.commit()

# Obtiene todos los productos de la tabla.
# Ideal para mostrar la lista completa en el menú principal.
def obtener_productos():
    cursor.execute("SELECT * FROM productos")
    return cursor.fetchall()

# Inserta un nuevo producto en la base de datos.
# Recibe los datos desde la interfaz del programa.
def insertar_producto(nombre, descripcion, cantidad, precio, categoria):
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio, categoria))
    conexion.commit()

# Busca un producto por su ID.
# Devuelve solo un resultado o None si no existe.
def buscar_producto_por_id(id_producto):
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    return cursor.fetchone()

# Actualiza todos los datos de un producto existente.
def actualizar_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
    cursor.execute('''
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    ''', (nombre, descripcion, cantidad, precio, categoria, id_producto))
    conexion.commit()

# Elimina un producto según su ID.
def eliminar_producto(id_producto):
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()