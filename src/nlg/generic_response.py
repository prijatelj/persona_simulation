"""
Methods for generating general responses for certain dialogue acts. These are
mostly canned text, but some may be template based. All of these will take the
persona speaking the utterance and detail variables in how to say the utterance,
such as the chosen sentiment for the utterance, which may be different from the
persona's personality.

:author: Derek S. Prijatelj
"""
from datetime import datetime
from random import choice, getrandbits
from conversation import QuestionType as QT
from nlg import insult

def greeting(persona, conversation, sentiment=None, formal=None):
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

    neutral = formality_select(neutral_formal, neutral_informal, formal)

    return sentiment_select(persona, sentiment, neutral, pos)

def farewell(persona, conversation, sentiment=None, formal=None):
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

    neutral = formality_select(neutral_formal, neutral_informal, formal)
    pos = formality_select(pos_formal, pos_informal, formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def agreement(persona, conversation, sentiment=None, formal=None):
    neutral = ["I agree", "I agree with you"]
    pos = ["definitely", "absolutely"]
    neg = ["I suppose I agree", "I suppose I agree with you",
        "unfortunately, I agree", "unforunteately, I agree with you"]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def disagreement(persona, conversation, sentiment=None, formal=None):
    neutral = ["I disagree", "I disagree with you"]
    pos = ["I definitely disagree", "I absolutely disagree"]
    neg = ["I suppose I disagree", "I suppose I disagree with you",
        "unfortunately, I disagree", "unforunteately, I disagree with you"]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def confirm(persona, conversation, sentiment=None, formal=None):
    neutral_formal = ["yes"]
    neutral_informal = ["yeah", "okay"] # uh-huh mm-hmm??
    pos = ["absolutely, yes", "definitely, yes", "definitely, yes"]
    neg = ["unfortunately, yes"]

    neutral = formality_select(neutral_formal, neutral_informal, formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def disconfirm(persona, conversation, sentiment=None, formal=None):
    neutral_formal = ["no"]
    neutral_informal = ["nah"]
    pos = ["unfortunately, no"]
    neg = ["absolutely not", "definitely not", "definitely no"]

    neutral = formality_select(neutral_formal, neutral_informal, formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def thanks(persona, conversation, sentiment=None, formal=None):
    neutral_formal = ["thank you"]
    neutral_informal = ["thanks"]
    pos = ["thank you very much"]
    neg = ["thanks for nothing"]

    neutral = formality_select(neutral_formal, neutral_informal, formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def apology(persona, conversation, sentiment=None, formal=None):
    neutral_formal = ["I apologize", "I did not mean to offend",
        "I did not intend any offense", "I did not mean any offense"]
    neutral_informal = ["I am sorry"]
    pos = ["please forgive me"]
    neg = ["I beg your pardon", "Forgive me"]

    neutral = formality_select(neutral_formal, neutral_informal, formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def backchannel(persona, conversation, sentiment=None, formal=None):
    neutral = ["uh-huh", "hmm", "mm-hmm", "okay", "I see"]
    pos = ["wow"]

    return sentiment_select(persona, sentiment, neutral, pos)

def request_confirmation(persona, conversation, sentiment=None, formal=None):
    neutral = ["really", "Is that so"]
    return sentiment_select(persona, sentiment, neutral)

def request_clarification(persona, conversation, sentiment=None, formal=None):
    neutral = ["could you repeat that", "could you clarify that",
        "what do you mean", "In what way", "could you elaborate on that",
        "could you rephrase that"]
    pos = ["could you please repeat that", "could you please clarify that",
        "could you please rephrase that", "could you please elaborate"]
    neg = ["you need to do a better job explaining what you mean"]
    return sentiment_select(persona, sentiment, neutral, pos, neg)

# TODO requires past phrase, include topic
def query(persona, conversation, sentiment=None, formal=None, topic="that"):
    return sentiment_select(persona, sentiment, neutral, pos, neg)

"""
    Probably will need more articulation for Statement and Question.
    Such as ensuring a statement was not already said or asked...
"""
def question_information(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    neutral = ["tell me more", "inform me on " + topic]
    pos = ["please", "could you"]
    pos = [s1 + " " + s2 for s1 in pos for s2 in neutral]
    neg = ["what else is there on " + topic]
    return sentiment_select(persona, sentiment, neutral, pos, neg)

def question_experience(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    neutral = [
        "do you have an experience with " + topic,
        "do you have an interesting experience with " + topic,
        "do you have a notable experience with " + topic,
    ]
    pos_formal = [
        "could you please share your experience with " + topic,
        "could you please share a notable experience with " + topic,
        "could you please share an interesting experience with " + topic
    ]
    pos_informal = [
        "what kind of " + positive_adj(formal)
            + " experience have you had with " + topic
    ]
    neg = [
        "what kind of " + negative_adj(formal)
            + " experience have you had with " + topic
    ]

    pos = formality_select(pos_formal, pos_informal, formal)

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def question_preference(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    if question_type == QT.polar:
        neutral = ["do you have a preference on " + topic]
    else: # elif question_type == QT.wh:
        neutral = ["what is your preference on " + topic]
        neg = ["what is your " + negative_adj(formal) + " preference on "
            + topic]
    return sentiment_select(persona, sentiment, neutral, neg=neg)

def question_opinion(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    if question_type == QT.polar:
        neutral = ["do you have a opinion on " + topic]
    else: # elif question_type == QT.wh:
        neutral = ["what is your opinion on " + topic]
        neg = ["what is your " + negative_adj(formal) + " opinion on " + topic]

    return sentiment_select(persona, sentiment, neutral, neg=neg)

def question_desire(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    if topic == "general" or topic == "self_user":
        neutral = [
            "what are your wants",
            "what are your desires"
        ]
        if question_type == QT.polar:
            neg = ["is there something you want"]
        else:
            neg = ["what do you want"]
    else:
        neutral = ["do you want to do something with regards to " + topic]
        neg = ["I suppose you want to do something with regards to " + topic]
    return sentiment_select(persona, sentiment, neutral, neg=neg)

def question_plan(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    #if topic == "general" or topic == "self_user":
    neutral = ["what are your plans"]
    neg = ["what are your" + negative_adj(formal) + " plans"]
    return sentiment_select(persona, sentiment, neutral, neg=neg)

def statement_information(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    neutral = [
        "I do not have much to say on " + topic,
        topic + " is a topic of conversation"
    ]

    neg = [insult_gen()]
    neg = [s1 + ", " + s2 for s1 in neg for s2 in neutral]

    return sentiment_select(persona, sentiment, neutral,neg=neg)

def statement_experience(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    neutral = [
        "I have no experience with " + topic,
        "I have limited experience with " + topic,
        "I have minimal experience with " + topic,
        "I have no noteworthy experience with " + topic
    ]

    neg = [insult_gen()]
    neg = [s1 + ", " + s2 for s1 in neg for s2 in neutral]

    return sentiment_select(persona, sentiment, neutral,neg=neg)

def statement_preference(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    return statement_opinion(persona, conversation, sentiment, formal, topic, question_type)
    #return sentiment_select(persona, conversation, sentiment, neutral, pos, neg)

def statement_opinion(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    neutral = ["I am impartial to " + topic]
    neg = [
        "I don't care for this " + negative_adj(formal) + " subject",
        "I do not like " + topic
    ]
    pos = [
        "I like " + topic
    ]

    return sentiment_select(persona, sentiment, neutral, pos, neg)

def statement_desire(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    neutral = [
        "I have no desire with regards to " + topic,
        "I have limited desire with regards to " + topic,
        "I have minimal desire with regards to " + topic,
        "I have no noteworthy desire with regards to " + topic,
        "I have no want with regards to " + topic,
        "I have limited want with regards to " + topic,
        "I have minimal want with regards to " + topic,
        "I have no noteworthy want with regards to " + topic
    ]

    neg = [insult_gen()]
    neg = [s1 + ", " + s2 for s1 in neg for s2 in neutral]

    return sentiment_select(persona, sentiment, neutral,neg=neg)

def statement_plan(persona, conversation, sentiment=None, formal=None, topic="that",
        question_type=None):
    neutral = [
        "I have no plans with regards to " + topic,
        "I have limited plans with regards to " + topic,
        "I have minimal plans with regards to " + topic,
        "I have no noteworthy plans with regards to " + topic,
        "I have no plans related to " + topic,
        "I have limited plans related to " + topic,
        "I have minimal plans related to " + topic,
        "I have no noteworthy plans related to " + topic
    ]

    neg = [insult_gen()]
    neg = [s1 + ", " + s2 for s1 in neg for s2 in neutral]

    return sentiment_select(persona, sentiment, neutral,neg=neg)

    #return sentiment_select(persona, sentiment, neutral, pos, neg)

def insult_gen():
    return insult.shakespeare(bool(getrandbits(1)), bool(getrandbits(1)))

def compliment():
    return

def silence(persona, conversation=None):
    return ""

def paraphrase(persona, conversation, sentiment=None, formal=None):
    #TODO: I cannot paraphrase yet. Just confirm or clarify what you said.
    return request_confirmation(persona, conversation, sentiment, formal)

# non-dialogue act specific:
def query_user_general_experience(persona, conversation, sentiment=None,
        formal=None):
    netural_formal = [
        "anything new with you",
        "what is new with you",
        "what are you up to"
    ]
    neutral_informal = [
        "sup",
        "what's up with you",
        "what's new",
        "what's up",
        "anything new",
        "what's going on"
    ]
    neutral = formality_select(neutral_formal, neutral_informal, formal)

    return choice(neutral)

def query_user_general_information(persona, conversation, sentiment=None,
        formal=None):
    netural_formal = [
        "how are you",
        "how are you doing",
        "how have you been",
    ]
    neutral_informal = [
        "how's everything",
        "how is everything"
    ]
    neutral = formality_select(neutral_formal, neutral_informal, formal)

    return choice(neutral)

# Helper Methods:
def sentiment_select(persona, sentiment, neutral, pos=None, neg=None):
    """
    Selects element from the provided lists of different sentiment types.
    :return: Returns a randomly selected element based on sentiment
    """
    # TODO perhaps have persona/sentiment accept either a person obj, or int val
    # use conditional statement to determine type and how to handle.
    sentiment = sentiment if sentiment is not None else persona.personality.mood
    if neg is not None and sentiment < 4:
        return choice(neg)
    elif pos is not None and sentiment > 6:
        return choice(pos)
    else:
        return choice(neutral)

def formality_select(formal_list, informal, formal=None):
    """
    Returns a list with the appropriate type of formality in its elements.
    :param formal: Bool that determines if formal or not.
    :return: Returns a list based on formality
    """
    if formal_list is None:
        return formal_list + informal
    elif formal_list:
        return formal_list
    elif not formal_list:
        return informal

def question_type_select(question_type, **kargs):
    return

# TODO perhaps find and use a preexisting word list for these and others?
# OR, actually use an ontology and infer what is a negative adj, etc...
def positive_adj(formal=None):
    formal_adj = ["excellent", "wonderful", "good", "great", "delightful"]
    informal_adj = ["superb"]
    return choice(formality_select(formal_adj, informal_adj, formal))

def negative_adj(formal=None):
    formal_adj = ["pathetic", "unintelligent", "foolish", "terrible"]
    informal_adj = ["lame", "stupid", "idiotic"]
    return choice(formality_select(formal_adj, informal_adj, formal))
