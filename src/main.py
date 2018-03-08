"""
Main interface to test/run the simulation.

:author: Derek S. Prijatelj
"""

from src.persona import Persona, ConversationHistory, DialogueAct

def main():
    args = parse_args()
    mood = args.mood

    # Create both Personas for the user and the system
    user_persona = Persona("user", mood, 5)
    simulated_persona = args.personality_profile

    # initiate conversation
    conversation_history = ConversationHistory(
        [user_persona, simulated_persona]
    )

    ongoing_conversation = True
    while ongoing_conversation:
        # Query user for utterance
        utterance, mood = nlu_cli(mood)

        # update conversation history
        conversation_history.add_utterance(utterance)

        # update user persona
        if user_persona.personality.mood != mood:
            user_persona.personality.set_mood(mood)
        # inference on aggressiveness if necessary for predictions

        # TODO update simulated persona(s) for future versions

        # Simulated Personality must determine how to respond and what to say
        # This is mostly outside of NLG, although the what to say part somewhat
        # overlaps with NLG task of content determination.
        response_metadata = tactician.decide_response(
            simulated_persona,
            user_persona,
            conversation_history
        )

        # call NLG module to generate actual text
        response_utterance = nlg.response(response_metadata)

        print(response_utterance, "\n")

        if response_metadata.dialogue_act == DialogueAct.farewell:
            ongoing_conversation = False


if __name__ == "__main__":
    main()
