```
ICS 33 Winter 2025 | News | Course Reference | Schedule | Project Guide | Notes and Examples | Reinforcement Exercises | Grade Calculator | About Alex
```
# ICS 33 Winter 2025

# Notes and Examples: Functions and Their Parameters

## Background

In Python, a _function_ is a sequence of statements that accepts a collection of _parameters_ , performs some job, and then either returns a value or raises an exception. Since a function is meant to perform a job, then we'll
generally want it to return a value when it has succeeded in performing that job, or to raise an exception when it's failed. By following that simple design rule, we'll most easily be able to tell the difference between
success and failure, and we'll most easily be able to allow failure to cascade naturally when it should (i.e., much more often than not, the failure of a function also implies the failure of the function that called it). But,
either way, much of what determines the outcome of calling a function revolves around the arguments passed into its parameters, which means that a richness in our ability to pass arguments leads to a flexibility in the
problems a function might solve.

Among the first things you likely learned about Python was how to write a simple function, like this one.

```
>>>>>>>>>>>> def square(n):
............ return n * n
............
```
This particular function accepts one argument into its parameter n, multiplies it by itself, and returns the result. Notably, square must always be given exactly one argument to correspond to its one and only
parameter. There's a little more to square than meets the eye, because it's flexible with respect to the type of argument it can accept. Anything that can be multiplied by itself is workable, so it can handle int, float,
complex, and a variety of other types in Python and its standard library — and, as we'll see later in the quarter, it'll be able to handle arguments of our types, too, when they're written in a way that allows them to
support multiplication, as well.

But some of the functions built into Python and its standard library offer a level of flexibility that you may not yet have discovered the ability to design into your own functions.

```
>>>>>>>>>>>> len([ 1 , 3 , 5 , 7 ])
4
>>>>>>>>>>>> len('Boo')
3 # Like square, the len function can accept arguments of many
# different types, but must always be given exactly one argument.
>>>>>>>>>>>> max([ 3 , 7 , 11 , 5 , 9 ])
11
>>>>>>>>>>>> max( 13 , 17 )
17
>>>>>>>>>>>> max( 3 , 7 , 11 , 5 , 9 )
11 # The max function, on the other hand, can accept different
# numbers of arguments.
>>>>>>>>>>>> print('Boo', 'is', 'happy', 'today')
Boo is happy today # So can print.
>>>>>>>>>>>> print('Boo', 'is', 'happy', 'today', sep = '!')
Boo!is!happy!today # But print can accept keyword arguments, too.
# When we don't specify them, they're defaulted automatically.
```
We should want to write functions with that same level of flexibility when it can improve our designs. So, let's take a look at functions and their parameters in detail, which will require a few more Python techniques
that you've likely not seen in previous coursework.

## Flexibility in what we pass into functions

Suppose we write a simple Python function with a handful of parameters. In what ways are we allowed to call it?

```
>>>>>>>>>>>> def subtract(n, m):
............ return n - m
............
>>>>>>>>>>>> subtract( 18 , 7 )
11 # We can specify an unnamed argument for each parameter.
>>>>>>>>>>>> subtract( 18 , m = 7 )
11 # We can specify some of them as keyword arguments.
>>>>>>>>>>>> subtract(n = 18 , m = 7 )
11 # We can specify all of them as keyword arguments.
>>>>>>>>>>>> subtract(m = 18 , n = 7 )
-11 # We can specify keyword arguments out of order. Look carefully!
>>>>>>>>>>>> subtract(n = 18 , 7 )
Traceback (most recent call last):
...
File "<input>", line 1
subtract(n = 18, 7)
^
SyntaxError: positional argument follows keyword argument
# But once we specify a keyword argument, all of the subsequent
# arguments must also be keyword arguments.
>>>>>>>>>>>> subtract( 18 , a = 7 )
Traceback (most recent call last):
...
TypeError: subtract() got an unexpected keyword argument 'a'
# The names of keyword arguments must match parameter names.
>>>>>>>>>>>> subtract(n = 7 , n = 18 , m = 11 )
Traceback (most recent call last):
...
SyntaxError: keyword argument repeated: n
# The same keyword argument can't be specified more than once.
```
From this, we see that Python draws a distinction between two kinds of arguments:

```
Positional arguments , which are matched to their corresponding parameters based only on the order in which they're specified in the call.
Keyword arguments , which are matched to their corresponding parameters based on how the keywords compare to the parameters' names.
```
The positional arguments must be listed first when calling a function, mainly because any other rule would be unnecessarily confusing. Keyword arguments, on the other hand, can be more flexible without introducing
confusion, since their names make clear how they correspond to the function's parameters.

## Unpacking iterables as positional arguments

You may have previously seen a technique known as _sequence assignment_ , which allows you to assign values into multiple variables in a single statement.

```
>>>>>>>>>>>> values = ( 1 , 2 , 3 )
>>>>>>>>>>>> a, b, c = values
>>>>>>>>>>>> print(a, b, c)
1 2 3
```
This technique rests on two assumptions:

```
The right-hand side of the assignment must contain a value that is iterable , which simply means that it's actually a sequence of values that can be iterated one at a time. Tuples certainly qualify (e.g., you could also
write for x in values:), but so do lists, sets, strings, ranges, and many other types of objects in Python.
The number of values to be iterated must exactly match the number of variables on the left-hand side of the assignment. Since values is a three-element tuple, we can safely assign it into three variables, but if we
had written a, b = values or a, b, c, d = values, we would have instead seen an exception raised.
```
Sequence assignment is actually an example of a broader need: It is common for us to need to take a collection of things and pull it apart into its individual components, as well as to take individual things and put them
together into a single collection. If this is such a common idea, it would be worth having a shorthand syntax for doing it.

_Unpackings_ in Python provide such a syntax. You can think of an unpacking as a single expression that "unpacks" into a collection of objects you would otherwise have had to specify individually. Iterables are
collections of objects, so we might expect to be able to unpack them. For example, if you wanted to pass two arguments to a function, and you had those two arguments stored in a list, you might expect to be able to
unpack them and pass them into the function individually. And, indeed, you can.

```
>>>>>>>>>>>> things = [ 18 , 7 ]
>>>>>>>>>>>> subtract(*things)
11
```
When a * operator precedes an expression, what you're doing is something called _iterable unpacking_ , which means that the expression following the * needs to be something iterable (e.g., a list, a tuple, etc.), and what
you want to do is the equivalent of having treated the elements as though they had been listed separately. So, in the example above, things is a list, which means that *things is an unpacking of the elements of that
list. It's as though we passed the values in things as a sequence of separately-listed positional arguments. Since there are two values in things, we've passed two positional arguments. The subtract function has
two parameters, so they're matched up in order — the 18 is matched up to n and the 7 is matched up to m — and subtract can do its job, returning 18 - 7 = 11.

As we saw with sequence assignment, the number of values being unpacked is important. Our subtract function must be given two arguments, so if all we're passing in is an unpacking, it must have exactly two
elements.

```
>>>>>>>>>>>> too_many = [ 6 , 1 , 17 ]
>>>>>>>>>>>> subtract(*too_many)
Traceback (most recent call last):
...
TypeError: subtract() takes 2 positional arguments but 3 were given
>>>>>>>>>>>> too_few = [ 11 ]
>>>>>>>>>>>> subtract(*too_few)
Traceback (most recent call last):
...
TypeError: subtract() missing 1 required positional argument: 'm'
```
It's worth noting, though, that an unpacking doesn't have to be the only argument listed in a function call.

```
>>>>>>>>>>>> subtract(*too_few, 10 )
1 # 11 - 10 = 1
>>>>>>>>>>>> subtract( 18 , *too_few)
7 # 18 - 11 = 7
```
## Unpacking dictionaries as keyword arguments

Dictionaries in Python have the basic goal of allowing us to associate each of a collection of unique keys with a value of our choosing. What if the keys were strings and the values were integers?

```
>>>>>>>>>>>> d = {'n': 18 , 'm': 7 }
```
That dictionary looks an awful lot like the keyword arguments we might pass to our subtract function. Since dictionaries are among the types in Python that are iterable, we might expect to be able to unpack d and
pass that into subtract.

```
>>>>>>>>>>>> subtract(*d)
Traceback (most recent call last):
...
File "<input>", line 2, in subtract
TypeError: unsupported operand type(s) for -: 'str' and 'str'
```
It didn't end up working out, but we should look carefully at the error message. What's it telling us? The failure here was in the subtract function, so the attempt to call the function actually succeeded; what went
wrong was inside the function, which was trying to subtract one string from another. Why was it trying to do that? What were the values of the arguments we passed?

The answer to that question lies in the answer to another: What do you get when you iterate a dictionary?

```
>>>>>>>>>>>> for x in d:
............ print(x)
............
n
m
```
Ah! When you iterate a dictionary, what you get are its keys. The keys in this dictionary were the strings 'n' and 'm', which we passed into the subtract function, which dutifully tried (and failed) to subtract one
from the other.

Still, the goal we had was a reasonable one: A dictionary is a natural expression of an idea — keys with associated values — that maps very nicely to the meaning of keyword arguments. Perhaps what we need is a syntax
for unpacking dictionaries into its individual keys and values.

```
>>>>>>>>>>>> subtract(**d)
11 # n = 18, m = 7
# n - m = 18 - 7 = 11
```
When a ** operator precedes an expression, you're doing something called _dictionary unpacking_. The expression following the ** needs to be something called a _mapping_ (i.e., keys and associated values), of which
dictionaries are the primary example in Python. When we use dictionary unpacking in a function call, it's as though we separately typed each of the key/value pairs in the dictionary as keyword arguments. So, in the
example above, Python took subtract(**d) to mean subtract(n = 18, m = 7) and was able to proceed successfully.

All of the same rules we already learned about keyword arguments still apply:

```
>>>>>>>>>>>> subtract( 18 , **{'m': 11 })
7 # n = 18, m = 11
# n - m = 18 - 11 = 7
>>>>>>>>>>>> subtract(**{'n': 3 }, 8 )
Traceback (most recent call last):
...
SyntaxError: positional argument follows keyword argument unpacking
>>>>>>>>>>>> subtract(**{'a': 3 , 'b': 8 })
Traceback (most recent call last):
...
TypeError: subtract() got an unexpected keyword argument 'a'
```
And, of course, we can combine these techniques, subject to the same rules we learned previously, with iterable unpackings becoming positional arguments and dictionary unpackings becoming keyword arguments.

```
>>>>>>>>>>>> some_things = [ 18 ]
>>>>>>>>>>>> other_things = {'m': 7 }
>>>>>>>>>>>> subtract(*some_things, **other_things)
11
```
All of these rules may rightly seem unnecessarily complicated for a function as simple as subtract — if you feel that way, I'd agree with you! — but we've taken our first step into writing functions that are more
powerful, by understanding how flexibly we can pass arguments into them. Without the same flexibility on the other side of the arrangement, though, we won't have gained much, because where we most need
flexibility in passing arguments is when we're calling functions that offer a similar variety in the ways they accept those arguments into their parameters.

## Flexibility in what we accept within functions

We began this topic by recalling a few of Python's built-in functions, observing that even some of the simplest ones offer a fair amount of flexibility in how they're called.

```
Some of their parameters use default arguments when a corresponding argument is not passed, making certain of their arguments optional.
Some of them can accept different numbers of arguments, perhaps behaving differently depending on how many there are.
Some of their parameters can only accept keyword arguments (i.e., if you don't specify a name for the argument, you can't pass it).
Some of their parameters can only be accepted positionally (i.e., you can't specify keyword arguments for them, even if you want to).
```
While we surely don't need all of our functions to have all of these abilities, there are plenty of functions — even some of the conceptually simpler ones built into Python — that benefit from being able to apply them
when appropriate. So, we should take a look at how to achieve these same design goals in our Python functions.

## Default arguments

The simplest way to increase the flexibility with which a function can be called is to specify _default arguments_ for one or more of its parameters. Syntactically, the approach is unsurprising: Assign a value into the
parameter, which will be its default value if not specified.

```
>>>>>>>>>>>> def read_integer(prompt = 'Enter an integer:'):
............ return int(input(f'{prompt} '))
............
>>>>>>>>>>>> value1 = read_integer()
Enter an integer: 98989898
>>>>>>>>>>>> value2 = read_integer('How old is Boo?')
How old is Boo? 13131313
>>>>>>>>>>>> value1 + value
111
```
Our read_integer function can be called with either one argument (which will be passed into prompt) or zero arguments (in which case prompt will be defaulted to 'Enter an integer:' instead).

Let's be sure we've gotten all the way to the bottom of this feature, though. Can we specify defaults for some arguments and not others?

```
>>>>>>>>>>>> def combine(first, second = None):
............ if second is not None:
............ return first + second
............ else:
............ return first
............
>>>>>>>>>>>> combine( 11 , 7 )
18
>>>>>>>>>>>> combine( 11 )
11
>>>>>>>>>>>> def combine2(first = None, second):
............ if first is not None:
............ return first + second
............ else:
............ return second
............
Traceback (most recent call last):
...
def combine2(first = None, second):
^^^^^^
SyntaxError: non-default argument follows default argument
```
The rule there matches the rule we saw when we were attempting to pass keyword arguments: Once you specify a default argument for some parameter, all subsequent parameters need defaults. This is motivated
similarly to the rule for passing keyword arguments: Since arguments are so often matched to parameters positionally, any other rule would easily lead to confusion.

There's one more detail we should think carefully about: You've seen that some objects in Python are _mutable_ (i.e., their values can be changed), while others are _immutable_. What if a default argument's value is
mutable? What happens if its value changes?

```
>>>>>>>>>>>> def add_to_end(value, x = []):
............ x.append(value)
............ return x
............
>>>>>>>>>>>> add_to_end('today', ['Boo', 'is', 'happy'])
['Boo', 'is', 'happy', 'today']
>>>>>>>>>>>> add_to_end('Hello')
['Hello'] # The default argument [] was used here.
>>>>>>>>>>>> add_to_end('there')
['Hello', 'there'] # If the default argument is [], where did 'Hello' come from?
>>>>>>>>>>>> add_to_end.__defaults__
(['Hello', 'there'],) # The defaults are stored within the function.
# If you mutate them, they change.
>>>>>>>>>>>> add_to_end('Boo')
['Hello', 'there', 'Boo']
>>>>>>>>>>>> add_to_end.__defaults__
(['Hello', 'there', 'Boo'],)
```
Of course, mutating a default argument is almost always going to be a mistake, so our best bet is not to use mutable objects as default arguments. If a default argument is mutable, we'll have to exercise caution with it —
we'll have to be sure we never mutate it, never return a reference to it that would allow another part of the program to mutate it, and so on. That's a tall order, so the problem is best avoided altogether.

## Accepting a variable number of arguments

The max function built into Python can be used in two ways:

```
When the function is given a single argument, it's expected to be an iterable, and the function's job is to find the largest element in that iterable.
When the function is given multiple arguments, its job is instead to find the largest of those arguments.
```
How do we write a function like that in Python? To do so, we need a way to specify that the number of arguments can vary. Previously, we saw that we can pass a variable number of arguments into a function by using
iterable unpacking. What if we did that same thing in reverse? In other words, what if we accepted a parameter that re-packed zero or more arguments into something iterable? If we could do that, then we could write
something like this.

```
>>>>>>>>>>>> def maximum(first, *rest):
............ if rest:
............ largest = first
............ else:
............ largest = None
............ rest = first
............ for value in rest:
............ if largest is None or value > largest:
............ largest = value
............ return largest
............
```
In that function, rest is something called a _tuple-packing parameter_. Given that parameter, we can call the function with one or more positional arguments. The first positional argument will be passed into first,
while all of the others will be packed into a tuple and passed into rest.

```
>>>>>>>>>>>> maximum( 1 , 3 , 2 , 5 , 4 , 0 )
5 # We can pass it many arguments. In this case, first = 1
# and rest = (3, 2, 5, 4, 0).
>>>>>>>>>>>> maximum([ 1 , 3 , 2 , 5 , 4 , 0 ])
5 # We can pass it one argument. In this case, first = [1, 3, 2, 5, 4, 0]
# and rest = () (i.e., an empty tuple).
```
This mechanism is the reason why we led off the function's body with if rest. A non-empty tuple is truthy, while an empty tuple is falsy, so if rest is really asking "Were there any arguments other than first?"
If so, we'll start by assuming that first is the largest, then look within rest for something larger; if not, we'll start by assuming nothing about which is largest, then look within first for something larger.

As always, we want to think about some of the sharp corners of what we're learning about. Given the way that a tuple-packing parameter behaves, what do we expect this to mean?

```
def f(a, *b, *c):
```
If we call f, there will need to be at least one argument, with the first argument matched positionally to a and all of the subsequent arguments will be packed into a tuple and matched to b. If that's the case, then what
purpose can c serve here? Isn't it true, by our understanding of this language feature, that c would always have to be an empty tuple? This idea was not lost on the designers of Python, so they rightly made this illegal:
Once you've specified a tuple-packing parameter in a function, you can't specify another.

What if we follow a tuple-packing parameter with additional parameters that aren't packings? In other words, what do we expect this to mean?

```
def f(a, *b, c):
```
This could have theoretically been made illegal, but there's a mechanism available that makes it useful: c could have a value passed via keyword argument. So, rather than this being illegal in Python, it's permissible,
but the only way to pass a value into c would be to pass a keyword argument giving it a value explicitly.

What about default arguments? What do we expect this to mean?

```
def f(a, *b = [ 1 , 3 , 5 ]):
```
While one could make an argument for its legality in Python, defaulting a tuple-packing parameter is not permitted, perhaps mainly because it would be confusing. There's already a well-understood notion of what it
means for b to be "defaulted" when not specified: an empty tuple. Overriding that could be at least as confusing as it might be useful. (There are few hard-and-fast rules in programming language design. It's a
balancing act, in which we trade one characteristic for another — in this case, reducing flexibility a little bit in favor of reducing the potential for confusion.)

## Requiring arguments to be passed via keyword

As you peruse the Python standard library documentation, you'll often find a function with many parameters that allow you to adjust various aspects of how it behaves. It's quite common for most of the parameters to
have default arguments that make them optional, so that when you want the usual behavior, you don't have to say very much, but when you want something less common, you have a way to ask for it. (The finesse in
designing a function like that is making good choices about what the defaults should be, so their values only need to be specified when they're truly out of the ordinary. This requires understanding the problem domain
in which your function resides, as well as people's expectations of the tools you're building, which may differ from your own.)

Some parameters are what we call _keyword-only parameters_ , which is to say that they can only have values passed into them via keyword arguments. There are two ways to require arguments to be passed via keyword
in Python.

```
As we've seen, once you've listed a tuple-packing parameter in a function, all subsequent parameters can only be filled in by keyword arguments.
The special notation * can be used in a parameter list to indicate that you're switching from parameters that can be matched positionally to parameters that can only be matched via keyword.
```
Let's see an example of the second of these.

```
>>>>>>>>>>>> def subtract(n, m, *, minimum = None):
............ difference = n - m
............ if minimum is not None:
............ difference = max(difference, minimum)
............ return difference
............
>>>>>>>>>>>> subtract( 11 , 7 )
4
>>>>>>>>>>>> subtract( 11 , 7 , 0 )
Traceback (most recent call last):
...
TypeError: subtract() takes 2 positional arguments but 3 were given
>>>>>>>>>>>> subtract( 11 , 7 , minimum = 0 )
4
>>>>>>>>>>>> subtract( 11 , 7 , minimum = 8 )
8
```
The * in the parameter list is not actually a parameter; it's simply a way to tell Python that all subsequent parameters must be passed via keyword. It's very common for parameters that follow a * to have default
values, as I've written here, though this is not strictly a requirement.

It's interesting to note that this feature of Python doesn't introduce any new abilities we didn't have already. Had we written the function with the signature def subtract(n, m, minimum = None): (without the
*) instead, we would still be able to call it as subtract(11, 7, minimum = 0). What we've done here is make things illegal that otherwise wouldn't have been, with the goal of making the code written by callers of
our function more readable than it might be otherwise. Our function named subtract with two arguments has relatively unsurprising behavior, subtracting the second argument from the first. Something like
subtract(11, 7, 0) is a lot less obvious without something to indicate what the 0 is supposed to mean. By forcing the 0 to be accompanied by a name, we force that clarity. As programs get larger — and as the
teams that write those programs get larger — this kind of thing becomes vastly more important, so it's worth keeping our eye on it early.

## Requiring arguments to be passed positionally

More recently, in Python 3.8, a similar feature was added: _positional-only parameters_ , which are those that can only be filled in with positional arguments. As with the previous feature we saw, this didn't provide any
new abilities, but instead provided an additional tool to clarify one's design (i.e., to clarify how your functions are to be used, and to require them to be used that way).

If we list a / among a function's parameters, it indicates a transition from positional-only parameters and those that might be filled in some other way. To the left of the /, all parameters become positional-only; to the
right of the /, they might be positional or keyword.

```
>>>>>>>>>>>> def subtract(n, m, /, minimum = None):
............ difference = n - m
............ if minimum is not None:
............ difference = max(difference, minimum)
............ return difference
............
>>>>>>>>>>>> subtract( 11 , 7 )
4
>>>>>>>>>>>> subtract( 11 , 7 , 0 )
4
>>>>>>>>>>>> subtract( 11 , 7 , minimum = 8 )
8
>>>>>>>>>>>> subtract(n = 11 , m = 7 , minimum = 8 )
Traceback (most recent call last):
...
TypeError: subtract() got some positional-only arguments passed as keyword arguments: 'n, m'
```
The two features can be combined, as well, as long as the order is respected; the / must precede the *.

```
>>>>>>>>>>>> def subtract(n, m, /, *, minimum = None):
............ difference = n - m
............ if minimum is not None:
............ difference = max(difference, minimum)
............ return difference
............
>>>>>>>>>>>> subtract( 11 , 7 )
4
>>>>>>>>>>>> subtract( 11 , 7 , 0 )
Traceback (most recent call last):
...
TypeError: subtract() takes 2 positional arguments but 3 were given
>>>>>>>>>>>> subtract( 11 , 7 , minimum = 8 )
8
>>>>>>>>>>>> subtract(n = 11 , m = 7 , minimum = 8 )
Traceback (most recent call last):
...
TypeError: subtract() got some positional-only arguments passed as keyword arguments: 'n, m'
```
## Dictionary-packing parameters

There is one more element of flexibility available in the design of Python functions. Sometimes, we want to write a function that can take any number of arguments, and whose names are also flexible (i.e., what our
function does is at least partly determined by the names of the keyword arguments passed to it). For example, the dict constructor is able to do this:

```
>>>>>>>>>>>> dict(a = 3 , b = 4 )
{'a': 3, 'b': 4}
>>>>>>>>>>>> dict(name = 'Boo', age = 13 )
{'name': 'Boo', 'age': 13}
```
Previously, we saw that we can unpack dictionaries into keyword arguments. The flip side of that feature is _dictionary-packing parameters_ , which accept all of the keyword arguments (other than those already
matched to other parameters), which are packaged up into a dictionary and passed to the parameter. The notation for unpacking a dictionary was led by **, so the notation for packing a parameter into a dictionary is
similar. (By convention, the parameter is normally named kwargs — short for "keyword arguments" — but this is not strictly required. Still, it's a good idea to follow the conventions in one's programming community
unless there's a good reason not to, so we'll follow them here.)

```
>>>>>>>>>>>> def print_all(**kwargs):
............ print(type(kwargs))
............ for key, value in kwargs.items():
............ print(key, value)
............
>>>>>>>>>>>> print_all(a = 3 , b = 4 , c = 5 )
<class 'dict'>
a 3
b 4
c 5
```
As usual, there are a couple of rules that need to be followed:

```
As with tuple-packing parameters, there can be only one dictionary-packing parameter listed in a function's parameter list.
A dictionary-packing parameter must be the last parameter listed in a function's parameter list.
```
Because dictionary-packing is the last step in matching arguments to parameters, all of the rules we've already learned remain intact. Additionally, if there are leftover keyword arguments after matching arguments to
the parameters other than a dictionary-packing parameter, they are collected up into a dictionary and passed to the dictionary-packing parameter. Otherwise, the dictionary-packing parameter will contain an empty
dictionary.

It is less common that you'll need a dictionary-packing parameter than some of the other features we've learned, but particularly as we write functions that are more dynamic — adjusting their behavior at run-time,
behaving very differently depending on the types involved, and so on — they will sometimes be very handy indeed.


