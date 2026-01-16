import sys
import MySQLdb
import MySQLdb.cursors


def pedir_num(tipo, msg, intentos=3):
    for _ in range(intentos):
        txt = input(msg).strip()
        try:
            return tipo(txt)
        except ValueError:
            print("Valor incorrecto. Debe ser", tipo.__name__)
    print("Demasiados intentos. Operación cancelada.")
    return None


def conectar_bd(host, usuario_bd, passwd_bd, nombre_bd):
    try:
        db = MySQLdb.connect(
            host=host,
            user=usuario_bd,
            passwd=passwd_bd,
            db=nombre_bd
        )
        return db
    except MySQLdb.Error as e:
        print("No puedo conectar a la base de datos:", e)
        sys.exit(1)


def desconectar_bd(db):
    db.close()


def listar_autores_total_libros(db):
    sql = """
    SELECT a.nombre AS autor, COUNT(l.codigo_libro) AS total
    FROM AUTOR a
    LEFT JOIN LIBRO l ON l.codigo_autor = a.codigo_autor
    GROUP BY a.codigo_autor, a.nombre
    ORDER BY a.nombre
    """
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(sql)
        filas = cursor.fetchall()
        if not filas:
            print("No hay autores.")
            return
        for f in filas:
            print("Autor:", f["autor"], "-", f["total"], "libros")
    except MySQLdb.Error as e:
        print("Error en la consulta:", e)


def buscar_titulos_por_prefijo(db, prefijo):
    sql = "SELECT titulo FROM LIBRO WHERE titulo LIKE %s ORDER BY titulo"
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(sql, (prefijo + "%",))
        filas = cursor.fetchall()
        if not filas:
            print("No hay libros que empiecen por esa subcadena.")
            return
        for f in filas:
            print("-", f["titulo"])
    except MySQLdb.Error as e:
        print("Error en la consulta:", e)


def filtrar_libros_por_precio(db, precio_min, precio_max):
    sql = """
    SELECT titulo, precio
    FROM LIBRO
    WHERE precio BETWEEN %s AND %s
    ORDER BY precio, titulo
    """
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(sql, (precio_min, precio_max))
        filas = cursor.fetchall()
        if not filas:
            print("No hay libros en ese rango de precios.")
            return
        for f in filas:
            print("-", f["titulo"], "(precio:", f["precio"], ")")
    except MySQLdb.Error as e:
        print("Error en la consulta:", e)


def buscar_relacionada_autor_libros_editorial(db, nombre_autor):
    sql = """
    SELECT a.nombre AS autor, l.titulo, e.nombre AS editorial, l.precio, l.`año` AS anio
    FROM AUTOR a, LIBRO l, EDITORIAL e
    WHERE l.codigo_autor = a.codigo_autor
    AND e.codigo_edit = l.codigo_editorial
    AND a.nombre LIKE %s
    ORDER BY a.nombre, l.titulo
    """
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(sql, ("%" + nombre_autor + "%",))
        filas = cursor.fetchall()
        if not filas:
            print("No se encontraron libros para ese autor.")
            return
        for f in filas:
            print("-", f["autor"], "|", f["titulo"], "|", f["editorial"], "|", f["precio"], "|", f["anio"])
    except MySQLdb.Error as e:
        print("Error en la consulta:", e)


def _siguiente_codigo_libro(db):
    cursor = db.cursor()
    cursor.execute("SELECT COALESCE(MAX(codigo_libro), 0) + 1 FROM LIBRO")
    return cursor.fetchone()[0]


def insertar_libro(db, titulo, codigo_autor, codigo_editorial, precio, anio, codigo_libro=None):
    if codigo_libro is None:
        codigo_libro = _siguiente_codigo_libro(db)

    sql = """
    INSERT INTO LIBRO (codigo_libro, titulo, codigo_autor, codigo_editorial, precio, `año`)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql, (codigo_libro, titulo, codigo_autor, codigo_editorial, precio, anio))
        db.commit()
        print("Libro insertado con codigo_libro =", codigo_libro)
    except MySQLdb.Error as e:
        print("Error al insertar:", e)
        db.rollback()


def borrar_libros_por_autor(db, nombre_autor):
    sql = """
    DELETE FROM LIBRO
    WHERE codigo_autor IN (
        SELECT codigo_autor
        FROM AUTOR
        WHERE nombre LIKE %s
    )
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql, ("%" + nombre_autor + "%",))
        db.commit()
        print("Libros eliminados:", cursor.rowcount)
    except MySQLdb.Error as e:
        print("Error al borrar:", e)
        db.rollback()


def actualizar_precios_por_editorial(db, nombre_editorial, porcentaje):
    factor = 1.0 + (porcentaje / 100.0)
    sql = """
    UPDATE LIBRO
    SET precio = precio * %s
    WHERE codigo_editorial IN (
        SELECT codigo_edit
        FROM EDITORIAL
        WHERE nombre LIKE %s
    )
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql, (factor, "%" + nombre_editorial + "%"))
        db.commit()
        print("Libros actualizados:", cursor.rowcount)
    except MySQLdb.Error as e:
        print("Error al actualizar:", e)
        db.rollback()
