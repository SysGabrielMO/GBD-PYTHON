import sys
import psycopg
from psycopg.rows import dict_row


def pedir_num(tipo, msg, intentos=3):
    for _ in range(intentos):
        txt = input(msg).strip()
        try:
            return tipo(txt)
        except ValueError:
            print("Valor incorrecto. Debe ser", tipo.__name__)
    print("Demasiados intentos. Operación cancelada.")
    return None


def conectar_bd(host, usuario, password, dbname, port=5432):
    """
    Devuelve una conexión psycopg (PostgreSQL).
    row_factory=dict_row hace que fetchone/fetchall devuelvan dict.
    """
    try:
        conn = psycopg.connect(
            host=host,
            user=usuario,
            password=password,
            dbname=dbname,
            port=port,
            row_factory=dict_row,
        )
        return conn
    except psycopg.Error as e:
        print("No puedo conectar a la base de datos:", e)
        sys.exit(1)


def desconectar_bd(conn):
    conn.close()


def listar_autores_total_libros(conn):
    sql = """
    SELECT a.nombre AS autor, COUNT(l.codigo_libro) AS total
    FROM AUTOR a
    LEFT JOIN LIBRO l ON l.codigo_autor = a.codigo_autor
    GROUP BY a.codigo_autor, a.nombre
    ORDER BY a.nombre
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            filas = cur.fetchall()

        if not filas:
            print("No hay autores.")
            return

        for f in filas:
            print("Autor:", f["autor"], "-", f["total"], "libros")
    except psycopg.Error as e:
        print("Error en la consulta:", e)


def buscar_titulos_por_prefijo(conn, prefijo):
    sql = "SELECT titulo FROM LIBRO WHERE titulo LIKE %s ORDER BY titulo"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (prefijo + "%",))
            filas = cur.fetchall()

        if not filas:
            print("No hay libros que empiecen por esa subcadena.")
            return

        for f in filas:
            print("-", f["titulo"])
    except psycopg.Error as e:
        print("Error en la consulta:", e)


def filtrar_libros_por_precio(conn, precio_min, precio_max):
    sql = """
    SELECT titulo, precio
    FROM LIBRO
    WHERE precio BETWEEN %s AND %s
    ORDER BY precio, titulo
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (precio_min, precio_max))
            filas = cur.fetchall()

        if not filas:
            print("No hay libros en ese rango de precios.")
            return

        for f in filas:
            print("-", f["titulo"], "(precio:", f["precio"], ")")
    except psycopg.Error as e:
        print("Error en la consulta:", e)


def buscar_relacionada_autor_libros_editorial(conn, nombre_autor):
    sql = """
    SELECT
        a.nombre AS autor,
        l.titulo,
        e.nombre AS editorial,
        l.precio,
        l."año" AS anio
    FROM AUTOR a, LIBRO l, EDITORIAL e
    WHERE l.codigo_autor = a.codigo_autor
      AND e.codigo_editorial = l.codigo_editorial
      AND a.nombre LIKE %s
    ORDER BY a.nombre, l.titulo
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, ("%" + nombre_autor + "%",))
            filas = cur.fetchall()

        if not filas:
            print("No se encontraron libros para ese autor.")
            return

        for f in filas:
            print("-", f["autor"], "|", f["titulo"], "|", f["editorial"], "|", f["precio"], "|", f["anio"])
    except psycopg.Error as e:
        print("Error en la consulta:", e)


def _siguiente_codigo_libro(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(codigo_libro), 0) + 1 AS next_id FROM LIBRO")
        fila = cur.fetchone()
        return fila["next_id"]


def insertar_libro(conn, titulo, codigo_autor, codigo_editorial, precio, anio, codigo_libro=None):
    if codigo_libro is None:
        codigo_libro = _siguiente_codigo_libro(conn)
    sql = """
    INSERT INTO LIBRO (codigo_libro, titulo, codigo_autor, codigo_editorial, precio, "año")
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (codigo_libro, titulo, codigo_autor, codigo_editorial, precio, anio))
        conn.commit()
        print("Libro insertado con codigo_libro =", codigo_libro)
    except psycopg.Error as e:
        print("Error al insertar:", e)
        conn.rollback()


def borrar_libros_por_autor(conn, nombre_autor):
    sql = """
    DELETE FROM LIBRO
    WHERE codigo_autor IN (
        SELECT codigo_autor
        FROM AUTOR
        WHERE nombre LIKE %s
    )
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, ("%" + nombre_autor + "%",))
            borrados = cur.rowcount
        conn.commit()
        print("Libros eliminados:", borrados)
    except psycopg.Error as e:
        print("Error al borrar:", e)
        conn.rollback()


def actualizar_precios_por_editorial(conn, nombre_editorial, porcentaje):
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
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (factor, "%" + nombre_editorial + "%"))
            actualizados = cur.rowcount
        conn.commit()
        print("Libros actualizados:", actualizados)
    except psycopg.Error as e:
        print("Error al actualizar:", e)
        conn.rollback()
