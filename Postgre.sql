-- TABLA AUTOR
CREATE TABLE autor (
    codigo_autor INTEGER,
    nombre VARCHAR(100) NOT NULL,
    codigo_profesion INTEGER,
    CONSTRAINT pk_codigo_autor PRIMARY KEY (codigo_autor)
);

-- TABLA EDITORIAL
CREATE TABLE editorial (
    codigo_editorial INTEGER,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT pk_codigo_editorial PRIMARY KEY (codigo_editorial)
);

-- TABLA LIBRO
CREATE TABLE libro (
    codigo_libro INTEGER,
    titulo VARCHAR(200) NOT NULL,
    codigo_autor INTEGER NOT NULL,
    codigo_editorial INTEGER NOT NULL,
    precio NUMERIC(8,2),
    año INTEGER,
    CONSTRAINT pk_codigo_libro PRIMARY KEY (codigo_libro),
    CONSTRAINT fk_libro_autor FOREIGN KEY (codigo_autor) REFERENCES autor(codigo_autor),
    CONSTRAINT fk_libro_editorial FOREIGN KEY (codigo_editorial) REFERENCES editorial(codigo_editorial)
);
