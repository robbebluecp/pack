


# /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pdfminer/psparser.py -- line 498
'''
def nexttoken(self):
    index = 0
    while not self._tokens:
        index += 1
        self.fillbuf()
        self.charpos = self._parse1(self.buf, self.charpos)
        if index >= 100:
            return
    token = self._tokens.pop(0)
    log.debug('nexttoken: %r', token)
    return token
'''


# /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pdfplumber/ line 177
'''
def extract_tables(self, table_settings={}):
    tables = self.find_tables(table_settings)
    table = sorted(tables, key=lambda x: x.bbox[1])
    return [ y.extract() for y in table]
'''
