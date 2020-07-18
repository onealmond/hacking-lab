* The program allow user to input student name, professor name and score for professor.
* It store the pointers to student and professor data in an array with maximum length 1000 contiguously.

``s`` for student, and ``p`` for professor, then we have the following structure

|s1.name|s1.score_func_ptr|p1.name|p1.score|s2.name|s2.score_func_ptr|p2.name|p2.score|...|

Notice that, when it needs to input name of student to give the score, it will look up the student by name in ``ADDRESSES`` array one by one. So if we input a professor with the same name as a student, it will interpret it as studen when it try to retrive student with the given name. Student and professor have similar structure, when a professor's data is interpreted as a student one, the score becomes the address that pointed to by the function pointer. We can change the score to address of ``win``, when the student's ``scoreProfessor`` got called, the flag is printed.
