
class Entity:
    def __init__(self, name):
        self.name = name


class Variable(Entity):
    def __init__(self, name, datatype, offset):
        super().__init__(name)
        self.datatype = datatype
        self.offset = offset

    def __repr__(self):
        return f'Variable: name: {self.name}, offset: {self.offset}'


class TemporaryVariable(Variable):
    def __init__(self, name, datatype, offset):
        super().__init__(name, datatype, offset)

    def __repr__(self):
        return f'TempVar: name: {self.name}, offset: {self.offset}'


class FormalParameter(Entity):
    def __init__(self, name, datatype, mode):
        super().__init__(name)
        self.datatype = datatype
        self.mode = mode

    def __repr__(self):
        return f'FormalParam: name: {self.name}, mode: {self.mode}'


class Parameter(FormalParameter):
    def __init__(self, name, datatype, mode, offset):
        super().__init__(name, datatype, mode)
        self.offset = offset

    def __repr__(self):
        return f'Param: name: {self.name}, mode: {self.mode} offset: {self.offset}'


class Procedure(Entity):
    def __init__(self, name, starting_quad, frame_length):
        super().__init__(name)
        self.starting_quad = starting_quad
        self.frame_length = frame_length
        self.formalParameters = []

    def __repr__(self):
        return f'Proc: name: {self.name} startingQuad: {self.starting_quad} framelen: {self.frame_length}'


class Function(Procedure):
    def __init__(self, name, starting_quad, frame_length, datatype):
        super().__init__(name, starting_quad, frame_length)
        self.datatype = datatype

    def __repr__(self):
        return f'Func: name: {self.name} startquad:{self.starting_quad} framelen:{self.frame_length}'


class SymbolTable:
    def __init__(self):
        self.scopes = []
        self.stack_position = []
        self.current_scope = None
        self.current_stack = -1
        self.function_scopes = {}
        self.outputFile = "symbolTable.txt"
        fd = open(self.outputFile, "w")
        fd.close()

    def enter_scope(self):
        if len(self.scopes) > 0:
            self.function_scopes[self.scopes[-1][-1].name] = len(self.scopes)
        self.scopes.append([])
        self.stack_position.append(12)
        self.current_scope = self.scopes[-1]
        self.current_stack += 1

    def print_state(self):
        with open(self.outputFile, 'a') as f:
            f.write("Exiting a scope, printing current state of Symbol table\n")
            for scope in self.scopes:
                f.write(f'scope:{self.scopes.index(scope)}\n')
                for entity in scope:
                    f.write(f'\t{entity}\n')

    def exit_scope(self):
        self.print_state()
        self.scopes.pop()
        if len(self.scopes) == 0:
            return
        self.current_scope = self.scopes[-1]
        self.update(self.current_scope[-1], frame_length=self.stack_position[self.current_stack])
        self.stack_position.pop()
        self.current_stack -= 1

    def get_last_frame_length(self):
        return self.stack_position[self.current_stack]

    def insert(self, entity):
        if entity.__class__.__name__ == 'Parameter' or \
                entity.__class__.__name__ == 'Variable' or \
                entity.__class__.__name__ == 'TemporaryVariable':
            entity.offset = self.stack_position[self.current_stack]
            self.stack_position[self.current_stack] += 4
        self.current_scope.append(entity)

    def lookup(self, name):
        scopeNum = 0
        for scope in reversed(self.scopes):
            scopeNum += 1
            for entity in scope:
                if entity.name == name:
                    return scopeNum, entity
        exit('Variable '+name+' not found')

    def lookup2(self, name):
        for scope in reversed(self.scopes):
            for entity in scope:
                if entity.name == name:
                    if entity.__class__.__name__ == 'Procedure' or \
                            entity.__class__.__name__ == 'Function':
                        return entity.starting_quad, entity.frame_length, entity.formalParameters
        exit('Function not found')

    def update(self, entity, frame_length=-1, starting_quad=-1):
        if entity.__class__.__name__ == 'Function' or\
                entity.__class__.__name__ == 'Procedure':
            if frame_length != -1:
                entity.frame_length = frame_length
            if starting_quad != -1:
                entity.starting_quad = starting_quad

    def add_parameter(self, entity, formal_parameter):
        if entity.__class__.__name__ == 'Function' or entity.__class__.__name__ == 'Procedure':
            entity.formalParameters.append(formal_parameter)

    def __repr__(self):
        string = ''
        for scope in self.scopes:
            for entity in scope.values():
                string += f'{entity}'
