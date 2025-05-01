```
ICS 33 Winter 2025 | News | Course Reference | Schedule | Project Guide | Notes and Examples | Reinforcement Exercises | Grade Calculator | About Alex
```
# ICS 33 Winter 2025

# Notes and Examples: Context Managers

## Why we need context managers

A very common software requirement is one you might call _automatic wrap-up_ , which is to say that sometimes our programs perform operations where certain things need to be finalized or unwound when the
operations have finished, whether the operations themselves succeeded or failed.

The usual way we introduce this idea to first-year computer science students is to talk about programs that interact with external resources like files, such as in this function that counts the number of lines of text in a
text file.

```
def count_lines_in_file(file_path, encoding = 'utf-8'):
the_file = open(file_path, 'r', encoding = encoding)
```
```
try:
lines = 0
```
```
for line in the_file:
lines += 1
```
```
return lines
finally:
the_file.close()
```
If we succeed at opening the file, we want to be sure that we close the file, even if we weren't successfully able to read the file. (Why is it possible for reading the file to fail? Because it may not be text, or because it may
experience some kind of I/O issue along the way, such as a disk failure or the accidental disconnection of a USB cable.) The function above achieves that goal correctly, if in a somewhat heavy-handed way.

```
Using a try statement with a finally clause to ensure that the file is closed in any circumstance where the file was opened successfully, even if reading the file was unsuccessful.
Opening the file outside of that try statement, so that failure to open the file will not reach the finally, so we won't (erroneously) try to close it if it wasn't opened successfully.
```
Unfortunately, it required some painstaking attention to detail to accomplish something simple: closing the file if (and only if) it was opened. When painstaking attention to detail is required, bugs in our programs
usually follow, a problem that's magnified greatly as programs get larger and teams grow. When a requirement is easy to describe, it should ideally be just as easy to implement.

Perhaps more unfortunately, this is not a rare requirement. That we would want to perform some kind of wrap-up before exiting a function, no matter what caused the function to exit, is a very common requirement.
So, it stands to reason that it ought to have a common, simple solution.

That's why Python provides a feature it calls _context managers_ , alongside a with statement that automates our interactions with them. Their name implies only that the job of a context manager is to "manage a
context," which leaves a lot to the imagination, mainly because they solve many more problems than you might first expect. Despite their intentionally open-ended name, we'll be able to wrap our minds around them
using some examples, and then we'll be in a position to learn how to write our own.

## The "with" statement

In Python, the with statement is used to perform the kind of automatic wrap-up we were talking about in the previous section. Precisely what it means depends on what kind of wrap-up is required, but the underlying
idea is always the same: React automatically when we leave the with statement, whether we're leaving it normally (e.g., because we've fallen out of its scope naturally or encountered a return statement) or because
an exception was raised. This is similar to what the finally clause on a try statement does, with one important difference: Another object, known as a context manager, will automate the details of the wrap-up that
needs to be done, so we won't have to write it ourselves in that same function. This way, instead of that logic being duplicated in many functions — everywhere we need that wrap-up to be done — it can be written once
and used anywhere we need that same kind of wrap-up to be done, solving a kind of problem instead of a problem.

You've likely seen before that the built-in open function has the job of opening a file, and that it returns an object that represents a sort of connection to that file. Interacting with that file object will read from the
underlying file, write to it, and so on. Its close method allows you to close it when you've finished with it, which is an important thing to remember to do, because leaving files open indefinitely can lead to the inability
for other programs to open them, as well as other undesirable outcomes such as output written to the file object not being flushed into the file properly (and, thus, never being written into the actual underlying file).

But file objects have one other ability that's important here. They're context managers, which means that they're able to automate their own cleanup. So, rather than following the pattern we wrote in the
count_lines_in_file, we can instead write this.

```
def count_lines_in_file(file_path, encoding = 'utf-8'):
with open(file_path, 'r', encoding = encoding) as the_file:
lines = 0
```
```
for line in the_file:
lines += 1
```
```
return lines
```
The function has become a little bit shorter, but, more importantly, has also become less error-prone for us to write:

```
We don't need to remember to call close on the file — though, to be fair, we need to remember to write the with statement in the first place. (We still have to realize that cleanup needs to be done; we just don't
need to fiddle with the details of implementing it.)
We don't need to worry about being sure that close is called in cases of both success and failure.
We don't need to be cautious about closing the file when it wasn't opened successfully.
```
Behind the scenes, the with statement automates all of those things, so that all we need to know is this:

```
The call to open returns a file object, which we've stored in the_file.
When we exit from the with statement (for whatever reason), any cleanup that needs to be done will be done automatically, and any that can't be done safely will be skipped.
```
Python's with statement is an example of what is often called _syntactic sugar_ in a programming language. Syntactic sugar doesn't introduce new abilities that can't be achieved in other ways — you can choose to
manually handle these situations using the try..finally technique we used before — but it allows us to express ourselves more succinctly and prevents us from making mistakes.

Structurally, the with statement is a compound statement made up of a few parts:

```
It begins with the keyword with, followed by a context expression , the result of which is an object that acts as a context manager.
In some cases, we might also want to act on the context manager ourselves in the body of the with statement, which is what the as ... syntax lets us do. It stores the object (in this case, the file object) into a
variable whose name we specify (in this case, the_file).
When the with statement is exited, the context manager is notified, including an indication of whether it was exited normally or because an exception was raised.
```
## Other examples of context managers

Files are far from the only example where context managers and the with statement are handy. Other kinds of external resources, such as sockets or HTTP connections, can also act as context managers, with similar
benefits.

```
import socket
import urllib.request
```
```
def receive_message(host, port):
with socket.socket() as download_socket:
download_socket.connect((host, port))
# ...
# The socket will be closed automatically
```
```
def download_file(url):
with urllib.request.urlopen(url) as response:
# ...
# The response object will be closed automatically
```
But it's important to realize that closing an external resource is not the only time that a technique like this is a useful one. Generalizing this idea, what we're really doing when we write a with statement is saying "We'll
be setting something up as we enter the with statement, and we want to be sure it's cleaned up when we exit it." As it turns out, that idea covers a lot of useful territory.

## Automatically checking whether exceptions have been raised

One example arises in Python's unittest library. Suppose we want to write a function called minimum, whose job is to take an iterable of values and return its smallest value. As a first cut, we might write something
like this.

```
def minimum(values):
smallest = None
```
```
for value in values:
if smallest is None or value < smallest:
smallest = value
```
```
if smallest is None:
raise ValueError('Cannot find minimum of empty iterable')
else:
return smallest
```
But, of course, rather than stopping there, we'll want to test it to see if we got the details right. The unittest library gives us the tools to do that job nicely.

```
import unittest
```
```
class MinimumTest(unittest.TestCase):
def test_smallest_of_one_element_is_that_element(self):
self.assertEqual(minimum([ 11 ]), 11 )
```
```
def test_smallest_element_can_be_first(self):
self.assertEqual(minimum([ 1 , 2 , 3 ]), 1 )
```
```
def test_smallest_element_can_be_last(self):
self.assertEqual(minimum([ 2 , 3 , 1 ]), 1 )
```
But then we come to the problem of testing that the function raises an exception when we pass it an empty iterable, such as an empty list. One way to write that test is the longhand way, by catching a ValueError and
turning any other situation into failure. (The self.fail method is a way to force a test method to fail immediately, rather than only if an asserted condition is not met.)

```
def test_cannot_find_minimum_of_empty_iterable(self):
try:
minimum([])
self.fail('Should have raised a ValueError, but did not')
except ValueError:
pass
```
However, what we're really trying to say is something simpler than that: "I assert that this code should raise a ValueError." So, we'd really like to be able to say that in a way that's clearer than what we had to say
above; we'd like the code to look more like what we intend it to mean. For that, we need two things.

```
A container of some kind to hold that code in. It could be a function, but we already have a test method that would otherwise be empty, so a compound statement would be better; in this case, there's no advantage
to having a function within our function, so it would just be needless complexity.
A way to configure that container to tell it what you want it to do: "On the way out, please check whether a ValueError was raised and, if not, make sure the test fails."
```
It's that phrase "on the way out" that's the important one here. That's exactly the kind of problem that context managers were invented to solve! They get notified automatically "on the way out," which gives them a
natural place to do what we're asking them to do. So, how about this instead?

```
def test_cannot_find_minimum_of_empty_iterable(self):
with self.assertRaises(ValueError):
minimum([])
```
The assertRaises method returns a context manager. We've told it, via an argument, that ValueError is the exception that we expect to be raised. We don't otherwise need to interact with the context manager, so
there's no need for us to store it in a variable (e.g., with self.assertRaises(ValueError) as x:), though we could if we wanted to. When the with statement is exited, whether an exception was raised or not,
the context manager will be notified — and it will be told whether an exception was raised and, if so, what its type was. It can check that outcome against the one we told it we expected (a ValueError) and ensure that
the test either succeeds or fails accordingly.

## Temporarily adjusting the global environment

The contextlib module in Python's standard library provides a collection of additional context managers, which solve a wide variety of problems automatically when used in combination with Python's with
statement. Among the problems we can solve with contextlib are situations where we want to make temporary adjustments to something that's otherwise global to our program, where a permanent adjustment
might have broad or unpredictable side effects.

For example, what happens when you call the print function in Python? The short answer is "It prints to the program's _standard output_ ." If we're in the Python shell, for example, we'll see that text printed in the
shell. If I write a function that calls print, what it does depends on the environment it runs in. In the Python shell, it'll print its output to the shell; from an operating system command prompt, it'll print its output
there; and so on.

What if I want to redirect the output printed by my function, but only for a single call to it? This would provide a way to unit test the function — even though it prints output to something global, if I could redirect that
output somewhere else, I could collect it up and test whether it ended up being correct. This might also allow me to reuse a piece of code in a new way that I hadn't imagined when I wrote it, or to repurpose a library so
that it's suitable for a new use beyond its original design.

```
>>>>>>>>>>>> def print_hello():
............ print('Hello Boo!')
............
>>>>>>>>>>>> print_hello()
Hello Boo! # Here, print wrote to the Python shell, as we'd expect.
>>>>>>>>>>>> import contextlib
>>>>>>>>>>>> import io
>>>>>>>>>>>> with contextlib.redirect_stdout(io.StringIO()) as output:
............ print_hello()
............ # Nothing was printed to the Python shell here, because the
# output printed by the print_hello() function was redirected.
>>>>>>>>>>>> output.getvalue()
'Hello Boo!\n' # There's the output from our last call to print_hello!
>>>>>>>>>>>> print_hello()
Hello Boo! # Back to normal automatically!
```
It's that last expression in the Python shell that's the most important one. "Back to normal automatically!" is why a context manager turns out to be a great choice here. That, in a nutshell, is what context managers
ensure.

## Making objects into context managers

Context managers have a special job in Python, so it's not surprising to find out that not all objects in Python are context managers. For example, strings have the job of storing a sequence of text characters, but that's
where their job ends. There's nothing special to unwind or clean up when we're finished with them; the memory where the characters are stored is made available when they're destroyed (as when any object in Python
is destroyed), and we don't much care whether that happens immediately or a little later, as long as it happens eventually. But there's nothing else to close, destroy, or undo; when the string has died, that's the end of
the story.

Because strings are not context managers, we wouldn't expect to be able to use them in the expression at the top of a with statement. What happens if we try it?

```
>>>>>>>>>>>> with 'Boo' as name:
............ print(f'Hello {name}!')
............
Traceback (most recent call last):
...
TypeError: 'str' object does not support the context manager protocol
```
As we expected, an exception is raised. But the details are curious. A TypeError is raised, explaining rather opaquely that strings don't support something called the _context manager protocol_. As it turns out, the
with statement can interact with many different kinds of objects, including objects of types that we write (which, if we write one today, didn't exist when the Python interpreter was written). Because of that, there
needs to be an agreement about the details of that interaction. What does a with statement do with the value of the expression we write on its top line? What does it do when we exit the with statement normally?
What if an exception is raised instead? The context manager protocol defines the answers to those questions. So, how does an object support it?

## Protocols in Python

You may have seen before that the design of Python programs relies on a technique that's sometimes called _duck typing_ , which is how it decides what we can and can't do with an object. The term "duck typing" comes
from an old saying that insinuates that "if a bird walks like a duck and quacks like a duck, it's a duck," meaning that we can deduce what something is — or at least some aspect of what something is — based on what it
can do.

In Python, that idea arises whenever we access an attribute of an object. Let's say we have a variable named x and we call a method on it, such as x.do_things(1, 2, 3). Under what circumstances are we allowed
to call do_things on x and pass it three integer arguments?

```
Whenever the class has a method named do_things that has four parameters: self and three additional ones.
Whenever the class has a method named do_things that has a self parameter and a tuple-packing parameter (into which we could pass three integers).
Whenever the object has an attribute do_things that stores a function that takes three parameters, or some other combination of parameters that can accept three arguments (such as one positional parameter
and one tuple-packing parameter).
Whenever x is a module that has an attribute named do_things that is a function that can be called with three arguments.
```
This is a pretty open-ended set of possibilities; the dynamic nature of Python allows for a great deal of flexibility, at the cost of having to find a way to manage that flexibility. (Too little flexibility leads us to write
multiple copies of the same code that are only subtly different. Too much flexibility leads us to have trouble reasoning about the meaning of our code, since it can mean so many different things. What is "too little" and
what is "too much" is larger a matter of taste, and one's taste evolves as one's experience grows and it becomes clear which techniques are helpful and which are confusing.)

As a means of managing that flexibility, the design of Python includes a number of _protocols_ , which specify the details of how classes and objects can provide a common set of attributes for solving the same kind of
problem. If we all agree on those attributes, then we can use those classes and their objects interchangeably.

I should point out here that you've encountered this idea previously, even if you didn't see it in precisely these terms. For example, when objects are created in Python, they're _initialized_ , so that their necessary
attributes can be created and have values stored in them right from the get-go. But if we write a class Person tomorrow, how can the Python interpreter — which was written, released, and installed on our computer
before we wrote our Person class — magically know how to initialize objects of our new class? Of course, the answer is that it doesn't need magic at all; it just needs us to follow its protocol for initialization, by
providing an __init__ method.

```
>>>>>>>>>>>> class Person:
............ def __init__(self, name):
............ self.name = name
............
>>>>>>>>>>>> p = Person('Boo')
>>>>>>>>>>>> p.name
'Boo'
```
That's all a protocol is in Python: "If you provide these attributes that have the following characteristics, here's what will be done with them and here's when." In the case of initialization, the rule is (roughly) that the
__init__ method will be called, and any arguments passed to Person's constructor will, in turn, be passed (along with the new object, which will be passed to the self parameter) to our __init__ method.

So, if we want to understand how to make our objects compatible with Python's with statement, we'll need to know the details of the protocol that it relies on. Since the with statement provides functionality that you
might call _context management_ , its protocol is known as the _context management protocol_. (It's worth noting that the error message referred to the differently named context manager protocol; in most parts of the
Python documentation, it's referred to as the context management protocol. Either way, we're talking about the same thing.)

## The context management protocol

Conceptually, the with statement provides two capabilities:

```
It knows how to be entered , which is done as control enters a with statement — after the context expression is evaluated, but before any of the code in the with statement's body is executed.
It knows how to be exited , which is done automatically when the scope of the with statement is exited (either normally or because an exception was raised).
```
In support of those two capabilities, context managers are required to provide two corresponding dunder methods.

```
__enter__(self), which is called just as the with statement is being entered. Whatever it returns is the value that would be stored in the context variable x if the top line of our with statement ends with as
x. (More often than not, __enter__ returns self, but it's not required to.)
__exit__(self, exc_type, exc_value, exc_traceback), which is called when the with statement is exited. If the exit was normal (i.e., because we left the scope of the with statement without an
exception being raised), exc_type, exc_value, and exc_traceback will each have the value None. If the exit was because an exception was raised, exc_type will specify the type of the exception,
exc_value will specify its error message, and exc_traceback will contain its traceback; in that case, returning True from __exit__ will cause Python to suppress the exception so that it does not propagate
any further.
```
Suppose, instead, that we have the following module, containing a class called ExampleContextManager.

**_context_example.py_**

```
class ExampleContextManager:
def __init__(self, value):
print('Initializing')
self.value = value
```
```
def __enter__(self):
print('Entering')
return self
```
```
def __exit__(self, exc_type, exc_value, exc_traceback):
if exc_type is None:
reason = 'normally'
else:
reason = f'because of an exception of type {exc_type.__name__}'
```
```
print(f'Exiting {reason}')
```
If we execute that module, can we then use an ExampleContextManager in a with statement? Let's find out.

```
>>>>>>>>>>>> with ExampleContextManager('Boo') as context:
............ print(context.value)
............
Initializing
Entering
Boo
Exiting normally
```
So far, so good. The output is what we'd expect, once we understand the protocol:

```
First, the ExampleContextManager object is created, which means that its __init__ method is called to initialize it. 'Boo' is stored in the object's value attribute. Additionally, Initializing is printed.
Next, the __enter__ method is called on our ExampleContextManager object, per the context management protocol. That's why Entering is printed. Since the __enter__ method returns self (i.e., the
ExampleContextManager we called it on), the context variable refers to our ExampleContextManager object.
After that, we enter the body of the with statement, which prints the value attribute of context. Since context is our ExampleContextManager and its value attribute is 'Boo', Boo is printed.
Finally, we leave the body of the with statement, without an exception having been raised. The __exit__ method is called on our ExampleContextManager object, with its exc_type, exc_value, and
exc_traceback parameters all having the value None. So, it prints Exiting normally.
```
How is it different when an exception is raised from the body of a with statement instead? Let's see.

```
>>>>>>>>>>>> with ExampleContextManager( 13 ) as context:
............ print('In with statement')
............ raise ValueError('This is not cool')
............ print('Still in with statement')
............
Initializing
Entering
In with statement
Exiting because of an exception of type ValueError
Traceback (most recent call last):
...
ValueError: This is not cool
```
The mechanics are what we would expect: The context manager is created, initialized, entered, and exited with an exception. Since the expression wasn't suppressed by __exit__ returning True, it continued
propagating normally, which is why we see its traceback in the Python shell.

## Finding out more about context managers (Optional)

Programming languages and their standard libraries tend to evolve over time, as the community of its users discovers where common pain points lie, and as changes in the broader technology community turn niche
requirements into everyday needs. However, that evolution doesn't take place in a vacuum. New features add complexity, which means that the language gradually becomes more difficult to learn and use. When
language features aren't designed carefully, they can interact with existing features in sometimes surprising ways, or, in the worst cases, simply not work with existing features at all. But, once a language feature has
been added and many users are depending on it, changing it later is even more painful — because it's best for a program that works in Python 3.13 to be (more or less) guaranteed to work the same way in Python 3.
and beyond — so we tend to be stuck with all but the most problematic decisions in the long run. So, it's obviously best to get these things right the first time.

Particularly when a programming language has a large user community, there's value in establishing a process by which proposed changes can be discussed and evaluated. By subjecting an idea to the rigorous scrutiny
of many experts, the odds are pretty good that someone will notice a potential problem, someone else will figure out a way to work around it, and still other people will make suggestions that improve the idea still
further. By the time the proposal emerges from the process, it will have the best chance to successfully stand the test of time.

Python's evolutionary process is centered around Python Enhancement Proposals (PEPs). Someone writes a PEP and submits it for consideration and discussion among the community ensues. Sometimes, the PEP is
adjusted in response to issues raised during the discussion. Other times, the PEP is rejected outright — some ideas simply aren't considered to be "Pythonic." If consensus is achieved, the PEP will be finalized and
implemented in a version of Python.

While it's been many years since context managers were added to Python (which happened around 2006), you might find value in reading PEP 343, which introduced the idea of the with statement, including a
detailed explanation of how the with statement was proposed to behave. It also describes some of the history around the proposal, including links to a few other PEPs that were aimed at a similar problem, but
ultimately withdrawn in favor of PEP 343, along with comparisons of these proposed techniques.

The details of PEP 343 aren't part of this course — I'm not requiring you to understand context managers and the with statement any further than I've presented here — but if you want a glimpse into how
programming languages are designed, it's an interesting read. One of the lessons you might gather from it is how human the process is. In the end, it's people with both similar and differing needs coming together,
discussing and refining possible solutions, giving up some things to get others in return, and then coming to an agreement in the end about how to move forward. This is a microcosm of how real-world software is built.


