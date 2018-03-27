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
    neutral_formal = ["Hello", "Greetings"]
    neutral_informal = ["Hi", "Hey", "Hey there"]
    pos = []

    now = datetime.now()

    if now.hour < 12:
        pos += ["Good Morning", "Good day"]
        neutral_informal += ["Morning"]
    elif now.hour >= 12 and now.hour <= 19:
        pos += ["Good Afternoon", "Good day"]
        neutral_informal += ["Afternoon"]
    else:
        pos += ["Good Evening"]
        neutral_informal += ["Evening"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def farewell(persona, sentiment=None, formal=None):
    neutral_formal = ["Goodbye", "Farewell"]
    neutral_informal = ["Bye", "Later", "See you later", "Talk to you later",
        "So long", "Until next time"]
    pos_formal = []
    pos_informal = ["Have a good one", "Take it easy", "Take care"]
    neg = ["I am done with you", "Good riddance", "We're done"]
    #insult = ["Sod off"]

    # farewell initial
    # I've got to get going or I must be going
    # farewell responses
    # "I look forward to our next meeting"

    now = datetime.now()

    if now.hour <= 19:
        pos_formal += ["Have a good day", "Have a nice day"]
    else:
        pos_formal += ["Have a good evening"]
        pos_informal += ["Good night"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)
    pos = formality_select(formal, pos_informal, pos_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def agree(persona, sentiment=None, formal=None):
    neutral = ["I agree", "I agree with you"]
    pos = ["Definitely", "Absolutely"]
    neg = ["I suppose I agree", "I suppose I agree with you",
        "Unfortunately, I agree", "Unforunteately, I agree with you"]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def disagree(persona, sentiment=None, formal=None):
    neutral = ["I disagree", "I disagree with you"]
    pos = ["I Definitely disagree", "I Absolutely disagree"]
    neg = ["I suppose I disagree", "I suppose I disagree with you",
        "Unfortunately, I disagree", "Unforunteately, I disagree with you"]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def confirm(persona, sentiment=None, formal=None):
    neutral_formal = ["Yes"]
    neutral_informal = ["Yeah", "Okay"] # uh-huh mm-hmm??
    pos = ["Absolutely, yes", "Definitely, yes", "Definitely, yes"]
    neg = ["Unfortunately, yes"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def disconfirm(persona, sentiment=None, formal=None):
    neutral_formal = ["No"]
    neutral_informal = ["Nah"]
    neg = ["Absolutely not", "Definitely not", "Definitely no"]
    neg = ["Unfortunately, no"]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def thanks(persona, sentiment=None, formal=None)
    neutral_formal = ["Thank you"]
    neutral_informal = ["Thanks"]
    pos = ["Thank you very much"]
    neg = ["Thanks for nothing"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def apology(persona, sentiment=None, formal=None)
    neutral_formal = ["I apologize", "I did not mean to offend",
        "I did not intend any offense", "I did not mean any offense"]
    neutral_informal = ["I am sorry"]
    pos = ["Please forgive me"]
    neg = ["I beg your pardon", "Forgive me"]

    neutral = formality_select(formal, neutral_informal, neutral_formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def backchannel(persona, sentiment=None, formal=None)
    neutral = ["Uh-huh", "Hmm", "Mm-hmm", "Okay", "I see"]
    pos = ["Wow"]

    return sentiment_select(persona, sentiment, neutral, pos)

def request_confirmation(persona, sentiment=None, formal=None)
    neutral = ["Really?", "Is that so?"]
    return sentiment_select(persona, sentiment, neutral)

def request_clarification(persona, sentiment=None, formal=None)
    neutral = ["Could you repeat that?", "Could you clarify that?",
        "What do you mean?", "In what way?", "Could you elaborate on that?",
        "Could you rephrase that?"]
    pos = ["Could you please repeat that?", "Could you please clarify that?",
        "Could you please rephrase that?", "Could you please elaborate?"]
    neg = ["You need to do a better job explaining what you mean"]
    return sentiment_select(persona, sentiment, neutral, pos, neg)

def query(persona, sentiment=None, formal=None):
    neutral = ["Tell me more."]
    pos = ["Please tell me more."]
    neg = ["What else?"]
    return sentiment_select(persona, sentiment, neutral, pos, neg)

"""
    Probably will need more articulation for Statement and Question.
    Such as ensuring a statement was not already said or asked...

"""
def question_information(persona, sentiment=None):

    return

def question_experience(persona, sentiment=None):
    neutral = ["Do you have a notable experience with that?"]
    pos = ["Could you please share a notable experience with that?"]
    neg = ["What kind of"]
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
        return neg[randint(0, len(neg)]
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

def negative_adjective(formal):
    formal_adj = ["pathetic", "unintelligent"]
    informal_adj = ["lame", "stupid", ""]
