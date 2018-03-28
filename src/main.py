"""
Main interface to test/run the simulation.

:author: Derek S. Prijatelj
"""
from src.nlu_cli import nlu_cli, parse_args
from src.persona import Persona, ConversationHistory, DialogueAct
import src.intelligent_agent as intelligent_agent
import src.nlg as nlg

def main():
    args = parse_args()
    mood = args.mood

    # Create both Personas for the user and the system
    user_persona = Persona("user", mood, 5)
    simulated_persona = args.personality_profile

    # personality dict:
    persona_dict = {
        user_persona.name:user_persona,
        simulated_persona.name:simulated_persona
    }

    # initiate conversation
    conversation_history = ConversationHistory(
        [user_persona.name, simulated_persona.name]
    )

    ongoing_conversation = True
    while ongoing_conversation:
        # Query user for utterance
        utterance, mood = nlu_cli(mood, user_persona.name)

        # update conversation history
        conversation_history.add_utterance(utterance)

        # update user persona
        if user_persona.personality.mood != mood:
            user_persona.personality.set_mood(mood)
        # inference on assertiveness if necessary for predictions

        # TODO update simulated persona(s) for future versions

        # Simulated Personality must determine how to respond and what to say
        # This is mostly outside of NLG, although the what to say part somewhat
        # overlaps with NLG task of content determination.
        response_metadata = intelligent_agent.decide_response(
            conversation_history,
            user_persona.name,
            persona_dict
        )

        # call NLG module to generate actual text, if needed.
        response_utterance = nlg.generate_response_text(
            response_metadata, conversation_history, simulated_persona) \
            if response_metadata.text is None else response_metadata

        response_utterance.print_out()

        # update conversation history
        conversation_history.add_utterance(response_utterance)

        if response_metadata.dialogue_act == DialogueAct.farewell:
            ongoing_conversation = False

if __name__ == "__main__":
    main()
