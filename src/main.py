"""
Main interface to test/run the simulation.

:author: Derek S. Prijatelj
"""
from nlu.nlu_cli import nlu_cli, parse_args
from persona import Persona
from conversation import Conversation, DialogueAct as DA
from intelligent_agent import intelligent_agent, tactic
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

    # TODO Actually implement ConversationHistory, rather than one conversation
    conversation_history = Conversation(
        {user_persona.name, simulated_persona.name}
    )

    # TODO check if there exists a conversation history between the user and bot

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
        try:
            response_utterance = intelligent_agent.decide_response(
                conversation_history,
                simulated_persona.name,
                persona_dict
            )
        except:
            response_utterance = tactic.psychiatrist(utterance, chatbot.name)

        # TODO ensure NLG expects meta text!
        #   TODO OR, make it so IA's tactics create the text.
        # Utterance text should never be none, it will instead be a string of
        # keywords for tactics to fill in their place.
        #   ie. greeting username, question_experience ?
        #       = "Hello Bob, how was your day?"

        # call NLG module to generate actual text, if needed.
        #response_utterance = nlg.generate_response_text(
        #    response_metadata, simulated_persona, conversation_history) \
        #        if response_metadata.text is None else response_metadata

        print(response_utterance)

        # update conversation history
        conversation_history.add_utterance(response_utterance)

        if response_utterance.dialogue_act == DA.farewell:
            ongoing_conversation = False

    # TODO Save conversation history log in "database" appropriately.

if __name__ == "__main__":
    main()
