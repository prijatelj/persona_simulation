"""
This is the intelligent agent behind the decision making of how to respond to
the user's utterance. The intelligent agent uses different methods of
selecting the correct response, including different strategies, selection
methods, and optimization methods.

# TODO ensure the rules apply to abstract concepts, ensure ML applies to well defined problems. Rule = Abstract && Macro, ML = explict/well-defined && Micro

:author: Derek S. Prijatelj
"""

from intelligent_agent import tactics
from conversation import DialogueAct, Utterance, \
    is_statement, is_question, is_response_action, is_backchannel, \
    topic_is_self, topic_is_user
from nlg.nlg import generate_response_text #TODO remove , run in src dir.

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
def decide_response(conversation_history, speaker_id, persona_dict):
    """
    Main interface for intelligent agent to decide how to response. With the NLU
    information and the persona making this decision, generates the metadata of
    the persona's response utterance. This metadata matches the type and format
    of the NLU information.
    """
    speaker = persona_dict[speaker_id]
    participants = conversation_history.participants
    participants.remove(speaker_id)
    user = persona_dict[participants[0]]
    last_utterance = conversation_history.last_utterance

    # Assess mood and magnitude of change to mood necessary
    mood_magnitude = speaker.personality.mood - user.personality.mood

    # Assess topic sentiment in relation to desired mood
    topic_magnitude = speaker.topic_magnitude(
        last_utterance.topic,
        speaker.personality.mood
    )
    # TODO give first utterance, should never occur in prototype

    # static reactions:
    if last_utterance.dialogue_act == DialogueAct.farewell:
        return Utterance(
            speaker_id,
            DialogueAct.farewell,
            "self_user",
            speaker.personality.mood,
            speaker.personality.assertiveness
        )
    elif last_utterance.dialogue_act == DialogueAct.greeting:
        return Utterance(
            speaker_id,
            DialogueAct.greeting,
            "self_user",
            speaker.personality.mood,
            speaker.personality.assertiveness
        )

    # TODO add ability to reference previous conversations for returning users
    if len(conversation_history.topic_to_utterance.keys()) == 0:
        # New conversation started
        query()

        # prev = greeting, then greeting, query, etc.
        # prev = question, then answer
        # statement then ... idk response? who are you?

    else:
        # topics have been discussed, and conversation ongoing
        # go through topics of desired sentiment till exhausted.
        # query new topics if topics of desired sentiment are exhausted.
        #TODO Need a way to know what topics have been exhausted! ia only. is it ia only?


        #TODO psychiatrist for self_user only, not self_bot.
        if topic_is_self(last_utterance.topic) \
                or topic_is_user(last_utterance.topic):
            return tactics.psychiatrist(last_utterance, speaker_id)
        elif last_utterance.topic in _standard_topic:
            # Check if standard topic:
            utterance_metadata = handle_standard_topic(simulation,
                user,
                conversation_history,
                mood_magnitude
            )

        # TODO remove this, this is just to stop code from crashing until IA finished
        return Utterance(speaker_id, DialogueAct.other, "None", 5, 5)

def decision_tree_static():
    return

def handle_standard_topic(conversation_history, speaker, user, mood_magnitude):
    """ Handles responding to standard topics, such as weather and news.  """
    return
