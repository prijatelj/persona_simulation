"""
The Natural Language Generation classes and functions for generting the
persona's response utterance.

:author: Derek S. Prijatelj
"""

from conversation import DialogueAct as DA, is_statement, is_question, \
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
        text = generic_response.statement(persona)
    elif utterance_metadata.dialogue_act == DA.statement_information:
        text = generic_response.statement_information(persona)
    elif utterance_metadata.dialogue_act == DA.statement_experience:
        text = generic_response.statement_experience(persona)
    elif utterance_metadata.dialogue_act == DA.statement_preference:
        text = generic_response.statement_preference(persona)
    elif utterance_metadata.dialogue_act == DA.statement_opinion:
        text = generic_response.statement_opinion(persona)
    elif utterance_metadata.dialogue_act == DA.statement_desire:
        text = generic_response.statement_desire(persona)
    elif utterance_metadata.dialogue_act == DA.statement_plan:
        text = generic_response.statement_plan(persona)

    text = text[0].upper() + text[1:] + "."
    utterance_metadata.set_text(text)
    return utterance_metadata

def question(utterance_metadata, persona):
    if utterance_metadata.dialogue_act == DA.question:
        text = generic_response.question(persona)
    elif utterance_metadata.dialogue_act == DA.question_information:
        text = generic_response.question_information(persona)
    elif utterance_metadata.dialogue_act == DA.question_experience:
        text = generic_response.question_experience(persona)
    elif utterance_metadata.dialogue_act == DA.question_preference:
        text = generic_response.question_preference(persona)
    elif utterance_metadata.dialogue_act == DA.question_opinion:
        text = generic_response.question_opinion(persona)
    elif utterance_metadata.dialogue_act == DA.question_desire:
        text = generic_response.question_desire(persona)
    elif utterance_metadata.dialogue_act == DA.question_plan:
        text = generic_response.question_plan(persona)

    text = text[0].upper() + text[1:] + "?"
    utterance_metadata.set_text(text)
    return utterance_metadata

def response_action(utterance_metadata, persona):
    if utterance_metadata.dialogue_act == DA.greeting:
        text = generic_response.greeting(persona)
    elif utterance_metadata.dialogue_act == DA.farewell:
        text = generic_response.farewell(persona)
    elif utterance_metadata.dialogue_act == DA.thanks:
        text = generic_response.thanks(persona)
    elif utterance_metadata.dialogue_act == DA.apology:
        text = generic_response.apology(persona)
    elif utterance_metadata.dialogue_act == DA.confirm:
        text = generic_response.confirm(persona)
    elif utterance_metadata.dialogue_act == DA.disconfirm:
        text = generic_response.disconfirm(persona)
    elif utterance_metadata.dialogue_act == DA.agreement:
        text = generic_response.agreement(persona)
    elif utterance_metadata.dialogue_act == DA.disagreement:
        text = generic_response.disagreement(persona)
    elif utterance_metadata.dialogue_act == DA.silence:
        text = generic_response.silence(persona)

    text = text[0].upper() + text[1:] + "."
    utterance_metadata.set_text(text)
    return utterance_metadata

def backchannel(utterance_metadata, persona):
    if utterance_metadata.dialogue_act == DA.backchannel:
        text = generic_response.backchannel(persona)
    elif utterance_metadata.dialogue_act == DA.request_confirmation:
        text = generic_response.request_confirmation(persona)
    elif utterance_metadata.dialogue_act == DA.request_clarification:
        text = generic_response.request_clarification(persona)
    elif utterance_metadata.dialogue_act == DA.repeat:
        utterance_metadata.set_text(persona.utterances[-1])
        return utterance_metadata
    elif utterance_metadata.dialogue_act == DA.paraphrase:
        text = generic_response.paraphrase(persona)

    text = text[0].upper() + text[1:] + "."
    utterance_metadata.set_text(text)
    return utterance_metadata

def other(utterance_metadata, persona):
    # TODO somehow implement other...
    #text = text[0].upper() + text[1:] + "."
    #utterance_metadata.set_text(text)
    return utterance_metadata
