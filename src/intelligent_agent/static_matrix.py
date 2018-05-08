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

def static_matrix(conversation, chatbot, user, personas=None):
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
        utterance = Utterance(
            chatbot.name,
            DA.farewell,
            "self_user",
            chatbot.personality.mood,
            chatbot.personality.assertiveness
        )

        text = nlg.generate_response_text(utterance, chatbot, conversation)
        utterance.set_text(text)
        return utterance

    if len(conversation.topic_to_utterances.keys()) <= 1:
        # New conversation started
        if last_utterance.dialogue_act == DA.greeting:
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
        elif ( not topic_is_self(last_utterance.topic)
            and not topic_is_user(last_utterance.topic)
            and is_question(last_utterance.dialogue_act)
            ):
            utterance = Utterance(
                chatbot.name,
                question_to_statement(last_utterance.dialogue_act),
                last_utterance.topic,
                chatbot.personality.mood,
                chatbot.personality.assertiveness
            )
            text = nlg.generate_response_text(utterance, chatbot, conversation)
            utterance.set_text(text)
            return utterance
        elif ( not topic_is_self(last_utterance.topic)
            and not topic_is_user(last_utterance.topic)
            and is_statement(last_utterance.dialogue_act)
            ):
            utterance = Utterance(
                chatbot.name,
                statement_to_question(last_utterance.dialogue_act),
                last_utterance.topic,
                chatbot.personality.mood,
                chatbot.personality.assertiveness
            )
            text = nlg.generate_response_text(utterance, chatbot, conversation)
            utterance.set_text(text)
            return utterance
        else:
            return tactic.psychiatrist(last_utterance, chatbot.name)
    else: # Ongoing Conversation
        # topics have been discussed, and conversation ongoing
        if topic_is_self(last_utterance.topic) \
                or topic_is_user(last_utterance.topic):
            return tactic.psychiatrist(last_utterance, chatbot.name)
        else:
            return response_matrix(last_utterance, chatbot, conversation)

def response_matrix(last_utterance, chatbot, conversation):
    mat = np.loadtxt(open("../data/da_matrix.csv"), delimiter=",", skiprows=1,
        usecols=range(1,27))
    mat = mat / np.sum(mat, axis=0)

    da_names = [da.name for da in DA if da.name not in
        ["statement", "question", "response_action"]]
    response_col = da_names.index(last_utterance.dialogue_act.name)
    utterance = Utterance(
        chatbot.name,
        DA[np.random.choice(da_names, p=mat[:, response_col])],
        last_utterance.topic,
        min(max(np.random.normal(chatbot.personality.mood, 2), 10), 1),
        min(max(np.random.normal(chatbot.personality.assertiveness, 2), 10), 1)
    )

    text = nlg.generate_response_text(utterance, chatbot, conversation)
    utterance.set_text(text)
    return utterance
