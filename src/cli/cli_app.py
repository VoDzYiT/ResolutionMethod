from logic import *

import re

# a and a
def tokenize(expr):
    token_spec = r'\w+|->|[()!&|∨¬~∧]'
    return re.findall(token_spec, expr)


def parse(tokens):
    def parse_expression(index):
        # Since implication has the lowest weight we begin with it (in tree it would be last)
        return parse_implication(index)

    def parse_implication(index):
        left, index = parse_or(index)
        while index < len(tokens) and tokens[index] == '->':
            index += 1
            right, index = parse_implication(index)
            left = Implication(left, right)
        return left, index

    def parse_or(index):
        left, index = parse_and(index)
        while index < len(tokens) and tokens[index] == '∨':
            index += 1
            right, index = parse_and(index)
            left = Or(left, right)
        return left, index

    def parse_and(index):
        left, index = parse_not(index)
        while index < len(tokens) and (tokens[index] == '&' or tokens[index] == '∧'):
            index += 1
            right, index = parse_not(index)
            left = And(left, right)
        return left, index

    def parse_not(index):
        if index < len(tokens) and (tokens[index] == '~' or tokens[index] == '!' or tokens[index] == '¬'):
            index += 1
            operand, index = parse_not(index)
            return Not(operand), index
        else:
            return parse_atom(index)

    def parse_atom(index):
        token = tokens[index]
        if token == '(':
            index += 1
            expr, index = parse_expression(index)
            if tokens[index] != ')':
                raise SyntaxError("Expected ')'")
            return expr, index + 1
        else:
            return Literal(token), index + 1

    tree, final_index = parse_expression(0)
    if final_index != len(tokens):
        raise SyntaxError("Unexpected tokens at end")
    return tree


def run_cli_app():
    print("=== Console Application: Resolutions method ===")
    print("------------------------------------------")
    print("Input format:")
    print("  Sentence: each literal separated by operator")
    print("             you can also use parentheses")
    print("                  Example: 'a -> b', 'apple ∧ plum -> fruits' ")
    print("  Prove: just a literal, that you want to prove")
    print("                  Example: 'a', 'apple'")
    print("  Available operators:")
    print("                       Implication: '->'")
    print("                       Disjunction: '∨'")
    print("                       Conjunction: '&' or '∧'")
    print("                       Negation: '~' or '!' or '¬'")
    print("To exit just press 'Ctrl' + 'C'")
    print("------------------------------------------")

    while True:
        sentence = input("\nEnter the expression: ").strip()
        if sentence:
            knowledge = input("\nEnter the what you want to prove: ").strip()

            try:
                sentence_parsed = parse(tokenize(sentence))

                if knowledge:
                    knowledge_parsed = parse(tokenize(knowledge))
                    full_sentence = And(sentence_parsed, Not(knowledge_parsed))
                else:
                    full_sentence = sentence_parsed


                result = Resolution(full_sentence)
                resolution_result = result.resolve()

                print(f"Your expression: {to_cnf(full_sentence)}")
                print(f"Resolution method result: {resolution_result}")

            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please check your input expression and knowledge.")
        else:
            print("The expression cannot be empty. Please enter a value")



if __name__ == "__main__":
    run_cli_app()
