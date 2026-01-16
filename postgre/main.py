from funciones import (
    conectar_bd, desconectar_bd,
    pedir_num,
    listar_autores_total_libros,
    buscar_titulos_por_prefijo, filtrar_libros_por_precio,
    buscar_relacionada_autor_libros_editorial,
    insertar_libro, borrar_libros_por_autor,
    actualizar_precios_por_editorial
)

MENU = """
1. Listar autores y total de libros
2. Buscar títulos por prefijo
3. Filtrar libros por rango de precio
4. Buscar relacionada (autor -> libros + editorial)
5. Insertar libro
6. Borrar libros por autor
7. Actualizar precios por editorial
0. Salir
"""

def menu():
    print(MENU)
    op = pedir_num(int, "Opción: ")
    return op if op is not None else -1

def main():
    db = conectar_bd("localhost", "admingabriel", "usuario", "libreria")

    op = menu()
    while op != 0:
        if op == 1:
            listar_autores_total_libros(db)

        elif op == 2:
            pref = input("Subcadena (prefijo del título): ").strip()
            buscar_titulos_por_prefijo(db, pref)

        elif op == 3:
            pmin = pedir_num(float, "Precio mínimo: ")
            pmax = pedir_num(float, "Precio máximo: ")
            if pmin is not None and pmax is not None:
                filtrar_libros_por_precio(db, pmin, pmax)

        elif op == 4:
            autor = input("Nombre (o parte) del autor: ").strip()
            buscar_relacionada_autor_libros_editorial(db, autor)

        elif op == 5:
            codigo = input("Código libro (ENTER para auto): ").strip()
            codigo_libro = int(codigo) if codigo.isdigit() else None
            titulo = input("Título: ").strip()
            cod_autor = pedir_num(int, "Código autor: ")
            cod_edit = pedir_num(int, "Código editorial: ")
            precio = pedir_num(float, "Precio: ")
            anio = pedir_num(int, "Año: ")

            if None not in (cod_autor, cod_edit, precio, anio) and titulo:
                insertar_libro(db, titulo, cod_autor, cod_edit, precio, anio, codigo_libro=codigo_libro)
            else:
                print("Datos incompletos. No se insertó el libro.")

        elif op == 6:
            autor = input("Nombre (o parte) del autor: ").strip()
            conf = input("¿Seguro? (s/n): ").lower().strip()
            if conf == "s":
                borrar_libros_por_autor(db, autor)

        elif op == 7:
            editorial = input("Nombre (o parte) de la editorial: ").strip()
            porc = pedir_num(float, "Porcentaje (ej: 10 para +10%, -5 para -5%): ")
            if porc is not None:
                actualizar_precios_por_editorial(db, editorial, porc)

        else:
            print("Opción incorrecta.")

        op = menu()

    desconectar_bd(db)

if __name__ == "__main__":
    main()
