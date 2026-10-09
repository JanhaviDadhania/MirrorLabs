oh. so there is no loose thread. positive numbers negative numbers and irrational numbers and complex numbers complete the whole number thingy

For solving equations, yes. Every polynomial equation has all its roots in the complex numbers, so that thread is closed. But the number story has other loose threads.

1. Going up in dimension. You can build bigger number systems, but each step costs a rule:

┌───────────────┬───────────┬──────────────────────────────────────────────────────┐
│    System     │ Dimension │                    What you lose                     │
├───────────────┼───────────┼──────────────────────────────────────────────────────┤
│ Real ℝ        │ 1         │ (ordering is lost in the next step)                  │
├───────────────┼───────────┼──────────────────────────────────────────────────────┤
│ Complex ℂ     │ 2         │ you can no longer say which of two numbers is bigger │
├───────────────┼───────────┼──────────────────────────────────────────────────────┤
│ Quaternions ℍ │ 4         │ order of multiplication matters: ij = k but ji = −k  │
├───────────────┼───────────┼──────────────────────────────────────────────────────┤
│ Octonions 𝕆   │ 8         │ grouping matters: (ab)c ≠ a(bc)                      │
└───────────────┴───────────┴──────────────────────────────────────────────────────┘

After 8 dimensions, division itself breaks. Hurwitz's theorem says there are exactly these four. Quaternions are used in practice to rotate 3D objects in games and robotics.

2. A completely different way to complete the rationals: p-adic numbers. The real numbers fill the gaps between fractions using ordinary distance. If you instead call two numbers "close" when their difference is divisible by a high power of p, you get the p-adic numbers. Ostrowski's theorem says the reals and the p-adics are the only two ways to do this. In the p-adics, 1 + 2 + 4 + 8 + … = −1 is literally true (for p = 2). Their geometry is fractal: each "ball" splits into p smaller balls, forever, like a Cantor set.

3. Infinitely small and infinitely large numbers. Hyperreal numbers add true infinitesimals, which make "dx" rigorous. Surreal numbers contain every real number, every infinity, and every infinitesimal in one ordered system.

4. Loose threads inside the real numbers.
- Almost all real numbers are transcendental: they aren't the root of any polynomial with integer coefficients, as π and e aren't. Yet proving that a specific number is transcendental is very hard. Nobody knows whether π + e is even irrational.
- Almost all real numbers are uncomputable: no program can print their digits. The numbers you can ever write down are a set of measure zero.

A bridge to your Wada idea: computers use neither the reals nor the rationals but float32, a finite grid. Ly & Gong's one-bit test flips the last bit of that grid. If basin boundaries are fat fractals (c > 0), then which basin a start lands in is not set by the real-number starting point at all. It is set by digits the machine can't represent. That is a real loose thread: is training even well-defined on ℝ, or only on the float grid?

---

so i can write all whole numbers right? all whole numbers are computable. ?

Yes, every whole number is computable. Pick any one, however big, and you can write it down. You'll finish, because it has a last digit.

Fractions are computable too. 1/3 = 0.3333… goes on forever, but it follows a rule ("keep writing 3"), and that rule is the recipe.

You do need two words, though: one at a time. You can write any whole number, but not all of them at once, because they never run out. Still, they come in a list: 1, 2, 3, and so on. That's why each one can be reached.

The uncomputable numbers only show up among infinite decimals that follow no rule at all.

ok. so instead of saying that most of real numbers are not computable i would have understaodod better if you had said that all irrational numbers are un computable and most of real numbers are irrational numbers.

That's close, but one piece doesn't hold. √2 and π are irrational, and they are computable. Their digits never end and never repeat, but there's a rule that produces them, so a computer can keep printing digits forever.

So there are three groups:

- Rational numbers (whole numbers and fractions) are computable. Their digits end or repeat.
- Irrational numbers that follow a rule, like √2, π and e, are also computable. Their digits never repeat, but a recipe exists.
- Irrational numbers with no rule at all are the uncomputable ones.

The last group is almost all of the number line. So "irrational" means the digits never repeat, and "uncomputable" means no rule produces them. Every uncomputable number is irrational, but some irrational numbers are computable.

---

maybe there is a way to generate all numbers but we just don't know the process. I am sure every year we are finding few more numbers whose method is being known to us

Part of what you're saying is true. People do find new recipes. But that doesn't make the uncomputable numbers smaller, and it's not because we haven't been clever enough yet. It comes from counting.

Any process, whether we know it today or find it in a thousand years, has to be described in words or code. Every description is a finite piece of text. So all possible processes, including undiscovered ones, can go in one long list, sorted by length and then alphabetically.

Now use the trick from before. Take the number made by the first process and change its first digit. Take the number made by the second process and change its second digit. Keep going. The number you build differs from every process's number somewhere, so no process makes it, not even one we haven't found yet.

So when someone finds a new recipe, that number was computable all along. They found its recipe; it didn't switch groups. The list was already complete, and it was already too short.

One example that might interest you: mathematicians have defined a specific number, called Chaitin's Omega. It's roughly "the chance that a random computer program eventually stops." It's a real, well-defined number, and it's proven that no process can ever compute its digits. You can point at it, but you can't write it out.

---

what is chaitin's omega?

Chaitin's Omega is the chance that a random computer program eventually stops.

Imagine writing a program by flipping a coin: heads is 1, tails is 0, and you keep flipping until you have a complete program. Then you run it. One of two things happens:

- it finishes and stops, or
- it runs forever and gets stuck in a loop.

Omega is the probability that it stops. So it's a number between 0 and 1, something like 0.0078…, and it's perfectly well-defined.

Why nobody can compute it. Back in 1936, Alan Turing proved there's no general method to tell whether a program will stop or run forever. You can watch it run, but if it hasn't stopped yet, you never know whether it's about to stop or never will. This is called the halting problem.

Omega packs the answers to the halting problem into its digits. If you knew the first 100 digits of Omega, you could tell, for every program up to about 100 bits long, whether it ever stops. Here's why:

- Run all of those programs side by side.
- Each time one stops, add its share of probability to a running total.
- Once the total reaches the value those 100 digits give, nothing short can still stop, because there's no probability left over. Every program that hasn't stopped yet runs forever.

But Turing showed the halting problem can't be solved. So the digits of Omega can't be computed, by any process, ever.

Two strange things about it:

- Its digits look perfectly random. No pattern and no shortcut: knowing some digits tells you nothing about the next ones.
- It's not one single number. It depends on which programming language you use, a bit like how a word's spelling depends on the language. But for every language, it's uncomputable.

People have worked out the first few dozen digits for one specific, simple language. Beyond that, the digits are true facts that can never be known. Omega is a number you can point at but can never write out.
