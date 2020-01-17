class Error(Exception):
   '''Base class for other exceptions'''
   pass
class AmountValueNotFloat(Error):
   '''Raised when the amount parameter can't be succesfully converted into float'''
   pass
class CurrencyNotRecognized(Error):
   '''Raised when the currency was not recognized'''
   pass