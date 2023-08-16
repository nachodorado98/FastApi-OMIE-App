import pytest
import datetime

from src.fecha import Fecha

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(30,2,2023),
		(70,1,2024),
		(1,20,2017),
		("a",8,2023),
		(-1,4,2019),
		(0,1,2020),
		(29,2,2023)
	]
)
def test_fecha_incorrecta_formato(dia, mes, ano):

	with pytest.raises(Exception):

		Fecha(dia, mes, ano)

def test_fecha_incorrecta_superior():

	manana=datetime.datetime.today()+datetime.timedelta(days=1)

	with pytest.raises(Exception):

		Fecha(manana.day, manana.month, manana.year)

def test_fecha_incorrecta_inferior():

	with pytest.raises(Exception):

		Fecha(31,12,2018)

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(28,2,2023),
		(31,1,2022),
		(1,10,2019),
		(6,8,2023),
		(13,4,2019),
		(22,6,2021),
		(29,2,2020),
		(1,1,2019),
		(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year)
	]
)
def test_fecha_correcta(dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	assert fecha.dia==dia
	assert fecha.mes==mes
	assert fecha.ano==ano
	assert fecha.fecha_datetime==datetime.datetime(ano,mes,dia)

def test_fecha_defecto(fecha):

	assert fecha.dia==1
	assert fecha.mes==1
	assert fecha.ano==2019
	assert fecha.fecha_datetime==datetime.datetime(2019,1,1)