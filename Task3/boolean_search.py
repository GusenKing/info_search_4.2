import re


def tokenize_query(query):
    query = query.upper()
    return re.findall(r'\(|\)|AND|OR|NOT|\w+', query)


def to_postfix(tokens):
    precedence = {"NOT": 3, "AND": 2, "OR": 1}
    output = []
    stack = []

    for token in tokens:
        if token not in precedence and token not in ("(", ")"):
            output.append(token)

        elif token in precedence:
            while (stack and stack[-1] != "(" and
                   precedence.get(stack[-1], 0) >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            while stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return output


def evaluate_postfix(postfix, index, all_docs):
    stack = []

    for token in postfix:
        if token == "AND":
            b = stack.pop()
            a = stack.pop()
            stack.append(a & b)

        elif token == "OR":
            b = stack.pop()
            a = stack.pop()
            stack.append(a | b)

        elif token == "NOT":
            a = stack.pop()
            stack.append(all_docs - a)

        else:
            stack.append(index.get(token.lower(), set()))

    return stack.pop()


def boolean_search(query, index):
    tokens = tokenize_query(query)
    postfix = to_postfix(tokens)

    all_docs = set()
    for docs in index.values():
        all_docs |= docs

    return evaluate_postfix(postfix, index, all_docs)
