from funciones_oracle import *

MENU = """
1. Listar autores y total de libros
2. Buscar títulos por prefijo
3. Filtrar libros por rango de precio
4. Buscar relacionada autor-libros-editorial
5. Insertar libro
6. Borrar libros por autor
7. Actualizar precios por editorial
0. Salir
"""

def menu():
    print(MENU)
    op = pedirnum(int, "Opción: ")
    return op if op is not None else -1

def main():
    db = conectarbd()
    op = menu()
    while op != 0:
        if op == 1:
            listarautorestotallibros(db)
        elif op == 2:
            pref = input("Subcadena prefijo del título: ").strip()
            buscartitulosporprefijodb(db, pref)
        elif op == 3:
            pmin = pedirnum(float, "Precio mínimo: ")
            pmax = pedirnum(float, "Precio máximo: ")
            if pmin is not None and pmax is not None:
                filtrarlibrosporpreciodb(db, pmin, pmax)
        elif op == 4:
            autor = input("Nombre o parte del autor: ").strip()
            buscarrelacionadaautorlibroseditorialdb(db, autor)
        elif op == 5:
            codigo = input("Código libro (ENTER para auto): ").strip()
            codigolibro = int(codigo) if codigo.isdigit() else None
            titulo = input("Título: ").strip()
            codautor = pedirnum(int, "Código autor: ")
            codedit = pedirnum(int, "Código editorial: ")
            precio = pedirnum(float, "Precio: ")
            anio = pedirnum(int, "Año: ")
            if None not in (codautor, codedit, precio, anio) and titulo:
                insertarlibro(db, titulo, codautor, codedit, precio, anio, codigolibro)
            else:
                print("Datos incompletos. No se insertó el libro.")
        elif op == 6:
            autor = input("Nombre o parte del autor: ").strip()
            conf = input("¿Seguro? (s/n): ").lower().strip()
            if conf == 's':
                borrarlibrosporautordb(db, autor)
        elif op == 7:
            editorial = input("Nombre o parte de la editorial: ").strip()
            porc = pedirnum(float, "Porcentaje (ej: 10 para +10%, -5 para -5%): ")
            if porc is not None:
                actualizarpreciosporeditorialdb(db, editorial, porc)
        else:
            print("Opción incorrecta.")
        op = menu()
    desconectarbdb(db)

if __name__ == "__main__":
    main()
