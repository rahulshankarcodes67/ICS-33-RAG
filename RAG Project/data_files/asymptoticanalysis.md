```
ICS 33 Winter 2025 | News | Course Reference | Schedule | Project Guide | Notes and Examples | Reinforcement Exercises | Grade Calculator | About Alex
```
# ICS 33 Winter 2025

# Notes and Examples: Asymptotic Analysis

## Background

One of the things you quickly realize as you study computer science is that there is quite often more than one way to solve the same problem. When you're in a situation like that, you need a way to make a reasonable
choice between them; which solution should you choose? Sometimes, there's a clear-cut winner or loser, with one approach plainly better than another no matter the situation. In most cases, though, it becomes
necessary for us to assess the _tradeoffs_ between the solutions, by understanding the situations in which each one excels and struggles, and then applying your understanding of the situation you're actually in, so you
can make the appropriate choice. Ideally, you apply at least some _quantitative reasoning_ , particularly when your goal is to choose a solution that runs within a certain length of time, or that uses no more than a certain
amount of memory. When choosing between possible solutions, a "gut feeling" or a choice based on which solution you're most comfortable implementing may not be good enough.

Let's consider an example. If you had a list containing a sequence of integers arranged in no particular order and your goal was to sort it into ascending order (i.e., smallest integer first, next-smallest integer second,
and so on), how would you do it? Sorting is a well-understood and well-researched problem, and there are actually lots of known ways to solve it; as of this writing, Wikipedia's page about sorting algorithms lists over
40 different algorithms, some of which were part of the computer science curriculum when I was a student, and others that have been invented in the years since. So, how do you choose one?

One way is to implement various solutions and then test them out on representative sets of input data. The upside of this approach is that you'll get a realistic view of which one is truly the winner, because you'll have
an objective measurement. On the other hand, there are some huge downsides here.

```
You'll need to actually implement the various solutions and test each implementation to make sure it's actually correct, which may be no small feat.
You'll need to make sure you've chosen test data that's representative of reality. A bad choice of test data — one that seems reasonable, but is different from realistic data in some way — could easily give you a
misleading answer.
Your measurement will depend on the lowest-level details of your implementation, maybe at least as much as it does on the approach being taken by the algorithm. This means it might be as much a measurement
of your ability to write performant code as anything else.
```
So, unfortunately, maybe that "objective measurement" won't be so objective after all!

You've no doubt learned, many times over, that writing correct code is not an easy thing to do, so we should prefer not to do it if we can avoid it. Why write 40 or more sorting algorithms just to see which one is the best
for your situation, when all you really need is one of them? Ideally, we'd be able to make a good choice — quantitatively, even! — without ever writing a line of code, so that once we started our implementation, we
would be making useful progress toward our final goal.

What we need, then, is a mechanism for doing this kind of analysis and expressing its result. One very commonly-used approach is called _asymptotic analysis_ , which considers the way some measurement of an
algorithm changes as the size of the problem changes (e.g., How does the amount of time spent sorting a collection of integers grow as the size of the collection grows?). We call this kind of analysis _asymptotic_ , because
it concerns itself mostly with the rate of growth as the problem sizes become arbitrarily large — technically, as they approach infinity (which is where the name "asymptotic" comes from), though we're obviously
concerned, in practice, with problems of finite size, with our emphasis on analysis becoming greater as problems become larger.

## A simple asymptotic analysis

To orient our minds correctly, if you'll indulge me, let's consider a couple of simple algorithms for getting from one side of a rectangular room to another. (They say an algorithm is a "step-by-step procedure"; what
could be more "step-by-step" than walking across a room?)

One obvious algorithm for getting across a rectangular room works like this:

```
start with your back against one side wall, facing the opposite wall
```
```
while you haven't reached the opposite wall:
take one step forward
```
In the absence of any obstacles, this algorithm should be correct in any rectangular room of any size. Sooner or later, you'll reach the opposite wall.

Since we're interested in a quantitative kind of analysis, the important question is how long it takes for the algorithm to run. The answer actually depends on a number of factors:

```
What is the time required for you to take each step?
What distance do you cover with each step you take?
How wide is the room? (In other words, what's the distance from the wall where you started to the opposite one where you finished?)
```
For the sake of keeping the analysis simple, let's assume that every step takes the same length of time, and that every step covers the same distance. Holding these things constant, the important remaining factor is the
width of the room; the wider the room is, the more time it'll take to cross it. In fact, we could draw a graph that expresses the relationship nicely, with the width of the room on the _x_ -axis and the time required to cross it
on the _y_ -axis. That graph would be a diagonal line (i.e., a straight line that grows as we move to the right).

In general, we see that the time it takes to walk across a room is _directly proportional_ to the width of that room. In other words, if we double the width of the room, we'll double the time it takes to cross it; if we
multiply the width of the room by 10, we'll multiply by 10 the time required to cross it. This kind of algorithm is known as a _linear-time_ algorithm (i.e., the time required grows linearly with respect to the size of the
problem).

A second algorithm for getting across a rectangular room comes from science fiction. And, in fact, there's not much "science" here; it's mostly fiction.

```
start with your back against one side wall, facing the opposite wall
press a button on your teleportation device
you'll be disintegrated, and a copy of you will be created, standing just in front of the opposite wall
```
Let's imagine that the teleportation device works in such a way that it takes thirty seconds to build a copy of you on the opposite side wall, regardless of how wide the room is. If we were to graph the time required to
cross the room using our new algorithm, the graph would look different: It would be a horizontal line (i.e., a straight line that doesn't grow at all as we move to the right).

In general, this is what is often called a _constant-time_ algorithm, so called because the time required to solve a problem is constant (i.e., it doesn't change as the size of the problem grows).

Now, the operative question is which of these algorithms is better, and let's say our notion of "better" has only to do with which one takes the least amount of time. (We'll leave aside the philosophical question of
whether the teleported copy of me is actually "me".) And if you think about it, you'll realize that there isn't a clear answer that's right for every room. For smaller rooms that take less than thirty seconds to cross,
walking across the room will be faster. For larger rooms that take longer, teleportation will be faster.

But there is one truth here worth considering. The _growth rate_ of a constant-time algorithm is slower than the growth rate of a linear-time algorithm. What this tells us is that if you consider rooms that are
progressively wider, you will sooner or later be considering rooms wide enough that the constant-time algorithm wins; for all rooms wider than that, the constant-time algorithm will still win. There's a point where the
slower-growing algorithm eventually wins, even if it doesn't win for the relatively narrow rooms.

What we've just done is an asymptotic analysis. In spirit, that's all there is to it.

## What do we do about the small details?

You could imagine that a particular algorithm that solves, say, the sorting problem could be measured against inputs of various sizes, and that it might be possible to describe the algorithm's running time as a function

of the size of the input. You might determine, for example, that the algorithm runs in 3 _n_^2 +4 _n_ +5 milliseconds. And you might determine that, for a different algorithm, the total is _n_^2 +6 _n_ milliseconds instead. Clearly,
given these functions, our two algorithms have different running times for inputs of various sizes. But is there a significant difference between them? Are they similar enough to be considered, more or less, equivalent
to each other? Are they different enough that our analysis needs to be this precise?

Before we answer those questions, let's consider a third algorithm, one that we've determined to run in 1234 _n_ milliseconds to solve the same problem. How different is this one from the others? Which one is fastest?
How does our notion of similarity (or lack thereof) change now that we've added this function to the mix?

First, let's think about it intuitively. What does our understanding of these functions tell us about them?

```
Though the algorithm that runs in 1234 n milliseconds will be slower initially, as n grows, sooner or later it will become the faster one, because the n^2 term in the others will ulimately dominate the 1234 n. Or,
thought differently, the 1234 n algorithm has a slower growth rate than the others, which is the key reason why it's the eventual winner as n grows.
Comparing only the first two algorithms, when n gets sufficiently large, the n^2 term will dominate the others in each algorithm, so these are essentially algorithms that run in (more or less) n^2 and 3 n^2 milliseconds.
One is obviously faster than the other by a constant factor, yet both have the same growth rate (i.e., if you double n , you'll multiply the time it takes to run both of these algorithms by 2^2 = 4).
```
Now let's consider where we might get this level of detail in the first place. In our explanation above, the assumption is that we implemented these algorithms and then measured them. But if our ideal goal is to be able
to do this kind of analysis without first writing any code — so we know whether we're on the right track before we start — then we're not easily going to be able to achieve this level of detail. The distinctions between

1234 _n_ , 1000 _n_ , and 13 _n_ are going to be difficult to deduce without some implementation details. The distinction between 3 _n_^2 +4 _n_ +5 and _n_^2 +6 _n_ will be similarly difficult.

So, the goal should be to leave some of the small details out. What we should be after are less-refined measurements that just tell us a ballpark estimate of how each algorithm behaves, giving us enough information to
compare them broadly, while leaving aside the fine-grained comparisons for cases where we need them. This process is driven primarily by describing the basic "shape" of a function, and by comparing these shapes to
see if they're the same or different. But how do we determine, quantitatively, the basic shape of a function? What does shape mean? The answer to that lies in a kind of mathematically-simplified form called _asymptotic
notation_ , which we'll learn about by focusing on one called _O_ -notation. Asymptotic notations and their corresponding definitions specify an agreement amongst mathematicians and computer scientists about the
general "shape" of a function, so we can all consider the same details to be relevant, while leaving out the others; this way, we're all on the same page.

## O-notation

We can begin to learn about _O-notation_ — sometimes also called _Big O-notation_ — by starting with its definition.

def. We say that _f_ ( _n_ ) is _O_ ( _g_ ( _n_ )) if and only if there are two positive constants, _c_ and _n_ 0 , such that _f_ ( _n_ ) ≤ _cg_ ( _n_ ) ∀ _n_ ≥ _n_ 0

Like a lot of mathematical definitions, this one can seem daunting at first, but it helps if you understand a few details:

```
f ( n ) and g ( n ) are two different functions; in practice, each fills a different role. f ( n ) is the function describing the actual behavior of some algorithm. g ( n ) is a (generally) simpler function that we want to
demonstrate has the same basic shape, i.e., the same basic growth rate.
The definition actually specifies that g ( n ) is an upper bound on f ( n ), ignoring two things (neither of which substantially affects growth rate):
Constant factors — that's what c is for. The functions n , 3 n , and 1000 n all grow at the same rate as n grows, so O -notation does not distinguish between them.
Relatively small values of n — that's what n 0 is for. In practice, it doesn't matter how you solve small problems.
```
So, for example, we might want to know if it's true that 3 _n_ +4 is _O_ ( _n_ ) (i.e., is it true that the functions 3 _n_ +4 and _n_ have, more or less, the same growth rate?). One way to do this is by proving it with the mathematical
definition:

```
f(n) ≤ cg(n) ∀n ≥ n 0
3n+4 ≤ cn ∀n ≥ n 0
```
```
let c = 4 (all we need is a c and n 0 that work)
```
```
3n+4 ≤ 4n ∀n ≥ n 0
```
```
let n 0 = 4
```
```
3n+4 ≤ 4n ∀n ≥ 4
4 ≤ n ∀n ≥ 4 (subtracted 3n from both sides of the inequality)
```
And we're left with an obviously true statement, that _n_ is at least 4 whenever _n_ is at least 4. Thus, it's proven that 3 _n_ +4 is _O_ ( _n_ ).

## Understanding the limitations of O-notation

_O_ -notation gives us a way to ignore lower-level details in favor of a quick, back-of-the-envelope analysis of the growth rate of a function. The quick analysis doesn't give us an exact answer about, say, how long it will
take to run a search of 1,000 elements in a linked list on a particular machine in a particular situation. But it does tell us, in general, that, as the problem size continues to grow, one algorithm would eventually beat
another one (and continue to beat it no matter how much larger the problem got). That's a powerful piece of knowledge to have.

The details that are ignored by _O_ -notation, though, are sometimes precisely the ones you might need, so it's important to understand the ways in which _O_ -notation is limited.

```
If you have two algorithms, one that runs in O ( n^2 ) time and the other that runs in O ( n ) time, and you want to run them on a problem of size n = 500, which one is faster? There's no way, using only O -notation to
know for sure, because O -notation isn't an absolute measurement; it measures asymptotic behavior (i.e., what happens as n grows toward infinity?).
If you have two algorithms, both of which run in O ( n^2 ) time, which one runs faster? Knowing only the O -notations, there's no way to know, because the details required to differentiate are precisely the details that
O -notation ignores.
```
These aren't problems we can fix, necessarily, but they do tell us that our analyses won't always end with an asymptotic analysis; sometimes, we'll need to do more.

Another limitation of _O_ -notation is that, technically, it's allowed to be a gross overestimate. Is it true that 3 _n_ is _O_ ( _n_^2 )? Let's see if we can prove it using the definition.

```
f(n) ≤ cg(n) ∀n ≥ n 0
3n ≤ cn^2 ∀n ≥ n 0
```
```
let n 0 = 1
```
```
3n ≤ cn^2 ∀n ≥ 1
```
```
let c = 3
```
```
3n ≤ 3n^2 ∀n ≥ 1
```
That last statement is certainly true for all _n_ ≥ 1, so it is indeed proven. In fact, we could also prove that 3 _n_ is _O_ ( _n_^3 ), _O_ ( _n_^4 ), _O_ ( _2_ n), and _O_ ( _n_ !), among many other functions whose growth rates are greater than the growth
rate of _n_.

That said, our goal here is to use analysis to convince ourselves and others about fundamental truths regarding algorithms and data structures. There will be no reason to make weaker statements when it's possible for
us to make stronger ones. So, we'll need to agree on how to keep our bounds as tight as we can.

## "Closest-fit" O-notation

Let's suppose we have the function 3 _n_^2 + 4 _n_ + 5. What is an _O_ -notation that expresses this function's shape? Any of these functions would be technically correct, by the definition of _O_ -notation.

```
n^2
3 n^2
1234 n^2
n^2 + n + 1
3 n^2 + 4 n + 5
n^3
n^4
2 n
n!
n n
```
The definition of _O_ -notation boils down to this: If we multiply our "shape" function by any constant we want and consider growing values of _n_ , there is a point beyond which it lies above our original function and stays

there. For any of the functions above, that's true when comparing it to the original function, 3 _n_^2 + 4 _n_ + 5.

So, when we have a choice, we'll make the following agreement. From among the all of the possible _O_ -notations for a given function, the "closest-fit" _O_ -notation is the one that has these three characteristics.

```
It has no constant coefficients (e.g., we'll never say 2 n when we could instead say n ).
It has no lower-order terms (e.g., we'll never say n^2 + n when we could instead say n^2 ).
Of the remaining functions with the first two characteristics, it is the slowest growing (e.g., we'll never say n^3 when we could instead say n^2 ).
```
## Measuring memory

It's important to note that we can use asymptotic notations to describe measurements other than time. If our goal is to measure the use of resources — usually for the purposes of limiting that use — then any resource
we can measure can be considered this way. The most common example you'll see, aside from time, is the usage of memory.

How much memory is required to store a list of _n_ three-digit integers? What does a list in Python look like? Speaking simplistically, a list object in Python will contain two things:

```
An integer indicating how many elements are in the list.
A reference to a block of memory that itself stores references to each element. If there are n objects in the list, there will be (more or less) n of those references.
```
So, how much memory is that? Of course, the answer to this question changes as _n_ changes: If you add more elements to a list, you naturally expect the list to require more memory than it did before. How much more?

```
We'll say that the integer that indicates the list's length requires a constant amount of memory. (This isn't quite true in Python. Since integers can grow arbitrarily large, they can consume arbitrarily large amounts
of memory. But, in practice, numbers less than a few billion fit into essentially the same amount of memory, so, for all practical purposes, the length of a list requires a constant amount of memory.) Let's call this
constant a.
All references are the same size, so the reference to the list's additional memory (where its contents are stored) requires a constant amount of memory. Let's call this constant b.
The list's contents are n of these references, with each taking a constant amount of memory. We've already decided to call that constant — how big is a reference? — b. If there are n of them, then that's a total of
bn.
```
Adding all of that up, we have _a_ + _b_ + _bn_. Don't let the letters fool you, though; we've already decided that _a_ and _b_ are constants, so this is no different in shape from 1 + 2 + 2 _n_. Constant coefficients and lower-order
terms are irrelevant in asymptotic notations (i.e., as _n_ gets large), so we would say that a total of _O_ ( _n_ ) memory is required.

Knowing that we don't need constant coefficients and lower-order terms means we don't need to think about them in the first place. My mental model for answering this question would break down into a few questions
and their answers.

```
Question Answer
```
```
What stays the same as n grows?
```
```
The amount of memory needed to store the list's length.
The amount of memory needed to store a reference to the list's contents.
We can treat these, collectively, as constant.
```
```
What changes as n grows and how does it change?
```
```
The number of references stored in the list.
It grows linearly with respect to n.
(If we multiply n by two, we multiply the number of references by two.)
(If we multiply n by ten, we multiply the number of references by ten.)
This is a linear amount of memory with respect to n.
```
What is a constant amount of memory added to a linear amount of memory? _O_ (1) + _O_ ( _n_ ) = _O_ ( _n_ ). (Why? Because whatever function _O_ (1) represents, it's a lower-order term in whatever function _O_ ( _n_ ) represents.)


