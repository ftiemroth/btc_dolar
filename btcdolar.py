import json, datetime, requests, time
import schedule
import pytz
import pandas as pd

def convert_datetime_timezone(dt, tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)
    dt = datetime.datetime.strptime(dt,"%Y/%m/%d %H:%M:%S")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y/%m/%d %H:%M")
    return dt

def getFloatVal(value):
    try:
        return float(value.replace(',','.'))
    except Exception:
        return None

# DATA BTC
def btc():
    btc_data = requests.get('https://api.coindesk.com/v1/bpi/currentprice/USD.json').json()
    btc_value = round(btc_data['bpi']['USD']['rate_float'],2)
    last_update_btc_iso = btc_data['time']['updatedISO'][:-6].replace('T',' ').replace('-','/')
    last_update_btc_arg = convert_datetime_timezone(last_update_btc_iso,'UTC','America/Argentina/Buenos_Aires')
    btc_df = pd.DataFrame({
        'DATE': [last_update_btc_arg],
        'PRICE': [btc_value]
         })
    try:
        file_btc = pd.read_csv('btc.csv')
        btc_df.to_csv(r'btc.csv', index=False, header=False, mode='a')
        print('Cotización guardada')
    except FileNotFoundError:
        btc_df.to_csv(r'btc.csv', index=False, header=True, mode='w')
        print('Archivo btc.csv creado y cotizacion guardada.')

# DATA DOLAR
def usd():
    dolar_endpoints = ['dolaroficial','dolarblue','contadoliqui','bbva','santander','nacion','galicia']
    for apis in dolar_endpoints:
        dolar_data = requests.get('https://api-dolar-argentina.herokuapp.com/api/'+apis).json()
        fecha_utc = dolar_data['fecha']
        fecha_arg = convert_datetime_timezone(fecha_utc,'UTC','America/Argentina/Buenos_Aires')
        usd_compra = dolar_data['compra']
        usd_venta = dolar_data['venta']
        usd_df = pd.DataFrame({
            'DATE': [fecha_arg],
            'TYPE': [apis],
            'BUY': [usd_compra],
            'SELL': [usd_venta]
            })
        try:
            file_usd = pd.read_csv('dolar.csv')
            usd_df.to_csv(r'dolar.csv', index=False, header=False, mode='a')
            print('Cotización guardada: '+apis)
        except FileNotFoundError:
            usd_df.to_csv(r'dolar.csv', index=False, header=True, mode='w')
            print('Archivo dolar.csv creado y cotizaciones guardadas.')

schedule.every(5).minutes.do(btc)
schedule.every(12).hours.do(usd)
while 1:
    schedule.run_pending()