from ply import lex, yacc

states = (
   ('chars','exclusive'),
)

tokens = (
   "BOOLEAN", "DASH", "NUMBER", "E", "PERIOD", "SEMICOLON", "QUOTE", "HASH", "STRUCT", "VECTOR", "MAP", "END", "COMMA", "CHARS", "NEWLINE"
)

t_chars_CHARS = "[^\0\r\n,}]+"
def t_chars_COMMA(t):
    ","
    t.lexer.begin('INITIAL')
    return t
def t_chars_END(t):
    "}"
    t.lexer.begin('INITIAL')
    return t
def t_chars_other(t):
    "[\0\r\n]"
    t.lexer.begin('INITIAL')
def t_chars_error(t):
    t.lexer.begin('INITIAL')
    raise TypeError("Unknown text in a character block: '%s'" % (t.value,))
def t_error(t):
    t.lexer.begin('INITIAL')
    raise TypeError("Unknown text: '%s'" % (t.value,))
t_BOOLEAN = r"T|F"
t_DASH = r"-"
t_NUMBER = r"[0-9]+"
t_E = r"e|E"
t_PERIOD = r"\."
t_SEMICOLON = r";"
def t_QUOTE(t):
    "\'"
    t.lexer.begin('chars')
    return t
def t_HASH(t):
    "\#"
    t.lexer.begin('chars')
    return t
t_STRUCT = "s{"
t_VECTOR = "v{"
t_MAP = "m{"
t_END = "}"
t_COMMA = ","
t_NEWLINE = r"\n"

######################### END LEXER #################

def p_records(p):
    """records : record
               | record NEWLINE
               | record COMMA arrayofrecords
               | record COMMA arrayofrecords NEWLINE"""
    p[0] = p[1]
    if len(p) > 3:
        p[0] = [p[1]] + p[3]

def p_arrayofrecords(p):
    """arrayofrecords : record
                      | record COMMA arrayofrecords"""
    p[0] = [p[1]]
    if len(p) > 3:
        p[0] = [p[1]] + p[3]

def p_record(p):
    """record : primitive
              | struct
              | vector
              | map"""
    p[0] = p[1]

def p_primative(p):
    """primitive : boolean
                 | int
                 | long
                 | float
                 | double
                 | ustring
                 | buffer"""
    p[0] = p[1]

def p_boolean(p):
    "boolean : BOOLEAN"
    if p[1] == "T" : p[0] = True
    else : p[0] = False

def p_int(p):
    """int : DASH NUMBER
           | NUMBER"""
    if len(p) == 3 : p[0] = -int(p[2])
    else : p[0] = int(p[1])

def p_long(p):
    """long : SEMICOLON int"""
    p[0] = p[2]

def p_float(p):
    """float : int PERIOD NUMBER
             | int PERIOD NUMBER E int"""
    if len(p) == 4 :
        p[0] = float(str(p[1]) + "." + p[3])
    else :
        p[0] = float(str(p[1]) + "." + p[3] + "e" + str(p[5]))

def p_double(p):
    """double : SEMICOLON float"""
    p[0] = p[2]

def p_chars(p) :
    """chars : 
             | CHARS"""
    if len(p) == 1:
        p[0] = ""
    else:
        p[0] = p[1]

class LazyString:
    def __init__(self, s, encoding="utf8", decodeFunc=None) :
        self._str = s
        self._encoding = encoding
        self._decoded = None
        self.decodeFunc = decodeFunc
    def _decode(self):
        if not self._decoded :
            self._decoded =  self._str.decode(self._encoding)
            if self.decodeFunc :
                self._decoded = self.decodeFunc(self._decoded)
        return self._decoded
    def __str__(self):
        decoded = self._decode()
        if type(decoded) == str : return decoded
        return decoded.encode('utf-8')
    def __unicode__(self):
        decoded = self._decode()
        if type(decoded) == unicode : return decoded
        return unicode(decoded)
    def __repr__(self):
        return 'LazyString(%s)' % repr(str(self))

def p_ustring(p):
    """ustring : QUOTE chars"""
    def decode(x) :
        for a,b in (("%00", "\0"), ("%0a", "\n"), ("%25", "%"), ("%2c", ",")):
            x = x.replace(a, b)
        return x
    p[0] = LazyString(p[2], 'utf-8', lambda x : decode(x))

def p_buffer(p):
    """buffer : HASH chars"""
    # don't decode it yet, because that takes a while
    p[0] = LazyString(p[2], 'hex')

def p_recordlist(p):
    """recordlist :
                  | record
                  | record COMMA recordlist"""
    if len(p) == 1 :
        p[0] = []
    else:
        p[0] = [p[1]]

    if len(p) > 3 :
        p[0] += p[3]

def p_struct(p):
    """struct : STRUCT recordlist END"""
    p[0] = p[2]

# not sure how this is stored
def p_vector(p):
    """vector : VECTOR recordlist END"""
    p[0] = p[2]

# not sure how this is stored
def p_map(p):
    """map : MAP recordlist END"""
    m = dict()
    a = p[2]
    if len(a) % 2 != 0 :
        raise TypeError("Map doesn't have an even number of keys. Length: %s" % len(a))
    for i in xrange(0, len(a), 2) :
        m[a[i]] = a[i+1]
    p[0] = m

def p_error(p):
    p.lexer.begin('INITIAL')
    raise TypeError("Unexpected %s" % (p))
    

######################### END PARSER #################

lexer = lex.lex()
parser = yacc.yacc(debug=0, write_tables=0)

def test():
    test_primatives()

def test_primatives() :
    assert yacc.parse("T") == True
    assert yacc.parse("F") == False
    assert yacc.parse("1234") == 1234
    assert yacc.parse("-1234") == -1234
    assert yacc.parse(";1234") == 1234
    assert yacc.parse(";-1234") == -1234
    assert yacc.parse("1.2") == 1.2
    assert yacc.parse("-1.2") == -1.2
    assert yacc.parse("1.0e10") == 1e10
    assert yacc.parse("1.0E10") == 1e10
    assert yacc.parse("1.0E-10") == 1e-10
    assert yacc.parse(";1.2") == 1.2
    assert yacc.parse("s{T,F}") == [True, False]
    assert yacc.parse("v{T,F}") == [True, False]
    assert yacc.parse("m{T,F}") == [True, False]
    assert yacc.parse("m{'don't,#20416120}") == ["don't", " Aa "]
    assert yacc.parse("v{s{T,F}}") == [[True,False]]
    assert yacc.parse("v{s{T,F}},v{s{F,F}}") == [[[True,False]], [[False, False]]]
    assert yacc.parse("'\xe2\x98\x83") == u"\u2603"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 :
        print parser.parse(file(sys.argv[1]).read())
    else :
        test()
        print "All tests passed."


######################## API ######################
def csv(s) :
    lexer.begin('INITIAL')
    return parser.parse(s, lexer=lexer)
