# *This project has been created as part of the 42 curriculum by amillan-*

---

## Description

Get_next_line is a project with the aim of returning consecutively lines from a given file descriptor.
The main function protoptype is **char *get_next_line(int fd)**, only requires the file descriptor.

### Normal version

This function uses a static variable to store the remaining characters between calls. Each call reads from the file descriptor using a buffer of size BUFFER_SIZE and concatenates it to the stored content until a newline character is found or EOF is reached.

### Bonus version

The only difference with the normal version is that I  changed the static variable to be an array of int in order to stack more than one file descriptor.

---

## Instructions

In order to compile this program, you must use cc with the normal 42 flags (-Wall -Wextra -Werror) and you can add another flag which is "-D BUFFER_SIZE=n" that adds the buffer size used in the function (it's optional, it has 10 by default).

---

## Resources

I used in this project gitbook, and uniquely google to understand how to do a main. There is someone that helped me to organize ideas and start the project.



