# Chapter 2: Core Calculator Functionality

This chapter delves into the heart of the application: the Calculator class and related functions for mathematical computations. It covers arithmetic operations, error handling, history tracking, and geometric calculations like area and circumference of a circle.


## Related Files

- `calculator.py`


## Sections

### The Calculator Class

The Calculator class encapsulates basic arithmetic methods (add, subtract, multiply, divide, power) with built-in history logging. It uses a list to store operation records and provides methods to retrieve or clear this history.


### Arithmetic Operations

Each method performs a calculation, appends a formatted string to the history, and returns the result. Division includes error checking for zero division.


### Geometric Calculations

Standalone functions calculate_area and calculate_circumference use the math module for pi and perform circle-related computations based on radius.

