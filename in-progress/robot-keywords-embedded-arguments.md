Let's look at how Robot Framework takes a statement like this

```
Add 3 and 4
```

And turns it into a function call like this

```python
add('1', '2')
```

Take an `Arithmetic` library that provides a few keywords with embedded
arguments

```python
from robot.api import deco

class Arithmetic:

    def __init__(self):
        pass

    @deco.keyword("Add ${first} and ${second}")
    def add(self, first: float, second: float) -> float:
        return float(first) + float(second)

    @deco.keyword("Subtract ${first} from ${second}")
    def subtract(self, first: float, second: float) -> float:
        return float(second) - float(first)

    @deco.keyword("Multiply ${first} and ${second}")
    def multiply(self, first: float, second: float) -> float:
        return float(first) * float(second)
```

At the beginning of a test case, Robot Framework creates an instance of
this class

```python
arithmetic = Arithmetic()
```

Robot Framework adds a `robot_name` attribute to keywords with embedded
arguments

```python
print(arithmetic.add.robot_name)
```

We can combine this with some magic from the inspect library to find all
keywords with embedded arguments that a library provides.

```python
import inspect
from collections import namedtuple

arithmetic_methods = [
    i[1] for i in inspect.getmembers(arithmetic_method, predicate=inspect.ismethod)
]

keywords = [
    Keyword(getattr(arithmetic_method, 'robot_name'), arithmetic_method)
    for arithmetic_method in arithmetic_methods
    if hasattr(arithmetic_method, 'robot_name')
]
```


