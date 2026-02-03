import sys
import oracledb

def pedirnum(tipo, msg, intentos=3):
    for _ in range(intentos):
        txt = input(msg).strip()
        try:
            return tipo(txt)
        except ValueError:
            print(f"Valor incorrecto. Debe ser {tipo.__name__}.")
    print("Demasiados intentos. Operación cancelada.")
    return None

def conectarbd():
    try:
        db = oracledb.connect(
            user="admingabriel",
            password="usuario"
        )
        print("Conectado a Oracle.")
        return db
    except oracledb.Error as e:
        print(f"No puedo conectar a Oracle: {e}")
        sys.exit(1)

def desconectarbdb(db):
    db.close()

def listarautorestotallibros(db):
    sql = """
    SELECT a.nombre AS autor, COUNT(l.codigo_libro) AS total
    FROM autor a 
    LEFT JOIN libro l ON l.codigo_autor = a.codigo_autor
    GROUP BY a.codigo_autor, a.nombre 
    ORDER BY a.nombre
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        filas = cursor.fetchall()
        if not filas:
            print("No hay autores.")
            return
        for row in filas:
            print(f"Autor: {row[0]} - {row[1]} libros")
    except oracledb.Error as e:
        print(f"Error en la consulta: {e}")
    finally:
        cursor.close()

def buscartitulosporprefijodb(db, prefijo):
    sql = "SELECT titulo FROM libro WHERE titulo LIKE :pref ORDER BY titulo"
    cursor = db.cursor()
    try:
        cursor.execute(sql, pref=prefijo + '%')
        filas = cursor.fetchall()
        if not filas:
            print("No hay libros que empiecen por esa subcadena.")
            return
        for row in filas:
            print(f"- {row[0]}")
    except oracledb.Error as e:
        print(f"Error en la consulta: {e}")
    finally:
        cursor.close()

def filtrarlibrosporpreciodb(db, preciomin, preciomax):
    sql = """
    SELECT titulo, precio FROM libro
    WHERE precio BETWEEN :min AND :max 
    ORDER BY precio, titulo
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql, min=preciomin, max=preciomax)
        filas = cursor.fetchall()
        if not filas:
            print("No hay libros en ese rango de precios.")
            return
        for row in filas:
            print(f"- {row[0]}, precio: {row[1]}")
    except oracledb.Error as e:
        print(f"Error en la consulta: {e}")
    finally:
        cursor.close()

def buscarrelacionadaautorlibroseditorialdb(db, nombreautor):
    sql = """
    SELECT a.nombre AS autor, l.titulo, e.nombre AS editorial,
           l.precio, l.año AS anio
    FROM autor a 
    JOIN libro l ON l.codigo_autor = a.codigo_autor
    JOIN editorial e ON e.codigo_edit = l.codigo_editorial
    WHERE UPPER(a.nombre) LIKE UPPER(:autor)
    ORDER BY a.nombre, l.titulo
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql, autor=f'%{nombreautor}%')
        filas = cursor.fetchall()
        if not filas:
            print("No se encontraron libros para ese autor.")
            return
        for row in filas:
            print(f"- {row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}")
    except oracledb.Error as e:
        print(f"Error en la consulta: {e}")
    finally:
        cursor.close()

def siguientecodigolibro(db):
    cursor = db.cursor()
    cursor.execute("SELECT NVL(MAX(codigo_libro), 0) + 1 FROM libro")
    return cursor.fetchone()[0]

def insertarlibro(db, titulo, codigoautor, codigoeditorial, precio, anio, codigolibro=None):
    if codigolibro is None:
        codigolibro = siguientecodigolibro(db)
    sql = """
    INSERT INTO libro (codigo_libro, titulo, codigo_autor, codigo_editorial, precio, año)
    VALUES (:cod, :tit, :aut, :edit, :prec, :anio)
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql, cod=codigolibro, tit=titulo, aut=codigoautor,
                       edit=codigoeditorial, prec=precio, anio=anio)
        db.commit()
        print(f"Libro insertado con código {codigolibro}.")
    except oracledb.Error as e:
        print(f"Error al insertar: {e}")
        db.rollback()
    finally:
        cursor.close()

def borrarlibrosporautordb(db, nombreautor):
    sql = """
    DELETE FROM libro WHERE codigo_autor IN (
        SELECT codigo_autor FROM autor WHERE UPPER(nombre) LIKE UPPER(:aut)
    )
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql, aut=f'%{nombreautor}%')
        db.commit()
        print(f"Libros eliminados: {cursor.rowcount}")
    except oracledb.Error as e:
        print(f"Error al borrar: {e}")
        db.rollback()
    finally:
        cursor.close()

def actualizarpreciosporeditorialdb(db, nombreeditorial, porcentaje):
    factor = 1 + (porcentaje / 100.0)
    sql = """
    UPDATE libro SET precio = precio * :factor
    WHERE codigo_editorial IN (
        SELECT codigo_edit FROM editorial WHERE UPPER(nombre) LIKE UPPER(:edit)
    )
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql, factor=factor, edit=f'%{nombreeditorial}%')
        db.commit()
        print(f"Libros actualizados: {cursor.rowcount}")
    except oracledb.Error as e:
        print(f"Error al actualizar: {e}")
        db.rollback()
    finally:
        cursor.close()
