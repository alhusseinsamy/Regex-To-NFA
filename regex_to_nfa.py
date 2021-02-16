import argparse



class Transition:
    def __init__(self, start, transition, end):
        self.start = start
        self.transition = transition
        self.end = end



class StackElement:
    def __init__(self, q, expression, alphabet, q0, f, transitions):
        self.q = q
        self.expression = expression
        self.alphabet = alphabet
        self.q0 = q0
        self.f=f
        self.transitions = transitions



def toInfix(expression):
    result = ''

    for i in range(0, len(expression)-1):
        result+=expression[i]
        if (expression[i] != '(') and (expression[i] != '|'):
            if (expression[i+1] != ')') and (expression[i+1] != '+') and (expression[i+1] != '*') and (expression[i+1] != '?') and (expression[i+1] != '|'):
                result+='.'        
    result+=expression[len(expression)-1]        
    return result           



# print(toInfix('(a|b)*ab')) 


def toPostfix(infix):
    stack = []
    postfix = ''

    stack = []

    for c in infix:

        if (c != '(') and (c != ')') and (c != '+') and (c != '*') and (c != '?') and (c != '|') and (c != '.'):
            postfix += c
        else:
            if (c == '('):
                stack.append(c)
            elif (c == ')'):
                operator = stack.pop()
                while not (operator == '('):
                    postfix += operator
                    operator = stack.pop()              
            else:
                while (not len(stack) == 0) and (priority(c) <= priority(stack[len(stack)-1])):
                    postfix += stack.pop()
                stack.append(c)

    while (not len(stack) == 0):
        postfix += stack.pop()
    return postfix

def priority(operator):
    if(operator=="?" or operator=="+" or operator=="*"):
        return 3
    elif(operator=="."):
        return 2
    elif(operator=="|"):
        return 1
    elif(operator==")" or operator=="("):
        return 0

# print(toPostfix(toInfix('(a|b)*ab')))    

def build_nfa(postfix):
    stack = []
    counter = 0
    char_counter = 0

    for c in postfix:
        if (c != '(') and (c != ')') and (c != '+') and (c != '*') and (c != '?') and (c != '|') and (c != '.'):
            state1 = 'q' + str(counter)
            state2 = 'q' + str(counter+1)
            states = [state1, state2]
            counter+=2

            transition = Transition(start=state1, transition=c, end=state2)
            transitions = [transition]
            element = StackElement(q=states, expression=c, alphabet=[c], q0=state1, f=state2, transitions=transitions)
            stack.append(element)

        else:
            if (c == '|'):
                element2=stack.pop()
                element1=stack.pop()
                initial_state = 'q' + str(counter)
                final_state = 'q' + str(counter+1)
                counter+=2
                transition1 = Transition(start=initial_state, transition=' ', end=element1.q0)
                transition2 = Transition(start=initial_state, transition=' ', end=element2.q0)
                transition3 = Transition(start=element1.f, transition=' ', end=final_state)
                transition4 = Transition(start=element2.f, transition=' ', end=final_state)

                old_transitions = element1.transitions + element2.transitions
                new_transitions = [transition1, transition2, transition3, transition4]
                current_transitions = old_transitions + new_transitions

                old_states = element1.q + element2.q
                new_states = [initial_state, final_state]
                current_states = old_states + new_states

                current_expression = '(' + element1.expression + '|' + element2.expression + ')'
                current_alphabet = element1.alphabet + element2.alphabet

                element = StackElement(q=current_states, expression=current_expression, alphabet=current_alphabet, q0=initial_state, f=final_state, transitions=current_transitions)
                stack.append(element)

            if (c == '.'):
                element2=stack.pop()
                element1=stack.pop()

                new_transitions = []
                element2_transitions = []
                
                for transition in element2.transitions:
                    if transition.start == element2.q0:
                        transition1 = Transition(start=element1.f, transition=transition.transition, end=transition.end)
                        new_transitions.append(transition1)
                    else:
                        element2_transitions.append(transition)    


                old_transitions = element1.transitions + element2_transitions
                current_transitions = old_transitions + new_transitions

                old_states = element1.q + element2.q
                current_states = []

                for state in old_states:
                    if state != element2.q0:
                        current_states.append(state)

                current_expression = '(' + element1.expression + '.' + element2.expression + ')'
                current_alphabet = element1.alphabet + element2.alphabet        

                element = StackElement(q=current_states, expression=current_expression, alphabet=current_alphabet, q0=element1.q0, f=element2.f, transitions=current_transitions)
                stack.append(element)

            if (c == '*'):
                element = stack.pop()
                initial_state = 'q' + str(counter)
                final_state = 'q' + str(counter+1)
                counter+=2
                transition1 = Transition(start=initial_state, transition=' ', end=element.q0)
                transition2 = Transition(start=element.f, transition=' ', end=final_state)
                transition3 = Transition(start=initial_state, transition=' ', end=final_state)
                transition4 = Transition(start=element.f, transition=' ', end=element.q0)

                old_transitions = element.transitions 
                new_transitions = [transition1, transition2, transition3, transition4]
                current_transitions = old_transitions + new_transitions

                old_states = element.q 
                new_states = [initial_state, final_state]
                current_states = old_states + new_states

                current_expression = '(' + element.expression + ')*'
                current_alphabet = element.alphabet

                element = StackElement(q=current_states, expression=current_expression, alphabet=current_alphabet, q0=initial_state, f=final_state, transitions=current_transitions)
                stack.append(element)

            if (c == '+'):
                element = stack.pop()
                initial_state = 'q' + str(counter)
                final_state = 'q' + str(counter+1)
                counter+=2
                transition1 = Transition(start=initial_state, transition=' ', end=element.q0)
                transition2 = Transition(start=element.f, transition=' ', end=final_state)
                transition4 = Transition(start=element.f, transition=' ', end=element.q0)

                old_transitions = element.transitions 
                new_transitions = [transition1, transition2, transition4]
                current_transitions = old_transitions + new_transitions

                old_states = element.q 
                new_states = [initial_state, final_state]
                current_states = old_states + new_states

                current_expression = '(' + element.expression + ')+'
                current_alphabet = element.alphabet

                element = StackElement(q=current_states, expression=current_expression, alphabet=current_alphabet, q0=initial_state, f=final_state, transitions=current_transitions)
                stack.append(element)    


            if (c == '?'):
                element = stack.pop()
                initial_state = 'q' + str(counter)
                final_state = 'q' + str(counter+1)
                counter+=2
                transition1 = Transition(start=initial_state, transition=' ', end=element.q0)
                transition2 = Transition(start=element.f, transition=' ', end=final_state)
                transition3 = Transition(start=initial_state, transition=' ', end=final_state)

                old_transitions = element.transitions 
                new_transitions = [transition1, transition2, transition3]
                current_transitions = old_transitions + new_transitions

                old_states = element.q 
                new_states = [initial_state, final_state]
                current_states = old_states + new_states

                current_expression = '(' + element.expression + ')?'
                current_alphabet = element.alphabet

                element = StackElement(q=current_states, expression=current_expression, alphabet=current_alphabet, q0=initial_state, f=final_state, transitions=current_transitions)
                stack.append(element)






    last = stack.pop()
    return (last)

   
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)


    with open(args.file) as f:
        inp = f.readline()


        exp = toPostfix(toInfix(inp))
        print(exp)
        x = build_nfa(exp)
        print(x.expression)
        print(x.f)


        with open('task_2_result.txt', 'w') as f:
            for state in x.q: 
                f.write(state + ', ') 
            f.write('\n')

            for char in x.alphabet:
                f.write(char + ', ')    
            f.write('\n')
            
            f.write(x.q0) 
            f.write('\n')

            f.write(x.f) 
            f.write('\n') 

            for transition in x.transitions:
                f.write('('+transition.start+', '+transition.transition+', '+transition.end+'), ') 