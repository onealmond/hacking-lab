* The program take any length of input from ``stdin``, the input buffer is initially a pointer to ``NULL``, will be allocated a pointer to a new buffer by ``getline``.
* The flag is stored in heap.
* ``printMessage1`` to call ``printMessage2``, which calls ``printMessage3`` to print the input with ``printf``,  as it simply pass whatever we input to ``printf``, we can use ``%n$s`` to jump to the ``nth`` layer of stack to print the string.
