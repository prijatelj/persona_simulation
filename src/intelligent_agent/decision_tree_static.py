"""
A static decision tree implementation of an intelligent agent for holding a
conversation. In otherwords, the baseline rule system of the intelligent agent.

based on hierarch:
    new convo / or on-going
        change topic / stay on topic
            passive / assertive tactic

:author: Derek S. Prijatelj
"""

import csv
import numpy as np
import pandas
#from scipy.stats import skewnorm
from intelligent_agent import tactic
from conversation import DialogueAct as DA, QuestionType, \
    Utterance, is_question, is_statement, \
    topic_is_self, topic_is_user, question_to_statement, statement_to_question
from nlg import nlg, generic_response

def decision_tree_static(conversation, chatbot, user, personas=None):
    """
    A manually constructed decision tree to implement a rule based system as a
    baseline.

    :param conversation: current Conversation
    :param chatbot: Persona of chatbot
    :param user: Persona of user
    :param personas: Dictionary of str "persona_id" to Persona
    """
    last_utterance = conversation.last_utterance

    # Assess mood and magnitude of change to mood necessary
    mood_magnitude = chatbot.personality.mood - user.personality.mood

    # Assess topic sentiment in relation to desired mood
    topic_magnitude = user.topic_magnitude(
        last_utterance.topic,
        chatbot.personality.mood
    )

    # static reactions:
    if last_utterance.dialogue_act == DA.farewell:
        return farewell(chatbot)

    # TODO add ability to reference previous conversations for returning users
    # This is now doable through ConversationHistory objects

    if len(conversation.topic_to_utterances.keys()) <= 1:
        return new_conversation(conversation, chatbot, user, personas,
            last_utterance)
    else: # Ongoing Conversation
        return ongoing_conversation(conversation, chatbot, user, personas,
            last_utterance)

def change_topic(assertiveness, mood_magnitude, topic_magnitude,
        chatbot):
    # if topic magnitude is far from desired, (and is mood_magnitude) change
    # TODO can calculate how much the desire to change is based on assertiveness

    # TODO look at last Dialogue Act, if Question, request, something requiring
    # a response, take that into consideration!
    if assertiveness > 5:
        return abs(topic_magnitude) >= 2 and abs(mood_magnitude) >= 2
    else:
        return abs(topic_magnitude) >= 3 and abs(mood_magnitude) >= 3

def respond_passively(assertiveness, chatbot, user, mood_magnitude):
    # TODO can calculate how much desire to be assertive based on chatbot & user
    # ie. can play off user's own assertiveness to complement it.
    # TODO mood may be affected by chatbot's assertiveness, esp. if deemed rude.
    return assertiveness < 5

def response_assertiveness(chatbot):
    """ determines how assertive the chatbot will respond """
    assertiveness = np.random.normal(chatbot.personality.assertiveness, 2)
    while assertiveness < 1 or assertiveness > 10:
        assertiveness = np.random.normal(chatbot.personality.assertiveness, 2)

    return assertiveness

def response_sentiment(chatbot):
    """ determines how assertive the chatbot will respond """
    sentiment = np.random.normal(chatbot.personality.mood, 2)
    while sentiment < 1 or sentiment > 10:
        sentiment = np.random.normal(chatbot.personality.mood, 2)

    return sentiment

def new_conversation(conversation, chatbot, user, personas=None,
        last_utterance=None):
    # New conversation started
    # prev = greeting, then greeting, query, etc.
    if last_utterance.dialogue_act == DA.greeting:
        #TODO overcome limitation of not making text here. (use meta text)
        # Ideal, would be able to be assertive and make
        # greeting + question_ or statement_
        # call nlg module here, from IA.

        assertiveness = response_assertiveness(chatbot)

        if respond_passively(assertiveness):
            # if passive response, then only greeting.
            utterance = Utterance(
                chatbot.name,
                DA.greeting,
                "self_user",
                chatbot.personality.mood,
                chatbot.personality.assertiveness
            )

            text = nlg.generate_response_text(utterance, chatbot, conversation)
            utterance.set_text(text)
            return utterance
        else: # respond with greeting AND something else.
            # else: query user general
            greeting_text = generic_response.greeting(chatbot, conversation,
                chatbot.personality.mood)
            greeting_text = greeting_text[0].upper() + greeting_text[1:]
            greeting_text = (greeting_text + "."
                if chatbot.personality.mood < 8
                and chatbot.personality.assertiveness < 8
                else greeting_text + "!"
            )

            utterance = tactic.query_user_general(
                conversation, chatbot, user, personas)

            text = greeting_text + " " + utterance.text
            utterance.set_text(text)
            return utterance
    elif (not topic_is_self(last_utterance.topic)
        and not topic_is_user(last_utterance.topic)
        and is_question(last_utterance.dialogue_act)
        ):
        return Utterance(
            chatbot.name,
            question_to_statement(last_utterance.dialogue_act),
            last_utterance.topic,
            chatbot.personality.mood,
            chatbot.personality.assertiveness
        )
    elif ( not topic_is_self(last_utterance.topic)
        and not topic_is_user(last_utterance.topic)
        and is_statement(last_utterance.dialogue_act)
        ):
        return Utterance(
            chatbot.name,
            statement_to_question(last_utterance.dialogue_act),
            last_utterance.topic,
            chatbot.personality.mood,
            chatbot.personality.assertiveness
        )
    else:
        return tactic.psychiatrist(last_utterance, chatbot.name)
    #else:
    #    return tactic.query()
    # statement then ... idk response? who are you?

def ongoing_conversation(conversation, chatbot, user, personas=None,
        last_utterance=None):
    # topics have been discussed, and conversation ongoing
    # go through topics of desired sentiment till exhausted.
    # query new topics if topics of desired sentiment are exhausted.
    #TODO Need a way to know what topics have been exhausted! ia only. is it ia only?

    # static response:
    # if greeting in middle of conversation either ignore or question it.
    #   perhaps respond confused.

    general_conversation(conversation, chatbot, user, personas, last_utterance)

def general_conversation(conversation, chatbot, user, personas=None,
        last_utterance=None):
    """
    How to typically respond in a conversation.
    """
    if topic_is_self(last_utterance.topic) \
            or topic_is_user(last_utterance.topic):
        return tactic.psychiatrist(last_utterance, chatbot.name)
    else:
        return response_matrix(last_utterance, chatbot)

    """
    if change_topic(mood_magnitude, topic_magnitude,
            chatbot.personality.mood):
        if respond_passively(chatbot, user, mood_magnitude):
            return change_topic_passive(conversation, chatbot, user,
                mood_magnitude, topic_magnitude, personas)
        else: # respond assertively
            return change_topic_assertive(conversation, chatbot, user,
                mood_magnitude, topic_magnitude, personas)

    else: # Stay on topic
        if topic_is_self(last_utterance.topic) \
                or topic_is_user(last_utterance.topic):
            return tactic.psychiatrist(last_utterance, chatbot.name)

        if respond_passively(chatbot, user, mood_magnitude):
            return stay_on_topic_passive(conversation, chatbot, user,
                mood_magnitude, topic_magnitude, personas)
        else: # respond assertively
            return stay_on_topic_assertive(conversation, chatbot, user,
                mood_magnitude, topic_magnitude, personas)
    """

# TODO have random select, have it be a skewed normal, and mean wherever
# personality.mood is.
def change_topic_passive(conversation, chatbot, user, mood_magnitude,
        topic_magnitude, personas):
    choice = np.random.choice(3,1)
    if choice == 0:
    # silence or no response or minimal response
        return Utterance(
            chatbot.name,
            DA.silence,
            last_utterance.topic,
            chatbot.personality.mood,
            chatbot.persoality.assertiveness
        )
    elif chocie == 1:
    # ask to change topic, no expression of sent, not alternatives
        return Utterance(
            chatbot.name,
            DA.question_information,
            last_utterance.topic,
            chatbot.personality.mood,
            chatbot.persoality.assertiveness
        )
    # express sent, no alternatives
    return Utterance(
        chatbot.name,
        DA.statement_opinion,
        last_utterance.topic,
        chatbot.personality.mood,
        chatbot.persoality.assertiveness
    )

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
    choice = np.random.choice(3,1)
    # Listening oriented

    # Reinforce passively, "me too", "interesting."


    return

def stay_on_topic_assertive(conversation, chatbot, user, mood_magnitude,
        topic_magnitude, personas):

    # Leading Conversation, Informing/Expressing views

    # Reinforce actively "yes and this too..."

    return

def response_matrix(last_utterance, chatbot):
    mat = np.loadtxt(open("../data/da_matrix.csv"), delimiter=",", skiprows=1,
        usecols=range(1,27))
    mat = mat / np.sum(mat, axis=0)

    da_names = [da.name for da in DA if da.name not in
        ["statement", "question", "response_action"]]
    response_col = da_names.index(last_utterance.dialogue_act.name)
    return Utterance(
        chatbot.name,
        DA[np.random.choice(da_names, p=mat[:, response_col])],
        last_utterance.topic,
        min(max(np.random.normal(chatbot.personality.mood, 2), 10), 1),
        min(max(np.random.normal(chatbot.personality.assertiveness, 2), 10), 1)
    )

def farewell(chatbot):
    return Utterance(
        chatbot.name,
        DA.farewell,
        "self_user",
        chatbot.personality.mood,
        chatbot.personality.assertiveness
    )
