from finalCode import FinalCode
from lexer import *
from Quad import *
from symbol_table import *


class MyParser:
    def __init__(self, input):
        self.lex = Lexer(input)
        self.token = self.lex.next_token()
        self.quad_list = QuadList()
        self.symbol_table = SymbolTable()
        self.final_code = FinalCode(self.symbol_table)

    def throw_error(self, expected):
        exit(f'SyntaxError in Line:{self.token.line_number}: Expected {expected} '
             f'but found {self.token.recognized_string}')

    def syntax_analyzer(self):
        self.start_rule()
        print('compilation complete')
        return self.quad_list.quads

    def start_rule(self):
        # self.symbol_table.enter_scope()
        self.def_main_part()
        self.call_main_part()
        # self.symbol_table.exit_scope()

    def def_main_part(self):
        if self.is_match('def'):
            self.def_main_function()
        else:
            self.throw_error('def')

        while self.is_match('def'):
            self.def_main_function()

    def def_main_function(self):
        self.match_and_next('def')
        id = self.match_family_and_next(Family.IDENTIFIER)

        proc = Procedure(id, None, None)
        self.final_code.main_function_list.append(proc)
        self.match_and_next('(')
        self.match_and_next(')')
        self.match_and_next(':')
        self.match_and_next('#{')
        self.symbol_table.enter_scope()

        self.declarations()

        while self.is_function():
            self.def_function()

        self.symbol_table.update(proc, starting_quad=self.quad_list.nextQuad())
        self.quad_list.genQuad('begin_block', id, '_', '_')
        self.quad_list.beginBlock()

        self.statements()

        self.symbol_table.update(proc, frame_length=self.symbol_table.stack_position[self.symbol_table.current_stack])
        self.quad_list.genQuad('end_block', id, '_', '_')
        self.quad_list.endBlock()
        self.final_code.generateSegment(self.quad_list.getLastBlock())
        self.symbol_table.exit_scope()

        self.match_and_next('#}')

    def def_function(self):
        self.match_and_next('def')
        id = self.match_family_and_next(Family.IDENTIFIER)
        func = Function(id, None, None, 'integer')
        self.symbol_table.insert(func)
        self.symbol_table.enter_scope()
        self.match_and_next('(')
        params = self.id_list()
        for param in params:
            func.formalParameters.append(FormalParameter(param, 'integer', 'in'))
            self.symbol_table.insert(Parameter(param, 'integer', 'in', None))
        self.match_and_next(')')
        self.match_and_next(':')
        self.match_and_next('#{')
        self.declarations()

        while self.is_function():
            self.def_function()

        self.symbol_table.update(func, starting_quad=self.quad_list.nextQuad())
        self.quad_list.genQuad('begin_block', id, '_', '_')
        self.quad_list.beginBlock()
        self.statements()
        self.symbol_table.update(func, frame_length=self.symbol_table.stack_position[self.symbol_table.current_stack])
        self.quad_list.genQuad('end_block', id, '_', '_')
        self.quad_list.endBlock()
        self.final_code.generateSegment(self.quad_list.getLastBlock())
        self.symbol_table.exit_scope()
        self.match_and_next('#}')

    def declarations(self):
        while self.is_declaration():
            for decl in self.declaration_line():
                self.symbol_table.insert(Variable(decl, 'integer', None))

    def declaration_line(self):
        self.match_and_next('#declare')
        return self.id_list()

    def statement(self):
        if self.is_simple_statement():
            self.simple_statement()
        elif self.is_structured_statement():
            self.structured_statement()
        else:
            self.throw_error('simple statement or structured statement')

    def statements(self):
        if self.is_simple_statement() or self.is_structured_statement():
            self.statement()
        else:
            self.throw_error('simple statement or structured statement')

        while self.is_simple_statement() or self.is_structured_statement():
            self.statement()

    def simple_statement(self):
        if self.is_match('print'):
            self.print_stat()
        elif self.is_match('return'):
            self.return_stat()
        elif self.is_family_match(Family.IDENTIFIER):
            self.assignment_stat()
        else:
            self.throw_error('print, return or assignment statement')

    def structured_statement(self):
        if self.is_match('if'):
            self.if_stat()
        elif self.is_match('while'):
            self.while_stat()
        else:
            self.throw_error('if or while')

    def assignment_stat(self):
        id = self.match_family_and_next(Family.IDENTIFIER)
        self.match_and_next('=')
        if self.is_match('int'):
            self.match_and_next('int')
            self.match_and_next('(')
            self.match_and_next('input')
            self.match_and_next('(')
            self.match_and_next(')')
            self.match_and_next(')')
            self.match_and_next(';')
            self.quad_list.genQuad('in', id, '_', '_')
        elif self.is_expression():
            expr = self.expression()
            self.match_and_next(';')
            self.quad_list.genQuad(':=', expr, '_', id)
        else:
            self.throw_error('expression or input')

    def print_stat(self):
        self.match_and_next('print')
        self.match_and_next('(')
        expr = self.expression()
        self.match_and_next(')')
        self.match_and_next(';')
        self.quad_list.genQuad('out', expr, '_', '_')

    def return_stat(self):
        self.match_and_next('return')
        self.match_and_next('(')
        expr = self.expression()
        self.match_and_next(')')
        self.match_and_next(';')
        self.quad_list.genQuad('ret', expr, '_', '_')

    def if_stat(self):
        ifList = []
        self.match_and_next('if')
        self.match_and_next('(')
        condtrue, condfalse = self.condition()
        self.match_and_next(')')
        self.quad_list.backPatch(condtrue, self.quad_list.nextQuad())
        self.match_and_next(':')
        if self.is_simple_statement() or self.is_structured_statement():
            self.statement()
            ifList = makeList(self.quad_list.nextQuad())
            self.quad_list.genQuad('jump', '_', '_', '_')
            self.quad_list.backPatch(condfalse, self.quad_list.nextQuad())
        elif self.is_match('#{'):
            self.match_and_next('#{')
            self.statements()
            ifList = makeList(self.quad_list.nextQuad())
            self.quad_list.genQuad('jump', '_', '_', '_')
            self.quad_list.backPatch(condfalse, self.quad_list.nextQuad())
            self.match_and_next('#}')
        else:
            self.throw_error('if statement body')

        if self.is_match('else'):
            self.match_and_next('else')
            self.match_and_next(':')
            if self.is_simple_statement() or self.is_structured_statement():
                self.statement()
            elif self.is_match('#{'):
                self.match_and_next('#{')
                self.statements()
                self.match_and_next('#}')
            else:
                self.throw_error('else statement body')
        self.quad_list.backPatch(ifList, self.quad_list.nextQuad())

    def while_stat(self):
        self.match_and_next('while')
        condQuad = self.quad_list.nextQuad()
        self.match_and_next('(')
        condtrue, condfalse = self.condition()
        self.match_and_next(')')
        self.quad_list.backPatch(condtrue, self.quad_list.nextQuad())
        self.match_and_next(':')
        if self.is_simple_statement() or self.is_structured_statement():
            self.statement()
            self.quad_list.genQuad('jump', '_', '_', condQuad)
            self.quad_list.backPatch(condfalse, self.quad_list.nextQuad())
        elif self.is_match('#{'):
            self.match_and_next('#{')
            self.statements()
            self.quad_list.genQuad('jump', '_', '_', condQuad)
            self.quad_list.backPatch(condfalse, self.quad_list.nextQuad())
            self.match_and_next('#}')
        else:
            self.throw_error('while statement body')

    def id_list(self):
        id_list = []
        if self.is_family_match(Family.IDENTIFIER):
            id_list.append(self.match_family_and_next(Family.IDENTIFIER))
            while self.is_match(','):
                self.match_and_next(',')
                id_list.append(self.match_family_and_next(Family.IDENTIFIER))
        return id_list

    def expression(self):
        sign = self.optional_sign()
        t1place = self.term()
        if sign == '-':
            w = self.quad_list.newTemp()
            self.symbol_table.insert(TemporaryVariable(w, 'integer', None))
            self.quad_list.genQuad('-', 0, t1place, w)
            t1place = w
        while self.is_family_match(Family.ADDOP):
            sign = self.token.recognized_string
            self.next()
            t2place = self.term()
            w = self.quad_list.newTemp()
            self.symbol_table.insert(TemporaryVariable(w, 'integer', None))
            self.quad_list.genQuad(sign, t1place, t2place, w)
            t1place = w

        eplace = t1place
        return eplace

    def term(self):
        f1place = self.factor()
        while self.is_family_match(Family.MULOP):
            sign = self.token.recognized_string
            if sign == '//':
                sign = '/'
            self.next()
            f2place = self.factor()
            w = self.quad_list.newTemp()
            self.symbol_table.insert(TemporaryVariable(w, 'integer', None))
            self.quad_list.genQuad(sign, f1place, f2place, w)
            f1place = w

        tplace = f1place
        return tplace

    def factor(self):
        if self.is_family_match(Family.NUMBER):
            ret = self.token.recognized_string
            self.match_family_and_next(Family.NUMBER)
            return ret
        elif self.is_match('('):
            self.match_and_next('(')
            ret = self.expression()
            self.match_and_next(')')
            return ret
        elif self.is_family_match(Family.IDENTIFIER):
            id = self.token.recognized_string
            self.match_family_and_next(Family.IDENTIFIER)
            tail = self.id_tail()
            if tail == -1:
                return id
            else:
                for param in tail:
                    self.quad_list.genQuad('par', param, 'cv', '_')
                temp = self.quad_list.newTemp()
                self.symbol_table.insert(TemporaryVariable(temp, 'integer', None))
                self.quad_list.genQuad('par', temp, 'ret', '_')
                self.quad_list.genQuad('call', id, '_', '_')
                return temp
        else:
            self.throw_error('factor')

    def id_tail(self):
        if self.is_match('('):
            self.match_and_next('(')
            ret = self.actual_par_list()
            self.match_and_next(')')
            return ret
        return -1

    def actual_par_list(self):
        params = []
        if self.is_expression():
            params.append(self.expression())
            while self.is_match(','):
                self.match_and_next(',')
                if self.is_expression():
                    params.append(self.expression())
        return params

    def optional_sign(self):
        if self.is_family_match(Family.ADDOP):
            ret = self.token.recognized_string
            self.next()
            return ret

    def condition(self):
        btrue, bfalse = self.bool_term()
        while self.is_match('or'):
            sign = self.token.recognized_string
            self.next()
            self.quad_list.backPatch(bfalse, self.quad_list.nextQuad())
            q2true, q2false = self.bool_term()
            btrue = mergeList(btrue, q2true)
            bfalse = q2false
        return btrue, bfalse

    def bool_term(self):
        qtrue, qfalse = self.bool_factor()
        while self.is_match('and'):
            sign = self.token.recognized_string
            self.next()
            self.quad_list.backPatch(qtrue, self.quad_list.nextQuad())
            r2true, r2false = self.bool_factor()
            qfalse = mergeList(qfalse, r2false)
            qtrue = r2true
        return qtrue, qfalse

    def bool_factor(self):
        if self.is_match('not'):
            self.match_and_next('not')
            self.match_and_next('[')
            rfalse, rtrue = self.condition()
            self.match_and_next(']')
            return rtrue, rfalse
        elif self.is_match('['):
            self.match_and_next('[')
            rtrue, rfalse = self.condition()
            self.match_and_next(']')
            return rtrue, rfalse
        elif self.is_expression():
            e1place = self.expression()
            sign = self.match_family_and_next(Family.RELOP)
            e2place = self.expression()
            rtrue = makeList(self.quad_list.nextQuad())
            self.quad_list.genQuad(sign, e1place, e2place, '_')
            rfalse = makeList(self.quad_list.nextQuad())
            self.quad_list.genQuad('jump', '_', '_', '_')
            return rtrue, rfalse
        else:
            self.throw_error('condition')

    def call_main_part(self):
        self.match_and_next('if')
        self.match_and_next('__name__')
        self.match_and_next('==')
        self.match_and_next('"__main__"')
        self.match_and_next(':')

        proc = Procedure('main', None, None)
        self.symbol_table.insert(proc)

        self.symbol_table.enter_scope()
        self.symbol_table.update(proc, starting_quad=self.quad_list.nextQuad())
        self.quad_list.genQuad('begin_block', 'main', '_', '_')
        self.quad_list.beginBlock()
        if self.is_family_match(Family.IDENTIFIER):
            self.main_function_call()
        else:
            self.throw_error('main function call')
        while self.is_family_match(Family.IDENTIFIER):
            self.main_function_call()
        self.quad_list.genQuad('halt', '_', '_', '_')
        self.symbol_table.update(proc, frame_length=self.symbol_table.stack_position[self.symbol_table.current_stack])
        self.quad_list.genQuad('end_block', 'main', '_', '_')
        self.quad_list.endBlock()
        self.final_code.generateSegment(self.quad_list.getLastBlock())
        self.symbol_table.exit_scope()
        '''print("Printing all defined Functions:")
        for func in self.self.final_code.main_function_list:
            print('\t', func)
        print(self.symbol_table.function_scopes)'''


    def main_function_call(self):
        id = self.match_family_and_next(Family.IDENTIFIER)
        self.match_and_next('(')
        self.match_and_next(')')
        self.match_and_next(';')
        self.quad_list.genQuad('call', id, '_', '_')

    def is_expression(self):
        return self.is_family_match(Family.NUMBER) or self.is_family_match(Family.ADDOP) \
            or self.is_match('(') or self.is_family_match(Family.IDENTIFIER)

    def is_structured_statement(self):
        return self.is_match('if') or self.is_match('while')

    def is_simple_statement(self):
        return self.is_match('print') or self.is_match('return') or self.is_family_match(Family.IDENTIFIER)

    def is_function(self):
        return self.token.recognized_string == 'def'

    def is_call(self):
        return self.token.recognized_string == 'if'

    def is_declaration(self):
        return self.token.recognized_string == '#declare'

    def match_and_next(self, expected):
        if self.token.recognized_string == expected:
            self.token = self.lex.next_token()
        else:
            self.throw_error(expected)

    def next(self):
        self.token = self.lex.next_token()

    def is_match(self, expected):
        return self.token.recognized_string == expected

    def is_family_match(self, expected):
        return self.token.family == expected

    def match_family_and_next(self, expected):
        if self.token.family == expected:
            ret = self.token.recognized_string
            self.token = self.lex.next_token()
            return ret
        else:
            self.throw_error(expected)
