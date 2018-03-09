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

    greeting                = 301 # greeting only, nothing else, no How are you?
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
    def __init__(self, text, topic, sentiment, aggressiveness, dialogue_act):
        assert isinstance(text, str)
        assert "[s]" in text and "[/s]" in text #Subject Tags, rest = prediacte
        assert isinstance(topic, str)
        assert isinstance(sentiment, int) and sentiment >= 1 and sentiment <= 10
        assert isinstance(aggressiveness, int) and aggressiveness >= 1 \
            and aggressiveness <= 10
        assert isinstance(dialogue_act, DialogueAct)

        self._text = text
        self._topic = topic
        self._sentiment = sentiment
        self._aggressiveness = aggressiveness
        self._dialogue_act = dialogue_act

    @property
    def text(self):
        """The string representation of the utterance's text"""
        return self._text

    @property
    def topic(self):
        """The conversational topic of the utterance"""
        return self._topic

    @property
    def sentiment(self):
        """The sentiment of the utterance"""
        return self._sentiment

    # TODO perhaps change aggressiveness to assertiveness
    @property
    def aggressiveness(self):
        """The aggressiveness of the utterance"""
        return self._aggressiveness

    @property
    def dialogue_act(self):
        """The dialogue act to depict the intent of the utterance"""
        return self._dialogue_act

    def print_out(self):
        print(
            "Topic: ", self.topic, "\n",
            "Dialogue Act: ", self.dialogue_act, "\n",
            "Sentiment: ", self.sentiment, "\n",
            "Aggressiveness: ", self.aggressiveness, "\n",
            "Text: ", self.text, "\n"
        )

class ConversationHistory(object):
    """
    Contains the conversation history with its NLU information.

    :param utterances: List of utterance objects detailing the conversation
        history.
    :param participants: dict of participant id to persona information.
    """
    def __init__(self, participants, utterances=[]):
        assert isinstance(utterances, list) \
            and (len(utterances) == 0
            or isinstance(utterances[0], Utterance))
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

    def print_out(self):
        print("Utterances:\n")
        for u in self.utterances:
            u.print_out()

        print("\nParticipants:\n")
        for p in self.participants:
            print(p.print_out())

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

    def print_out(self):
        print(
            "Personality:\n",
            "mood: ", self.mood, "\n",
            "aggressiveness: ", self.aggressiveness, "\n"
        )


class Persona(object):
    """ Defines a Persona of a participant in the conversation. """
    # TODO add history of Personality dict of {turn count, Personality}
    # However, this only works if able to be matched to correct conversation
    # history. This will become the PersonalityProfile class in future versions.
    # TODO add a list of conversation histories to this Persona. like memory
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], dict):
                name, personality, topic_sentiment = self.extract_profile_dict(
                    args[0]
                )
            elif isinstance(args[0], str):
                name, personality, topic_sentiment = \
                    self.load_personality_profile(args[0])
        elif len(args) >= 2 and len(args) <= 4:
            name = args[0]
            personality = Personality(args[1], args[2])
            if len(args) == 4:
                topic_sentiment = args[3]
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
        name = profile_dict["personality profile"]["name"]
        personality = Personality(
            profile_dict["personality profile"]["personality"]["mood"],
            profile_dict["personality profile"]["personality"]["aggressiveness"]
        )
        topic_sentiment = profile_dict["personality profile"]["preferences"]

        return name, personality, topic_sentiment

    def load_personality_profile(self, path_to_json):
        """ given a file path, loads the personality profile from json. """
        with open(path_to_json, encoding='utf-8') as json_personality:
            profile_dict = json.load(json_personality)
            return self.extract_profile_dict(profile_dict)

    def print_out(self):
        print("Name: ", self.name, "\n")
        self.personality.print_out()
        print("topic sentiment:\n")
        if self.topic_sentiment:
            for ts in self.topic_sentiment.items():
                print(ts, "\n")
        else:
            print(None)
