#!/usr/bin/env python

import sys
import subprocess
import argparse
from datetime import datetime
from matplotlib import pyplot as plt

def ledger_fetch_data(command):
    print(' '.join(command), file=sys.stderr)
    stdout = subprocess.check_output(command).decode().split('\n')
    stdout = list(filter(None, stdout)) # Remove empty items
    return stdout

def process_line(transaction):
    date, amount = transaction.split()
    date = datetime.strptime(date, '%Y-%m-%d')
    amount = float(amount)
    return date, amount

def main():
    parser = argparse.ArgumentParser(description='Visually plot ledger files.')
    parser.add_argument('ledger_files', nargs='+', metavar='FILE', help='Input ledger file(s).')
    # Limit timeframes specified to only one
    timeframe_arg = parser.add_mutually_exclusive_group()
    timeframe_arg.add_argument('-D', '--daily', const='-D', default='-D', # Default value
            help='Group postings by day. (Default)',
            dest='timeframe', action='store_const')
    timeframe_arg.add_argument('-W', '--weekly', const='-W',
            help='Group postings by week (starting on Sundays).',
            dest='timeframe', action='store_const')
    timeframe_arg.add_argument('-M', '--monthly', const='-M',
            help='Group postings by month.',
            dest='timeframe', action='store_const')
    timeframe_arg.add_argument('--quarterly', const='--quarterly',
            help='Group postings by fiscal quarter.',
            dest='timeframe', action='store_const')
    timeframe_arg.add_argument('-Y', '--yearly', const='-Y',
            help='Group postings by year.',
            dest='timeframe', action='store_const')
    args = parser.parse_args()

    ledger_command = ['ledger', 'reg', args.timeframe]
    for file in args.ledger_files:
        ledger_command.extend(['-f', file])

    ledger_queue = {
            'Cashflow':     ledger_command + ['-j', '-n', '^income', '^expenses'],
            'Asset total':  ledger_command + ['-J', '-n', '^assets'],
            'Asset growth': ledger_command + ['-j', '-n', '^assets'],
            'Expenditure':  ledger_command + ['-j', '-n', '^expenses'],
            'Networth':     ledger_command + ['-J', '-n', '^assets', '^liabilities'],
    }

    for category, command in ledger_queue.items():
        dates, amounts = [], []
        for transaction in ledger_fetch_data(command):
            date, amount = process_line(transaction)
            dates.append(date)
            amounts.append(amount)
        plt.plot(dates, amounts, label=category)


    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
