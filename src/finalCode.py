import os


class FinalCode:
    def __init__(self, symbol_table):


        self.symbol_table = symbol_table
        self.labelCounter = 0
        self.code = []
        self.outputFile = "finalCode.s"
        self.outputFilePath = os.path.join("..", "final_code_output", self.outputFile)

        fd = open(self.outputFilePath, "w")
        fd.close()

        self.produce('.data')
        self.produce('newline: .asciz "\\n"')
        self.produce('.text')
        self.produce('Lstart:')
        self.produce('j Lmain')
        self.parameters = []
        self.main_function_list = []


    def gnlvcode(self, v):
        scope, entity = self.symbol_table.lookup(v)
        if scope == 1:
            return
        for i in range(scope-1):
            if i == 0:
                self.produce('lw t0, -4(sp)')
            else:
                self.produce('lw t0, -4(t0)')
        self.produce(f'addi t0, t0, -{entity.offset}')

    def loadvr(self, v, reg):
        if v.isdigit():
            self.produce(f'li {reg}, {v}')
            return
        scope, entity = self.symbol_table.lookup(v)
        if scope == 1:
            self.produce(f'lw {reg}, -{entity.offset}(sp)')
        elif scope > 1:
            self.gnlvcode(v)
            self.produce(f'lw {reg}, (t0)')

    def storerv(self, reg, v):
        if reg.isdigit():
            self.loadvr(reg, 't0')
            self.storerv('t0', v)
        scope, entity = self.symbol_table.lookup(v)
        if scope == 1:
            self.produce(f'sw {reg}, -{entity.offset}(sp)')
        elif scope > 1:
            self.gnlvcode(v)
            self.produce(f'sw {reg}, (t0)')

    def produceLabel(self):
        self.code.append(f'L{self.labelCounter}:')
        with open(self.outputFilePath, 'a') as f:
            f.write(f'L{self.labelCounter}:\n')
        #print(f'L{self.labelCounter}:')
        self.labelCounter += 1

    def produce(self, command):
        self.code.append(command)
        with open(self.outputFilePath, 'a') as f:
            f.write(f'\t{command}\n')
        #print("\t", command)

    def generateSegment(self, quadBlock):
        # begin block
        if quadBlock[0].arg1 == 'main':
            self.produce('Lmain:')
        else:
            self.produceLabel()
            self.produce('sw ra,(sp)')
        funcName = quadBlock[0].arg1
        # commands
        for quad in quadBlock[1:-1]:
            if quad.op == 'par':
                self.parameters.append(quad)
                continue
            if quad.op == 'call':
                isMain = False
                for func in self.main_function_list:
                    if quad.arg1 == func.name:
                        starting_quad, frame_length, formalParameters = \
                            func.starting_quad, func.frame_length, func.formalParameters
                        isMain = True
                        break
                else:
                    starting_quad, frame_length, formalParameters = \
                        self.symbol_table.lookup2(quad.arg1)
                if len(formalParameters) != max(len(self.parameters)-1, 0):
                    raise Exception(f'Wrong number of parameters in function {quad.arg1}')
                for par in self.parameters:
                    self.produceLabel()
                    if self.parameters.index(par) == 0:
                        self.produce(f'addi fp, sp, {frame_length}')
                    if par.arg2 == 'cv':
                        d = 12+4*(self.parameters.index(par))
                        self.loadvr(par.arg1, 't0')
                        self.produce(f'sw t0, -{d}(fp)')
                    elif par.arg2 == 'ret':
                        scope, entity = self.symbol_table.lookup(par.arg1)
                        if scope != 1:
                            exit("error")
                        self.produce(f'addi t0, sp, -{entity.offset}')
                        self.produce('sw t0, -8(fp)')
                # Syndesmos prospelasis
                self.produceLabel()
                if not isMain:
                    scope = 0
                    if funcName not in [func.name for func in self.main_function_list]:
                        scope, entity = self.symbol_table.lookup(funcName)
                        scope = len(self.symbol_table.scopes)-scope+1
                    if self.symbol_table.function_scopes[quad.arg1] == scope:
                        self.produce('lw t0, -4(sp)')
                        self.produce('sw t0, -4(fp)')
                    elif self.symbol_table.function_scopes[quad.arg1] > scope:
                        self.produce('sw sp, -4(fp)')
                    else:
                        exit("cant call this function")

                # Deiktis stoivas
                self.produce(f'addi sp, sp, {frame_length}')
                # Klisi
                self.produce(f'jal L{starting_quad}')
                # clean setup
                if not isMain:
                    self.parameters = []
                continue

            self.produceLabel()
            if quad.op == ':=':
                self.loadvr(quad.arg1, 't1')
                self.storerv('t1', quad.arg3)
            elif quad.op == '+':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce('add t1, t1, t2')
                self.storerv('t1', quad.arg3)
            elif quad.op == '-':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce('sub t1, t1, t2')
                self.storerv('t1', quad.arg3)
            elif quad.op == '*':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce('mul t1, t1, t2')
                self.storerv('t1', quad.arg3)
            elif quad.op == '/':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce('div t1, t1, t2')
                self.storerv('t1', quad.arg3)
            elif quad.op == 'jump':
                self.produce(f'j L{quad.arg3}')
            elif quad.op == '==':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce(f'beq t1, t2, L{quad.arg3}')
            elif quad.op == '!=':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce(f'bne t1, t2, L{quad.arg3}')
            elif quad.op == '<':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce(f'blt t1, t2, L{quad.arg3}')
            elif quad.op == '>':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce(f'bgt t1, t2, L{quad.arg3}')
            elif quad.op == '<=':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce(f'ble t1, t2, L{quad.arg3}')
            elif quad.op == '>=':
                self.loadvr(quad.arg1, 't1')
                self.loadvr(quad.arg2, 't2')
                self.produce(f'bge t1, t2, L{quad.arg3}')
            elif quad.op == 'out':
                self.loadvr(quad.arg1, 'a0')
                self.produce('li a7,1')
                self.produce('ecall')
                self.produce('la a0, newline')
                self.produce('li a7,4')
                self.produce('ecall')
            elif quad.op == 'in':
                self.produce('li a7, 5')
                self.produce('ecall')
                self.storerv('a0', quad.arg1)
            elif quad.op == 'ret':
                self.produce('lw t1, -8(sp)')
                self.loadvr(quad.arg1, 't0')
                self.produce(f'sw t0, (t1)')
                self.produce('lw ra, (sp)')
                frame_length = self.symbol_table.get_last_frame_length()
                self.produce(f'addi sp, sp, -{frame_length}')
                self.produce('jr ra')
            elif quad.op == 'halt':
                self.produce('li a0, 0')
                self.produce('li a7, 93')
                self.produce('ecall')
                return


        # end block
        self.produceLabel()
        frame_length = self.symbol_table.get_last_frame_length()
        self.produce('lw ra,(sp)')
        self.produce(f'addi sp, sp, -{frame_length}')
        self.produce('jr ra')



