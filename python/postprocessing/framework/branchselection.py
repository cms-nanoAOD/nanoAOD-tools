import re
try:
    Pattern = re._pattern_type
except AttributeError:
    # Python 3.7
    Pattern = re.Pattern


class BranchSelection():
    def __init__(self, filename):
        comment = re.compile(r"#.*")
        ops = []
        for line in open(filename, 'r'):
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            line = re.sub(comment, "", line)
            while line[-1] == "\\":
                line = line[:-1] + " " + file.next().strip()
                line = re.sub(comment, "", line)
            try:
                (op, sel) = line.split()
                if op == "keep":
                    ops.append((sel, 1))
                elif op == "drop":
                    ops.append((sel, 0))
                elif op == "keepmatch":
                    ops.append((re.compile("(:?%s)$" % sel), 1))
                elif op == "dropmatch":
                    ops.append((re.compile("(:?%s)$" % sel), 0))
                else:
                    print("Error in file %s, line '%s': "% (filename, line)
                        + ": it's not (keep|keepmatch|drop|dropmatch) "
                        + "<branch_pattern>"
                    )
            except ValueError as e:
                print("Error in file %s, line '%s': " % (filename, line)
                    + "it's not (keep|keepmatch|drop|dropmatch) "
                    + "<branch_pattern>"
                )
        self._ops = ops

    def selectBranches(self, tree):
        tree.SetBranchStatus("*", 1)
        branchNames = [b.GetName() for b in tree.GetListOfBranches()]
        for bre, stat in self._ops:
            if type(bre) == Pattern:
                for n in branchNames:
                    if re.match(bre, n):
                        tree.SetBranchStatus(n, stat)
            else:
                tree.SetBranchStatus(bre, stat)
