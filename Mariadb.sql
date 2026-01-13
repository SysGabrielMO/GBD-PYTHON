-- TABLA AUTOR
CREATE TABLE AUTOR (
    codigo_autor INT,
    nombre VARCHAR(100) NOT NULL,
    codigo_profesion INT,
    CONSTRAINT pk_codigo_autor PRIMARY KEY (codigo_autor)
);


-- TABLA EDITORIAL
CREATE TABLE EDITORIAL (
    codigo_edit INT,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT pk_codigo_editorial PRIMARY KEY (codigo_edit)
);


-- TABLA LIBRO
CREATE TABLE LIBRO (
    codigo_libro INT ,
    titulo VARCHAR(200) NOT NULL,
    codigo_autor INT NOT NULL,
    codigo_editorial INT NOT NULL,
    precio DECIMAL(8,2),
    año INT,
    CONSTRAINT pk_codigo_libro PRIMARY KEY (codigo_libro),
    CONSTRAINT fk_libro_autor FOREIGN KEY (codigo_autor) REFERENCES AUTOR(codigo_autor),
    CONSTRAINT fk_libro_editorial FOREIGN KEY (codigo_editorial) REFERENCES EDITORIAL(codigo_edit)
);
