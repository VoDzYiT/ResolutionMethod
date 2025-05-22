# Resolution Method for Propositional Logic
A Python implementation of the basic principle of resolution - building a logical conclusion through contradiction. It is limited only to checking direct contradictions between disjuncts

---
### How to Use
After installing the project you can use the `resolution-cli` command directly from your terminal.

You can also import and use the logic components directly in your Python scripts.

---
### Project structure
- `src` - Contains the source code of the project
  - `logic/` — contains the implementation of logical operations and the resolution method
    - `expressions/` — classes for representing logical expressions (e.g., `Literal`, `And`, `Or`, `Not`, `Implication`)
    - `resolution/` — core logic for applying the resolution method
    - `transformations/` — different functions
  - `tests/` — unit tests for validating the logic operations and resolution process
  - `main.py` — example script demonstrating how to use the resolution algorithm
  - `cli` - contains the command-line interface
    - `cli_app` - the main script for the CLI application.
- `test` -  Unit tests
- `pyproject.toml` - Project metadata and build configuration

---

### What is resolution method

The resolution method is a rule that allows us to derive new logical conclusions by combining clauses that contain complementary literals (like A and ¬A). It uses proof by contradiction: we assume the opposite of what we want to prove, and if that leads to a contradiction, the original statement must be true.
#### A Simple Example
Let’s say we have a sentence:
**“If it is sunny, I will go playing.”**
Suppose today is sunny, and we want to check if it’s logically valid to conclude that **I will go playing**.  
In logic, this whole situation can be represented like:
(sunny → play) ∧ sunny ⊢ play
*(If it is sunny, I will go playing. It is sunny. So, do I go playing?)*

To verify this, we can use the resolution method.

- First, convert everything into CNF (Conjunctive Normal Form):
sunny → play ≡ ¬sunny ∨ play
⊢ play ≡ ¬play (Want to prove play, so we assume ¬play)

And how look our set of clauses:
`[[¬sunny, play], [sunny], [¬play]]`

Resolution steps
We take one clause for example `[¬sunny, play]` and another `[sunny]` and looking for contradiction, in our case this is
`¬sunny` and `sunny` we eliminate them and create a new clause without them `[play]`. After this we repeat this step with
another pair of clauses `[¬play]` and new one `[play]`, this two clauses creates an empty clause `[]` that mean that our
sentence is true and I go playing.

