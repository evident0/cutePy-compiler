#$ PLEASE NOTE that this is the math.floor of the square root not the closest integer #$
#$ example: if the square root is 178.98 the output will be 178 #$
def closest_integer_square_root():
#{
    #declare x, result
    def closest_integer_square_root_helper(n):
    #{
        #declare low, high, mid, closest, square
        if (n==0 or n==1):
        #{
            return (n);
        #}
        low = 0;
        high = n;

        while (low <= high):
        #{
            mid = (low + high) // 2;
            square = mid * mid;

            if (square == n):#{
                return (mid);
            #}
            if (square < n):
            #{
                low = mid + 1;
                closest = mid;
            #}
            else:
            #{
                high = mid - 1;
            #}
        #}
        return (closest);
    #}
    x = int(input());
    result = closest_integer_square_root_helper(x);
    print(result);
#}
if __name__ == "__main__":
    closest_integer_square_root();