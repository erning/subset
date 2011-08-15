# -*- coding: utf-8 -*-

def _is_subset_factor(a, b, absent=False):
    '''  a ⊆ b ? True : False '''
    an, ao, av = a
    bn, bo, bv = b

    if an != bn:
        return absent
    #if type(av) != type(bv):
    #    return False

    if ao == '==':
        if bo == '==': return bv == av
        if bo == '>' : return bv <  av
        if bo == '<' : return bv >  av
        if bo == '>=': return bv <= av
        if bo == '<=': return bv >= av
        if bo == '!=': return bv != av
        
    elif ao == '>':
        if bo == '==': return False
        if bo == '>' : return bv <= av
        if bo == '<' : return False
        if bo == '>=': return bv <= av
        if bo == '<=': return False
        if bo == '!=': return bv <= av

    elif ao == '<':
        if bo == '==': return False
        if bo == '>' : return False
        if bo == '<' : return bv >= av
        if bo == '>=': return False
        if bo == '<=': return bv >= av
        if bo == '!=': return bv >= av

    elif ao == '>=':
        if bo == '==': return False
        if bo == '>' : return bv <  av
        if bo == '<' : return False
        if bo == '>=': return bv <= av
        if bo == '<=': return False
        if bo == '!=': return bv <  av

    elif ao == '<=':
        if bo == '==': return False
        if bo == '>' : return False
        if bo == '<' : return bv >  av
        if bo == '>=': return False
        if bo == '<=': return bv >= av
        if bo == '!=': return bv >  av

    elif ao == '!=':
        if bo == '==': return False
        if bo == '>' : return False
        if bo == '<' : return False
        if bo == '>=': return False
        if bo == '<=': return False
        if bo == '!=': return bv == av

def _is_subset(a, b, absent=False):
    al, ao, ar = a
    bl, bo, br = b

    if ao == '||':
        return _is_subset(al, b) and _is_subset(ar, b)
    elif bo == '||':
        return _is_subset(a, bl) or _is_subset(a, br)
    elif bo == '&&':
        return _is_subset(a, bl) and _is_subset(a, br)
    elif ao == '&&':
        return _is_subset(al, b) or _is_subset(ar, b)
    else:
        return _is_subset_factor(a, b, absent)

    return ret    

def is_subset(a, b):
    '''
    params a, b are expressions in string
    return True if a ⊆ b or False if a ⊈ b
    '''
    import parser
    import normalizer

    if type(a) is str:
        a = parser.parse(a)
    a = normalizer.normalize(a)

    if type(b) is str:
        b = parser.parse(b)
    b = normalizer.normalize(b)
    
    return _is_subset(a, b)

def is_superset(a, b):
    '''
    params a, b are expressions in string
    return True if a ⊇ b or False if a ⊉ b
    '''    
    return is_subset(b, a)

if __name__ == '__main__':
    try:
        import sys
        if len(sys.argv) < 3:
            print "Usage: {0} <expression> <expression>".format(sys.argv[0])
            sys.exit(1)
        a = sys.argv[1]
        b = sys.argv[2]

        ret = is_subset(a, b)
        print '"' + a + '" is',
        if not ret:
            print 'NOT',
        print 'subset of "' + b + '"'

        ret = is_subset(b, a)
        print '"' + b + '" is',
        if not ret:
            print 'NOT',
        print 'subset of "' + a + '"'    
    except Exception as e:
        print e
        raise e

__all__ = ['is_subset', 'is_superset']

