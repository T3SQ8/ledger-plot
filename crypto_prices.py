#!/usr/bin/env python

from datetime import datetime, timedelta
import json
import requests

def gecko_date(date):
    # For some reason, CoinGecko uses the dd-mm-yyyy format instead of the ISO standard.
    return date.strftime('%d-%m-%Y')

def day_range(start_day):
    days = [start_day]
    for i in range(1, 8):
        day_before = start_day - timedelta(days=i)
        day_after = start_day + timedelta(days=i)
        if day_after.date() < datetime.today().date(): # Don't add dates in the future
            days.append(day_after)
        days.insert(0, day_before)
    return days

def main(coin, date, currency, commodity, **symbs):
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    for day in day_range(date):
        url = f'https://api.coingecko.com/api/v3/coins/{coin}/history?date={gecko_date(day)}'
        day = day.strftime('%Y-%m-%d')
        data = json.loads(requests.get(url).text)
        try:
            rate = data['market_data']['current_price'][currency]
        except KeyError:
            break
        if symbs['currency_symbol'] is not None:
            currency_symbol = symbs['currency_symbol']
        else:
            currency_symbol = currency.upper()
        print(f'P {day} {commodity} {rate} {currency_symbol}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='''Get cryptocurrency price history from CoinGecko <https://www.coingecko.com>.
        See <https://www.ledger-cli.org/3.0/doc/ledger3.html#Commodities-and-Currencies> for
        explanation.''')
    parser.add_argument('coin', metavar='COIN',
            help='ID of coin (Example: bitcoin). See <https://api.coingecko.com/api/v3/coins/>.')
    parser.add_argument('-d', '--date',
            default=datetime.today(),
            help='Date to use in query. (Format: \'yyyy-mm-dd\', Default: today)')
    parser.add_argument('currency', metavar='CURRENCY',
            help='Symbol for currency to convert to (Example: eur).')
    parser.add_argument('commodity', metavar='COMMODITY',
            help='Symbol for cryptocurrency used in your ledger files.')
    parser.add_argument('currency_symbol', nargs='?', metavar='CURRENCY-SYMBOL',
            help='Symbol for currency used in your ledger files.')
    args = parser.parse_args()
    main(args.coin, args.date, args.currency, args.commodity, currency_symbol=args.currency_symbol)
