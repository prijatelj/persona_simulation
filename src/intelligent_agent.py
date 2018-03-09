"""
This is the intelligent agent behind the decision making of how to respond to
the user's utterance.

:author: Derek S. Prijatelj
"""

def decide_response(simulated_persona, user_persona, conversation_history):
    """
    Main interface for intelligent agent to decide how to response. With the NLU
    information and the persona making this decision, generates the metadata of
    the persona's response utterance. This metadata matches the type and format
    of the NLU information.
    """

    """
    Tactics:
    Query:  Query General: query the user in general terms, askw hat they think of what has been discussed or a few canned phrases.
            Query Specific: ask what they think of a specific topic/subtopic of
            a previsouly discussed topic. (searches Database for specifics)
    Request elaboration, clarification, etc...
    Statement:
        State things about a topic using database information. (expert system)

    Tell a joke.
    """

    # determine state of conversation


