"""
Tests all related to the conversation files.
"""

from copy import copy
from src.conversation import DialogueAct as DA, QuestionType, \
    Utterance, Conversation, ConversationHistory, \
    is_statement, is_question, is_response_action, is_backchannel, \
    statement_to_question, question_to_statement, topic_is_self, topic_is_user

class TestGeneralFunctions(object):
    def test_dialogue_acts_names(self):
        """ Confirms that the dialogue acts are named as expected. """
        da_names = [da.name for da in DA]
        assert 'statement' in da_names
        assert 'statement_information' in da_names
        assert 'statement_experience' in da_names
        assert 'statement_preference' in da_names
        assert 'statement_opinion' in da_names
        assert 'statement_desire' in da_names
        assert 'statement_plan' in da_names

        assert 'question' in da_names
        assert 'question_information' in da_names
        assert 'question_experience' in da_names
        assert 'question_preference' in da_names
        assert 'question_opinion' in da_names
        assert 'question_desire' in da_names
        assert 'question_plan' in da_names

        assert 'response_action' in da_names
        assert 'greeting' in da_names
        assert 'farewell' in da_names
        assert 'thanks' in da_names
        assert 'apology' in da_names
        assert 'confirm' in da_names
        assert 'disconfirm' in da_names
        assert 'agreement' in da_names
        assert 'disagreement' in da_names
        assert 'silence' in da_names

        assert 'backchannel' in da_names
        assert 'request_confirmation' in da_names
        assert 'request_clarification' in da_names
        assert 'repeat' in da_names
        assert 'paraphrase' in da_names

        assert 'other' in da_names

    def test_question_type_names(self):
        qt_names = [q.name for q in QuestionType]
        assert 'polar' in qt_names
        assert 'declarative' in qt_names
        assert 'wh' in qt_names
        assert 'open_ended' in qt_names
        assert 'rhetorical' in qt_names
        assert 'other' in qt_names

    def test_is_statement(self):
        assert is_statement(DA.statement)
        assert is_statement(DA.statement_information)
        assert is_statement(DA.statement_experience)
        assert is_statement(DA.statement_preference)
        assert is_statement(DA.statement_opinion)
        assert is_statement(DA.statement_desire)
        assert is_statement(DA.statement_plan)

        # Checks if all Dialogue Acts that are said to be a statement also
        # contain the string 'statement' in their names. This is the full test.
        assert (
            [is_statement for is_statement in
                map(is_statement,
                    [da for da in DA]
                )
            ]
            == [statement_in_name for statement_in_name in
                map(lambda da_name: 'statement' in da_name,
                    [da.name for da in DA]
                )
            ]
        )

    def test_is_question(self):
        assert is_question(DA.question)
        assert is_question(DA.question_information)
        assert is_question(DA.question_experience)
        assert is_question(DA.question_preference)
        assert is_question(DA.question_opinion)
        assert is_question(DA.question_desire)
        assert is_question(DA.question_plan)

        # Checks if all Dialogue Acts that are said to be a question also
        # contain the string 'question' in their names. This is the full test.
        assert (
            [is_question for is_question in
                map(is_question,
                    [da for da in DA]
                )
            ]
            == [question_in_name for question_in_name in
                map(lambda da_name: 'question' in da_name,
                    [da.name for da in DA]
                )
            ]
        )

    # TODO Note, all these is_a tests (except statement and question) only test
    # if the correct DA returns True, note if the incorrect DA returns False.
    # Therefore incomplete test!
    def test_is_response_action(self):
        assert is_response_action(DA.response_action)
        assert is_response_action(DA.greeting)
        assert is_response_action(DA.farewell)
        assert is_response_action(DA.thanks)
        assert is_response_action(DA.apology)
        assert is_response_action(DA.confirm)
        assert is_response_action(DA.disconfirm)

    def test_is_backchannel(self):
        assert is_backchannel(DA.backchannel)
        assert is_backchannel(DA.request_confirmation)
        assert is_backchannel(DA.request_clarification)
        assert is_backchannel(DA.repeat)
        assert is_backchannel(DA.paraphrase)

    def test_statement_to_question(self):
        # Dependent on test_is_statement and test_is_question
        statement_das = [da for da in DA if 'statement' in da.name]
        question_das = [da for da in DA if 'question' in da.name]

        results = [question_da for question_da in
            map(statement_to_question, statement_das)
        ]

        assert question_das == results

    def test_question_to_statement(self):
        # Dependent on test_is_statement and test_is_question
        statement_das = [da for da in DA if 'statement' in da.name]
        question_das = [da for da in DA if 'question' in da.name]

        results = [statement_da for statement_da in
            map(question_to_statement, question_das)
        ]

        assert statement_das == results

    def test_topic_is_self(self):
        assert topic_is_self("you")
        assert topic_is_self("yourself")
        assert topic_is_self("self_bot")

    def test_topic_is_user(self):
        assert topic_is_user("me")
        assert topic_is_user("myself")
        assert topic_is_user("self_user")

class TestUtterance(object):

    def test_copy(self):
        utterance = Utterance(
            "test_speaker",
            DA.statement_information,
            "test",
            5,
            5,
            "This is a test."
        )
        utterance_copy = copy(utterance)
        assert utterance == utterance_copy and utterance is not utterance_copy

        utterance_copy = utterance.copy()
        assert utterance == utterance_copy and utterance is not utterance_copy

        utterance = Utterance(
            "test_speaker",
            DA.question_information,
            "test",
            5,
            5,
            "This is a test?",
            QuestionType.polar
        )
        utterance_copy = copy(utterance)
        assert utterance == utterance_copy and utterance is not utterance_copy

        utterance_copy = utterance.copy()
        assert utterance == utterance_copy and utterance is not utterance_copy

    # TODO test the properties to see if they are copies or the actual objects.
    #def test_properties

# TODO test Conversation and ConversationHistory on json save/load
