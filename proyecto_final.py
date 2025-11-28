import modulo_sql as db
from colorama import Fore, init

# Inicializamos la librería colorama, que nos permite usar colores en la terminal.
init(autoreset=True)

# Función para validar que el usuario ingrese texto no vacío
def validar_texto(mensaje):
    while True:
        texto = input(Fore.CYAN + mensaje + Fore.RESET).strip().title()
        if texto:
            return texto
        else:
            print(Fore.RED + "❌ ERROR: Este campo no puede estar vacío.")

# Función para validar que el usuario ingrese un número entero mayor o igual a cero
def validar_numero_entero(mensaje):
    while True:
        numero = input(Fore.CYAN + mensaje + Fore.RESET).strip()
        if numero.isdigit() and int(numero) >= 0: 
            return int(numero)
        else:
            print(Fore.RED + "❌ ERROR: Debe ingresar un número entero mayor o igual a cero.")

# Función para agregar un nuevo producto al inventario
def agregar_producto(productos):
    print(Fore.MAGENTA + "\n--- 🛒 AGREGAR PRODUCTO ---")
    
    # Validar que el nombre del producto no esté repetido
    while True:
        nombre = validar_texto("Ingrese el nombre del producto: ")
        nombre_lower = nombre.lower()
        repetido = any(nombre_lower == p[1].lower() for p in productos)
        if repetido:
            print(Fore.RED + "❌ Ya existe un producto con ese nombre. Ingrese otro.")
        else:
            break  
     
    # Solicitar los demás datos del producto       
    categoria = validar_texto("Ingrese la categoría del producto: ")
    descripcion = validar_texto("Ingrese una breve descripción del producto: ")
    cantidad = validar_numero_entero("Ingrese la cantidad disponible: ") 
    precio = validar_numero_entero("Ingrese el precio del producto (sin centavos): ") 

    # Ingresar producto en la base de datos
    db.insertar_producto(nombre, descripcion, cantidad, precio, categoria)

    print(Fore.GREEN + "✅ Producto agregado con éxito 🛒")

    # Actualizar la lista de productos desde la base de datos
    productos = db.obtener_productos()

    return productos

# Función para mostrar todos los productos registrados
def mostrar_productos(productos):
 
    print(Fore.MAGENTA + "\n--- 🛍️  LISTA DE PRODUCTOS REGISTRADOS ---")
    if not productos:
        print(Fore.RED + "❌ No hay productos cargados todavía.")
        return productos 

    # Mostrar los productos con formato
    for i, p in enumerate(productos, start=1):
        id_, nombre, descripcion, cantidad, precio, categoria = p
        texto = (
            Fore.BLUE + f"{i}. " + Fore.WHITE +
            f"ID: {id_} | Nombre: {nombre.title()} | Categoría: { (categoria or '').title() }"
            f" | Precio: ${precio} | Cantidad: {cantidad}"
        )
        print(texto)

    print(Fore.CYAN + f"\nTotal de productos: {len(productos)}")
    return productos

# Función para buscar productos por nombre o categoría
def buscar_producto_por_nombre(productos):
    print(Fore.MAGENTA + "\n--- 🔍 BUSCAR PRODUCTO POR NOMBRE O CATEGORÍA ---")
    if not productos:
        print(Fore.RED + "❌ No hay productos cargados todavía.")
        return []

    producto_buscado = validar_texto("Ingrese el nombre o categoría del producto a buscar: ").lower()
    
    # Buscar en nombre o categoría (si existe)
    encontrados = [p for p in productos if producto_buscado in p[1].lower() or producto_buscado in (p[5] or '').lower()]

    if encontrados:
        print(Fore.GREEN + "\n✅ Productos encontrados:")
        for p in encontrados:
            print(Fore.WHITE + f"Nombre: {p[1].title()} | Categoría: {p[5].title()} | Precio: ${p[4]}")
    else:
        print(Fore.RED + f"❌ El producto '{producto_buscado}' no está registrado.")
    return encontrados

# Función para buscar un producto por su ID
def buscar_producto_por_id():

    print(Fore.MAGENTA + "\n--- 🔎 BUSCAR PRODUCTO POR ID ---")
    id_str = input(Fore.CYAN + "Ingrese el ID del producto: ").strip()
    
    # Validar que sea un número entero
    if not id_str.isdigit():
        print(Fore.RED + "❌ ID inválido. Debe ser un número entero.")
        return []

    id_num = int(id_str)
    fila = db.buscar_producto_por_id(id_num)
    if not fila:
        print(Fore.RED + f"❌ No existe ningún producto con ID {id_num}.")
        return []
    
    # Mostrar los datos del producto encontrado
    id_, nombre, descripcion, cantidad, precio, categoria = fila
    print(Fore.GREEN + "✅ Producto encontrado:")
    print(Fore.WHITE + f"ID: {id_}")
    print(Fore.WHITE + f"Nombre: {nombre.title()}")
    print(Fore.WHITE + f"Descripción: {descripcion}")
    print(Fore.WHITE + f"Cantidad: {cantidad}")
    print(Fore.WHITE + f"Precio: ${precio}")
    print(Fore.WHITE + f"Categoría: {categoria}")
    return [fila]

# Función para actualizar los datos de un producto por su ID
def actualizar_producto_por_id(productos):
    print(Fore.MAGENTA + "\n--- ✏️ ACTUALIZAR PRODUCTO POR ID ---")
    id_str = input("Ingrese el ID del producto a actualizar: ").strip()
    
    # Validar que el ID sea válido
    if not id_str.isdigit():
        print("❌ ID inválido. Debe ser un número entero.")
        return productos

    id_num = int(id_str)
    fila = db.buscar_producto_por_id(id_num)

    if not fila:
        print(f"❌ No existe ningún producto con ID {id_num}.")
        return productos

    # Mostrar los datos actuales para referencia
    id_, nombre_act, descripcion_act, cantidad_act, precio_act, categoria_act = fila

    print(f"\nProducto encontrado:")
    print(f"Nombre actual: {nombre_act}")
    print(f"Descripción actual: {descripcion_act}")
    print(f"Cantidad actual: {cantidad_act}")
    print(f"Precio actual: {precio_act}")
    print(f"Categoría actual: {categoria_act}")

    # Solicitar nuevos datos al usuario, validando que no queden vacíos o inválidos
    while True:
        nuevo_nombre = input("Nuevo nombre: ").strip()
        if nuevo_nombre:
            break
        print("❌ El nombre no puede quedar vacío.")

    while True:
        nueva_descripcion = input("Nueva descripción: ").strip()
        if nueva_descripcion:
            break
        print("❌ La descripción no puede quedar vacía.")

    while True:
        nueva_cantidad_str = input("Nueva cantidad: ").strip()
        if nueva_cantidad_str.isdigit() and int(nueva_cantidad_str) >= 0:
            nueva_cantidad = int(nueva_cantidad_str)
            break
        print("❌ Ingrese una cantidad válida (número entero mayor o igual a cero).")

    while True:
        nuevo_precio_str = input("Nuevo precio (sin centavos): ").strip()
        if nuevo_precio_str.isdigit() and int(nuevo_precio_str) > 0:
            nuevo_precio = int(nuevo_precio_str)
            break
        else:
            print("❌ Ingrese un precio válido (número entero positivo).")

    while True:
        nueva_categoria = input("Nueva categoría: ").strip()
        if nueva_categoria:
            break
        print("❌ La categoría no puede quedar vacía.")

    # Actualizar en la base de datos
    db.actualizar_producto(id_, nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria)
    print(f"\n✅ Producto ID {id_} actualizado correctamente.")

    # Actualizar la lista de productos desde la base de datos
    productos = db.obtener_productos()
    return productos

# Función para generar un reporte de productos con cantidad igual o menor a un límite dado
def reporte_por_cantidad_limite(productos):
    print(Fore.MAGENTA + "\n--- 📊 REPORTE POR CANTIDAD MÍNIMA ---")
    
    # Validar el límite ingresado
    while True:
        limite_str = input(Fore.CYAN + "Ingrese la cantidad límite para el reporte: ").strip()
        if limite_str.isdigit() and int(limite_str) >= 0:
            limite = int(limite_str)
            break
        else:
            print(Fore.RED + "❌ Por favor, ingrese un número entero mayor o igual a 0.")
    
    # Filtrar productos según el límite
    productos_filtrados = [p for p in productos if p[3] <= limite]
    
    if productos_filtrados:
        print(Fore.GREEN + f"\nProductos con cantidad igual o menor a {limite}:")
        for p in productos_filtrados:
            estado = Fore.RED + " ❌ (AGOTADO)" if p[3] == 0 else ""
            print(Fore.WHITE + f"ID: {p[0]} | Nombre: {p[1].title()} | Cantidad: {p[3]} | Categoría: {p[5].title()} | Precio: ${p[4]}" + estado)
    else:
        print(Fore.YELLOW + f"\n❌ No hay productos con cantidad igual o menor a {limite}.")

# Función para eliminar un producto por su ID
def eliminar_producto_por_id(productos):
    print(Fore.MAGENTA + "\n--- 🗑️  ELIMINAR PRODUCTO POR ID ---")
    if not productos:
        print(Fore.RED + "❌ No hay productos para eliminar.")
        return productos

    id_str = input(Fore.CYAN + "Ingrese el ID del producto a eliminar: ").strip()
    
    # Validar que el ID sea entero
    if not id_str.isdigit():
        print(Fore.RED + "❌ ID inválido. Debe ser un número entero.")
        return productos

    id_num = int(id_str)
    producto = next((p for p in productos if p[0] == id_num), None)
    if not producto:
        print(Fore.RED + f"❌ No existe ningún producto con ID {id_num}.")
        return productos

    # Confirmar eliminación
    confirmar = input(Fore.YELLOW + f"¿Confirma eliminar el producto '{producto[1].title()}'? (s/n): ").strip().lower()
    if confirmar != 's':
        print(Fore.CYAN + "❌ Operación cancelada.")
        return productos

    # Eliminar producto de la base de datos
    db.eliminar_producto(id_num)
    productos = db.obtener_productos()
    print(Fore.GREEN + f"✅ Producto '{producto[1].title()}' eliminado con éxito.")

    return productos

# Función para mostrar el menú principal de opciones
def imprimir_menu():
    print(Fore.MAGENTA + "\n--- 🛒 MENÚ PRINCIPAL ---")
    print(Fore.BLUE + "1." + Fore.WHITE + " Agregar producto")
    print(Fore.BLUE + "2." + Fore.WHITE + " Mostrar productos")
    print(Fore.BLUE + "3." + Fore.WHITE + " Buscar producto por nombre o categoría")
    print(Fore.BLUE + "4." + Fore.WHITE + " Buscar producto por ID")  
    print(Fore.BLUE + "5." + Fore.WHITE + " Actualizar producto por ID")  
    print(Fore.BLUE + "6." + Fore.WHITE + " Reporte por cantidad límite")  
    print(Fore.BLUE + "7." + Fore.WHITE + " Eliminar producto por ID")
    print(Fore.BLUE + "8." + Fore.WHITE + " Salir")

# Función principal que ejecuta el programa y controla el flujo con el menú
def menu():
    # Obtener productos actuales de la base de datos
    productos = db.obtener_productos()

    while True:
        imprimir_menu()
        eleccion = input(Fore.CYAN + "Seleccione una opción (1-8): ").strip()

        # Validar que la opción sea un número
        if not eleccion.isdigit():
            print(Fore.RED + "❌ Ingrese un número válido.")
            continue
        
        # Elegir función según opción
        match eleccion:
            case "1":
                productos = agregar_producto(productos)
            case "2":
                mostrar_productos(productos)
            case "3":
                buscar_producto_por_nombre(productos)
            case "4":
                buscar_producto_por_id()  
            case "5":
                productos = actualizar_producto_por_id(productos)
            case "6":
                reporte_por_cantidad_limite(productos)
            case "7":
                productos = eliminar_producto_por_id(productos)
            case "8":
                print(Fore.GREEN + "👋 Gracias por usar el sistema de gestión de productos. ¡Hasta luego!")
                break
            case _:
                print(Fore.RED + "❌ Opción incorrecta.")

# Ejecutar el menú principal
menu()