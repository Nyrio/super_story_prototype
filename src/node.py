from .parsing import parse_text, eval_expression

class Node:
    """This class allows to read the data for a node, process conditions,
    display the node, provide what input can be accepted, and manage what
    happens depending on user's choice.
    """

    def __init__(self, filename):
        self.read_json(filename)


    def read_json(self, filename):
        """Open and read the given json file, processes the conditions and
        prerequisites, and save the data in attributes.
        The json is read directly as Python code, not through a lib.
        """

        with open(filename, 'r') as f:
            json_data = eval(f.read())

        self.base_text = json_data["text"]
        self.all_options = json_data["options"]


    def process_conditions(self, dico):
        """Parse the texts for conditional parts, and filter options with
        prerequisites.
        """

        self.text = parse_text(self.base_text, dico)
        self.options = []

        for option in self.all_options:
            if eval_expression(option["prerequisites"], dico):
                option["text"] = parse_text(option["text"], dico)
                self.options.append(option)


    def display(self):
        """Displays the node (text and options).
        """
        print(self.text)

        for i in range(len(self.options)):
            print("%d. %s" % (i, self.options[i]["text"]))

        print("S: save ; Q: quit")


    def max_choice(self):
        """Give the biggest number which can be input to choose an option.
        """
        return len(self.options)