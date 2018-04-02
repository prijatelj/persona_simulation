"""
Methods for generating general responses for certain dialogue acts. These are
mostly canned text, but some may be template based. All of these will take the
persona speaking the utterance and detail variables in how to say the utterance,
such as the chosen sentiment for the utterance, which may be different from the
persona's personality.

:author: Derek S. Prijatelj
"""
from datetime import datetime
from random import randint

def greeting(persona, sentiment=None, formal=None):
    """ Given persona, selects appropriate response. """
    neutral_formal = ["hello", "greetings"]
    neutral_informal = ["hi", "hey", "hey there"]
    pos = []

    now = datetime.now()

    if now.hour < 12:
        pos += ["good morning", "good day"]
        neutral_informal += ["morning"]
    elif now.hour >= 12 and now.hour <= 19:
        pos += ["good afternoon", "good day"]
        neutral_informal += ["afternoon"]
    else:
        pos += ["good evening"]
        neutral_informal += ["evening"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def farewell(persona, sentiment=None, formal=None):
    neutral_formal = ["goodbye", "farewell"]
    neutral_informal = ["bye", "later", "see you later", "talk to you later",
        "so long", "until next time"]
    pos_formal = []
    pos_informal = ["have a good one", "take it easy", "take care"]
    neg = ["I am done with you", "good riddance", "we're done"]
    #insult = ["sod off"]

    # farewell initial
    # I've got to get going or I must be going
    # farewell responses
    # "I look forward to our next meeting"

    now = datetime.now()

    if now.hour <= 19:
        pos_formal += ["ave a good day", "have a nice day"]
    else:
        pos_formal += ["have a good evening"]
        pos_informal += ["good night"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)
    pos = formality_select(formal, pos_informal, pos_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def agreement(persona, sentiment=None, formal=None):
    neutral = ["I agree", "I agree with you"]
    pos = ["definitely", "absolutely"]
    neg = ["I suppose I agree", "I suppose I agree with you",
        "unfortunately, I agree", "unforunteately, I agree with you"]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def disagreement(persona, sentiment=None, formal=None):
    neutral = ["I disagree", "I disagree with you"]
    pos = ["I definitely disagree", "I absolutely disagree"]
    neg = ["I suppose I disagree", "I suppose I disagree with you",
        "unfortunately, I disagree", "unforunteately, I disagree with you"]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def confirm(persona, sentiment=None, formal=None):
    neutral_formal = ["yes"]
    neutral_informal = ["yeah", "okay"] # uh-huh mm-hmm??
    pos = ["absolutely, yes", "definitely, yes", "definitely, yes"]
    neg = ["unfortunately, yes"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def disconfirm(persona, sentiment=None, formal=None):
    neutral_formal = ["no"]
    neutral_informal = ["nah"]
    neg = ["absolutely not", "definitely not", "definitely no"]
    neg = ["unfortunately, no"]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def thanks(persona, sentiment=None, formal=None):
    neutral_formal = ["thank you"]
    neutral_informal = ["thanks"]
    pos = ["thank you very much"]
    neg = ["thanks for nothing"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def apology(persona, sentiment=None, formal=None):
    neutral_formal = ["I apologize", "I did not mean to offend",
        "I did not intend any offense", "I did not mean any offense"]
    neutral_informal = ["I am sorry"]
    pos = ["please forgive me"]
    neg = ["I beg your pardon", "Forgive me"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def backchannel(persona, sentiment=None, formal=None):
    neutral = ["uh-huh", "hmm", "mm-hmm", "okay", "I see"]
    pos = ["wow"]

    return sentiment_select(persona, sentiment, neutral, pos)

def request_confirmation(persona, sentiment=None, formal=None):
    neutral = ["really", "Is that so"]
    return sentiment_select(persona, sentiment, neutral)

def request_clarification(persona, sentiment=None, formal=None):
    neutral = ["could you repeat that", "could you clarify that",
        "what do you mean", "In what way", "could you elaborate on that",
        "could you rephrase that"]
    pos = ["could you please repeat that", "could you please clarify that",
        "could you please rephrase that", "could you please elaborate"]
    neg = ["you need to do a better job explaining what you mean"]
    return sentiment_select(persona, sentiment, neutral, pos, neg)

def query(persona, sentiment=None, formal=None):
    neutral = ["tell me more", "inform me on this"]
    pos = ["please", "could you"]
    pos = [s1 + " " + s2 for s1 in pos for s2 in neutral]
    neg = ["what else"]
    return sentiment_select(persona, sentiment, neutral, pos, neg)

"""
    Probably will need more articulation for Statement and Question.
    Such as ensuring a statement was not already said or asked...

"""
def question_information(persona, sentiment=None):

    return

def question_experience(persona, sentiment=None):
    neutral = ["do you have a notable experience with that"]
    pos = ["could you please share a notable experience with that"]
    neg = ["what kind of"]
    return sentiment_select(persona, sentiment, neutral, pos, neg)

def question_preference(persona, sentiment=None):
    return

def question_opinion(persona, sentiment=None):
    return

def question_desire(persona, sentiment=None):
    return

def question_plan(persona, sentiment=None):
    return

def insult():
    return

def compliment():
    return

def sentiment_select(persona, sentiment, neutral, pos=None, neg=None):
    # TODO perhaps have persona/sentiment accept either a person obj, or int val
    # use conditional statement to determine type and how to handle.
    sentiment = sentiment if sentiment is not None else persona.personality.mood
    if neg is not None and sentiment < 4:
        return neg[randint(0, len(neg))]
    elif pos is not None and sentiment > 6:
        return pos[randint(0, len(pos))]
    else:
        return neutral[randint(0, len(neutral))]

def formality_select(formality, informal, formal=None):
    if formality is None:
        return formal + informal
    elif formality:
        return formal
    elif not formality:
        return informal

# TODO perhaps find and use a preexisting word list for these and others?
# OR, actually use an ontology and infer what is a negative adj, etc...
def positive_adjective():
    formal_adj = ["excellent", "wonderful", "good", "great"]
    informal_adj = ["superb"]

def negative_adjective(formal):
    formal_adj = ["pathetic", "unintelligent", "foolish", "terrible"]
    informal_adj = ["lame", "stupid", "idiotic"]
