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

-- Autores
INSERT INTO AUTOR (nombre, codigo_profesion, codigo_autor) VALUES 
('Marcos García', 1, 1),
('Ana López', 2, 2),
('Carlos Ruiz', 1, 3);

-- Editoriales
INSERT INTO EDITORIAL (nombre, codigo_editorial) VALUES 
('Planeta', 1),
('Alfaguara', 2),
('Anaya', 3);

-- Libros
INSERT INTO LIBRO (titulo, codigo_autor, codigo_editorial, precio, año, codigo_libro) VALUES 
('El viaje perdido', 1, 1, 19.95, 2020, 1),
('El camino oscuro', 1, 2, 22.50, 2021, 2),
('Sombras del pasado', 1, 1, 18.00, 2019, 3),
('Luz de invierno', 2, 3, 15.99, 2022, 4),
('La última frontera', 2, 2, 24.00, 2023, 5),
('Ecos del mar', 3, 1, 20.00, 2021, 6);

