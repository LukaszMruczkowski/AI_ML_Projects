import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Loop through variables in domains dictionary
        for variable, words in self.domains.items():

            # Loop through values (words) in every variable
            for word in words.copy():

                # Check if word in variable domain is equal to length of variable
                if len(word) != variable.length:

                    # If not remove word from domain
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Check where overlap occurs
        overlap = self.crossword.overlaps[x, y]

        # Domains of variable x and y
        domain_x = self.domains[x]
        domain_y = self.domains[y]
        
        # Check if revised 
        revised = 0

        # Loop through words of domain x
        for word_x in domain_x.copy():

            # Number of words in domain y
            word_number_y = len(domain_y)

            # Loop through words of domain y
            for word_y in domain_y:

                # If expected overlap is not satisfied by these pair of words, mark it as impossible value
                if word_x[overlap[0]] != word_y[overlap[1]]:
                    word_number_y -= 1

                # If there is no possible corresponding value in y domain for word from x domain remove that word from x domain
                if word_number_y == 0:
                    self.domains[x].remove(word_x)
                    revised = 1
        if revised == 0:
            return False
        else:
            return True
                    



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # Create initial list of all arcs in problem
            arcs = []

            # Loop through all variables to add pairs of them to an arcs list
            for var_a in self.crossword.variables:
                for var_b in self.crossword.neighbors(var_a):
                    arcs.append((var_a, var_b))
        
        while len(arcs) != 0:
            arc = arcs.pop()

            # Try to force arc consistency
            if self.revise(arc[0], arc[1]):

                # If domain of revised variable is empty then there is no solution
                if len(self.domains[arc[0]]) == 0:
                    return False
                
                # Loop through all neighbors of revised variable besides that one which was already revised
                for neighbor in self.crossword.neighbors(arc[0]):

                    # Variable that revised variable was already revised with
                    if neighbor == arc[1]:
                        continue

                    # Append new arc
                    arcs.append((neighbor, arc[0]))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if every key has a value
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if all values are distinct
        if len(assignment) != len(set(assignment.values())):
            return False
        
        # Check if values have correct length
        for variable, word in assignment.items():
            if variable.length != len(word):
                return False

        # Check if chosen words have conflicting characters with it's neighbors
        for variable in assignment:
            # Set of all variable neighbors
            neighbors = self.crossword.neighbors(variable)
            
            # Value that is assigned to a variable in assignment
            variable_value = assignment.get(variable)

            # Loop through all neighbors to check if everyone's overlaps are correct
            for neighbor in neighbors:

                # Check if neighbor is assigned already if not check another one
                if neighbor not in assignment:
                    continue

                # Overlap between a variable and it's neighbor
                overlap = self.crossword.overlaps[variable, neighbor]

                # Value that is assigned to neighbor in assignment
                neighbor_value = assignment.get(neighbor)

                # If overlap is not correct return False
                if variable_value[overlap[0]] != neighbor_value[overlap[1]]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Dictionary of words in the domain of var and it's number of possible neighbors
        domain_values = dict()

        # Set of all neighbors of var
        neighbors = self.crossword.neighbors(var)

        # Loop through words in var domain and assign every word to possible future choices of it's neighbors
        for word_var in self.domains[var]:

            # Number of possible neighbors values
            possible_neighbors = 0

            for neighbor in neighbors:

                overlap = self.crossword.overlaps[var, neighbor]

                for word_neighbor in self.domains[neighbor]:

                    if word_var == word_neighbor:
                        continue

                    # If value from var has 
                    if word_var[overlap[0]] == word_neighbor[overlap[1]]:
                        possible_neighbors += 1

            # Add value var to dictionary and assign it's possible neighbor words count
            domain_values[word_var] = possible_neighbors
        
        # Sort dictionary by value number descending
        sorted_domain_values = dict(sorted(domain_values.items(), key=lambda item: item[1], reverse=True))

        # Turn it into a list
        sorted_domain_values_list = list(sorted_domain_values.keys())

        return sorted_domain_values_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Set of unasigned variables
        unasigned_variables = self.crossword.variables.symmetric_difference(assignment)

        # Assume that random variable has fewest values in it's domain
        min_domain_variable = []
        min_domain_variable.append(unasigned_variables.pop())

        # Loop through all unasigned variables
        for variable in unasigned_variables:

            # Check if some different variable has fewer words in the domain if so append a variable
            if len(self.domains[variable]) < len(self.domains[min_domain_variable[0]]):
                min_domain_variable.clear()
                min_domain_variable.append(variable)

            # Else if variable has same number of words in domain append a variable
            elif len(self.domains[variable]) == len(self.domains[min_domain_variable[0]]):
                min_domain_variable.append(variable)
        
        # If there is a tie in fewest words in domain
        if len(min_domain_variable) > 1:

            # Assume that random variable has highest degree
            max_degree_variable = []
            max_degree_variable.append(min_domain_variable.pop())

            # Loop through all selected variables
            for variable in min_domain_variable:

                # Check if some differrent variable has higher degree if so append a variable
                if len(self.crossword.neighbors(variable)) > len(self.crossword.neighbors(max_degree_variable[0])):
                    max_degree_variable.clear()
                    max_degree_variable.append(variable)

                # Else if variable has equal degree append a variable
                elif len(self.crossword.neighbors(variable)) == len(self.crossword.neighbors(max_degree_variable[0])):
                    max_degree_variable.append(variable)

            # Return any of variable with highest degree
            return max_degree_variable[0]
        
        # Else return one-element list
        else:
            return min_domain_variable[0]

            
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Implementation of backtrack search
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):

            # Try to sign a value to a variable
            assignment[var] = value

            # Check if it is consistent
            if self.consistent(assignment):

                result = self.backtrack(assignment)

                if result is not None:               
                    return result
                
            del assignment[var]

        return None

        


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
