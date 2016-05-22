import sys

def set_next_symbol():
    global i
    global n
    
    if ( i+1 < n ):
        i += 1
        return True
    else:
        return False

def S():
    sys.stdout.write('S')
    global i
    global input
    symbol = input[i]
    
    if (symbol == 'a'):
        if (not set_next_symbol()):
            return False
        if (A() is False):
            return False
        if (B() is False):
            return False
        return True
        
    elif (symbol == 'b'):
        if (not set_next_symbol()):
            return False
        if (B() is False):
            return False
        if (A() is False):
            return False
        return True
        
    else:
        return False
        
def A():
    sys.stdout.write('A')
    global i
    global input
    symbol = input[i]
    
    if (symbol == 'b'):
        if (not set_next_symbol()):
            return False
        if (C() is False):
            return False
    
    elif (symbol != 'a'):
        return False
    
    else:
        if (not set_next_symbol()):
            return False
    return True
    
def B():
    sys.stdout.write('B')
    global i
    global input
    symbol = input[i]
    
    if (symbol == 'c'):
        if (not set_next_symbol()):
            return False
        symbol = input[i]
 
        if (symbol != 'c'):
            return False
        
        if (not set_next_symbol()):
            return False
        
        if ( S() is False):
            return False
        symbol = input[i]
        
        if (symbol != 'b'):
            return False
        
        if (not set_next_symbol()):
            return False
        symbol = input[i]
        
        if (symbol != 'c'):
            return False
        if (not set_next_symbol()):
            return False
    return True       
    
def C() :
    sys.stdout.write('C')
    
    if (A() is False):
        return False
    if (A() is False):
        return False
    return True

input = sys.stdin.readline()
input = input.strip() +'$'

i = 0
n = len(input)
symbol = input[i]
accepted = S()

print ""   
if (accepted and (not (i+1) < (n-1) )):
    print "DA"
else:
    print "NE"