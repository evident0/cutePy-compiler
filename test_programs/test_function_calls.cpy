def main_function():
#{
    #declare result, a_variable, another_variable
    def parent_function(param):
    #{
        def sibling_one(param):
        #{
            return (param+another_variable);
        #}
        def sibling_two(param):
        #{
            return (param+another_variable);
        #}
        def sibling_three(param):
        #{
            return (sibling_one(param));
        #}
        #$ return explanation #$
        #$ sibling_three calls sibling_one #$
        #$ sibling_one is now called by the parent_function NOT ANOTHER SIBLING #$
        #$ lastly parent_function calls sibling_two #$
        return (sibling_three(param) + sibling_one(param) + sibling_two(param));

    #}
    a_variable = 32;
    another_variable = 32;
    result = parent_function(a_variable);
    #$ prints 192 from because return is (64+64+64) #$
    print(result);

#}
if __name__ == "__main__":
    main_function();