import sys
import os

from src.menu import Menu
from src.node import Node

def main():
    """Main function which gets information from the user concerning the story
    directory, and manages the highest level of navigation.
    """

    story_folder = ""
    if len(sys.argv) > 1:
        story_folder = sys.argv[1]
    while not os.path.isdir(story_folder):
        story_folder = input("Please input valid directory: ")
    if story_folder[-1] != "/":
        story_folder += "/"

    history = []
    dico = {}

    next_node = "menu"

    while next_node != "quit":
        print("*")

        if next_node == "back":
            history.pop()
            if not history:
                next_node = "menu"
            else:
                next_node = history.pop()

        if next_node == "menu":
            try:
                menu = Menu("%smenu.json" % story_folder)
            except:
                print("Error reading %smenu.json" % story_folder)
                return
            menu.display()
            choice = choose(3, [])

            if choice == 1:
                next_node = menu.starting_node
            elif choice == 2:
                try:
                    history, dico = load("%ssave.txt" % story_folder)
                    next_node = history.pop()
                except:
                    print("Failed to load an existing game.")
                    history, dico = [], {}
                    next_node = menu.starting_node
            elif choice == 3:
                return

        else:
            if next_node == "self":
                next_node = history.pop()

            history.append(next_node)

            try:
                node = Node("%s%s.json" % (story_folder, next_node))
            except:
                print("Error reading %s%s.json" % (story_folder, next_node))
                return

            try:
                node.process_conditions(dico)
            except:
                print("Error processing conditional parts. Check %s.json."
                       % next_node)

            node.display()

            while True:
                choice = choose(node.max_choice(), ["s", "q"])
                if choice == "q":
                    return
                if choice == "s":
                    try:
                        save("%ssave.txt" % story_folder, history, dico)
                    except:
                        print("Failed to save progress")
                else:
                    next_node = node.chosen(choice, dico)
                    break


def choose(num_max, text_options):
    """Asks the user to make a choice: either a number from 1 to num_max or a
    string in the list text_options.
    """
    while True:
        choice = input("Choice: ").lower()
        if choice in text_options:
            return choice
        try:
            num_choice = int(choice)
        except:
            num_choice = 0
        if num_choice > 0 and num_choice <= num_max:
            return num_choice

        print("Invalid choice. Options are numbers from 1 to %d, and %s."
              % (num_max, ", ".join(text_options)))


def load(filename):
    """Load a saved game.
    The 1st line of the file contains the history (space-separated node names).
    The other lines contains a variable and its value separated by a space.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    history = lines[0].split()
    dico = {val[0]: int(val[1]) for val in map(lambda x: x.split(), lines[1:])}

    return history, dico


def save(filename, history, dico):
    """Save a saved game.
    The 1st line of the file contains the history (space-separated node names).
    The other lines contains a variable and its value separated by a space.
    """
    file_text = " ".join(history) + "\n"
    file_text += "\n".join("%s %d" % (key, dico[key]) for key in dico)

    with open(filename, 'w') as f:
        f.write(file_text)

    print("Progress saved successfully")


main()