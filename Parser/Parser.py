import sys

def set_next_symbol():
    global i; global n
    
    if ( i+1 < n ):
        i += 1; return True
    else:
        end(False)

def S():
    sys.stdout.write('S')
    global i; global input
    symbol = input[i]
    
    if (symbol == 'a'):
        set_next_symbol()
        A(); B()
        return True
    elif (symbol == 'b'):
        set_next_symbol()
        B(); A()
        return True
    else:
        end(False)
        
def A():
    sys.stdout.write('A')
    global i; global input
    symbol = input[i]
    
    if (symbol == 'b'):
        set_next_symbol()
        C();
    elif (symbol != 'a'):
        end(False)
    else:
        set_next_symbol()
    return True
    
def B():
    sys.stdout.write('B')
    global i; global input
    symbol = input[i]
    
    if (symbol == 'c'):
        set_next_symbol()
        symbol = input[i]
 
        if (symbol != 'c'):
            end(False)
        set_next_symbol()
        
        S()
        symbol = input[i]
        
        if (symbol != 'b'):
            end(False)
        set_next_symbol()
        symbol = input[i]
        
        if (symbol != 'c'):
            end(False)
        set_next_symbol()

    return True       
    
def C():
    sys.stdout.write('C')
    A(); A()
    return True

def end(accepted):
    global i; global n  
    if (accepted and (not (i+1) < (n-1) )):
        print "\nDA"
    else:
        print "\nNE"
    exit(0)

input = sys.stdin.readline().strip() +'$'
i = 0; n = len(input)
symbol = input[i]
S()
end(True)