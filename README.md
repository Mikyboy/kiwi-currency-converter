# Kiwi Currency Converter
Currency converter for a kiwi job application as per the [specification](https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip3 install -r requirements.txt
```

## Usage

This application is both a CLI and a web API application.

To run this application as a web API application run
```bash
source kiwi/bin/activate
FLASK_APP=currency_converter.py flask run
```

this will make the WEB API application run on http://localhost:5000

## Examples

### CLI 
```
./python3 currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{   
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2513.5041
    }
}
```

### API
```
GET /currency-converter?amount=1&input_currency=US$&output_currency=GBP HTTP/1.1
{
    "input": {
        "amount": 1,
        "currency": "USD"
    },
    "output": {
        "GBP": 0.7670046502751817
    }
}
```


## Implementation details
- Since there is many currencies represented by, for example, symbol £ (Pound sterling, Egyptian pound, Syrian pound,...) I have decided to let the program simply choose the first currency it finds in the currencies dictionary (I could imagine a solution for example where certain currencies have bigger priority but as it was not specified I have chosen this solution)


## Docker
The reason I haven't put this application into docker container is that I was developing it on a Windows 10 home (Linux Bash Shell), which I found out (I have always used linux before which I currently don't have installed) does't support docker desktop and is not a very good friend with using docker in the windows provided Linux Bash Shell. I hope this fact won't result in a negative review of this project.