"""
A Shakespeare Insult generator based on the lists and method involving 3 lists
of words meant to be randomly selected from and appended to one another in order
was apparently originally the work of an English teacher at Center Grove High
School in Greenwood Indiana named Jerry Maguire.

Taken from Chris Seidel's website:
http://www.pangloss.com/seidel/shake_rule.html

This serves mostly for humor and a place holder for insult generation.

:author: Derek S. Prijatelj
"""
from yaml import load
from random import choice

def shakespeare(adverb=True, adjective=True, noun=True, complete=True):
    with open("../data/insults/shakespeare_insults.yaml") as insult_parts:
        insult_parts = load(insult_parts)
        insult = ""
        if adverb:
            insult += choice(insult_parts["adverb"])
        if adjective:
            insult += choice(insult_parts["adjective"]) if insult == "" else \
                " " + choice(insult_parts["adjective"])
        if noun:
            insult += choice(insult_parts["noun"]) if insult == "" else \
                " " + choice(insult_parts["noun"])
        if complete:
            insult = "you " + insult
    return insult

def main():
    insult = shakespeare()
    print(insult[0].upper() + insult[1:] + "!")

if __name__ == "__main__":
    main()
