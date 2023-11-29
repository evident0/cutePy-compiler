def main_function():
#{
    #declare VARIABLE_ONE, VARIABLE_TWO
    def function1():
    #{
        #declare result_code
        def function2():
        #{
            #declare result_code
            def function3():
            #{
                #declare result_code
                def function4():
                #{
                    #declare local_variable, result_code
                    local_variable = 32;
                    VARIABLE_TWO = local_variable;
                    VARIABLE_ONE = VARIABLE_TWO + local_variable;
                    return(result_code);

                #}
                result_code = function4();
                return ((result_code) + 1);
            #}

            result_code = function3();
            return ((result_code) + 1);

        #}
         result_code = function2();
         return ((result_code) + 1);
    #}
    print(function1()); #$ prints 3 #$
    print(VARIABLE_TWO); #$ prints 32 #$
    print(VARIABLE_ONE); #$ prints 64 #$
#}
if __name__ == "__main__":
    main_function();