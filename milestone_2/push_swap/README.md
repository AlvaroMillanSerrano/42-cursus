*This project has been created as part of the 42 curriculum by amillan-*

---

## Description

Push_Swap consist of a project about sorting sets of unordered numbers with a serie o coded orders, trying to use the less amount of steps. I used in my project 2 separated algorithms to sort 3, 4 and 5 sequences, and a big algorithm called chunks-algorithm to sort bigger series.

The aim of chunks is to transfer every element from A to B, but following a conditional where it sends every element to b when it is inside of the index chunk range, sends every smaller elements and rotates it sending it to the bottom of the stack, and passes every bigger element, until A is empty, This allows me to strategically put the biggest ones first and the smallest ones last. With this distribution i can now iterate over the stack, rotating and sending the biggest element back on every call of the function with the least steps possible, due to the fact that the biggest elements a re the first in the stack B.  

---

## Instructions

In order to compile this program, you must execute the makefile using make. In the terminal type ./push_swap and next to it the sequence of numbers. Repeated numbers and words are not allowed in the function, but you can use number strings:
```bash
- Allowed: ./push_swap 2 1 "4 35" 5 "20";
- Not Allowed: ./push_swap "+1" 1 "three" 2 1
```

You can use the command shuf to generate an arbitrary amount of numbers to test the project:
```bash
- Example: ARG=$(shuf -i 1-1000 -n 500 | tr '\n' ' '); ./push_swap 
$ARG | wc -l
```

---

## Resources

I used in this project gitbook which helped me to create the orders for the steps, a page called medium to develop the algorithm for sorting 3, 4 and 5 numbers.
And wikipedia and AI to understand graphically how chunks works.
