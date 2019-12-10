
import argparse
import wcnf
import msat_runner


class SPU_Solver():
    """
    Software Package Upgrade Solver Class
    """

    #formula = None
    #solver = None
    #problem

    def __init__(self, solver_path=None, problem_path=None):
        """
        """
        #print("Constructor")

        self.formula = wcnf.WCNFFormula()
        self.solver = msat_runner.MaxSATRunner(solver_path)
        self.problem = self.parser(problem_path)


    def parser(self, problem_path=None):
        """
        """
        print("Parser")

        if problem_path == None:
            print("No problem to solve !")
            return None

        if problem_path.split(".")[-1] != 'spu':
            print("Problem file with wrong extension")
            return None

        with open(problem_path, 'r') as file:

            total_packages = 0
            packages = []
            dependencies = []
            conflicts = []

            for line in file:
                aux = line.split("\n")[0]
                #print(aux)
                items = aux.split(" ")
                #print(items)
                if items[0] == 'p':
                    total_packages = int(items[2])
                    #self.n_nodes = int(l[2])
                    #n_edges = int(l[3])
                elif items[0] == 'n':
                    packages.append(items[1])

                elif items[0] == 'd':
                    for dependency in items[2:]:
                        dependencies.append([items[1], dependency])

                elif items[0] == 'c':
                    conflicts.append([items[1:]])

                else:
                    print("Line not considered")

            print("Total packages: " + str(total_packages))
            print("Packages:")
            print(packages)
            print("Dependencies:")
            print(dependencies)
            print("Conflicts:")
            print(conflicts)

        file.close()

        return None


    def solve(self):
        """
        - input:
            - path to binary solver
            - problem to solve
        - output:
        """
        print("Solve")

        # transform problem to WPMS

        # solve the formula

        # interpret the solution

        return None


# Main

def main(argv=None):
    """
    """

    args = parse_command_line_arguments(argv)
    #print(args.solver)
    #print(args.problem)

    spu_solver = SPU_Solver(args.solver, args.problem)
    print("##### Software Package Upgrade Solver #####")
    spu_solver.solve()


# Utilities

def parse_command_line_arguments(argv=None):

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("solver", help="Path to the MaxSAT solver.")
    parser.add_argument("problem", help="Path to the file with the problem to solve.")

    return parser.parse_args(args=argv)


# entry point

if __name__ == "__main__":
    main()
