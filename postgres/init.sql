CREATE DATABASE bbdd_omie_data;

\c bbdd_omie_data;

CREATE TABLE prodespana (id SERIAL PRIMARY KEY,
						fecha DATE,
						hora INT,
						carbon DOUBLE PRECISION,
						fuel_gas DOUBLE PRECISION,
						autoproductor DOUBLE PRECISION,
						nuclear DOUBLE PRECISION,
						hidraulica DOUBLE PRECISION,
						ciclo DOUBLE PRECISION,
						eolica DOUBLE PRECISION,
						solar_termica DOUBLE PRECISION,
						solar_fotovoltaica DOUBLE PRECISION,
						resto DOUBLE PRECISION,
						importacion_mibel DOUBLE PRECISION,
						importacion_sin_mibel DOUBLE PRECISION);


