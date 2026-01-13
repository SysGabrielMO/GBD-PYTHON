from funciones import (
    conectar_bd, desconectar_bd,
    listar_autores_total_libros,
    buscar_titulos_por_prefijo, filtrar_libros_por_precio,
    buscar_relacionada_autor_libros_editorial,
    insertar_libro, borrar_libros_por_autor,
    actualizar_precios_por_editorial
)


def menu():
    print("""
1. Listar autores y total de libros
2. Buscar títulos por prefijo
3. Filtrar libros por rango de precio
4. Buscar relacionada (autor -> libros + editorial)
5. Insertar libro
6. Borrar libros por autor
7. Actualizar precios por editorial
0. Salir
""")
    while True:
        try:
            return int(input("Opción: "))
        except:
            print("Opción incorrecta, debe ser un número.")


def pedir_int(msg):
    while True:
        try:
            return int(input(msg))
        except:
            print("Debe ser un número entero.")


def pedir_float(msg):
    while True:
        try:
            return float(input(msg))
        except:
            print("Debe ser un número (ej: 12.50).")


db = conectar_bd("localhost", "admingabriel", "usuario", "libreria")

op = menu()
while op != 0:

    if op == 1:
        listar_autores_total_libros(db)

    elif op == 2:
        pref = input("Subcadena (prefijo del título): ")
        buscar_titulos_por_prefijo(db, pref)

    elif op == 3:
        pmin = pedir_float("Precio mínimo: ")
        pmax = pedir_float("Precio máximo: ")
        filtrar_libros_por_precio(db, pmin, pmax)

    elif op == 4:
        autor = input("Nombre (o parte) del autor: ")
        buscar_relacionada_autor_libros_editorial(db, autor)

    elif op == 5:
        codigo = input("Código libro (ENTER para auto): ").strip()
        codigo_libro = int(codigo) if codigo else None

        titulo = input("Título: ")
        cod_autor = pedir_int("Código autor: ")
        cod_edit = pedir_int("Código editorial: ")
        precio = pedir_float("Precio: ")
        anio = pedir_int("Año: ")

        insertar_libro(db, titulo, cod_autor, cod_edit, precio, anio, codigo_libro=codigo_libro)

    elif op == 6:
        autor = input("Nombre (o parte) del autor: ")
        conf = input("¿Seguro? (s/n): ").lower().strip()
        if conf == "s":
            borrar_libros_por_autor(db, autor)

    elif op == 7:
        editorial = input("Nombre (o parte) de la editorial: ")
        porc = pedir_float("Porcentaje (ej: 10 para +10%, -5 para -5%): ")
        actualizar_precios_por_editorial(db, editorial, porc)

    else:
        print("Opción incorrecta.")

    op = menu()

desconectar_bd(db)
