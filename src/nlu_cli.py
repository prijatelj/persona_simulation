"""
Natural Language Understanding Command Line Interface which serves as a
substitute for the actual Natural Language Understanding component of the
chatbot.

The NLU component will consist of:

- History of Conversation, including most recent user utterance.
- Persona of each utterance in the history
- Persona of User overall.
- Dialogue Act for each utterance

TODO: Switch from Python to C++ or Cython or Java.
    Python feels only good for prototype...

:author: Derek S. Prijatelj
"""

import argparse
from src.persona import DialogueAct, Utterance, Persona, ConversationHistory

def nlu_cli(default_mood):
    """ Command line interface for user to give all NLU data of utterance. """
    mood = -1
    while mood not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        mood = input(
            "Enter your current mood on a scale of 1 to 10 where "
            + "1 is negative, 5 is neutral, and 10 is positive: "
        )
        if mood == "":
            mood = default_mood
        else:
            mood = int(mood)

    topic = input("Enter Topic: ").strip().lower()

    #loop until they select correct dialogue act, show help after first fail
    dialogue_act = ""
    first = True
    da_names = [da.name for da in DialogueAct]
    while dialogue_act not in da_names:
        dialogue_act = input("Enter dialogue Act: ").strip().lower()

        # TODO fix help print out descriptions
        if first and dialogue_act not in da_names:
            first = False
            # Help, details what each dialogue act means.
            print("Enter a dialogue act from list below:\n", da_names)

    text = ""
    while "[s]" not in text or "[/s]" not in text:
        text = input(
            "Enter utterance text with [s] and [/s] tags around the subject: "
        ).strip()

    sentiment = -1
    while sentiment not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        sentiment = int(input(
            "Enter utterance sentiment 1 to 10. "
            + "1 negative, 5 neutral, and 10 positive: "
        ))

    aggressiveness = -1
    while aggressiveness not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        aggressiveness = int(input(
            "Enter utterance aggressiveness 1 to 10. "
            + "1 passive/listening oriented, 5 neutral, and "
            + "10 assertive/leading conversation: "
        ))

    return Utterance(text,
            topic,
            sentiment,
            aggressiveness,
            DialogueAct[dialogue_act]
        ), mood

def construct_persona(x):
    """Helper function for creating simulated persona"""
    return Persona(x)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("personality_profile",
        type=construct_persona,
        help="Enter the file path to the personality profile"
    )
    #"""
    parser.add_argument(
        "-s", "--mood",
        default=5,
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        help="The general mood of the user based on a scale of "
            + "polar mood where 1 is negative and 10 is "
            + "postive (5 is neutral).",
        metavar="user mood"
    )
    #"""
    return parser.parse_args()

def main():
    """Simple implementation of nlu_cli."""
    args = parse_args()
    mood = args.mood

    # Create both Personas for the user and the system
    user_persona = Persona("user", mood, 5)
    simulated_persona = args.personality_profile
    #simulated_persona = Persona(args.personality_profile)

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

        print("output NLU_CLI data:\n")
        utterance.print_out()
        print("\n", mood, "\n")

        print("output conversation_history updated\n")
        conversation_history.print_out()

        print("output user_persona.mood updated\n")
        user_persona.print_out()

        if utterance.dialogue_act == DialogueAct.farewell:
            ongoing_conversation = False

if __name__ == "__main__":
    main()
