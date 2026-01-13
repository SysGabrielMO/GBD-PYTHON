# GBD-PYTHON
El proyecto consiste en codificar tres programas en Python que realicen operaciones DML sobre una base de datos.
Deberá realizar el mismo programa Python pero sobre cada uno de los SGBD relacionales trabajados en clase (Oracle, MySQL/MariaDB y PostgreSQL).

Mi proyecto se basa en la gestión de una biblioteca virtual la cual contendra autores, la editorial de cada libro y los libros

En mi caso, la BD contendra las siguientes tablas:
1. AUTOR: codigo (PK), nombre, codigo_profesion
2. EDITORIAL: codigo (PK), nombre.
3. LIBRO: codigo (PK), titulo, codigo_autor (FK), codigo_editorial (FK),precio, año.

Las funciones requeridas seran las siguientes:

1. Listar información
Muestra autores y total de libros por autor. Ejemplo: "Autor: Marcos García: 5 libros"

2. Buscar o filtrar
Pide subcadena y lista títulos de libros que empiecen por ella. O pide rango de precios y filtra libros.
​
3. Buscar relacionada
Pide nombre de autor y muestra sus libros con editoriales.

4. Insertar
Pide datos de nuevo libro (título, autor_codigo, editorial_codigo, precio, año) y los inserta.

5. Borrar
Pide nombre de autor y elimina sus libros.

6. Actualizar
Pide nombre de editorial y porcentaje; actualiza precios de sus libros.
