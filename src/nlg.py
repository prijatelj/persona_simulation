"""
The Natural Language Generation classes and functions for generting the
persona's response utterance.

:author: Derek S. Prijatelj
"""

from persona import DialogueAct as DA, is_statement, is_question, \
    is_response_action, is_backchannel
import generic_response

def generate_response_text(utterance_metadata, conversation_history,
        persona):
    """
    Generate response utterance given the utterance metadata, which is an
    incomplete Utterance object missing the text.
    """
    if is_statement(utterance_metadata.dialogue_act):
        utterance_metadata = statement(utterance_metadata, persona)
    elif is_question(utterance_metadata.dialogue_act):
        utterance_metadata = question(utterance_metadata, persona)
    elif is_response_action(utterance_metadata.dialogue_act):
        utterance_metadata = response_action(
            utterance_metadata, persona)
    elif is_backchannel(utterance_metadata.dialogue_act):
        utterance_metadata = backchannel(utterance_metadata, persona)
    else:
        utterance_metadata = other(utterance_metadata, persona)

    # TODO returning the utterance object may be unnecessary, given set_text()
    return utterance_metadata

def statement(utterance_metadata, persona):
    if utterance_metadata.dialogue_act == DA.statement:
        utterance_metadata.set_text(generic_response.statement(persona))
    elif utterance_metadata.dialogue_act == DA.statement_information:
        utterance_metadata.set_text(
            generic_response.statement_information(persona))
    elif utterance_metadata.dialogue_act == DA.statement_experience:
        utterance_metadata.set_text(
            generic_response.statement_experience(persona))
    elif utterance_metadata.dialogue_act == DA.statement_preference:
        utterance_metadata.set_text(
            generic_response.statement_preference(persona))
    elif utterance_metadata.dialogue_act == DA.statement_opinion:
        utterance_metadata.set_text(
            generic_response.statement_opinion(persona))
    elif utterance_metadata.dialogue_act == DA.statement_desire:
        utterance_metadata.set_text(
            generic_response.statement_desire(persona))
    elif utterance_metadata.dialogue_act == DA.statement_plan:
        utterance_metadata.set_text(
            generic_response.statement_plan(persona))
    return utterance_metadata

def question(utterance_metadata, persona):
    if utterance_metadata.dialogue_act == DA.question:
        utterance_metadata.set_text(generic_response.question(persona))
    elif utterance_metadata.dialogue_act == DA.question_information:
        utterance_metadata.set_text(
            generic_response.question_information(persona))
    elif utterance_metadata.dialogue_act == DA.question_experience:
        utterance_metadata.set_text(
            generic_response.question_experience(persona))
    elif utterance_metadata.dialogue_act == DA.question_preference:
        utterance_metadata.set_text(
            generic_response.question_preference(persona))
    elif utterance_metadata.dialogue_act == DA.question_opinion:
        utterance_metadata.set_text(
            generic_response.question_opinion(persona))
    elif utterance_metadata.dialogue_act == DA.question_desire:
        utterance_metadata.set_text(
            generic_response.question_desire(persona))
    elif utterance_metadata.dialogue_act == DA.question_plan:
        utterance_metadata.set_text(
            generic_response.question_plan(persona))
    return utterance_metadata

def response_action(utterance_metadata, persona):
    if utterance_metadata.dialogue_act == DA.greeting:
        utterance_metadata.set_text(generic_response.greeting(persona))
    elif utterance_metadata.dialogue_act == DA.farewell:
        utterance_metadata.set_text(generic_response.farewell(persona))
    elif utterance_metadata.dialogue_act == DA.thanks:
        utterance_metadata.set_text(generic_response.thanks(persona))
    elif utterance_metadata.dialogue_act == DA.apology:
        utterance_metadata.set_text(generic_response.apology(persona))
    elif utterance_metadata.dialogue_act == DA.confirm:
        utterance_metadata.set_text(generic_response.confirm(persona))
    elif utterance_metadata.dialogue_act == DA.disconfirm:
        utterance_metadata.set_text(generic_response.disconfirm(persona))
    elif utterance_metadata.dialogue_act == DA.agreement:
        utterance_metadata.set_text(generic_response.agreement(persona))
    elif utterance_metadata.dialogue_act == DA.disagreement:
        utterance_metadata.set_text(generic_response.disagreement(persona))
    elif utterance_metadata.dialogue_act == DA.silence:
        utterance_metadata.set_text(generic_response.silence(persona))
    return utterance_metadata

def backchannel(utterance_metadata, persona):
    if utterance_metadata.dialogue_act == DA.backchannel:
        utterance_metadata.set_text(generic_response.backchannel(persona))
    elif utterance_metadata.dialogue_act == DA.request_confirmation:
        utterance_metadata.set_text(
            generic_response.request_confirmation(persona))
    elif utterance_metadata.dialogue_act == DA.request_clarification:
        utterance_metadata.set_text(
            generic_response.request_clarification(persona))
    elif utterance_metadata.dialogue_act == DA.repeat:
        utterance_metadata.set_text(persona.utterances[-1])
    elif utterance_metadata.dialogue_act == DA.paraphrase:
        utterance_metadata.set_text(generic_response.paraphrase(persona))
    return utterance_metadata

def other(utterance_metadata, persona):
    return utterance_metadata
