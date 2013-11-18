from utils import FlexibleIterator

"""
Objectif: add an INDENT token and a DEDENT token arround every block

Strategy: put after every ":" that is not in a slice/dictionary declaration/lambda

Slice and dictionary are easy: increase a number when a "[" or "{" is found,
decrease it for a "]" or "}". If the number != 0, we are in a dictionary or
slice -> do not put a INDENT when a ":" is found.

Lambda are a bit different: increase another number when a "lambda" is found,
if the number is != 0 and a ":" is found, decrease this number, otherwise put a
INDENT

For the DEDENT, I'm probably going to need to keep a list of indentation and
decheck the last one every time I encounter a meaningfull line. Still need to
test this idea.
"""


def mark_indentation(sequence):
    return list(mark_indentation_generator(sequence))


def mark_indentation_generator(sequence):
    iterator = FlexibleIterator(sequence)
    current = None, None
    indent = 0
    while True:
        if iterator.end():
            return

        current = iterator.next()

        if current is None:
            return

        if current[0] == "ENDMARKER" and indent:
            while indent > 0:
                yield ('DEDENT', '')
                indent -= 1

        print current, iterator.show_next()
        if current[0] == "COLON" and iterator.show_next()[0] == "ENDL":
            indent += 1
            yield current
            yield iterator.next()
            yield ('INDENT', '')

        else:
            yield current
