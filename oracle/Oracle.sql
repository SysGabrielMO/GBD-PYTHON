-- TABLA AUTOR
CREATE TABLE autor (
    codigo_autor NUMBER,
    nombre VARCHAR2(100) NOT NULL,
    codigo_profesion NUMBER,
    CONSTRAINT pk_codigo_autor PRIMARY KEY (codigo_autor)
);

-- TABLA EDITORIAL
CREATE TABLE editorial (
    codigo_edit NUMBER,
    nombre VARCHAR2(100) NOT NULL,
    CONSTRAINT pk_codigo_editorial PRIMARY KEY (codigo_edit)
);

-- TABLA LIBRO
CREATE TABLE libro (
    codigo_libro NUMBER,
    titulo VARCHAR2(200) NOT NULL,
    codigo_autor NUMBER NOT NULL,
    codigo_editorial NUMBER NOT NULL,
    precio NUMBER(8,2),
    año NUMBER(4),
    CONSTRAINT pk_codigo_libro PRIMARY KEY (codigo_libro),
    CONSTRAINT fk_libro_autor FOREIGN KEY (codigo_autor) REFERENCES autor (codigo_autor),
    CONSTRAINT fk_libro_editorial FOREIGN KEY (codigo_editorial) REFERENCES editorial (codigo_edit)
);

-- Autores
INSERT ALL
  INTO AUTOR (nombre, codigo_profesion, codigo_autor) VALUES ('Marcos García', 1, 1),
  INTO AUTOR (nombre, codigo_profesion, codigo_autor) VALUES ('Ana López', 2, 2),
  INTO AUTOR (nombre, codigo_profesion, codigo_autor) VALUES ('Carlos Ruiz', 1, 3);

-- Editoriales
INSERT ALL
  INTO EDITORIAL (nombre, codigo_edit) VALUES ('Planeta', 1),
  INTO EDITORIAL (nombre, codigo_edit) VALUES ('Alfaguara', 2),
  INTO EDITORIAL (nombre, codigo_edit) VALUES ('Anaya', 3);

-- Libros
INSERT ALL
  INTO LIBRO (titulo, codigo_autor, codigo_editorial, precio, año, codigo_libro) VALUES ('El viaje perdido', 1, 1, 19.95, 2020, 1),
  INTO LIBRO (titulo, codigo_autor, codigo_editorial, precio, año, codigo_libro) VALUES ('El camino oscuro', 1, 2, 22.50, 2021, 2),
  INTO LIBRO (titulo, codigo_autor, codigo_editorial, precio, año, codigo_libro) VALUES ('Sombras del pasado', 1, 1, 18.00, 2019, 3),
  INTO LIBRO (titulo, codigo_autor, codigo_editorial, precio, año, codigo_libro) VALUES ('Luz de invierno', 2, 3, 15.99, 2022, 4),
  INTO LIBRO (titulo, codigo_autor, codigo_editorial, precio, año, codigo_libro) VALUES ('La última frontera', 2, 2, 24.00, 2023, 5),
  INTO LIBRO (titulo, codigo_autor, codigo_editorial, precio, año, codigo_libro) VALUES ('Ecos del mar', 3, 1, 20.00, 2021, 6);

