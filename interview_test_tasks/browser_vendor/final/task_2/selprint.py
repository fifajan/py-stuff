#! /usr/bin/python
"""
Task description:

For a new project purposes a simple hierarchical database was prepared.
All data are kept in a single file. Each line inside the file contains single
entity. Entities are placed in the random order inside the file.

  Format of the entity is as follow:
{id:<entity_id>, key:<key_string>, value:<value_string>, parent:<parent_id>}

  where:
<entity_id>    - positive integer, unique throughout the database
<key_string>   - key (string) of the entity (there may be many entities
                 with the same key)
<value_string> - value (string) of the entity (there may be many entities
                 with the same value)
<parent_id>    - entity_id of the parent of the entity. If the entity is
                 the main entity (doesn't have a parent) the parent_id
                 is equal 0
                 (there may be only one main entity in the database).

[See example database in db.txt file]

Prepare an application that displays (on the screen) the value_string for
all entities that match a selector given as an argument. The selector may
be a single key_string or a list of those keys. If a single key is given,
the application should display value of the value_string field for all
entities that contain the key in the key_string field. Basing on the above
example, the following result should be displayed for "bearing" key given
as an argument for the application:

> python selprint.py bearing
AX65
AAH
GGH321D

In the case of usage of multiple key elements in the selector, the value
of the value_string field for the last key will be displayed. All preceding
keys are used to specify the search range, i.e. selector in the form
"underbody bearing" should cause displaying all bearings which constitute
the underbody element. As an example:

> python selprint.py underbody bearing
GGH321D

Similarly, selector "underbody driving_system bearing" should display the
same bearing:

> python selprint.py underbody driving_system bearing
GGH321D

In addition, please estimate the time and memory consumption of your algorithm
with usage of the Big O notation (http://en.wikipedia.org/wiki/Big_O_notation).
"""


# Remarks from me:
# 1: There is "underbody" key in given query examples but it seem to look like
#    "under_body" (with "_") in given example database.
#    I don't want to be picky but if some auto-tests will be applied to
#    following code please use "under_body" key in all cases.
#
# 2: It is mentioned that "id" should be unique for every entry in database
#    but there are two "13" ids and two "18" ids in example database.
#
# So ill fix the database (db.txt) to deal with those both above issues.
#
# 3: In multi-key query case this solution will return multiple values if
#    they are in query search range (this case was not covered in clear way by
#    task description). 


from collections import deque as queue
from common.tree import TreeNode


def query_database(keys, engine='auto'):
    """Task function implementation."""
    db_engine_classes = {
        'tree' : HierarchicalDatabase,
        'dict' : DictionaryDatabase,
        'auto' : HierarchicalDatabase if ' ' in keys else DictionaryDatabase,
    }
    db = db_engine_classes[engine]('db.txt')
    return db.query(keys)


class Database(object):
    """Represents database to store described structured key-value entries.

    Should be subclassed.
    """
    keys_to_be_quoted = ('id', 'key', 'value', 'parent')
    def __init__(self, input_file_name):
        self.load_database(input_file_name)

    def dict_from_line(self, line):
        return eval(self.quoted_keys(line))

    def quoted_keys(self, line):
        for key in Database.keys_to_be_quoted:
            line = line.replace(key, '"%s"' % key, 1)
        return line

    def load_database(self, file_name):
        with open(file_name) as file:
            self.entries = [self.dict_from_line(line) for line in file]

    def query(keys):
        print 'INFO: Database.query is not implemented.'


# Two strategies for database deployment:
# Following 2 Database subclasses represent different data organisation and
# querying approaches: hierarchical (tree of nodes) and dictionary-based
# (hash table inside).
#
# Despite we can actually solve given querying problem using any of following
# we will use dictionary in case of single key query and tree-based in case
# of multi-key query. Frankly this desicion was made not due to desire of
# meeting some practical aims but just to play around with different
# data structures :).


class HierarchicalDatabase(Database):
    """Represents tree-based approach to store and query entries described
    in the task.

    Can handle both single and multi-key query situations.

    Terms used:
        N - size of initial imput record set;
        R - size of parent -> child relation (edges) set for records.
        T - number of query times to gather result output set.

    Algorithm summary:
        This class uses BFS for internal tree data structure construction,
        and multiple DFS queries to select values of interest.

        In comparison to Dictionary approach:
            Pros:
                - Tree could be more space efficient than dict (hash table).
            Cons:
                - Slower because of linear total query time.

    Complexity analysis:
        Tree construction (BFS, known complexity):
            Time: O(R);
            Space: O(N);

        Selection (multiple DFS, known complexity):
            Time: O(T*R);
            Space: O(T*N);
                In multi-key query case each new call will be perfrmed on
                subtree of interest to optimize the query.
    """

    class TreeIdNode(TreeNode):
        """Represents tree node with multiple data entries in it."""
        def __init__(self, value, *children):
            self.key = value['key']
            self.id = value['id']
            self.parent = value['parent']
            value = value['value']
            super(HierarchicalDatabase.TreeIdNode, self).__init__(value,
                                                                  *children)
        def __hash__(self):
            return self.id

    def __init__(self, input_file_name):
        super(HierarchicalDatabase, self).__init__(input_file_name)
        self.build_tree()

    def build_tree(self):
        """Constructs tree from the set of disconnected nodes using BFS."""
        nodes = {HierarchicalDatabase.TreeIdNode(d) for d in self.entries}
        for node in nodes:
            if node.parent == 0: # Root node.
                self.root = node
                break
        nodes.remove(self.root)
        child_queue = queue([self.root])
        while child_queue:
            parent = child_queue.pop()
            children = []
            for node in nodes:
                if node.parent == parent.id:
                    children.append(node)

            parent.children.extend(children)
            child_queue.extendleft(children)
            nodes -= set(children)
        assert not nodes # There should be nothing.
        return self.root

    def find_node(self, node, key, discard_ids=None):
        """Finds node in tree using iterative DFS."""
        node_stack = [node]
        while node_stack:
            node = node_stack.pop()
            if node.key == key:
                if not discard_ids or node.id not in discard_ids:
                    return node
            node_stack.extend(node.children)
        return None

    def query(self, keys):
        keys = keys.split(' ')
        result = []
        found_ids = []
        last_key = keys.pop()
        node = self.root
        if keys:
            # In multi-key case this will find
            # parent node for nodes of interest.
            for key in keys:
                node = self.find_node(node, key)
        result_node = node
        while result_node:
            result_node = self.find_node(node, last_key, found_ids)
            if result_node:
                result.append(result_node.value)
                found_ids.append(result_node.id)
        return '\n'.join(result)


class DictionaryDatabase(Database):
    """Represents dictionary-based approach to store and query entries
    described in the task.

    Can handle only single key query situations at the moment due to
    limited implementation.

    Terms used:
        N - size of initial imput record set;

    Algorithm summary:
        This class construct dictionary holding only 'key' -> ['value1', ...]
        pairs from initial record set in this limited implementation, and
        then performs single "get values by key" call.

        In comparison to Hierarchical approach:
            Pros:
                - Provides much faster queries due to constant query time
                  complexity.
            Cons:
                - Hash table could be less space efficient than tree because
                  requires 1/3 free (unused) space inside to perform fast.
                - Multi-key queries not implemented here but it colud be done.

    Complexity analysis:
        Dict construction:
            Time: O(N);
            Space: O(N);

        Selection (hash table search):
            Time: O(1);
            Space: O(1);

    """
    def __init__(self, input_file_name):
        super(DictionaryDatabase, self).__init__(input_file_name)
        self.build_dict()

    def build_dict(self):
        """Constructs custom dict from initial database entry dicts."""
        self.dictionary = dict()
        for entry in self.entries:
            key = entry['key']
            self.dictionary[key] = (
                            self.dictionary.get(key, []) + [entry['value']])
        return self.dictionary

    def query(self, keys):
        return '\n'.join(self.dictionary.get(keys, []))


if __name__ == '__main__':

    from sys import argv

    if len(argv) < 2:
        print 'USAGE: ./selprint.py <keys>'
    else:
        print query_database(' '.join(argv[1:]))
