"""
This is the intelligent agent behind the decision making of how to respond to
the user's utterance. The intelligent agent uses different methods of
selecting the correct response, including different strategies, selection
methods, and optimization methods.

# TODO ensure the rules apply to abstract concepts, ensure ML applies to well defined problems. Rule = Abstract && Macro, ML = explict/well-defined && Micro

:author: Derek S. Prijatelj
"""

from conversation import DialogueAct as DA, Utterance, \
    is_statement, is_question, is_response_action, is_backchannel, \
    topic_is_self, topic_is_user
from nlg.nlg import generate_response_text #TODO remove , run in src dir.
from intelligent_agent.decision_tree_static import decision_tree_static
from intelligent_agent.static_matrix import static_matrix

_standard_topic = {
    "self_user",
    "self_bot",
    "weather",
    "news",
    "politics",
    "sports",
    "joke"
}

#def decide_response(simulation, user, conversation_history):
def decide_response(conversation_history, chatbot_id, persona_dict):
    """
    Main interface for intelligent agent to decide how to response. With the NLU
    information and the persona making this decision, generates the metadata of
    the persona's response utterance. This metadata matches the type and format
    of the NLU information.
    """
    chatbot = persona_dict[chatbot_id]
    participants = conversation_history.participants
    participants.remove(chatbot_id)
    user = persona_dict[next(iter(participants))]
    last_utterance = conversation_history.last_utterance

    # Assess mood and magnitude of change to mood necessary
    mood_magnitude = chatbot.personality.mood - user.personality.mood

    # Assess topic sentiment in relation to desired mood
    topic_magnitude = chatbot.topic_magnitude(
        last_utterance.topic,
        chatbot.personality.mood
    )
    # TODO give first utterance, should never occur in prototype


    return static_matrix(conversation_history, chatbot, user, persona_dict)

    #return decision_tree_static(conversation_history, chatbot, user, persona_dict)

    # static reactions:
    if last_utterance.dialogue_act == DA.farewell:
        return Utterance(
            chatbot_id,
            DA.farewell,
            "self_user",
            chatbot.personality.mood,
            chatbot.personality.assertiveness
        )
    #elif last_utterance.dialogue_act == DA.greeting:
    #    return Utterance(
    #        chatbot_id,
    #        DA.greeting,
    #        "self_user",
    #        chatbot.personality.mood,
    #        chatbot.personality.assertiveness
    #    )

    # TODO remove this, this is just to stop code from crashing until IA finished
    return Utterance(chatbot_id, DA.other, "None", 5, 5)
