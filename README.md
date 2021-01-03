# btc_dolar
Scraper muy simple para obtener valores de BTC y distintos tipos de dolar (oficial, blue, ccl, etc)

El valor del BTC se obtiene desde la API de [CoinDesk](https://github.com/Castrogiovanni20/api-dolar-argentina), mientras que los valores del dolar se obtienen desde [api-dolar-argentina](https://github.com/Castrogiovanni20/api-dolar-argentina).

Se devuelve un dataframe que luego se exporta a .csv para cada tipo (btc y dolar) con la siguiente estructura:

**BTC**:

| DATE | PRICE |
| ----------- | ----------- |
| 1/1/21 | 32500 |

**USD**:

| DATE | TYPE | BUY | SELL |
| ----------- | ----------- | ----------- | ----------- |
| 1/1/21 | dolaroficial | 83.00 | 89.00 |

Las fechas obtenidas están en UTC, por lo que se utiliza [PYTZ](https://pypi.org/project/pytz/) para convertirlas a GMT-3.
