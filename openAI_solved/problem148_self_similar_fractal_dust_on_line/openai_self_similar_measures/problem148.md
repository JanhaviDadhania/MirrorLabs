# Problem 148: The dimension formula for self-similar measures on the line

Source: OpenAI Research Catalog, entry 148. Notes from a working conversation, pasted verbatim.

---

tell me in simple words first what the problem 148 is. Is it talking about fractals(becasue i saw self similar), or entropy or geometry or something else. help me get onbaord with the problem. no wall of text, keep it showrt and wait for me to ask questiosn
1 skill available

#148 is about all three: fractals, entropy and geometry. They fit into one formula.

The setup: take a few maps that each shrink the line by some factor, say "multiply by 1/3" or "multiply by 1/3 and add 2/3". Pick one at random, apply it, then pick again, forever. The points you land on form a fractal dust. That dust is "self-similar" because each piece is a shrunken copy of the whole. The measure is how much probability mass sits on each part of it.

The question: what is the dimension of that dust? Is it a thin Cantor-like set (dimension below 1), or does it fill the line?

The answer: dim = min{1, h/χ}.
- χ is how fast things shrink per step, as an average of log(contraction).
- h is how much new information each random choice gives you, as an entropy per step.
- So dimension is information gained per step divided by shrinkage per step.

Why it's hard: if the maps overlap exactly, some different choice sequences land on the same point, so the entropy overcounts. The result says the formula still holds when you count entropy correctly. Earlier work needed the maps to be well separated.

---

let's take an example and understand what h and x is. take a toy example and expalin. use diagrames to help me. if there is coin flip ask me, I will tell you what came. you give initial line first, i iwll flip coin and then show me the updated. do not give entire toy example at once. let's do this together

Let's build it step by step.

Toy setup: the line is [0, 1]. We have two maps:
- Heads (H): x → x/3 (squeeze into the left third)
- Tails (T): x → x/3 + 2/3 (squeeze into the right third)

Each one shrinks the line by a factor of 1/3.

Start (step 0):

```
0                                   1
|===================================|
        the whole line [0,1]
```

You will flip a coin and I will apply the matching map to the whole line.

Flip #1: heads or tails?

✻ Baked for 6s · done 5:13 PM

❯ tails

Tails means x → x/3 + 2/3, so the whole line gets squeezed into the right third.

```
Step 0:  0                                   1
         |===================================|

Step 1:  0           1/3         2/3         1
         |            .           |=========|
                                  [2/3 , 1]
```

The line is now 1/3 as long as before. That shrink is the χ part: each step multiplies the length by 1/3, so the log-shrink is ln(1/3) in size, or ln 3 ≈ 1.10 per step.

You also made a choice. With 2 equally likely options (H or T), your flip carried 1 bit of information, or ln 2 ≈ 0.69 in natural units. That is the h part.

Flip #2: heads or tails? This one gets applied to the piece we have now.

✻ Cogitated for 6s · done 5:13 PM

❯ heads

Heads means x → x/3, applied to the piece [2/3, 1]. It lands in the left third of that piece.

```
Step 0:  0                                   1
         |===================================|

Step 1:  0           1/3         2/3         1
                                  |=========|

Step 2:  0           1/3         2/3   7/9   1
                                  |===|
                                [2/3 , 7/9]
```

The new interval is [2/3, 7/9], with length 1/9. Two flips, so the length has shrunk by 1/3 twice.

Running totals after 2 flips:
- Shrinkage: 2·ln 3 ≈ 2.20
- Information from choices: 2·ln 2 ≈ 1.39

Both grow by one step's worth per flip. Their ratio stays fixed at ln 2 / ln 3 ≈ 0.63.

That ratio is h/χ, and it is the dimension: dim ≈ 0.63. A line has dimension 1, so this dust is thinner than a line. It is the classic Cantor set.

Question for you: why do you think the ratio is below 1? (Hint: look at how many pieces you could choose from vs. how much each one shrank.)

✻ Cogitated for 6s · done 5:13 PM

❯ how did we get information as .69 and 1.39 in these two times? I did nto understand. what is the formula, how do yo uget it. help me see it.

Formula: information of one choice = ln(number of equally likely options).

You have 2 options (H or T), so one flip gives ln 2 = 0.69.

Why ln? Count the possible histories. Each flip doubles the count, and ln turns "doubling" into "adding":

```
0 flips:  1 history                    ln 1 = 0
1 flip:   H, T                         2 histories   ln 2 = 0.69
2 flips:  HH, HT, TH, TT               4 histories   ln 4 = 1.39
3 flips:  HHH, HHT, ... (8 of them)    8 histories   ln 8 = 2.08
```

ln 4 = ln 2 + ln 2 = 0.69 + 0.69 = 1.39. Each flip adds 0.69, which is why I wrote 2·ln 2.

In plain words: the information is how many yes/no questions it takes to pin down your flips, measured in a ln scale. Two flips have 4 possible outcomes, so you needed 2 bits, which is 2·0.69 = 1.39 in ln units. If you use log base 2, it comes out as exactly 1 bit per flip.

Same trick for shrinkage: after 2 flips the interval is 1/9 long, and ln 9 = 2.20 = 2·ln 3.

So both are just logs of a count or a size, and each flip adds one step's worth.

Does that make sense? Next, I can show why the ratio ln 2 / ln 3 is the dimension, using the count of pieces.

✻ Cooked for 8s · done 5:18 PM

❯ does each unique flip sequence map to one unique line on x-axis with unique x1 and x2? if that is there then we ca nlook at a line and tell what the flip sequences were

In our toy, yes. Each flip sequence gives its own interval, and no two overlap, so you can read the sequence back from the interval.

Step 2, all 4 sequences:

```
0    1/9  2/9  1/3          2/3  7/9  8/9  1
|====|    |====|              |====|    |====|
 HH   (gap) HT                 TH   (gap) TT
```

Check with ours: we flipped T then H and got [2/3, 7/9]. That is the TH slot. Reading it backwards, the interval sits in the right third (so the first flip was T), and inside that, in the left part (so the second was H).

The gaps are why this works. The two maps put their pieces in the left third and the right third, with the middle third left empty, so the pieces never touch. This is the "well separated" case.

Where #148 comes in: change the maps so the pieces overlap. For example, make both maps shrink by 1/2 and put the pieces at [0, 1/2] and [1/4, 3/4].

```
H piece: |========|
T piece:     |========|
             ^^^^ overlap
```

A point in the overlap can come from H-then-something or T-then-something, so you can no longer read the sequence off the interval. Counting information as ln 2 per flip then overcounts, because some sequences are indistinguishable. That is exactly the problem #148 solves.

Want to go into the overlap case next, with a coin flip each time?

✻ Churned for 7s · done 5:23 PM

❯ i see. then there will be multiple sequences mapping to same line segment. a

Yes, that's the core of it: several sequences can land on the same segment, so the sequence can't be read back from where you ended up.

Your message cut off after "a". What were you going to add?

If you want to continue, here is a concrete case to see it with:

```
H: x → x/2          piece [0, 1/2]
T: x → x/2 + 1/4    piece [1/4, 3/4]
```

Take two sequences, HT and TH:
- HT: apply H, then T on that piece. Result is [1/4, 1/2] shrunk... we'd compute it together.
- TH: apply T, then H.

Both land on the same interval, even though the flips differ. So 4 sequences at step 2 collapse into fewer than 4 distinct intervals, and the true information is less than 2·ln 2.

Shall we flip coins and find that collision by hand?

✻ Cogitated for 6s · done 5:23 PM

❯ wehre does information gain comes in to picture here?

The information gain is how much the final position tells you about your flips. In the separated case, the interval tells you everything, so you gain the full ln 2 per flip. In an overlapping case, the interval tells you less, so the real gain is below ln 2 per flip. That real gain is the h in the formula.

Correction: my last message was wrong. HT and TH do not land on the same interval for those maps. Computing it properly (first flip applied first):

```
H: x → x/2        T: x → x/2 + 1/4

HH: [0,   1/4]
TH: [1/8, 3/8]
HT: [1/4, 1/2]
TT: [3/8, 5/8]
```

These four intervals are all different, but they partly overlap: TH overlaps HH and HT, and HT overlaps TT. A point in an overlap, say x = 0.3, could have come from TH or HT. So you can no longer read the flips back from the position, and the information about the flips that the position carries is less than 2·ln 2.

Exact collisions, where two sequences give the identical interval, also happen for some choices of maps. These maps just aren't one of them.

Shall we flip a coin and track one point through this to see where it becomes ambiguous?

✻ Cogitated for 14s · done 5:24 PM

❯ I understand things will start to become ambiguous. with more flips will it increase or it can stay same?

Both can happen, depending on the maps.

- Separated maps (our first toy): ambiguity stays at exactly 0 forever. Every sequence keeps its own interval.
- Overlapping maps: the total ambiguity usually keeps growing as you add flips. It grows roughly in proportion to the number of flips, because every new flip can create fresh overlaps.

---

I understand things will start to become ambiguous. with more flips will it increase or it can stay same?

Both can happen, depending on the maps.

---

In our first toy (H: x → x/3, T: x → x/3 + 2/3, fair coin):

χ (shrinkage rate): the average of ln(1/ratio) per flip.
- Both maps shrink by 1/3, so every flip contributes ln 3.
- χ = ln 3 ≈ 1.10
- If the maps had different ratios, you would average them using the flip probabilities. That is why the definition says "average logarithmic contraction".

h (entropy rate): the information per flip that the final position actually keeps.
- The maps are separated, so nothing is lost and each flip keeps its full ln 2.
- h = ln 2 ≈ 0.69
- For a fair coin, h = ln 2. For a biased coin, h = −p ln p − (1−p) ln(1−p), which is smaller. That is the "entropy rate of random composed maps" in the statement.
- With overlaps, h drops below that, because the position can't tell some sequences apart.

Dimension: dim = min{1, h/χ} = min{1, 0.69/1.10} = 0.63.

---

so what the question was that got solved? in very simpler words ?

The question: "Is the dimension of this dust always information per flip divided by shrinkage per flip, even when the pieces overlap?"

What was known:
- When the pieces are kept apart, the answer was yes. You can read the flips back from the position, so h is just the coin's entropy.
- When they overlap, nobody could prove it in general. Overlap loses information, and it was unclear whether the formula still held, with h counted as the information that survives.

What got solved: it holds in every case on the line, including exact overlaps and different shrink ratios. The only change is that h is the entropy of the random composed maps. So the dimension is always min{1, h/χ}.

Why it matters: you can predict the size of a fractal from two numbers, how fast it shrinks and how much information each step keeps. You don't have to measure the fractal itself.

---

no no. in general. what is dimension?

Dimension is how fast the "amount of stuff" grows when you zoom in.

Cover the shape with small boxes of size s and count how many boxes N you need. Then:

N ≈ (1/s)^dim, or equivalently dim = ln N / ln(1/s).

Check with familiar shapes. Shrink the box size by 10×:

```
Line     (length 1):   need 10 times more boxes    -> 10^1  -> dim 1
Square   (area):       need 100 times more boxes   -> 10^2  -> dim 2
Cube     (volume):     need 1000 times more boxes  -> 10^3  -> dim 3
```

---

c

so what is the dimension of our line? .63?

No. Two different things:

- The starting line [0, 1] has dimension 1. It is a solid line.
- The dust we get after infinitely many flips has dimension 0.63. Each flip cuts away the middle third, so you are left with a thin set of points.

```
Step 0:  |===================================|   dim 1 (solid)
Step 1:  |===========|           |===========|
Step 2:  |===|   |===|           |===|   |===|
Step 3:  ...keep cutting...
Limit:   dust of points                          dim 0.63
```

Our two flips so far, T then H, gave the interval [2/3, 7/9]. That is still a small solid piece. It is one step along the way to the dust, and each further flip zooms into a smaller piece of it.

So the 0.63 describes the final limit shape, the set of all points you can reach with infinite flip sequences.

✻ Crunched for 6s · done 5:32 PM

❯ how does step 1 has two lines? we had only one

Good catch. Two different pictures got mixed.

- Your actual run: one sequence, one interval. After T you had [2/3, 1], after H you had [2/3, 7/9]. One piece each step.
- My diagram: it showed all possible outcomes at once, so step 1 had both the H piece (left) and the T piece (right).

```
Your run (one coin sequence):
Step 1:                          |=========|        only T happened
Step 2:                          |===|              then H

All possible runs (the dust picture):
Step 1:  |=========|             |=========|        H or T
Step 2:  |==|  |==|             |==|  |==|          HH HT TH TT
```

The dust is the set of all places that some infinite flip sequence could end up. Your single run just follows one branch of it, shrinking toward one single point of the dust.

So 0.63 is the dimension of the full tree of possibilities, not of your one path. Your path alone ends at a single point, which has dimension 0.

---

so we are always talking about infinite flip sequence? we will end up with line minues some points. right?

Infinite sequences, yes. But the leftover is the other way around: we end up with a few points, not a line minus a few points.

- Line minus some points would be almost everything left. That has dimension 1.
- Our dust removes almost everything and keeps almost nothing. Each flip throws away the middle third of what remains, so what survives has length 0 and dimension 0.63.

```
Length left after n cuts:  (2/3)^n  ->  0
```

The dust is still uncountably many points (one for each infinite H/T sequence), but they take up zero length.

Examples of points in the dust: 0 (HHHH...), 1 (TTTT...), and 1/4 (TH TH TH...). A point like 1/2 is in the middle third, so it was removed at step 1.

The same flip sequence always gives the same point, and different infinite sequences give different points in the separated case. So the dust is a map of all possible infinite coin histories laid out on the line.

✻ Worked for 6s · done 5:34 PM

❯ so people didn't know what the dimension of the dust was? what that the question? is there wikipedia page? any main stream pages I can see to get confidence that htis was the problem in maths and peopel were tryign to solve.

Partly. People knew the answer for the nice case. The open question was the overlapping case.

- Cantor dust (our toy): the dimension ln 2 / ln 3 has been known for over a century. It is not the problem.
- Known theorem: if the pieces don't overlap (the "open set condition"), the dimension is the simple formula from the shrink ratios. This is textbook.
- The open problem: if the pieces overlap, the dimension is only known to be at most min{1, h/χ}. Everyone expected it to be equal, and that was open for decades. A classic test case is Bernoulli convolutions: random sums ±1 ± λ ± λ² ± ... for different λ. It is a famous problem in fractal geometry.
- Main earlier results: Hochman (Annals of Mathematics, 2014) proved it under an "exponential separation" condition. Shmerkin and Varjú proved related results on Bernoulli convolutions.

Where to read: search Wikipedia for "Bernoulli convolution", "Self-similar set", "Hausdorff dimension" and "Open set condition". For the research side, search for "Hochman self-similar sets with overlaps inverse theorems for entropy" on arXiv.

Confidence caveat: I'm giving the background from memory, and I haven't checked it online in this session. The claim that #148 fully settles the overlap case comes only from OpenAI's catalog. I haven't seen the proof, and it is not independently confirmed. Treat it as a claim until experts review it.

I can run a web search now to check the Hochman and Bernoulli convolution details. Want me to?

✻ Crunched for 12s · done 5:35 PM

❯ everyone expected it to be equal to what?

Equal to min{1, h/χ}, the formula itself.

What was proven before: the dimension is at most min{1, h/χ}. That direction is easy, because the information that survives can't exceed the information you put in, so you can't need more pieces than that.

What everyone expected, and what was open: the dimension equals min{1, h/χ}, so the formula is exact and not just an upper bound.

```
Known:      dim  ≤  min{1, h/χ}
Expected:   dim  =  min{1, h/χ}      <- #148 claims this, with no separation assumption
```
