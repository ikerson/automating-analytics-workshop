# Before You Begin — Python Foundations

## Introduction

This session is a one-hour primer on core Python before you touch pandas, Oracle, or web APIs. It condenses the parts of *Automate the Boring Stuff with Python* (Chapters 1–7) that the rest of the workshop assumes you already know. If you have written Python before, this will be a fast review. If you have not, treat this as the minimum vocabulary you need to read and write every script that follows.

By the end you should be able to read a `.py` file and explain, line by line, what it does: what gets imported, what kind of data each variable holds, the order the lines execute in, what a function call is doing, how a loop or an `if` branches the flow, and how to look something up in a list, set, or dictionary.

Reference: Source material — [*Automate the Boring Stuff with Python*, 3rd Edition](https://automatetheboringstuff.com/), Chapters 1–7. This session is a summary, not a replacement — the full chapters are worth reading on your own time.

## Setting Up

Open VS Code, activate your conda environment in the terminal, and open or clear `scratch.py` in the repo root. Every example below can be typed or pasted into that file and run with:

```bash
python scratch.py
```
Run each section, look at the output, then move to the next. Do not skip running the code — reading Python and running Python teach you different things.

## How a Script Runs: Top to Bottom

A Python file is a list of instructions. Python executes them **in order, one at a time, starting at the top of the file and ending at the bottom**. There is no hidden ordering, no "main" function that gets found automatically — whatever line is first runs first.

```python
print('first')
print('second')
print('third')
```
Run it. The output appears in that exact order. This sounds obvious, but it is the single most useful fact for debugging: when something goes wrong, find the line, then read upward. Everything above it has already happened; everything below it has not happened yet.

Two things change strict top-to-bottom order, and you will meet both later in this session:

- **Functions** define a block of code but do not run it until it is *called*, possibly from somewhere else entirely.
- **`if` statements and loops** can skip lines or repeat them.

Keep this mental model running underneath everything else in this session: Python is always, at any given moment, sitting on exactly one line.

## Variable Assignment

A variable is a name that points to a value. You create one with `=`, which assigns whatever is on the right side to the name on the left.

```python
city = 'Atlanta'
print(city)

city = 'Augusta'   # reassignment — the name now points to a new value
print(city)
```

A few things worth knowing right away:

- `=` is assignment, not mathematical equality. `city = 'Atlanta'` means "make `city` refer to `'Atlanta'`," not "`city` equals `'Atlanta'`."
- A variable can be reassigned at any point in the script — whatever value it last pointed to is the one Python uses.
- Variable names are case-sensitive (`city` and `City` are different names) and conventionally written in `lowercase_with_underscores`.

You will spend the rest of this session assigning values to variables, so this single rule — a name on the left, a value on the right, `=` in between — is worth having solid before moving on.

## Basic Data Types

Every value in Python has a type. The four you will use constantly:

```python
age = 41                 # int — whole number
gpa = 3.85               # float — decimal number
name = 'Casey'           # str — text, single or double quotes
is_active = True         # bool — True or False
```

Check any value's type with the built-in `type()` function:

```python
print(type(age))
print(type(name))
```

### Strings

Strings are sequences of characters. A few operations you will use in nearly every script:

```python
first = 'Jane'
last = 'Doe'
full = first + ' ' + last        # concatenation
print(full)

greeting = f'Hello, {first}!'     # f-string: insert a variable into text
print(greeting)

print(full.upper())               # 'JANE DOE'
print(full.lower())               # 'jane doe'
print(len(full))                  # number of characters
```

f-strings — a letter `f` right before the opening quote — are the standard way to build a string that includes variable values. You will use this constantly to build file paths, log messages, and report titles.

### Numbers

```python
a = 10
b = 3
print(a + b)    # 13
print(a - b)    # 7
print(a * b)    # 30
print(a / b)    # 3.333... — division always returns a float
print(a // b)   # 3       — floor division, drops the remainder
print(a % b)    # 1       — modulo, the remainder
```

`/` vs `//` trips people up constantly: `/` gives you a precise decimal answer; `//` gives you a whole number with anything left over thrown away. You will use `%` later for things like "is this row index even or odd."

### Converting between types

Python will not silently combine a string and a number — you must convert explicitly:

```python
count = 12
print('You have ' + str(count) + ' items')   # int -> str

text = '42'
print(int(text) + 8)                          # str -> int, gives 50
```

If you ever see `TypeError: can only concatenate str`, this is almost always the fix.

## Functions and Methods

### Functions

A function is a named, reusable block of code. You **define** it once and **call** it as many times as you want.

```python
def greet(name):
    message = f'Hello, {name}!'
    return message

print(greet('Sam'))
print(greet('Alex'))
```

A few terms worth being precise about:

- **Defining** a function (the `def` block) does not run anything by itself — Python just remembers it exists. It runs only when you **call** it: `greet('Sam')`.
- `name` here is a **parameter** — a placeholder for whatever value gets passed in when the function is called.
- `'Sam'` is an **argument** — the actual value supplied at call time.
- `return` sends a value back to wherever the function was called from. A function with no `return` statement implicitly returns `None`.

This matters for top-to-bottom order: if `def greet(...)` appears on line 5 and `greet('Sam')` is called on line 40, the *body* of `greet` actually executes at line 40, not line 5.

### Methods

A method is a function that belongs to a value — you call it with dot notation, attached to the thing it operates on. You already used several above:

```python
text = 'hello world'
print(text.upper())       # method, belongs to the string
print(text.title())       # 'Hello World'

numbers = [3, 1, 2]
numbers.sort()            # method, belongs to the list
print(numbers)
```

The distinction is simple: `len(text)` is a function — you hand it a value. `text.upper()` is a method — it lives on the value and you call it with a dot. Later, when you write `df.head()` or `df.groupby(...)`, those are methods belonging to a pandas DataFrame; the dot-call pattern is identical to what you just did with strings and lists.

## Control Flow

### `if` / `else`

`if` statements let a script branch — run one block of code or another, depending on a condition. Python decides which block to run based on whether the condition evaluates to `True` or `False`.

```python
temperature = 85

if temperature > 90:
    print('It is hot.')
elif temperature > 70:
    print('It is warm.')
else:
    print('It is cool.')
```

Indentation is not a style choice in Python — it is how Python knows which lines belong inside the `if` block. Four spaces, consistently, is the standard.

Common comparison operators: `==` (equal — note the double equals; a single `=` is assignment, not comparison), `!=` (not equal), `>`, `<`, `>=`, `<=`. Combine conditions with `and` / `or`:

```python
gpa = 3.4
credits = 45

if gpa >= 3.0 and credits >= 30:
    print('Eligible for honors review')
```
> A single `=` assigns a value. A double `==` compares two values. Mixing these up is one of the most common early bugs — `if x = 5:` is a syntax error, not a typo Python will quietly fix.

### `for` Loops

A `for` loop repeats a block of code once for each item in a sequence (a list, a string, a range of numbers, and so on).

```python
schools = ['Bloomfield Middle School', 'Carteret Middle School', 'Newark Academy']

for school in schools:
    print(school)
```
On each pass through the loop, `school` is reassigned to the next item in `schools`. The indented block runs once per item, then the loop ends and execution continues with whatever comes after it.

`range()` generates a sequence of numbers, useful when you want to repeat something a fixed number of times rather than loop over existing data:

```python
for i in range(5):
    print(i)        # prints 0, 1, 2, 3, 4
```

A common pattern: build up a result by looping and accumulating.

```python
scores = [88, 92, 79, 95, 84]
total = 0

for score in scores:
    total = total + score

average = total / len(scores)
print(average)
```
You will see this exact shape — loop, accumulate, summarize — echoed later by pandas methods like `.sum()` and `.mean()`, which do the same thing without you having to write the loop yourself.

## Importing Code

Python's standard library and third-party packages are not available automatically — you have to `import` them. This is the first line of nearly every script you will write in this workshop.

```python
import math
print(math.sqrt(16))      # 4.0 — sqrt belongs to the math module
```

A few import forms you will see repeatedly:

```python
import pandas as pd          # import a package, give it a short alias
from datetime import date    # import one specific thing out of a module

today = date.today()
print(today)
```

`import pandas as pd` is everywhere in this workshop because typing `pandas.read_csv(...)` a hundred times is slower than typing `pd.read_csv(...)`. The alias is a convention, not a requirement — `pd` for pandas is just what everyone agreed on.

By convention, **all imports go at the top of the file**, before anything else runs. This is not enforced by Python, but every script in this workshop follows it, and you should too — it tells a reader immediately what tools the script depends on.

## Data Containers
### Lists

A list is an ordered, changeable collection of values, written with square brackets. Items can be looked up by their position (**index**), starting at `0`.

```python
schools = ['Bloomfield Middle School', 'Carteret Middle School', 'Newark Academy']

print(schools[0])        # 'Bloomfield Middle School' — first item
print(schools[-1])       # 'Newark Academy' — last item
print(len(schools))      # 3

schools.append('Eastside High School')   # add to the end
print(schools)

print('Carteret Middle School' in schools)   # True — membership check
```

Lists allow duplicates and preserve the order you put things in. Use a list when order matters or when the same value might legitimately appear more than once — for example, a list of enrollment rows where a student can appear multiple times.

### Sets

A set is an unordered collection of **unique** values, written with curly braces. Adding the same value twice has no effect — duplicates are automatically dropped.

```python
school_ids = {101, 102, 103, 101, 102}
print(school_ids)            # {101, 102, 103} — duplicates collapsed

school_ids.add(104)
print(104 in school_ids)     # True
```

A common real use: turn a list with repeated values into a set to get the distinct values out.

```python
visited_ids = [101, 102, 101, 103, 102, 101]
unique_ids = set(visited_ids)
print(unique_ids)            # {101, 102, 103}
```

You do not need sets often in this workshop, but the underlying idea — "give me only the distinct values" — is exactly what pandas' `.unique()` and `.drop_duplicates()` do later on, just on a whole column instead of one Python list.

### Dictionaries

A dictionary stores **key-value pairs** — instead of looking something up by position like a list, you look it up by a name (the key), written with curly braces and colons.

```python
student = {
    'student_id': 124,
    'name': 'Jordan Lee',
    'school': 'Bloomfield Middle School'
}

print(student['name'])          # 'Jordan Lee'

student['gpa'] = 3.6             # add a new key
print(student)

print('gpa' in student)         # True — checks keys, not values
```

Looping over a dictionary's keys and values together is a pattern you will see often:

```python
for key, value in student.items():
    print(key, '->', value)
```

A dictionary is the right tool when each value has a meaningful label — a single record describing one student, one row, one config setting. A list of dictionaries (one dict per record) is also exactly the shape that a CSV file or a database query result takes before it becomes a pandas DataFrame in Session 3 — recognizing that shape now will make `df.to_dict()` and similar conversions much less mysterious later.

## Putting It Together

Here is a single short script that uses everything from this session — import, types, a function, a loop, an `if`, and a dictionary:

```python
import statistics

students = [
    {'name': 'Jordan Lee', 'gpa': 3.6},
    {'name': 'Casey Smith', 'gpa': 2.8},
    {'name': 'Riley Chen', 'gpa': 3.9},
]

def honor_roll(students, threshold=3.5):
    names = []
    for student in students:
        if student['gpa'] >= threshold:
            names.append(student['name'])
    return names

honored = honor_roll(students)
print(f'Honor roll: {honored}')

gpas = [s['gpa'] for s in students]
print(f'Average GPA: {statistics.mean(gpas):.2f}')
```
Run it, then read it back top to bottom out loud: an import, a list of dictionaries, a function definition, a function call, an f-string, and a built-in module method. If every piece of that sentence makes sense, you have what you need for Session 3.

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

The starter script is at [`exercises/session_03_fundamentals_exercise.py`](../exercises/session_03_fundamentals_exercise.py). It contains instructions and fill-in-the-blank placeholders. Every exercise in this workshop uses the same convention: a `# TODO:` comment marks each blank. Replace `"___"` (with the quotes) with a string value, and replace a bare `___` (no quotes) with a variable name or expression. If you get stuck, the completed version is at [`exercises/session_03_fundamentals_answer.py`](../exercises/session_03_fundamentals_answer.py).


## Additional Resources

- [*Automate the Boring Stuff with Python*, Chapters 1–7](https://automatetheboringstuff.com/) — the full source material this session summarizes
- [Python official tutorial](https://docs.python.org/3/tutorial/)
- [Python data types cheat sheet (DataCamp)](https://www.datacamp.com/cheat-sheet/python-data-types-cheat-sheet)