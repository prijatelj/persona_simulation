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
from enum import Enum
import json

class Dialogue_Act(Enum):
    """ Dialogue Act tag set. Shirberg et.al 1998"""
    statement           = 1
    statement_description   = 1.1
    statement_opinion       = 1.2
    question            = 2
    question_yes_no         = 2.1
    question_wh             = 2.2
    question_declarative    = 2.3
    question_open           = 2.4
    backchannels        = 3
    incomplete_units    = 4
    agreements          = 5
    appreciations       = 6
    other               = 7

class Utterance:
    """Defines an individual utterance with the specific NLU information"""
    def __init__(self, text, topic, sentiment, dialogue_act):
        assert isinstance(text, str)
        assert "[s]" in text and "[\s]" in text # Subject Tags, rest = prediacte
        assert isinstance(topic, str)
        assert isinstance(sentiment, int) && sentiment >= 1 and sentiment <= 10
        assert isinstance(dialogue_act, Dialogue_Act)

        self._text = text
        self._topic = topic
        self._sentiment = sentiment
        self._dialogue_act = dialogue_act

    @property
    def text(self):
        return self._text.copy()

    @property
    def topic(self):
        return self._topic.copy()

    @property
    def sentiment(self):
        return self._sentiment.copy()

    @property
    def dialogue_act(self):
        return self._dialogue_act.copy()

class Personality:
    """ The Personality of a speaker. Polar sentiment. """
    def __init__(self, sentiment, attitude):
        assert sentiment in [1,2,3,4,5,6,7,8,9,10]
        assert attitude in [1,2,3,4,5,6,7,8,9,10]
        self._sentiment = sentiment
        self._attitude = attitude

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def attitude(self):
        return self._attitude

    def set_sentiment(self, sentiment):
        self._sentiment = sentiment

    def set_attitude(selt, attitude):
        self._attitude = attitude

class Persona:
    """ Defines a Persona of a participant in the conversation. """
    # TODO add history of Personality dict of {turn count, Personality}
    #   However, this only works if able to be matched to correct conversation
    #   history.
    def __init__(self, name, personality, topic_sentiment=none):
        assert isinstance(name, str)
        assert isinstance(personality, Personality)
        assert isinstance(topic_sentiment, dict) or topic_sentiment is None
        if topic_sentiment is not None and len(topic_sentiment) > 0:
            # values ints [1,10]
            assert isinstance(list(topic_sentiment.values())[0], int)

        #self._id = name # maybe necessary later, not in prototype. Use names.
        self._name = name
        self._personality = personality
        self._topic_sentiment = topic_sentiment

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def attitude(self):
        return self._attitude

    @property
    def name(self):
        return self._name

    @property
    def personality(self):
        return self._personality

    @property
    def topic_sentiment(self):
        return self._topic_sentiment

    def set_name(self, name):
        self._name = name

    def set_personality(self, personality):
        self._personality = personality

    def set_topic(self, topic, sentiment):
        self._topic_sentiment[topic] = sentiment

class Conversation_History:
    """
    Contains the conversation history with its NLU information.

    :param utterances: List of utterance objects detailing the conversation
        history.
    :param participants: dict of participant id to persona information.
    """
    def __init__(self, participants, utterances=None):
        assert isinstance(utterances, list) \
            and isinstance(utterances[1], Utterance)
        self._utterances = utterances
        self._participants = participants

    @property
    def utterances(self):
        return self._utterances

    @property
    def participants(self):
        return self._participants

    def add_utterance(self, utterance):
        assert isinstance(utterance, Utterance)
        self._utterances.append(utterance)

    def add_participant(self, participant):
        self._participants.append(participant)

def load_personality_file(path_to_json):
    with open(path_to_json, encoding='utf-8') as json_personality:
        personality = json.load(json_personality)

def nlu_cli(default_mood):
    """ Command line interface for user to give all NLU data of utterance. """
    mood = -1
    while mood not in [1,2,3,4,5,6,7,8,9,10]:
        mood = input("Enter your current mood on a scale of 1 to 10 where "
            + "1 is negative, 5 is neutral, and 10 is positive.")
        if mood == "":
            mood = default_mood
        else:
            mood = int(mood)

    topic = input("Enter Topic: ").strip().lower()

    #loop until they select correct dialogue act, show help after first fail
    dialogue_act = ""
    first = True
    da_names = [da.name for da in Dialogue_Act]
    while dialogue_act not in da_names:
        dialogue_act = input("Enter dialogue Act").strip().lower()

        if first and dialogue_act not in da_names:
            first = False
            # Help, details what each dialogue act means.
            print("Enter a dialogue act from list below:\n"
                #+ "statement"
                + "statement_description"
                + "statement_opinion"
                #+ "question"
                + "question_yes_no"
                + "question_wh"
                + "question_declarative"
                + "question_open"
                + "backchannels"
                + "incomplete_units"
                + "agreements"
                + "appreciations"
                + "other"
                )

    text = ""
    while "[s]" not in text or "[\s]" not in text:
        text = input("Enter utterance text with [s] and [\s] tags around "
        + "the subject:").strip()

    sentiment = -1
    while sentiment not in [1,2,3,4,5,6,7,8,9,10]:
        sentiment = int(input("Enter utterance sentiment 1 to 10. "
            + "1 negative, 5 neutral, and 10 positive"))

    # Make Utterance from input
    #return utterance and mood
    return Utterance(text, topic, sentiment, dialogue_act), mood

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("personality_file", type=load_personality_file)
    parser.add_argument(["-s","--sentiment"],
                        default=5,
                        type=int,
                        choices=[1,2,3,4,5,6,7,8,9,10],
                        help="The general mood of the user based on a scale of "
                            + "polar sentiment where 1 is negative and 10 is "
                            + "postive (5 is neutral).",
                        metavar="user sentiment")
    args = parser.parse_args()
    mood = args.mood

    # Create both Personas for the user and the system
    user_persona = Persona("user", Personality(mood, 5))
    simulated_persona = args.sentiment

    # initiate conversation
    conversation_history = Conversation_History([user, simulation])
    ongoing_conversation = True
    while(ongoing_conversation)
        # Query user for utterance
        utterance, mood = nlu_cli(mood)

        # update conversation history
        conversation_history.add_utterance(utterance)

        # update user persona
        if user_persona.personality.sentiment != mood:
            user_persona.personality.set_sentiment(mood)
        # inference on attitude if necessary for predictions

        # TODO update simulated persona(s)

        # Simulated Personality must determine how to respond and what to say
        # This is mostly outside of NLG, although the what to say part somewhat
        # overlaps with NLG task of content determination.

        # call NLG module

if __name__ == "__main__":
    main()
