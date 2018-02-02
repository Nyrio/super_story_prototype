Super Story Prototype (SuStoy Pro)
===

This project allows to quickly create a prototype for a story with choices and consequences. The story is described in a simple [json](https://en.wikipedia.org/wiki/JSON) format, and the progression can be saved, so that the testers don't have to play your story in one rush.

An example story prototype is given in the example/ folder and givers you an overview of the features. To try it, after completing the **installation** step below, you can launch the program and give it as a parameter the folder `example`, and just follow the instructions.

_Work in progress._

## Installation
To use this tool you need to [install Python 3](https://www.python.org/downloads/) (note: it is usually installed by default on Linux). Then:
- on **Windows**: double-click on `sustoy.py`, and enter the name of the directory where the `menu.json` file is located. You can either give an absolute path (like `C:\Users\yourname\tools\sustoy\project`), or a relative path (just `project` for example).
- on **Linux**: from a terminal opened in the same folder as `sustoy.py`, run `python3 sustoy.py` or `python3 sustoy.py path_to_project`. If you don't provide the path to the project as an arg, it will be asked. The path can be either absolute (like `/home/yourname/tools/sustoy/project`) or relative (just `project` for example).

## Write your story
The story is described with json files. You don't need any specific knowledge of json, you can just fill the provided templates.
A story is made of a menu and nodes. There is one file per node, and the node name is the name of the file without the extension. For example a file `node.json` in the folder `chapter1` is recognized by the name `chapter1/node`.

Let's take a look at the templates.

First, you need a file named `menu.json` at the source of the project directory:
```json
{
    "menu_text":     "Welcome to my story prototype!",
    "new_game_text": "New Game",
    "starting_node": "",
    "continue_text": "Continue",
    "quit_text":     "Quit"
}
```
Most of the parameters here are quite easy to understand: this decides how your menu will be displayed.
An important parameter here is `starting_node`. This decides which node will start your story when the tester creates a new game.

---

Let's now take a look at the structure of a node.
```json
{
    "text":    "",
    "options": [
        {
            "text":          "",
            "prerequisites": "",
            "target":        "",
            "consequences":  [
		{
                    "variable": "",
	            "value":    ""
		}
	    ]
        }
    ]
}
```
A node has a main description and one or more options for the player. To add more options, copy the structure (including braces) annd don't forget to separate with a comma. The `target` of an option is the node which this option leads to. It can be the name of a node, or `back`, `self`, `menu` or `quit`. `back` uses the history to find the node where the tester was before. It is possible to go up the history multiple times, but if this is used in the starting node, it takes back to the menu and the progression is not saved (we'll talk about saving later).

## Choices and consequences
To increase the possibilities of prototyping to advanced stories with choices and consequences, the tool is very modular.
The tool has a simple system of integer variables which can be used to change what text is displayed, or enable or disable options depending on their values.

### Variables and expressions
Variable names can only contain lower-case letters and the underscore character.
The variables are integers but ultimately, the conditions are binary: 0 corresponds to `false` and all other values correspond to `true`.

In expressions, the following operators can be used:

Symbol | Operator | Precedence
------ | -------- | --------
`*` | Multiply | Highest
`/` | Divide | Highest
`+` | Add | Medium
`-` | Substract | Medium
`=` | Equals | Low
`>` | Greater than | Low
`<` | Smaller than | Low
`&` | Logical and | Lowest
`\|` | Logical or | Lowest
`!` | Logical not | Lowest

Be careful when using logical operators with integers: for example `2&3` gives 3, whereas `3&2` gives 2.
Be also careful with the priority of logical operators: they come after everything, so for example `!0+1` gives `0`, because `0+1` gives 1, then `!1` gives 0.

To make expressions clear, it is a good practise to use parentheses. Moreover, you can use spaces in expression to make them more readable.

Expressions use variables or integers. A variable which has not been assigned yet **is created with a value of 0**.

### Giving values to variables
You can assign values to variables when the user is making a choice: just add entries in `consequences` for this specific option. If you want no affectation for an option, let an empty list (nothing between brackets). Don't let an entry with empty fields like in the template.

An entry has two fields: `variable` is the variable which will be given a value, and `value` must be a valid expression.

### Defining prerequisites for options
Every option has a `prerequisites` field. This will display the option only if the expression is true (value different than 0). By default, an empty expression has the value true, so if you want to show an option in any case, just let this field empty.

### Modifying the text depending on the variables
This is the most powerful feature of the tool: you can customize the description of a node, or the text of options, with expressions. The syntax is the following:
```
%condition%[text if true][text if false]
```
The text if the condition is false is optional. There must be no space between the percent symbol and bracket, and between closing bracket of the text if true and opening bracket of the text if false. Moreover, the percent symbol can't be used in the text because it will be interpreted as a condition. Brackets can be used elsewhere though.

This feature allow nesting. Just be careful to always close your brackets, otherwise you will have errors or the display will not be as you expect it to be.

## The save system
