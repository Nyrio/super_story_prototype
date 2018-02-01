def eval_expression(expression, dico):
    """Evaluates an expression containing integer variables and the
    following operators: +, -, *, /, & (and), | (or), ! (not), <, >,
    giving to the variables the values found in dico, or 0 otherwise.
    """
    if not expression:
        return 1

    expression = expression.lower()

    expr_string = ""
    word = ""
    variables = []
    letters = "abcdefghijklmnopqrstuvwxyz_"

    for chara in expression + " ":
        if chara in letters:
            word += chara
        else:
            if word:
                variables.append(word)
                expr_string += "%d"
                word = ""
            expr_string += chara

    for variable in variables:
        if variable not in dico:
            dico[variable] = 0

    replacements = {"=": "==", "&": " and ", "|": " or ", "!": "not "}
    for key in replacements:
        expr_string = expr_string.replace(key, replacements[key])

    expression = expr_string % tuple(map(lambda x: dico[x], variables))
    return eval(expression)


def find_matching(text, pos, char1, char2):
    """Finds the matching closing character char2 corresponding to the opening
    character char1, starting from position pos.
    """
    
    depth = 1
    for i in range(pos, len(text)):
        if text[i] == char1:
            depth += 1
        elif text[i] == char2:
            depth -= 1

        if depth == 0:
            return i

    return -1
