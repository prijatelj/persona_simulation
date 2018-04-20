"""
Persona contains all classes and functions related to creating and using a
persona in conversation.

:author: Derek S. Prijatelj
"""

# TODO use vars(self) to get dict of attributes! do for json_dump
#   perhaps override __vars__ (if possible) to allow recursive vars() on child
#   make complete dict equivalent and ready for json_dump

from collections import OrderedDict
from datetime import datetime
import json

class Personality(object):
    """ The Personality of a speaker. Polar mood."""
    def __init__(self, mood, assertiveness):
        assert mood in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert assertiveness in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.__mood = mood
        self.__assertiveness = assertiveness

    @property
    def mood(self):
        """The mood the Personality which is polar negative/positive"""
        return self.__mood

    @property
    def assertiveness(self):
        """"The assertiveness in pursueing the Personality's goals."""
        return self.__assertiveness

    def set_mood(self, mood):
        self.__mood = mood

    def set_assertiveness(self, assertiveness):
        self.__assertiveness = assertiveness

    def get_dict(self):
        """
        Returns dict of Personality for easy saving and addition to Personality
        Profile.
        """
        return {"personality":
                    {"mood" : self.__mood,
                     "assertiveness": self.__assertiveness
                    }
               }

    def print_out(self):
        print(
            "Personality:\n",
            "mood: ", self.mood, "\n",
            "assertiveness: ", self.assertiveness, "\n"
        )

    def __eq__(self, other):
        return (
            isinstance(other, Personality)
            and self.__mood == other.__mood
            and self.__assertiveness == other.__assertiveness
        )

    # Personality is mutable: not hashable by python standards

class Persona(object):
    """ Defines a Persona of a participant in the conversation. """
    # TODO add history of Personality dict of {turn count, Personality}
    # However, this only works if able to be matched to correct conversation
    # history. This will become the PersonalityProfile class in future versions.

    # TODO add a list of conversation histories to this Persona. like memory,
    # this would be a dict of user_ids to conversation histories ordered by time
    # The conversation histories would have to be external and global. If there
    # are only one conversation history per pair of participants, then time
    # ordering is unnecessary, simply user_id to list of all conversation
    # histories they occur in.

    #TODO does a personality profile require Desires for detailing explicit goals
    # along with the existing Personality, Philosophy, and Preferences?

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
        assert isinstance(topic_sentiment, OrderedDict) \
            or topic_sentiment is None
        if topic_sentiment:
            # values ints [1,10]
            assert isinstance(list(topic_sentiment.values())[0], int)
        else:
            topic_sentiment = OrderedDict()

        #self.__id = name # maybe necessary later, not in prototype. Use names.
        self.__name = name
        self.__personality = personality
        self.__topic_sentiment = topic_sentiment

    @property
    def name(self):
        return self.__name

    @property
    def personality(self):
        return self.__personality

    @property
    def topic_sentiment(self):
        return self.__topic_sentiment

    # set functions for tracing errors
    def set_name(self, name):
        self.__name = name

    def set_personality(self, personality):
        self.__personality = personality

    def set_topic(self, topic, sentiment):
        self.__topic_sentiment[topic] = sentiment

    def topic_magnitude(self, topic, desired_sentiment):
        """ The difference of the desired and topic sentiments """
        if topic in self.__topic_sentiment.keys():
            return desired_sentiment - self.__topic_sentiment[topic]
        else:
            return None

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
            profile_dict["personality profile"]["personality"]["assertiveness"]
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

    def __eq__(self, other):
        return (
            isinstance(other, Persona)
            and self.__name == other.__name
            and self.__personality == other.__personality
            and self.__topic_sentiment == other.__topic_sentiment
        )

    # Persona is mutable: not hashable by python standards
