import sys
import oracledb
from oracledb import rows


def pedirnum(tipo, msg, intentos=3):
    for _ in range(intentos):
        txt = input(msg).strip()
        try:
            return tipo(txt)
        except ValueError:
            print("Valor incorrecto. Debe ser", tipo.__name__)
    print("Demasiados intentos. Operación cancelada.")
    return None


def conectarbd(host, usuario, password, service_name="XE", port=1521):
    try:
        dsn = f"{host}:{port}/{service_name}"
        return oracledb.connect(user=usuario, password=password, dsn=dsn)
    except oracledb.Error as e:
        print("No puedo conectar a la base de datos:", e)
        sys.exit(1)


def desconectarbd(conn):
    conn.close()


def _dict_cursor(conn):
    cur = conn.cursor()
    cur.rowfactory = rows.dictfactory
    return cur


def listarautorestotallibros(conn):
    sql = """
    SELECT a.nombre AS autor, COUNT(l.codigolibro) AS total
    FROM AUTOR a
    LEFT JOIN LIBRO l ON l.codigoautor = a.codigoautor
    GROUP BY a.codigoautor, a.nombre
    ORDER BY a.nombre
    """
    try:
        with _dict_cursor(conn) as cur:
            cur.execute(sql)
            filas = cur.fetchall()
            if not filas:
                print("No hay autores.")
                return
            for f in filas:
                print("Autor", f["AUTOR"], "-", f["TOTAL"], "libros")
    except oracledb.Error as e:
        print("Error en la consulta:", e)


def buscartitulosporprefijo(conn, prefijo):
    sql = "SELECT titulo FROM LIBRO WHERE titulo LIKE :1 ORDER BY titulo"
    try:
        with _dict_cursor(conn) as cur:
            cur.execute(sql, (prefijo + "%",))
            filas = cur.fetchall()
            if not filas:
                print("No hay libros que empiecen por esa subcadena.")
                return
            for f in filas:
                print("-", f["TITULO"])
    except oracledb.Error as e:
        print("Error en la consulta:", e)


def filtrarlibrosporprecio(conn, preciomin, preciomax):
    sql = """
    SELECT titulo, precio
    FROM LIBRO
    WHERE precio BETWEEN :1 AND :2
    ORDER BY precio, titulo
    """
    try:
        with _dict_cursor(conn) as cur:
            cur.execute(sql, (preciomin, preciomax))
            filas = cur.fetchall()
            if not filas:
                print("No hay libros en ese rango de precios.")
                return
            for f in filas:
                print("-", f["TITULO"], "precio", f["PRECIO"])
    except oracledb.Error as e:
        print("Error en la consulta:", e)


def buscarrelacionadaautorlibroseditorial(conn, nombreautor):
    sql = """
    SELECT a.nombre AS autor,
           l.titulo,
           e.nombre AS editorial,
           l.precio,
           l.ao AS anio
    FROM AUTOR a, LIBRO l, EDITORIAL e
    WHERE l.codigoautor = a.codigoautor
      AND e.codigoeditorial = l.codigoeditorial
      AND a.nombre LIKE :1
    ORDER BY a.nombre, l.titulo
    """
    try:
        with _dict_cursor(conn) as cur:
            cur.execute(sql, ("%" + nombreautor + "%",))
            filas = cur.fetchall()
            if not filas:
                print("No se encontraron libros para ese autor.")
                return
            for f in filas:
                print("-", f["AUTOR"], "|", f["TITULO"], "|", f["EDITORIAL"], "|", f["PRECIO"], "|", f["ANIO"])
    except oracledb.Error as e:
        print("Error en la consulta:", e)


def siguientecodigolibro(conn):
    sql = "SELECT COALESCE(MAX(codigolibro), 0) + 1 AS nextid FROM LIBRO"
    with _dict_cursor(conn) as cur:
        cur.execute(sql)
        fila = cur.fetchone()
        return fila["NEXTID"]


def insertarlibro(conn, titulo, codigoautor, codigoeditorial, precio, anio, codigolibro=None):
    if codigolibro is None:
        codigolibro = siguientecodigolibro(conn)

    sql = """
    INSERT INTO LIBRO (codigolibro, titulo, codigoautor, codigoeditorial, precio, ao)
    VALUES (:1, :2, :3, :4, :5, :6)
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (codigolibro, titulo, codigoautor, codigoeditorial, precio, anio))
        conn.commit()
        print("Libro insertado con codigolibro", codigolibro)
    except oracledb.Error as e:
        print("Error al insertar:", e)
        conn.rollback()


def borrarlibrosporautor(conn, nombreautor):
    sql = """
    DELETE FROM LIBRO
    WHERE codigoautor IN (
        SELECT codigoautor
        FROM AUTOR
        WHERE nombre LIKE :1
    )
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, ("%" + nombreautor + "%",))
            borrados = cur.rowcount
        conn.commit()
        print("Libros eliminados:", borrados)
    except oracledb.Error as e:
        print("Error al borrar:", e)
        conn.rollback()


def actualizarpreciosporeditorial(conn, nombreeditorial, porcentaje):
    factor = 1.0 + (porcentaje / 100.0)
    sql = """
    UPDATE LIBRO
    SET precio = precio * :1
    WHERE codigoeditorial IN (
        SELECT codigoeditorial
        FROM EDITORIAL
        WHERE nombre LIKE :2
    )
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (factor, "%" + nombreeditorial + "%"))
            actualizados = cur.rowcount
        conn.commit()
        print("Libros actualizados:", actualizados)
    except oracledb.Error as e:
        print("Error al actualizar:", e)
        conn.rollback()
