#!/usr/bin/env python

import sys
import subprocess
from datetime import datetime
from matplotlib import pyplot as plt

LEDGER = 'ledger'

def ledger_fetch_data(ledger_files):
    ledger_command = [LEDGER, 'reg']
    for file in ledger_files:
        ledger_command.extend(['-f', file])

    ledger_queue = {
            'Monthly cashflow':     ledger_command + ['-M', '-j', '-n', '^income', '^expenses'],
            #'Daily asset total':    ledger_command + ['-D', '-J', '-n', '^assets'],
            #'Monthly asset growth': ledger_command + ['-M', '-j', '-n', '^assets'],
            'Monthly expenditure':  ledger_command + ['-M', '-j', '-n', '^expenses'],
            'Daily networth':       ledger_command + ['-D', '-J', '-n', '^assets', '^liabilities'],
            #'Monthly networth':     ledger_command + ['-M', '-J', '-n', '^assets', '^liabilities'],
    }

    for category, command in ledger_queue.items():
        print(' '.join(command))
        # Grab STDOUT and split into list.
        command_output = subprocess.check_output(command).decode().split('\n')
        command_output = list(filter(None, command_output)) # Remove empty items
        dates = []
        amounts = []
        for transaction in command_output:
            date, amount = transaction.split()
            dates.append(datetime.strptime(date, '%Y-%m-%d'))
            amounts.append(float(amount))
        ledger_queue[category] = (dates, amounts)

    return ledger_queue

def main():
    ledger_files = sys.argv[1:]
    if not ledger_files:
        print('No files given')
        sys.exit(1)

    data = ledger_fetch_data(ledger_files)

    for category, items in data.items():
        plt.plot(items[0], items[1], label=category)

    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
