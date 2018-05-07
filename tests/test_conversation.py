"""
Tests all related to the conversation files.
"""

from src.conversation import DialogueAct as DA, QuestionType, \
    Utterance, Conversation, ConversationHistory, \
    is_statement, is_question, is_response_action, is_backchannel, \
    statement_to_question, question_to_statement, topic_is_self, topic_is_user

class TestGeneralFunctions(object):
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

#class TestUtterance(object):

