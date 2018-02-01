class Menu:
    """This class allows to read the data for the menu and display the menu.
    The results are processed by the caller because this one may need to load
    saved data.
    """

    def __init__(self, filename):
        self.read_json(filename)


    def read_json(self, filename):
        """Open and read the given json file, and save the data in attributes.
        The json is read directly as Python code, not through a lib.
        """

        with open(filename, 'r') as f:
            json_data = eval(f.read())

        self.menu_text = json_data["menu_text"]
        self.new_game_text = json_data["new_game_text"]
        self.starting_node = json_data["starting_node"]
        self.continue_text = json_data["continue_text"]
        self.quit_text = json_data["quit_text"]


    def display(self):
        """Displays the menu to the user.
        """

        print("%s\n1. %s\n2. %s\n3. %s"
              % (self.menu_text, self.new_game_text, self.continue_text,
                 self.quit_text))