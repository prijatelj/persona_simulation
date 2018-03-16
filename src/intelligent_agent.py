"""
This is the intelligent agent behind the decision making of how to respond to
the user's utterance.

:author: Derek S. Prijatelj
"""

from src.persona import DialogueAct
from src.nlg import generate_response

_standard_topic = [
    "self_user",
    "self_bot",
    "weather",
    "news",
    "politics",
    "sports",
    "joke"
]

#def decide_response(simulation, user, conversation_history):
def decide_response(conversation_history, responder_id, persona_dict):
    """
    Main interface for intelligent agent to decide how to response. With the NLU
    information and the persona making this decision, generates the metadata of
    the persona's response utterance. This metadata matches the type and format
    of the NLU information.
    """
    #TODO if conversation_history has access to personas (ids) then no need for
    # actual personas.
    """
    Tactics:
    Query:  Query General: query the user in general terms, askw hat they think of what has been discussed or a few canned phrases.
            Query Specific: ask what they think of a specific topic/subtopic of
            a previsouly discussed topic. (searches Database for specifics)
    Request elaboration, clarification, etc...
    Statement:
        State things about a topic using database information. (expert system)

    Tell a joke.
    """
    responder = persona_dict[responder_id]
    participants = conversation_history.participants.remove(responder_id)
    user = persona_dict[participants[0]]

    # determine state of conversation

    # Assess mood and magnitude of change to mood necessary
    mood_magnitude = responder.personality.mood - user.personality.mood

    user_previous_utterance = conversation_history.utterances[-1]

    #if len(conversation_history.utterances) > 0:
    #    user_previous_utterance = conversation_history.utterances[-1]
    #else: # No previous utterances, we are giving first utterance
    #   # TODO give first utterance, should never occur in prototype

    if len(conversation_history.topic_to_utterance.keys()) == 0:
        # No topic discussed, query new topics.
        query()

        # prev = greeting, then greeting, query, etc.
        # prev = question, then answer
        # statement then ... idk response? who are you?

    else:
        # topics have been discussed, and conversation ongoing???
        # TODO to determine if this conversation instance is new or ongoing,
        # check time of last utterance
        # For now, assume that if previous topics exist, then ongoing convo.

        # go through topics of desired sentiment till exhausted.
        # query new topics
        #TODO Need a way to know what topics have been exhausted! ia only.

        # check DA, Topic sentiment, Topic,

        # determine appropriate DA.
        if topic_is_self(user_previous_utterance.topic) \
                and dialogue_act_is_question(
                    user_previous_utterance.dialogue_act
                ):
            dialogue_act = DialogueAct(
                user_previous_utterance.dialogue_act.value - 100
            )

        # Check if standard topic:
        if user_previous_utterance.topic in _standard_topic:
            utterance_metadata = handle_standard_topic(simulation,
                user,
                conversation_history,
                mood_magnitude
            )

def dialogue_act_is_question(da):
    return da.value >= DialogueAct.question.value \
        and da.value < DialogueAct.question.value + 100

def topic_is_self(topic):
    """ Check if the topic is about the simulation/chatbot itself. """
    return topic in ["you", "yourself"]

def handle_standard_topic(conversation_history, responder, user, mood_magnitude):
    """ Handles responding to standard topics, such as weather and news.  """
    return

# Tactics
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

def psychiatrist():
    """ Use ELIZA to generate respons eutterances when the topic is on user. """
    return
