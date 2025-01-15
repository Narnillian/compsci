def get_one():
    if len(stack) == 0:
        return "    ERR: Not enough stack..."
    return stack.pop()

def get_two():
    if len(stack) < 2:
        return "    ERR: Not enough stack...", 0
    return stack.pop(), stack.pop()


stack = []
print("Reverse Polish Notation Calculator")
print("+:  Add       (a + b)")
print("-:  Subtract  (a - b)")
print("*:  Multiply  (a * b)")
print("/:  Divide    (a / b)")
print("**: Exponent  (a to the b-th power)")
print("//: Root      (b-th root of a)")
print("!:  Factorial (a!)")
print("#:  Fibonacci ((a + b,...) c times)")
print("':  Clear Stack")
print("@:  Exit Program")
print("\n")
while True:
    user_input = input()
    valid = True
    match user_input:
        case "@": #end program
            break
        case "+": #add
            a, b = get_two()
            if type(a) == str: print(a)
            else: stack.append(a+b)
        case "*": #multiply
            a, b = get_two()
            if type(a) == str: print(a)
            else: stack.append(a*b)
        case "-": #subtract
            a, b = get_two()
            if type(a) == str: print(a)
            else: stack.append(b-a)
        case "/": #divide
            a, b = get_two()
            if type(a) == str: print(a)
            else:
                if a == 0:
                    print("    ERR: Divide by zero...")
                    stack.append(b)
                    stack.append(a)
                    valid = False
                else: stack.append(b/a)
        case "**": #exponent
            a, b = get_two()
            if type(a) == str: print(a)
            else: stack.append(b**a)
        case "//": #root
            a, b = get_two()
            if type(a) == str: print(a)
            elif b < 0:
                print("    ERR: Negative root...")
                stack.append(a)
                stack.append(b)
                valid = False
            else:
                a = int(a)
                b = int(b)
                stack.append(b**(1/a))
        case "!": #factorial
                a = get_one()
                if type(a) == str: print(a)
                elif a % 1 != 0:
                    print("    ERR: Not an integer...")
                    valid = False
                    #`a` gets pushed back to the stack after `else`
                else:
                    i = a-1
                    while (i):
                        a *= i
                        i -= 1
                stack.append(a)
        case "#": #fibonacci(a,b,limit)
            if len(stack) < 3:
                """
                even though this looks unlike the rest of the program, this seemed to be
                                        the best way to handle this
                !!! because we check this, it is unnecessary to check stack length later
                                        i.e. the rest of fib won't be executed unless
                                        there is enough stack
                """
                print("    ERR: Not enough stack...")
                valid = False
            else:
                iterations = int(get_one())
                for i in range(iterations):
                    a, b = get_two()
                    stack.append(a)
                    stack.append(a+b)
                a, b = get_two()
                stack.append(b)
        case "'": #clear stack
            stack = []
        case _: #default
                try:
                    stack.append(float(user_input))
                except:
                    print("    ERR: Input invalid...")
                    valid = False
    if len(stack) and valid:
        print("    " + str(stack[-1]))
    print(stack, end = "\n\n") #add an extra newline to make it look nicer