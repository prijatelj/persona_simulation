"""
This is the intelligent agent behind the decision making of how to respond to
the user's utterance.

:author: Derek S. Prijatelj
"""

def decide_response(simulated_persona, user_persona, conversation_history):
    """
    Main interface for tactician to decide how to response. Given the NLU
    information and the persona making this decision, generates the metadata of
    the persona's response utterance. This metadata matches the type and format
    of the NLU information.
    """

