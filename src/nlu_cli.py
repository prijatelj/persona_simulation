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

from enum import Enum
import json
import argparse

class DialogueAct(Enum):
    """
    Customized dialogue acts: an abstraction of the intent of an utterance.
    Inspired by the dialogue act tag sets by Shirberg et. al 1998, and
    Megura et. al 2010.
    """
    statement_information   = 101
    statement_experience    = 102
    statement_preference    = 103
    statement_opinion       = 104 # May overlap with preference.
    statement_desire        = 105
    statement_plan          = 106

    question_information    = 201 # perhaps a gneral between fact, exp, & pref.
    question_experience     = 202
    question_preference     = 203
    question_opinion        = 204
    question_desire         = 205
    question_plan           = 206

    greeting                = 301
    farewell                = 302

    backchannel             = 500 # Listening Oriented. Perhaps unnecessary?
    request_confirmation    = 501
    request_clarification   = 502
    repeat                  = 503
    paraphrase              = 504
    sympathetic             = 505
    unsympathetic           = 506

    thanks                  = 601
    apology                 = 602
    confirm                 = 603
    disconfirm              = 604
    agreement               = 601 # perhaps agreeance be a range?
    disagreement            = 602

    silence                 = 700

    other                   = 000

class Utterance(object):
    """Defines an individual utterance with the specific NLU information"""
    def __init__(self, text, topic, sentiment, dialogue_act):
        assert isinstance(text, str)
        assert "[s]" in text and "[\\s]" in text #Subject Tags, rest = prediacte
        assert isinstance(topic, str)
        assert isinstance(sentiment, int) and sentiment >= 1 and sentiment <= 10
        assert isinstance(dialogue_act, DialogueAct)

        self._text = text
        self._topic = topic
        self._sentiment = sentiment
        self._dialogue_act = dialogue_act

    @property
    def text(self):
        """The string representation of the utterance's text"""
        return self._text.copy()

    @property
    def topic(self):
        """The conversational topic of the utterance"""
        return self._topic.copy()

    @property
    def sentiment(self):
        """The sentiment of the utterance"""
        return self._sentiment.copy()

    @property
    def dialogue_act(self):
        """The dialogue act to depict the intent of the utterance"""
        return self._dialogue_act.copy()

class Personality(object):
    """ The Personality of a speaker. Polar mood."""
    def __init__(self, mood, aggressiveness):
        assert mood in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert aggressiveness in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self._mood = mood
        self._aggressiveness = aggressiveness

    @property
    def mood(self):
        """The mood the Personality which is polar negative/positive"""
        return self._mood

    @property
    def aggressiveness(self):
        """"The aggressiveness in pursueing the Personality's goals."""
        return self._aggressiveness

    def set_mood(self, mood):
        self._mood = mood

    def set_aggressiveness(self, aggressiveness):
        self._aggressiveness = aggressiveness

    def get_dict(self):
        """
        Returns dict of Personality for easy saving and addition to Personality
        Profile.
        """
        return {"personality":
                    {"mood" : self._mood,
                     "aggressiveness": self._aggressiveness
                    }
               }

class Persona(object):
    """ Defines a Persona of a participant in the conversation. """
    # TODO add history of Personality dict of {turn count, Personality}
    # However, this only works if able to be matched to correct conversation
    # history. This will become the PersonalityProfile class in future versions.
    def __init__(self, name, personality, topic_sentiment=None):
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
    def name(self):
        return self._name

    @property
    def personality(self):
        return self._personality

    @property
    def topic_sentiment(self):
        return self._topic_sentiment

    # set functions for tracing errors
    def set_name(self, name):
        self._name = name

    def set_personality(self, personality):
        self._personality = personality

    def set_topic(self, topic, sentiment):
        self._topic_sentiment[topic] = sentiment

    def save_personality_profile(self, path_output_json):
        """ store personality profile (prototype's persona) into json """
        with open(path_output_json, 'w', encoding='utf-8') as json_output:
            # create dictionary structure of Personality Profile first:
            profile = dict()

            # create intricate parts if necessary
            name = {"name":self.name}
            personality = self.personality.get_dict()
            # TODO add philosophy part
            preferences = {"preferences": self.topic_sentiment}
            # TODO add explicit preferences

            content = [name, personality, preferences]

            # Then save all into final profile
            profile["personality profile"] = {
                key:value for d in content for key, value in d.items()
            }

            json.dump(
                profile,
                json_output,
                ensure_ascii=False,
                indent=4,
                sort_keys=True
            )

class ConversationHistory(object):
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

def load_personality_profile(path_to_json):
    """ given a file path, loads the personality profile from json. """
    # TODO Implement load_personality_profile from json
    with open(path_to_json, encoding='utf-8') as json_personality:
        profile = json.load(json_personality)

        # Construct Personality Profile object from json decoded data


    return

def nlu_cli(default_mood):
    """ Command line interface for user to give all NLU data of utterance. """
    mood = -1
    while mood not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        mood = input(
            "Enter your current mood on a scale of 1 to 10 where "
            + "1 is negative, 5 is neutral, and 10 is positive."
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
        dialogue_act = input("Enter dialogue Act").strip().lower()

        # TODO fix help print out descriptions
        if first and dialogue_act not in da_names:
            first = False
            # Help, details what each dialogue act means.
            print("Enter a dialogue act from list below:\n", da_names)

    text = ""
    while "[s]" not in text or "[\\s]" not in text:
        text = input(
            "Enter utterance text with [s] and [\\s] tags around the subject:"
        ).strip()

    sentiment = -1
    while sentiment not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        sentiment = int(input(
            "Enter utterance sentiment 1 to 10. "
            + "1 negative, 5 neutral, and 10 positive"
        ))

    # Make Utterance from input
    #return utterance and mood
    return Utterance(text, topic, sentiment, dialogue_act), mood

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("personality_profile", type=load_personality_profile)
    parser.add_argument(
        ["-s", "--sentiment"],
        default=5,
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        help="The general mood of the user based on a scale of "
            + "polar sentiment where 1 is negative and 10 is "
            + "postive (5 is neutral).",
        metavar="user sentiment"
    )
    return parser.parse_args()

def main():
    """Simple implementation of nlu_cli."""
    args = parse_args()
    mood = args.mood

    # Create both Personas for the user and the system
    user_persona = Persona("user", Personality(mood, 5))
    simulated_persona = args.personality_profile

    # initiate conversation
    conversation_history = Conversation_History(
        [user_persona, simulated_persona]
    )

    ongoing_conversation = True
    while ongoing_conversation:
        # Query user for utterance
        utterance, mood = nlu_cli(mood)

        # update conversation history
        conversation_history.add_utterance(utterance)

        # update user persona
        if user_persona.personality.sentiment != mood:
            user_persona.personality.set_sentiment(mood)
        # inference on aggressiveness if necessary for predictions

        # TODO update simulated persona(s)

        # Simulated Personality must determine how to respond and what to say
        # This is mostly outside of NLG, although the what to say part somewhat
        # overlaps with NLG task of content determination.

        # call NLG module

if __name__ == "__main__":
    main()
