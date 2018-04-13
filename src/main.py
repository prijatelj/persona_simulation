"""
Main interface to test/run the simulation.

:author: Derek S. Prijatelj
"""
from nlu.nlu_cli import nlu_cli, parse_args
from persona import Persona
from conversation import Conversation, DialogueAct
from intelligent_agent import intelligent_agent
from nlg import nlg

def main():
    args = parse_args()
    mood = args.mood

    # Ask user for their unique name: TODO have bot ask and parse this in convo
    username = input("Enter your name: ").strip()

    # Create both Personas for the user and the system
    user_persona = Persona(username, mood, 5)
    simulated_persona = args.personality_profile

    # personality dict:
    persona_dict = {
        user_persona.name:user_persona,
        simulated_persona.name:simulated_persona
    }

    conversation_history = Conversation(
        {user_persona.name, simulated_persona.name}
    )

    ongoing_conversation = True
    while ongoing_conversation:
        # Query user for utterance
        utterance, mood = nlu_cli(mood, user_persona.name)
        print("\n")

        # update conversation history
        conversation_history.add_utterance(utterance)

        # update user persona
        if user_persona.personality.mood != mood:
            user_persona.personality.set_mood(mood)
        # TODO Save topic sentiment for user_persona!

        # TODO update simulated persona(s) for future versions, non-prototype

        # Simulated Personality must determine how to respond and what to say
        # This is mostly outside of NLG, although the what to say part somewhat
        # overlaps with NLG task of content determination.
        response_metadata = intelligent_agent.decide_response(
            conversation_history,
            simulated_persona.name,
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

    # TODO Save conversation history log in "database" appropriately.

if __name__ == "__main__":
    main()
