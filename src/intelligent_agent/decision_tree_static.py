"""
A static decision tree implementation of an intelligent agent for holding a
conversation. In otherwords, the baseline rule system of the intelligent agent.

based on hierarch:
    new convo / or on-going
        change topic / stay on topic
            passive / assertive tactic

:author: Derek S. Prijatelj
"""

from intelligent_agent import tactic

def decision_tree_static(conversation_history, chatbot, user, personas=None):
    """
    A manually constructed decision tree to implement a rule based system as a
    baseline.

    :param conversation_history: current ConversationHistory
    :param chatbot: Persona of chatbot
    :param user: Persona of user
    :param personas: Dictionary of str "persona_id" to Persona
    """
    # Assess mood and magnitude of change to mood necessary
    mood_magnitude = chatbot.personality.mood - user.personality.mood

    # Assess topic sentiment in relation to desired mood
    topic_magnitude = user.topic_magnitude(
        last_utterance.topic,
        chatbot.personality.mood
    )

    # static reactions:
    if last_utterance.dialogue_act == DialogueAct.farewell:
        return Utterance(
            chatbot_id,
            DialogueAct.farewell,
            "self_user",
            chatbot.personality.mood,
            chatbot.personality.assertiveness
        )

    # TODO add ability to reference previous conversations for returning users
    if len(conversation_history.topic_to_utterance.keys()) <= 1:
        # New conversation started
        tactic.query()

        # prev = greeting, then greeting, query, etc.
        # prev = question, then answer
        # statement then ... idk response? who are you?

    else: # Ongoing Conversation
        # topics have been discussed, and conversation ongoing
        # go through topics of desired sentiment till exhausted.
        # query new topics if topics of desired sentiment are exhausted.
        #TODO Need a way to know what topics have been exhausted! ia only. is it ia only?

        if change_topic(mood_magnitude, topic_magnitude,
                chatbot.personality.mood):
            if respond_passive(chatbot, user, mood_magnitude, topic_magnitude):

            else:

        else:

    return

def psych():
    # Placeholder for now, will put w/in hierarchy where necessary.
    #TODO psychiatrist for self_user only, not self_bot.
    if topic_is_self(last_utterance.topic) \
            or topic_is_user(last_utterance.topic):
        return tactics.psychiatrist(last_utterance, chatbot_id)

def change_topic(mood_magnitude, topic_magnitude, desired_mood):
    return

def respond_passively(chatbot, user, mood_magnitude, topic_magnitude):
    return

def change_topic_passive():
    return

def change_topic_assertive():
    return

def stay_on_topic_passive():
    return

def stay_on_topic_assertive():
    return
