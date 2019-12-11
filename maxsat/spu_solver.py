
import argparse
import wcnf
import msat_runner
import graph


class SPU_Solver(object):
    """
    Software Package Upgrade Solver Class
    """


    def __init__(self, solver_path=None, problem_path=None, file_path=None):
        """
        constructor
        """
        #print("Constructor")

        self.formula = wcnf.WCNFFormula()
        self.solver = msat_runner.MaxSATRunner(solver_path)
        self.custom_graph = graph.Graph()

        #self.problem = self.parser(problem_path)
        self.parser(problem_path)

        if file_path is not None:
            self.visualize(file_path)

        self.build(file_path)


    def parser(self, problem_path):
        """
        parse the file of the problem
        """
        print("Parser")

        if problem_path == None:
            raise ValueError("No problem to solve !")

        if problem_path.split(".")[-1] != 'spu':
            raise ValueError("Problem file with wrong extension. Should be '.spu'")

        with open(problem_path, 'r') as file:

            total_packages = 0
            packages = []
            #dependencies = []
            #conflicts = []

            for line in file:

                items = line.split("\n")[0].split(" ")

                if items[0] == 'p' and items[1] == 'spu':
                    total_packages = int(items[2])

                # if it's a package
                elif items[0] == 'n':
                    packages.append(items[1])
                    self.custom_graph.nodes.append(items[1])

                # if it's a dependency
                elif items[0] == 'd':

                    # check package exist
                    if self.check_packages(packages, items[1:]):

                        for dependency in items[2:]:

                            # first option
                            #dependencies.append([items[1], dependency])

                            # second option
                            #dependencies.append([items[1], "-"+dependency])

                            # add edges to graph
                            self.custom_graph.edges.append([items[1], dependency])

                # if it's a conflict
                elif items[0] == 'c':

                    # check package exist
                    if self.check_packages(packages, items[1:]):
                        # add edge to graph
                        self.custom_graph.edges.append(items[1:])

                else:
                    print("Line not considered")

            if total_packages != len(package):
                raise ValueError("Error reading packages.")

            #print("Total packages: " + str(total_packages))
            #print("Packages:")
            #print(packages)
            #print("Dependencies:")
            #print(dependencies)
            #print("Conflicts:")
            #print(conflicts)

        file.close()


    def build(self, file_path):
        """
        build the wcnf formula of the problem
        """
        print("Build")

        nodes = { node : self.formula.new_var() for node in self.custom_graph.nodes }
        print(nodes)

        # soft
        for node in nodes:
            self.formula.add_clause([nodes[node]], weight=1)

        # revise: d pkg1 pkg2 pkg3 -> pkg1 and pkg2 or pkg1 and pkg3
        # revise: c pkg1 pkg4 -> pkg1 v pkg2

        # hard
        for n1, n2 in self.custom_graph.edges:

            # option 1
            #self.formula.add_clause([nodes[n1], nodes[n2]], weight=wcnf.TOP_WEIGHT)

            # option 2
            if n2.startswith('-'):
                self.formula.add_clause([nodes[n1], -nodes[n2[1:]]], weight=wcnf.TOP_WEIGHT)
            else:
                self.formula.add_clause([nodes[n1], nodes[n2]], weight=wcnf.TOP_WEIGHT)

        self.formula.write_dimacs_file('dimacs/' + file_path)
        #formula_13 = self.formula.to_13wpm()


    def visualize(self, file_path):
        """
        show the graph pdf
        """
        #print("Visualize")

        self.custom_graph.visualize("pdfs/" + file_path)

    def solve(self):
        """
        solve the problem
        """
        print("Solve")

        # solve the problem
        opt, model = self.solver.solve(self.formula)
        print(opt)
        print(model)

        # interpret the solution
        return [n for n in model if n > 0]


    def check_packages(self, packages, items):
        """
        packages comprobation
        """

        for pkg in items:
            if pkg not in packages:
                raise ValueError("Dependency or conflict with no exist package.")

        return True


# Main

def main(argv=None):
    """
    main program
    """

    args = parse_command_line_arguments(argv)
    #print(args.solver)
    #print(args.problem)
    #print(args.file)

    spu_solver = SPU_Solver(args.solver, args.problem, args.file)
    spu_solver.solve()


# Utilities

def parse_command_line_arguments(argv=None):
    """
    parse argumnents
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("solver", help="Path to the MaxSAT solver.")
    parser.add_argument("problem", help="Path to the file with the problem to solve.")
    parser.add_argument("-file", "-f", default="file", help="Name of the output graph pdf.")

    return parser.parse_args(args=argv)


# entry point

if __name__ == "__main__":
    main()
