"""
Persona contains all classes and functions related to creating and using a
persona in conversation.

:author: Derek S. Prijatelj
"""
from enum import Enum
import json

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
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], dict):
                name, personality, topic_sentiment = self.extract_profile_dict(
                    args[0]
                )
            elif isinstance(args[0], str):
                name, personality, topic_sentiment = \
                    self.load_personality_profile(
                        args[0]
                    )
        elif len(args) >= 2 and len(args) <= 3:
            name = args[0]
            personality = args[1]
            if len(args) == 3:
                topic_sentiment = args[2]
            else:
                topic_sentiment = None

        assert isinstance(name, str)
        assert isinstance(personality, Personality)
        assert isinstance(topic_sentiment, dict) or topic_sentiment is None
        if topic_sentiment:
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

    def extract_profile_dict(self, profile_dict):
        name = profile_dict["personality_profile"]["name"]
        personality = Personality(
            profile_dict["personality_profile"]["personality"]["mood"],
            profile_dict["personality_profile"]["personality"]["aggressiveness"]
        )
        topic_sentiment = profile_dict["personality profile"]["preferences"]

        return name, personality, topic_sentiment

    def load_personality_profile(self, path_to_json):
        """ given a file path, loads the personality profile from json. """
        with open(path_to_json, encoding='utf-8') as json_personality:
            profile_dict = json.load(json_personality)
            return self.extract_profile_dict(profile_dict)
