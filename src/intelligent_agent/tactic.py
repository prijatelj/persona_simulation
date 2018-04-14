"""
The tactics used in maintaining the conversation.
"""

from nltk.chat.eliza import eliza_chatbot
from conversation import Utterance, DialogueAct

"""
Tactics:
Query:  Query General: query the user in general terms, askw hat they think of
what has been discussed or a few canned phrases.
        Query Specific: ask what they think of a specific topic/subtopic of
        a previsouly discussed topic. (searches Database for specifics)
Request elaboration, clarification, etc...
Statement:
    State things about a topic using database information. (expert system)

Tell a joke.
"""

def query(conversation_history, persona):
    """
    General query to obtain topic information from user and encourage
    conversation
    """
    return

def query_topics(simulation, user, conversation_history, mood_magnitude):
    """
    Query tactics interface. The proper query tactic is selected and executed.
    The generated response metadata will be returned.
    """
    return

def query_user_general():
    """ General questions of user to find a topic of discussion. """
    return

def query_user_specific():
    """ Ask user to select a subtopic of a topic. """
    return

def query_database_general():
    """ randomly query database, or query similar topics to those discussed. """
    return

def query_database_specific():
    """ query the subtopics of a topic. """
    return

def insult():
    """ generate blatant insult, optionally related to previous utterance """
    return

def compliment():
    """ Generate compliment, optionally related to previous utterance. """
    return

def joke():
    """ Generate joke, optionally related to previous utterance. """
    return

def psychiatrist(utterance, responder_id):
    """ Use ELIZA to generate respons eutterances when the topic is on user. """
    return Utterance(
        responder_id,
        DialogueAct.other,
        "self_user",
        5,
        5,
        eliza_chatbot.respond(utterance.text)
    )
