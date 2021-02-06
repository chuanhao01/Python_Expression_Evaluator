# Python_Expression_Evaluator - common/expression_sorter


| Class         | Description |
| --------------| ------------------------------------------------- |
| [`File`][c1]  | Deals with the File I/O, Read and Writes only |
| [`Sort`][c2]  | Deals with Sorting a list of expressions, requires a specific format to be passed in |

[c1]: https://github.com/chuanhao01/Python_Expression_Evaluator/blob/dev/src/common/expression_sorter/file.py
[c2]: https://github.com/chuanhao01/Python_Expression_Evaluator/blob/dev/src/common/expression_sorter/sort.py


**File**

*Methods:*
- read(filename) *staticmethod*
- write(filename, sortedList) *staticmethod*

*File.read()* only requires 1 argument, the input filename to be read from and returns a list of expressions read from the input file.

*File.write()* requires 2 arguments, the outfile filename to write to as well as the sorted list of expressions to write. It does not return anything.

The sorted list of expressions should follow the following format:
```
[
    (value_1, [expressions_evaluating_to_value_1]),
    (value_2, [expressions_evaluating_to_value_2]),
    (value_3, [expressions_evaluating_to_value_3]),
                    .
                    .
                    .
    (value_n, [expressions_evaluating_to_value_n])
 ]
 ```


**Sort**

*Attributes:*
- __all_expr_list
- __sort_type       ("value", "length")
- __sort_order      ("ascending", "descending")

The value of __all_expr_list should follow the following format:
```
[
    (expression_1, evaluated_value),
    (expression_2, evaluated_value),
    (expression_3, evaluated_value),
                .
                .
                .
    (expression_n, evaluated_value),
]
```


*Sorting*
Sort.sort() does not take in any arguments and returns a compiledList of sorted expressions in the following format:
```
[
    (value_1, [expressions_evaluating_to_value_1]),
    (value_2, [expressions_evaluating_to_value_2]),
    (value_3, [expressions_evaluating_to_value_3]),
                    .
                    .
                    .
    (value_n, [expressions_evaluating_to_value_n])
 ]
 ```

The sublist of expressions evaluating to each value will already be sorted according to the length of the expression.

* Sort.sort() is not a *staticmethod* and an object must be instantiated with the values of all_expr_list, sort_type and sort_order.

* The values of sort_type and sort_order will default to "value" and "ascending" if no argument is provided.
  
* In the event that there are multiple expressions with the same value and same length, the expressions will be sorted in ordered sort.


**Printing Result**

Printing result using the sortedList returned from Sort.sort():
#### **`src/basic/cli.py`**
``` python
for sublist in sortedList:
    value = sublist[0]
    print(f"\n*** Expressions with value = {value}")

    for expression in sublist[1]:
        print(f"{expression[0]} ==> {value}")
```