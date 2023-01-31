# testit-mini
Build a test suite that reveals two bugs in the function 

This repository contains a buggy.py, which contains a buggy function, and tests.py, which contains one test case (that doesn't uncover the bugs). You add to tests.py and turn that in.

## How to proceed

Try first to write test cases based just on the header of the buggy function. (We call these black box tests, because they treat the system under test as an opaque black box.) Think about some test cases you would want to try for any function that takes a list as input, and for any function that looks for things in a list.

I suspect you'll be able to find at least one bug with black box testing. Maybe both! But if you can't then look inside the function and try to think of test cases that would exercise the function in ways that might reveal more bugs. (We call these, quite illogically, white box test cases. Glass box would make more sense.)
