"""
A static decision tree implementation of an intelligent agent for holding a
conversation. In otherwords, the baseline rule system of the intelligent agent.

based on hierarch:
    new convo / or on-going
        change topic / stay on topic
            passive / assertive tactic

:author: Derek S. Prijatelj
"""
import numpy as np
from intelligent_agent import tactic

def decision_tree_static(conversation, chatbot, user, personas=None):
    """
    A manually constructed decision tree to implement a rule based system as a
    baseline.

    :param conversation: current Conversation
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
    if len(conversation.topic_to_utterance.keys()) <= 1:
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

        # static response:
        # if greeting in middle of conversation either ignore or question it.
        #   perhaps respond confused.



        if change_topic(mood_magnitude, topic_magnitude,
                chatbot.personality.mood):
            if respond_passively(chatbot, user, mood_magnitude):
                return change_topic_passive(conversation, chatbot, user,
                    mood_magnitude, topic_magnitude, personas)
            else: # respond assertively
                return change_topic_assertive(conversation, chatbot, user,
                    mood_magnitude, topic_magnitude, personas)

        else: # Stay on topic
            if respond_passively(chatbot, user, mood_magnitude):
                return stay_on_topic_passive(conversation, chatbot, user,
                    mood_magnitude, topic_magnitude, personas)
            else: # respond assertively
                return stay_on_topic_assertive(conversation, chatbot, user,
                    mood_magnitude, topic_magnitude, personas)

def psych():
    # Placeholder for now, will put w/in hierarchy where necessary.
    #TODO psychiatrist for self_user only, not self_bot.
    # only really fits when stay on topic. Maybe if change topic to user too?
    if topic_is_self(last_utterance.topic) \
            or topic_is_user(last_utterance.topic):
        return tactics.psychiatrist(last_utterance, chatbot_id)

def change_topic(mood_magnitude, topic_magnitude, chatbot):
    # if topic magnitude is far from desired, (and is mood_magnitude) change
    # TODO can calculate how much the desire to change is based on assertiveness

    # TODO look at last Dialogue Act, if Question, request, something requiring
    # a response, take that into consideration!
    if chatbot.personality.assertiveness > 5:
        return abs(topic_magnitude) >= 2 and abs(mood_magnitude) >= 2)
    else:
        return abs(topic_magnitude) >= 3 and abs(mood_magnitude) >= 3)

def respond_passively(chatbot, user, mood_magnitude):
    # TODO can calculate how much desire to be assertive based on chatbot & user
    # ie. can play off user's own assertiveness to complement it.
    # TODO mood may be affected by chatbot's assertiveness, esp. if deemed rude.
    return chatbot.personality.assertiveness > 5


# TODO have random select, have it be a skewed normal, and mean wherever
# personality.mood is.
def change_topic_passive(conversation, chatbot, user, mood_magnitude,
        topic_magnitude, personas):

    # silence or no response or minimal response

    # ask to change topic, no expression of sent, not alternatives

    # express sent, no alternatives

    return

def change_topic_assertive(conversation, chatbot, user, mood_magnitude,
        topic_magnitude, personas):

    # provide alts. only

    # express sent, provide alts.

    # provide alts & begin talking

    # begin talking (abruptly change topic)



    # TODO look at last Dialogue Act, if Question, request, something requiring
    # a response, take that into consideration! change topic, but address this.

    return

def stay_on_topic_passive(conversation, chatbot, user, mood_magnitude,
        topic_magnitude, personas):

    # Listening oriented

    # Reinforce passively, "me too", "interesting."


    return

def stay_on_topic_assertive(conversation, chatbot, user, mood_magnitude,
        topic_magnitude, personas):

    # Leading Conversation, Informing/Expressing views

    # Reinforce actively "yes and this too..."

    return
