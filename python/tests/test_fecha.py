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
	assert fecha.fecha_str==datetime.datetime(ano,mes,dia).strftime("%d/%m/%Y")
	assert fecha.fecha_str_formato==datetime.datetime(ano,mes,dia).strftime("%Y-%m-%d")

def test_fecha_defecto():

	fecha=Fecha()

	assert fecha.dia==1
	assert fecha.mes==1
	assert fecha.ano==2019
	assert fecha.fecha_datetime==datetime.datetime(2019,1,1)
	assert fecha.fecha_str==datetime.datetime(2019,1,1).strftime("%d/%m/%Y")
	assert fecha.fecha_str_formato==datetime.datetime(2019,1,1).strftime("%Y-%m-%d")

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
def test_fecha_desde_datetime(dia, mes, ano):

	fecha=Fecha.desdeDatetime(datetime.datetime(ano,mes,dia))

	assert fecha.dia==dia
	assert fecha.mes==mes
	assert fecha.ano==ano
	assert fecha.fecha_datetime==datetime.datetime(ano,mes,dia)
	assert fecha.fecha_str==datetime.datetime(ano,mes,dia).strftime("%d/%m/%Y")
	assert fecha.fecha_str_formato==datetime.datetime(ano,mes,dia).strftime("%Y-%m-%d")

@pytest.mark.parametrize(["dia","mes","ano", "dias","dia_nuevo","mes_nuevo","ano_nuevo"],
	[
		(27,2,2023,1,28,2,2023),
		(31,1,2022,10,10,2,2022),
		(1,10,2019,20,21,10,2019),
		(6,8,2023,4,10,8,2023),
		(13,4,2019,9,22,4,2019),
		(22,6,2021,365,22,6,2022),
		(29,2,2020,0,29,2,2020),
		(1,1,2019,22,23,1,2019)
	]
)
def test_fecha_aumentar_dias(dia, mes, ano, dias, dia_nuevo, mes_nuevo, ano_nuevo):

	fecha=Fecha(dia, mes, ano)

	fecha_original=fecha.fecha_datetime

	fecha.aumentarDias(dias)

	diferencia=(fecha.fecha_datetime-fecha_original).days

	assert diferencia==dias
	assert fecha.dia==dia_nuevo
	assert fecha.mes==mes_nuevo
	assert fecha.ano==ano_nuevo
	assert fecha.fecha_datetime==datetime.datetime(ano_nuevo,mes_nuevo,dia_nuevo)
	assert fecha.fecha_str==datetime.datetime(ano_nuevo,mes_nuevo,dia_nuevo).strftime("%d/%m/%Y")
	assert fecha.fecha_str_formato==datetime.datetime(ano_nuevo,mes_nuevo,dia_nuevo).strftime("%Y-%m-%d")