# -*- coding: utf-8 -*-

def normalize(expr):

    def recursion(expr):
        left, op, right = expr
        if op == '&&':
            lst1 = recursion(left)
            lst2 = recursion(right)
            lst=[]
            for i1 in lst1:
                for i2 in lst2:
                    item = i1[:]
                    item.extend(i2)
                    lst.append(item)
        elif op == '||':
            lst1 = recursion(left)
            lst2 = recursion(right)
            lst = []
            lst.extend(lst1)
            lst.extend(lst2)
        else:
            lst = [[expr]]

        return lst

    lst = recursion(expr)

    def build_expr(lst, op):
        expr = lst[0]
        for factor in lst[1:]:
            expr = (expr, op, factor)
        return expr

    expr = build_expr(lst[0], '&&')
    for sublst in lst[1:]:
        expr = (expr, '||', build_expr(sublst, '&&'))

    return expr

__all__ = ['normalize']

