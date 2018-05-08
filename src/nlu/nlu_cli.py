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
from persona import Persona
from conversation import DialogueAct as DA, QuestionType as QT, Utterance, \
    Conversation, is_question

def nlu_cli(default_mood, user_id):
    """ Command line interface for user to give all NLU data of utterance. """
    mood = -1 # TODO currently superfulous while loop given default mood.
    while mood not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        mood = input(
            "Enter your current mood on a scale of 1 to 10 where "
            + "1 is negative, 5 is neutral, and 10 is positive: "
        )
        if mood == "":
            mood = default_mood
        else:
            mood = int(mood)
        mood = default_mood if mood == "" else int(mood)

    topic = input("Enter Topic: ").strip().lower()

    #loop until they select correct dialogue act, show help after first fail
    dialogue_act = ""
    first = True
    da_names = [da.name for da in DA if da.name not in
        ['statement', 'question', 'response_action']
    ]
    while dialogue_act not in da_names:
        dialogue_act = input("Enter dialogue Act: ").strip().lower()

        # TODO add help print out descriptions
        if first and dialogue_act not in da_names:
            first = False
            # Help, details what each dialogue act means.
            print("Enter a dialogue act from list below:\n", da_names)

    question_type = None
    if is_question(DA[dialogue_act]):
        question_type = ""
        first = True
        question_types = [qt.name for qt in QT]
        while question_type not in question_types:
            question_type = input("Enter question type: ").strip().lower()

            # TODO add help print out descriptions
            if first and question_type not in question_types:
                first = False
                # Help, details what each dialogue act means.
                print("Enter a question type from list below:\n",
                    question_types)

    text = input(
        "Enter utterance text: "
    ).strip()

    sentiment = -1
    while sentiment not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        sentiment = input(
            "Enter utterance sentiment 1 to 10. "
            + "1 negative, 5 neutral, and 10 positive: "
        )
        sentiment = -1 if sentiment == "" else int(sentiment)

    assertiveness = -1
    while assertiveness not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        assertiveness = input(
            "Enter utterance assertiveness 1 to 10. "
            + "1 passive/listening oriented, 5 neutral, and "
            + "10 assertive/leading conversation: "
        )
        assertiveness = -1 if assertiveness == "" else int(assertiveness)

    return Utterance(
            user_id,
            DA[dialogue_act],
            topic,
            sentiment,
            assertiveness,
            text,
            question_type
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
    conversation_history = Conversation(
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

        if utterance.dialogue_act == DA.farewell:
            ongoing_conversation = False

if __name__ == "__main__":
    main()
