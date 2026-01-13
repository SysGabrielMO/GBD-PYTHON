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
