-- Crear la tabla Usuarios
CREATE TABLE Usuarios (
    ID SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contacto VARCHAR(255) UNIQUE NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE
);

-- Crear la tabla Cadenas
CREATE TABLE Cadenas (
    ID SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    valor_cuota_mensual DECIMAL(10,2) NOT NULL
);

-- Crear la tabla Puestos
CREATE TABLE Puestos (
    ID SERIAL PRIMARY KEY,
    mes INTEGER CHECK (mes BETWEEN 1 AND 12) NOT NULL,
    ID_cadena INTEGER REFERENCES Cadenas(ID) ON DELETE CASCADE NOT NULL,
    ID_usuario_asignado INTEGER REFERENCES Usuarios(ID) ON DELETE SET NULL NOT NULL,
    UNIQUE(mes, ID_cadena)  -- Asegura que un mes solo puede ser asignado una vez por cadena
);

-- Crear la tabla Pagos
CREATE TABLE Pagos (
    ID INTEGER PRIMARY KEY,
    ID_puesto INTEGER REFERENCES Puestos(ID) ON DELETE CASCADE NOT NULL UNIQUE,
    monto DECIMAL(10,2) NOT NULL,
    fecha DATE NOT NULL
);
