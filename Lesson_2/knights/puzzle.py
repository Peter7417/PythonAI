from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Known logic that a character cannot be assigned two roles and can only be a Knight or a Knave
    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),

    # Given that A says it's both:
    Biconditional(AKnight, (And(AKnight, AKnave))),
    Biconditional(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Known logic that a character cannot be assigned two roles and can only be a Knight or a Knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # Given that A says both A and B are Knaves:
    Biconditional(AKnave, Not(And(AKnave, BKnave))),
    Biconditional(AKnight, (And(AKnave, BKnave)))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Known logic that a character cannot be assigned two roles and can only be a Knight or a Knave
    Or(AKnight,AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # Given that A says both A and B are of the same roles:
    Biconditional(AKnave, Not(Or(And(AKnave,BKnave), And(AKnight, BKnight)))),
    Biconditional(AKnight, (Or(And(AKnave,BKnave), And(AKnight, BKnight)))),

    # But B says that they are of different roles:
    Biconditional(BKnave, Not(Or(And(AKnave,BKnight), And(AKnight, BKnave)))),
    Biconditional(BKnight, Or(And(AKnave,BKnight), And(AKnight, BKnave)))
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Known logic that a character cannot be assigned two roles and can only be a Knight or a Knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # Given that A could be either a Knight or a Knave:
    Or(
        # If A is a Knight  (will result True from truth table):
        And(Biconditional(AKnave, AKnave), Biconditional(AKnight, Not(AKnave))),
        # If A is a Knave (will result False from truth table):
        And(Biconditional(AKnave, AKnight), Biconditional(AKnight, Not(AKnight)))
    ),

    # B says that A is a Knave:
    Biconditional(BKnight, And(Biconditional(AKnave, AKnight), Biconditional(AKnight, Not(AKnight)))),
    Biconditional(BKnave, Not(And(Biconditional(AKnave, AKnight), Biconditional(AKnight, Not(AKnight))))),

    # B also says that C is a Knave:
    Biconditional(BKnight, CKnave),
    Biconditional(BKnave, CKnight),

    # C says A is a Knight:
    Biconditional(CKnight, AKnight),
    Biconditional(CKnave, AKnave)



)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
