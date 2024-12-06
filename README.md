# non-recursive-predictive-parser-LL1
Implementing a non-recursive predictive parser using the LL(1) method

▎The given code is a Python script that implements a parser generator for LL(1) grammars. It performs the following tasks:
1. Imports the `PrettyTable` module, which is used to create formatted tables.
2. Defines several global variables and data structures to store grammar rules, non-terminals, terminals, FIRST sets, FOLLOW sets, and productions.
3. Defines a function `operator` that checks if a given string is an operator.
4. Defines a function `get_grammar` that prompts the user to enter the grammar rules and builds the necessary data structures.
5. Defines a function `LeftRecursion` that checks if a non-terminal has left recursion doesn't have exit condition.
6. Defines a function `first` that calculates the FIRST set for a given string (terminal or non-terminal).
7. Defines a function `follow` that calculates the FOLLOW set for a given non-terminal.
8. Defines a function `fifo_table` that calculates and displays the FIRST and FOLLOW sets for each non-terminal in a formatted table.
9. Defines a function `generate_parse_table` that constructs the LL(1) parsing table based on the FIRST and FOLLOW sets.
10. Defines a function `parse` that takes an input string and the parsing table, and performs LL(1) parsing by matching the input against the parsing table rules.
11. Calls the `get_grammar` function to get the grammar rules from the user.
12. Checks if any non-terminal doesn't have exit condition and raises an error if found.
13. Prompts the user to enter the start symbol of the grammar.
14. Calls the `fifo_table` function to calculate and display the FIRST and FOLLOW sets.
15. Calls the `generate_parse_table` function to construct the LL(1) parsing table.
16. Prompts the user to enter an input string to be parsed.
17. Calls the `parse` function to perform LL(1) parsing on the input string using the parsing table.

Overall, the code allows the user to define a context-free grammar, calculates the FIRST and FOLLOW sets, constructs an LL(1) parsing table, and performs LL(1) parsing on input strings according to the grammar rules.

▎License

This project is licensed under the MIT License. See the LICENSE file for more details.

▎Acknowledgments

This implementation is based on the mathematical principles of Lagrange interpolation. For more information on this topic, you can refer to any standard numerical analysis textbook or online resources.

Feel free to contribute to this project by submitting issues or pull requests!
