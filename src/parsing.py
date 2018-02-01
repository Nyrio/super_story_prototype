def parse_text(text, dico):
    """Parse a text. See the full documentation for more information.
    """
    final_text = ""
    i = 0
    j = 0
    while j != -1:
        j = text.find("%", i)
        if j == -1:
            final_text += text[i:]
        else:
            final_text += text[i:j]
            i = text.find("%", j+1)
            expression = text[j+1:i]

            j = find_matching(text, i+2, "[", "]")
            option1 = text[i+2:j]

            if len(text) > j+1 and text[j+1] == "[":
                i = find_matching(text, j+2, "[", "]")
                option2 = text[j+2:i]
                if i != -1:
                    i = i+1
                    j = i
            else:
                option2 = ""
                if j != -1:
                    i = j+1
                    j = i

            good_option = (option1 if eval_expression(expression, dico)
                            else option2)
            final_text += parse_text(good_option, dico)

    return final_text


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
