Hello!

0. You could also check out my private git repo for this project:
   (Commit messages, history of changes all there!)
   Clone it (20 Mb of data due to old trash in history, sorry)
   first commit related to this task:
   7f908fbb102af6d3f5d97b82a4eda61ae7cd6fed  from Fri Mar 20 14:47:23
       $ git clone X@swdevelop.net:/home/Y/py-alg
       PASSWORD: XYZ

   Check out 'dev' branch:
       $ cd py-alg
       $ git checkout dev

   List files:
       $ ls XYZ

1. Files & directories inside:
    (Symlinks are used to ease package imports)
    task:                             - root dir
        readme.txt                    - this document
        run_all_tests.py (executable) - all tasks unit-tests runner
        db.txt                        - Symlink to task #2 db
        git.log                       - Development process log
        task.txt                      - initial tasks text
                                        (provided by MBV)
        common:                       - 'common' package directory
            __init__.py               - package init
            custom_test_case.py       - base class for all tests
            tree.py                   - few tree node base classes
        task_1:                       - Task #1 package directory
            __init__.py               - package init
            connected_areas.py        - Task #1 implementation
            test.py                   - unit-tests for task
            common                    - Symlink to 'common' package dir
        task_2:                       - Task #2 package directory
            __init__.py               - package init
            selprint.py (executable)  - Task #1 implementation
            db.tx                     - example database for task
            test.py                   - unit-tests for task
            common                    - Symlink to 'common' package dir
        task_3:                       - Task #3 package directory
            __init__.py               - package init
            print_tree.py             - Task #3 implementation
            test.py                   - unit-tests for task
            common                    - Symlink to 'common' package dir
        task_4_bonus:                 - Task #4 package directory
            __init__.py               - package init
            tree_diameter.py          - Task #4 implementation
            test.py                   - unit-tests for task
            common                    - Symlink to 'common' package dir

2. Before you dig in to my code:
    Each task implementation holds task description as a module docstring;
    Implementation details are given in entities docstrings and inside
    in-place comments (# ...). Please refer to them!

    Start with running all tests:
        $ ./run_all_tests.py

Thank you!

Alexey Ivchenko <yanepman@gmail.com>
