#!/usr/bin/env python

"""Kiwi currency converter"""

__author__ = "Martin Mikan"
__email__ = 'Martin.Mikan@email.cz'
__version__ = '1.0'

import data_format_exceptions
import sys
import argparse
import json
import requests 
from flask import Flask, request, abort
from forex_python.converter import CurrencyCodes


def get_parsed_arguments():
    '''Function for argument parsing and application description'''
    parser = argparse.ArgumentParser(description='Kiwi currency converter')
    parser.add_argument('--amount', dest='amount', required=True, help='amount which we want to convert - float', type=float)
    parser.add_argument('--input_currency', dest='input_currency', required=True, help='3 letters name or currency symbol')
    parser.add_argument('--output_currency', dest='output_currency', required=False, help='3 letters name or currency symbol')
    args = parser.parse_args()

    argumentsArr = {
        'amount': args.amount,
        'input_currency': args.input_currency,
        'output_currency': args.output_currency
    }
    
    return argumentsArr

class CurrencyConverter:
    '''Class for the currency converter logic'''
    FIXER_API_KEY = '2a5d4330c22c57a4f74888b74560e318'
    url = "http://data.fixer.io/api/latest?access_key={}".format(FIXER_API_KEY)
    rates = {}
    amount = 0
    inputCurrency = None
    outputCurrency = None

    def __init__(self, amount, inputCurrency, outputCurrency):
        requestData = requests.get(self.url).json()
        self.rates = requestData['rates']
        self.amount = amount
        self.inputCurrency = inputCurrency
        self.outputCurrency = outputCurrency
        self.validate_and_transform_input_data()

    # converting function
    def convert(self):
        '''Function for the converting itself'''
        # base currency is EUR by default
        convertedAmount = float(self.amount) / self.rates[self.inputCurrency]
        
        convertedDict = {}
        # if we dont have an output currency - we convert to all available currencies
        if not self.outputCurrency:
                for currency, rate in self.rates.items():
                    convertedDict[currency] = convertedAmount * rate
        else:
            # if we do, we convert to just that one currency
            convertedDict[self.outputCurrency] = convertedAmount * self.rates[self.outputCurrency]

        result = self.get_output_dictionary(convertedDict)
        return result 

    # function that creates proper output syntaxe
    def get_output_dictionary(self, convertedDict):
        '''Creates proper output syntax'''
        result = {
            "input": {
                "amount": self.amount,
                "currency": self.inputCurrency
            },
            "output": convertedDict
        }

        return json.dumps(result, indent=4, sort_keys=True)

    def validate_and_transform_input_data(self):
        '''Checks if the input parameters are valid amount and known currencies'''
        try:
            self.amount = float(self.amount)
        except ValueError:
            raise data_format_exceptions.AmountValueNotFloat('The --amount input parameter "' + self.amount + '" is not float')
        
        self.inputCurrency = self.check_currency_code_and_transform_symbol(self.inputCurrency)
        self.outputCurrency = self.check_currency_code_and_transform_symbol(self.outputCurrency)

    def check_currency_code_and_transform_symbol(self, currency):
        '''Checks if the currency code is known and transforms symbol into currency code'''
        if not currency:
            return None

        c = CurrencyCodes()
        if currency in self.rates:
            return currency
        else:
            for code in self.rates:
                symbol = c.get_symbol(code)

                if symbol == currency:
                    return code
                
        raise data_format_exceptions.CurrencyNotRecognized('Didn\'t recognize "' + currency + '" currency')


# API
app = Flask(__name__)
@app.route('/currency-converter', methods=['GET'])
def currency_converter():
    amount = request.args['amount']
    input_currency = request.args['input_currency']
    output_currency = request.args.get('output_currency')

    try:
        converter = CurrencyConverter(amount, input_currency, output_currency)
        return converter.convert()
    except (data_format_exceptions.AmountValueNotFloat, data_format_exceptions.CurrencyNotRecognized) as e:
        abort(400, str(e))

# CLI
if __name__ == '__main__':
    arguments = get_parsed_arguments()

    try:
        converter = CurrencyConverter(arguments['amount'], arguments['input_currency'], arguments['output_currency'])
        print(converter.convert())
    except (data_format_exceptions.AmountValueNotFloat, data_format_exceptions.CurrencyNotRecognized) as e:
        sys.exit(str(e))
