#! /usr/bin/python3

'''
TASK:

This year, Santa brought little Bobby Tables a set of wires and bitwise logic
gates! Unfortunately, little Bobby is a little under the recommended age range,
and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit
signal (a number from 0 to 65535). A signal is provided to each wire by a gate,
another wire, or some specific value. Each wire can only get a signal from one
source, but can provide its signal to multiple destinations. A gate provides no
signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together:
x AND y -> z means to connect wires x and y to an AND gate, and then connect
its output to wire z.

For example:
123 -> x means that the signal 123 is provided to wire x.
x AND y -> z means that the bitwise AND of wire x and wire y is provided to
wire z.
p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then
provided to wire q.
NOT e -> f means that the bitwise complement of the value from wire e is
provided to wire f.
Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for
some reason, you'd like to emulate the circuit instead, almost all programming
languages (for example, C, JavaScript, or Python) provide operators for these
gates.

For example, here is a simple circuit:
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i

After it is run, these are the signals on the wires:
d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to __wire_a__?
'''

# we need this to do bitwise operations with unsigned shorts in the
# right way:
from ctypes import c_ushort as unsigned_short

DEBUG = True

if not DEBUG:
    def munted_print(*args, **kwargs):
        pass
    print = munted_print


class Circuit():
    """Represents circuit with interconnected bitwise gates. "Resolvable"."""

    STORAGE = dict()
    ROOT_NODE = 'a'

    def __init__(self, input_file_name):
        self.nodes = set()
        self.load_input(input_file_name)
        print('Finished reading input.\n%d nodes read.' % len(self.nodes))
        self.resolve()
        self.root = type(self).STORAGE[type(self).ROOT_NODE]

    def __repr__(self):
        result = ''
        for key, value in type(self).STORAGE.items():
            result += '%s: %s\n' % (key, value)

        return result

    def load_input(self, filename):
        with open(filename) as input_file:
            id = 1
            for line in input_file:
                exp = Expression(line)
                self.nodes.add(exp.parse(id))
                id += 1

    def resolve(self):
        graph = CircuitGraph(self.nodes)
        graph.resolve()
        print('SIGNALS:\n%s' % self)


###############################################################################


class CircuitGraph():
    """Represents bitwise gates dependecies tree-graph. "Resolvable"."""

    LEAF_MARK = 'LEAF'

    def __init__(self, nodes):
        self.queue = []
        self.nodes = nodes
        self.deps_cache = dict()

    def resolve(self):
        node_count = len(self.nodes)

        deps = None
        for node in self.nodes:
            if node.output.get_name() == Circuit.ROOT_NODE:
                deps = {node : self.construct_deps_tree(
                                            node, self.nodes - {node})}
                break

        print('DEPS_TREE: DONE')
        if not deps:
            raise ValueError('No root node in graph: %s' % Circuit.ROOT_NODE)

        self.resolve_deps_tree(deps)

    def resolve_deps_tree(self, deps):
        """Recursive methods for resolving nodes in deps tree.

        Nodes are resolved from leafs to root (backwards) with help of
        tail recursion."""
        items = deps.items()
        for node, node_deps in items:
            if node not in NodeResolver.RESOLVED_CACHE:
                if type(self).LEAF_MARK == node_deps:
                    if (not node.is_resolved) and node.is_ready():
                        NodeResolver.resolve(node) # RECURSION EXIT POINT
                else:
                    if not node.is_resolved:
                        self.resolve_deps_tree(node_deps)
                        if node.is_ready():
                            NodeResolver.resolve(node)
            else:
                pass # skipping previously resolved node

    def construct_deps_tree(self, node, nodes):
        """Recursive method for dependecies construction. Uses deps cache."""
        if isinstance(node.operator(), Binary):
            inputs = node.inputs
        else:
            inputs = {node.inputs}

        deps = {nd for nd in nodes - {node} if nd.output in inputs}
        if not deps: # RECURSION EXIT POINT
            return type(self).LEAF_MARK

        dep_dict = dict()
        for nd in deps:
            if nd in self.deps_cache:
                dep_dict[nd] = self.deps_cache[nd]
            else:
                dep_dict[nd] = self.construct_deps_tree(nd, nodes - {node, nd})
                self.deps_cache[nd] = dep_dict[nd]
        return dep_dict


###############################################################################


class Expression():
    """Represents expression read from one line of input file."""

    def __init__(self, string):
        self.string = string

    def parse(self, id):
        """Parses a line of input file. Constructs "Nodes"."""
        self.node = None
        parts = self.string.split()
        if parts[-2] != '->':
            raise ValueError('Not a valid expression: "->" is missing.')
        elif len(parts) < 3:
            raise ValueError('Not a valid expression: too short.')
        elif (len(parts) == 3) and parts[0].isalnum() and parts[2].isalpha():
            # variable assignment
            self.node = Node(id, Input, parts[0], parts[2])
        elif (len(parts) == 4) and parts[0] == Not.STR:
            # NOT unary operator
            if parts[1].isdecimal():
                parts[1] = int(parts[1])
            self.node = Node(id, Not, parts[1], parts[3])
        elif (len(parts) == 5) and parts[4].isalpha():
            # Some binary operator
            bin_op = BinaryOperatorFactory(parts[1]).get_type()
            if parts[0].isdecimal():
                parts[0] = int(parts[0])
            if parts[2].isdecimal():
                parts[2] = int(parts[2])
            self.node = Node(id, bin_op, [parts[0], parts[2]], parts[4])
        else:
            raise ValueError('Not a valid expression at all: ' + self.string)

        return self.node

class Operand():
    """Represents operand abstraction used for input or output in a node."""

    def __init__(self, var_value):
        if isinstance(var_value, Operand):
            self.value = var_value.value
            self.variable = var_value.variable
        else:
            self.variable = self.value = None
            if isinstance(var_value, int) or var_value.isdecimal():
                num = int(var_value)
                if 0 <= num <= 65535:
                    self.value = num
                else:
                    raise ValueError('Value is not in '
                                     'unsigned_short=[0, (2^16)-1] range.')
            elif var_value.isalpha():
                self.variable = var_value
            else:
                raise TypeError(
                        'Value is of wrong type: %s' % str(type(var_value)))

    def __int__(self):
        return self.get_value()

    def __repr__(self):
        return ('VAR-%s' % self.variable) if self.variable else str(
                                                            self.get_value())

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def get_value(self):
        value = Circuit.STORAGE.get(self.variable)
        return value if value is not None else self.value

    def get_name(self):
        return self.variable

    def is_valued(self):
        """Checks if it is ready to participate in some node resolving."""
        val = self.get_value()
        return val is not None

class Node():
    """Represents abstraction for bitwise gate as a node in a graph (tree)."""

    def __init__(self, id, operator, inputs, output):
        self.id = id # correspons to line number from input file
        self.operator = operator
        self.inputs = self.prepare_in_out(inputs)
        self.output = self.prepare_in_out(output)
        self.is_resolved = False
        if isinstance(self.output, list):
            raise ValueError('Output should be a single Operand.')

    def __repr__(self):
        return '%d:%s:%s:%s' % (self.id, self.operator(), self.inputs,
                                self.output)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def prepare_in_out(self, in_outs):
        return [Operand(io) for io in in_outs] if isinstance(
                                in_outs, list) else Operand(in_outs)

    def is_ready(self):
        """Checks is this node is ready to be resolved (operands are ok)."""
        operator_obj = self.operator()
        result = all(op.is_valued() for op in self.inputs) if (
                            isinstance(self.operator(), Binary)) else (
                                                    self.inputs.is_valued())
        return result


class NodeResolver():
    """Static class used in node resolution. Has internal node cache."""

    RESOLVED_CACHE = set()

    @staticmethod
    def resolve(node):
        if not node.is_resolved:
            operator_obj = node.operator()
            if node.is_ready():
                key = node.output.get_name()
                if isinstance(operator_obj, Binary):
                    evaluated_inputs = [inp.get_value() for inp in node.inputs]
                    value = operator_obj.evaluate(*evaluated_inputs)
                elif isinstance(operator_obj, Unary):
                    value = operator_obj.evaluate(node.inputs.get_value())
                else:
                    raise ValueError('Unknown operator: %s' % operator_obj)
            else:
                raise ValueError('Node is not ready.')
            Circuit.STORAGE[key] = value
            node.is_resolved = True
            NodeResolver.RESOLVED_CACHE.add(node)


###############################################################################


class Operator():
    """Represents abstract parent class for any kind of operators."""

    STR = 'Abstract Operator'

    def __repr__(self):
        return type(self).STR

    def evaluate(self):
        raise NotImplemented()


class Unary(Operator):
    STR = 'Unary Operator'

    @staticmethod
    def ushort_bitwise(func):
        def bitwise(value):
            result = unsigned_short(func(value)).value
            return result
        return bitwise

class Binary(Operator):
    STR = 'Binary Operator'

    @staticmethod
    def ushort_bitwise(func):
        def bitwise(value_1, value_2):
            result = unsigned_short(func(value_1, value_2)).value
            return result
        return bitwise


class Input(Unary):
    STR = 'Input'

    @staticmethod
    def evaluate(value):
        return value

class Not(Unary):
    STR = 'NOT'

    @staticmethod
    @Unary.ushort_bitwise
    def evaluate(a):
        return ~ a

class Or(Binary):
    STR = 'OR'

    @staticmethod
    @Binary.ushort_bitwise
    def evaluate(a, b):
        return a | b

class And(Binary):
    STR = 'AND'

    @staticmethod
    @Binary.ushort_bitwise
    def evaluate(a, b):
        return a & b

class RShift(Binary):
    STR = 'RSHIFT'

    @staticmethod
    @Binary.ushort_bitwise
    def evaluate(a, b):
        return a >> b

class LShift(Binary):
    STR = 'LSHIFT'

    @staticmethod
    @Binary.ushort_bitwise
    def evaluate(a, b):
        return a << b


class BinaryOperatorFactory():
    """DesignPattern`ish class for choosing concrete binary operator."""

    def __init__(self, string):
        op_list = [Or, And, RShift, LShift]
        for op in op_list:
            if string == op.STR:
                self.operator = op
                break

    def get_type(self):
        return self.operator

##############################################################################

# basic tests are performed if executed as sole script:
if __name__ == '__main__':
    input_files = (
        # my small tests (described in my_test.txt):
        ('st0.txt', 536), ('mt1.txt', 536), ('mt2.txt', 536), ('mt3.txt', 536),
        # big "real" (from AoC site, ~340 lines) tests:
        ('bigt1.txt', 3176), ('bigt2.txt', 46065),
    )
    for in_file, result in input_files:
        circuit = Circuit(in_file)
        if result is not None:
            assert circuit.root == result
        else:
            print('%s root = %s' % (in_file, circuit.root))
