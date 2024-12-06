from prettytable import PrettyTable

productions = {}
non_terminals = []
terminals = []
copy_of_rule = []
pro_rule = []

FIRST = dict()
FOLLOW = dict()

def operator(string):
    operators = ["+", "-", "=", "(", ")", "*", "%", "/", "<", ">", "^"]
    if string in operators:
        return True
    else:
        return False
    
def get_grammar():
    # get number of nonterminals
    while True:
        try:
            num_of_nonterminals = int(input("Enter num of non_terminals: "))
        except ValueError:
            print("Invalid input. Please enter an integer.😏")
        else:
            break
    print("Enter the productions: ")
    for _ in range(num_of_nonterminals):
        rule = input()
        copy_of_rule.append(rule)
        main_firstpart, second_part = rule.split("->")
        main_firstpart = main_firstpart.rstrip()
        second_part = second_part.rstrip()
        non_terminals.append(main_firstpart)

        # terminal list and invalid input
        for i in second_part:
            if i not in terminals:
                if (i.isalpha() and i.islower()) or operator(i):
                    terminals.append(i)
                elif (i.isalpha() and i.isupper()) or i == "|" or i == "Ɛ":
                    None
                else:
                    #! not upper not lower not operator
                    raise ValueError(f"❌ {i} is Invalid input.")
           
    #! if left side not upper             
    for i in non_terminals:
        if not i.isupper():
            raise ValueError(f"❌ {i} is Invalid nonterminal. {i} should be alphabetical and uppercase.")
 
    for nT in non_terminals:
        productions[nT] = []

    # productions {"E": [t, a]}   copy_of_rule ["E->t|a"]  pro_rule ["E->t", "E->a"]
    for rule in copy_of_rule:
        rule = rule.rstrip()
        non_terminal = rule.split("->")
        rules = non_terminal[1].split("|")
        for rule in rules:
            productions[non_terminal[0]].append(rule)
            d = (str(non_terminal[0]) + "->" + rule)
            pro_rule.append(d)
            
    return productions

def LeftRecursion(NT):
    rules = productions[NT]
    for rule in rules:
        if NT == rule[0] and len(rules) < 2:
            return True
            
def first(string, visited=None):
    # Example 7
    if visited is None:
        visited = set()
    if string in visited:
        return set()
    visited.add(string)
    d = len(string) - 1
    visited = visited - {string[d]}
    
    main_first = set()
    if string in non_terminals:
        rule = productions[string]
        for rule_ in rule:
            first2 = first(rule_, visited)
            main_first = main_first.union(first2)

    elif string in terminals:
        main_first = {string}

    elif string == "" or string == "Ɛ":
        main_first = {"Ɛ"}

    else:
        first2 = first(string[0], visited)
        if "Ɛ" in first2:
            i = 1
            while "Ɛ" in first2:

                main_first = main_first.union(first2) - {"Ɛ"}

                if string[i:] in terminals:
                    main_first = main_first.union({string[i:]})
                    break
                
                elif string[i:] == "":
                    main_first = main_first.union({"Ɛ"})
                    break
                
                first2 = first(string[i:], visited)
                main_first = main_first.union(first2) - {"Ɛ"}
                i += 1
                
        else:
            main_first = main_first.union(first2)

    return  main_first
    
def follow(string, visited=None):
    # Example 3
    if visited is None:
        visited = set()
    if string in visited:
        return set()
    visited.add(string)
    main_follow = set()

    #? (1) {$} ∈ Fo (S) , S: start symbol
    if string == start_symbol:
        main_follow = main_follow.union({"$"})
        
    for non_t, rule in productions.items():  #non_t: before ->    rule: after ->
        for ru_le in rule:
            for i, char in enumerate(ru_le):
                if char == string:
                    # after char
                    following_string = ru_le[i + 1:]
                    
                    #? (3.1)
                    if following_string == "":
                        # E -> + T E
                        if non_t == string:
                            continue
                        #? (3.1) A -> a B --->>> Fo(A) ⊂ Fo(B)
                        else:
                            main_follow = main_follow.union(follow(non_t, visited))
                    
                    # ?(2) (3.2)
                    else:
                        follow2 = first(following_string)
                        #? (3.2) A -> a B c , Ɛ ∈ Fi(c) --->>> Fo(A) ⊂ Fo(B)
                        if "Ɛ" in follow2:
                            main_follow = main_follow.union(follow2 - {"Ɛ"})
                            main_follow = main_follow.union(follow(non_t, visited))
                        #? (2) A -> a B c --->>> Fi(c) ⊂ Fo(B)
                        else:
                            main_follow = main_follow.union(follow2)
    
    return main_follow

def fifo_table():
    # first
    for non_terminal in non_terminals:
        FIRST[non_terminal] = set() 
    for non_terminal in non_terminals:
        FIRST[non_terminal] = first(non_terminal)

    # follow    
    for non_terminal in non_terminals:
        FOLLOW[non_terminal] = set()
    for non_terminal in non_terminals:
        FOLLOW[non_terminal] = follow(non_terminal)
        
    # create table
    table = PrettyTable()
    table.field_names = ["Non Terminal", "First Set", "Follow Set"]
    # Add rows to the table
    for nt in non_terminals:
        first_set = " | ".join(sorted(FIRST[nt]))
        follow_set = " | ".join(sorted(FOLLOW[nt]))
        table.add_row([nt, first_set, follow_set])

    return table

def generate_parse_table():
    terminals.append("$")
    parse_table = [[""]*len(terminals) for _ in range(len(non_terminals))]

    # put firsts    
    for non_terminal in non_terminals:
        rule_ = productions[non_terminal]
        for terminal in terminals:
            if terminal in first(non_terminal):
                for i in range(len(pro_rule)): # pro_rule ["E->t", "E->a"]
                    if pro_rule[i][0] == non_terminal and (pro_rule[i][3:] in rule_) and terminal in first(pro_rule[i][3:]):
                        rule = (non_terminal + " -> " + pro_rule[i][3:])
                        # FIFI and FOFO 
                        for g in range(len(rule_)):
                            for d in range(len(rule_)):
                                if d != g :
                                    if any(element in first(rule_[d]) for element in first(rule_[g])) and terminal in first(rule_[d]):
                                        rule = (non_terminal + " -> " + rule_[d] + " | " + non_terminal + " -> " + rule_[g])
            else:
                rule = ""
            parse_table[non_terminals.index(non_terminal)][terminals.index(terminal)] = rule
            
    # put follows and synch        
    for non_terminal in non_terminals:
        for terminal in terminals:  
            if("Ɛ" in first(non_terminal) and terminal in follow(non_terminal)):
                if parse_table[non_terminals.index(non_terminal)][terminals.index(terminal)] == "":
                    rule = non_terminal + " -> Ɛ"
                else:
                    d = str(non_terminal + " -> Ɛ")
                    rule = str(parse_table[non_terminals.index(non_terminal)][terminals.index(terminal)]) + " | " + d   
                    
            elif(terminal in follow(non_terminal) and (terminal not in first(non_terminal))):
                    rule = "Sync"
                
            else:
                # if parse_table[non_terminals.index(non_terminal)][terminals.index(terminal)] == "":
                #     rule = ""
                # else:
                rule = parse_table[non_terminals.index(non_terminal)][terminals.index(terminal)]
            parse_table[non_terminals.index(non_terminal)][terminals.index(terminal)] = rule
    
    # create table
    table = PrettyTable()
    table.field_names = [""] + terminals
    for i, row in enumerate(parse_table):
        table.add_row([non_terminals[i]] + row)
         
    print("\nParsing Table:")
    print(table)
    
    # not LL(1)
    for non_terminal in non_terminals:
        for terminal in terminals:  
            if "|" in parse_table[non_terminals.index(non_terminal)][terminals.index(terminal)]:
                raise ValueError(f"🤡 Grammar is not LL(1)")
          
    return parse_table
    
def parse(input, parse_table):
    stack = ["$"]
    stack.insert(0, start_symbol)
    # create table
    table = PrettyTable()
    table.field_names = ["Matched", "Stack", "Input", "Action"]
    
    # first row
    action = ""
    matched = ""
    stack_ = ""
    for i in stack:
        stack_ = str(stack_ + i)
    table.add_row([matched] + [stack_] + [input] +[action])

    while True:
        action = ""
        # finished input
        if(stack[0] == input[0] and stack[0] == "$"):
            accept = 1
            break
        
        elif(stack[0] == input[0]):
            # match input[0]
            if(matched == ""):
                matched = input[0]
            # match input[1:]
            else:    
                matched = matched + input[0]
            action = "Matched " + input[0]

            input = input[1:]
            stack.pop(0)
        
        # non_terminal goes to non_terminal to match input[index]
        else:
            if input[0] in terminals and stack[0] in non_terminals and parse_table[non_terminals.index(stack[0])][terminals.index(input[0])] != "Sync" and parse_table[non_terminals.index(stack[0])][terminals.index(input[0])] != "":
                action = parse_table[non_terminals.index(stack[0])][terminals.index(input[0])]
                stack.pop(0)
                i = 0
                # nonterminal goes to its rule
                for item in action[5:]: # E -> Se  action[5] = S
                    if(item != "Ɛ"):
                        stack.insert(i, item) # i = index
                    i += 1
                action = "output " + action
            else:
                #! not match
                raise ValueError(f"🤡 Error: Doesn't Match.")
            
        stack_ = ""
        for i in stack:
            stack_ = str(stack_ + i)
            
        table.add_row([matched] + [stack_] + [input] +[action])
        
    table.align["Matched"] = "l"    
    table.align["Stack"] = "r"    
    table.align["Input"] = "r"    
    table.align["Action"] = "l"  
    print("\nParsing Expression:")  
    print(table)
    # Accept input
    if accept == 1:
        print("\n✅ Input is Accepted.")        

get_grammar()

#! NT doesn't have exit condition
for key in productions.keys():
    if LeftRecursion(key):
        raise ValueError(f"❌ {key} doesn't have exit condition")
    
start_symbol = input("Enter the start symbol: ")
# start_symbol = non_terminals[0]
#! start symbol not in non_terminals
if start_symbol not in non_terminals:
    raise ValueError(f"❌ {start_symbol} is not in nonterminal.") 

print("\nFist/Follow:")
print(fifo_table())

parse_table = generate_parse_table()
        
input = input("\nEnter input: ") + "$"
input = input.rstrip()

parse(input, parse_table)