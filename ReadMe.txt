The instruction to run the code in bottom up strategy:
**When you run any command line, make sure the current location is under src folder.**
1. Copy the facts and rules into a text file named code1.txt
2. Copy the contexts into a text file named context1.txt
3. In the main.py, change the value of two variables named codefile_name and contextfile_name ( line 12 and 13) to the corresponding file names.
4. Run the command: 'python main.py'

To run the unit tests: 'python -m unittest'
To run the top down query test: 'python -m unittest test/test_query.py'
an IMPORTANT note for running the test_query.py:
as you can see in the line 124: self.assertEqual(3, count). The number 3 is based on the as specific example(lines 88,89, and 90). If you change the example, you should change the line 124 as well.