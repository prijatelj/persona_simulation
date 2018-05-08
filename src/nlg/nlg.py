"""
The Natural Language Generation classes and functions for generting the
persona's response utterance.

:author: Derek S. Prijatelj
"""

from nltk.chat.eliza import eliza_chatbot
from conversation import DialogueAct as DA, is_statement, is_question, \
    is_response_action, is_backchannel
from nlg import generic_response

def generate_response_text(utterance_metadata, persona, conversation):
    """
    Generate response utterance given the utterance metadata, which is an
    incomplete Utterance object missing the text.

    :return: str Text that matches the corresponding Utterance metadata.
    """
    if is_statement(utterance_metadata.dialogue_act):
        text = statement(utterance_metadata, persona, conversation)
    elif is_question(utterance_metadata.dialogue_act):
        text = question(utterance_metadata, persona, conversation)
    elif is_response_action(utterance_metadata.dialogue_act):
        text = response_action(
            utterance_metadata, persona, conversation)
    elif is_backchannel(utterance_metadata.dialogue_act):
        text = backchannel(utterance_metadata, persona, conversation)
    else:
        text = other(utterance_metadata, persona, conversation)

    if text != '' and utterance_metadata.sentiment <= 1:
        insult = generic_response.insult_gen()
        text = text + ' ' + insult[0].upper() + insult[1:]

        text = text+'!' if utterance_metadata.assertiveness >= 9 else text+'.'

    # TODO returning the utterance object may be unnecessary, given set_text()
    return text

def statement(utterance_metadata, persona, conversation):
    #if utterance_metadata.dialogue_act == DA.statement:
    #    text = generic_response.statement(persona, conversation)
    if utterance_metadata.dialogue_act == DA.statement_information:
        text = generic_response.statement_information(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.statement_experience:
        text = generic_response.statement_experience(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.statement_preference:
        text = generic_response.statement_preference(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.statement_opinion:
        text = generic_response.statement_opinion(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.statement_desire:
        text = generic_response.statement_desire(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.statement_plan:
        text = generic_response.statement_plan(persona, conversation)

    return text[0].upper() + text[1:] + "."
    #utterance_metadata.set_text(text)
    #return utterance_metadata

def question(utterance_metadata, persona, conversation):
    #if utterance_metadata.dialogue_act == DA.question:
    #    text = generic_response.question(persona, conversation)
    if utterance_metadata.dialogue_act == DA.question_information:
        text = generic_response.question_information(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.question_experience:
        text = generic_response.question_experience(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.question_preference:
        text = generic_response.question_preference(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.question_opinion:
        text = generic_response.question_opinion(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.question_desire:
        text = generic_response.question_desire(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.question_plan:
        text = generic_response.question_plan(persona, conversation)

    return text[0].upper() + text[1:] + "?"
    #utterance_metadata.set_text(text)
    #return utterance_metadata

def response_action(utterance_metadata, persona, conversation):
    if utterance_metadata.dialogue_act == DA.greeting:
        text = generic_response.greeting(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.farewell:
        text = generic_response.farewell(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.thanks:
        text = generic_response.thanks(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.apology:
        text = generic_response.apology(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.confirm:
        text = generic_response.confirm(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.disconfirm:
        text = generic_response.disconfirm(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.agreement:
        text = generic_response.agreement(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.disagreement:
        text = generic_response.disagreement(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.silence:
        text = generic_response.silence(persona, conversation)

    if text != "":
        text = text[0].upper() + text[1:] + "."
    return text
    #utterance_metadata.set_text(text)
    #return utterance_metadata

def backchannel(utterance_metadata, persona, conversation):
    if utterance_metadata.dialogue_act == DA.backchannel:
        text = generic_response.backchannel(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.request_confirmation:
        text = generic_response.request_confirmation(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.request_clarification:
        text = generic_response.request_clarification(persona, conversation)
    elif utterance_metadata.dialogue_act == DA.repeat:
        #utterance_metadata.set_text(persona.utterances[-1])
        # TODO add conversation/convo history/last utterance to these
        #utterance_metadata.set_text("Please repeat that.")
        return "Please repeat that."
    elif utterance_metadata.dialogue_act == DA.paraphrase:
        text = generic_response.paraphrase(persona, conversation)

    return text[0].upper() + text[1:] + "."
    #utterance_metadata.set_text(text)
    #return utterance_metadata

def other(utterance_metadata, persona, conversation):
    # TODO somehow implement other...
    #text = text[0].upper() + text[1:] + "."
    #utterance_metadata.set_text(text)
    last_utterance = conversation.last_utterance
    if last_utterance is None:
        return eliza_chatbot.respond("")
    return eliza_chatbot.respond(last_utterance.text)


def finish_text(text, is_question, sentiment=None, formal=None):
    text = text[0].upper() + text[1:]
