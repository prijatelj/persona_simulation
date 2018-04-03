"""
Persona contains all classes and functions related to creating and using a
persona in conversation.

:author: Derek S. Prijatelj
"""
from collections import OrderedDict
from datetime import datetime
from enum import Enum
import json

class DialogueAct(Enum):
    """
    Customized dialogue acts: an abstraction of the intent of an utterance.
    Inspired by the dialogue act tag sets by Shirberg et. al 1998, and
    Megura et. al 2010.
    """
    statement               = 100 # dummy enum, may serve as other/general stmnt
    statement_information   = 101
    statement_experience    = 102
    statement_preference    = 103
    statement_opinion       = 104 # May overlap with preference.
    statement_desire        = 105
    statement_plan          = 106

    #TODO may want y/n, declarative, wh, etc... question types somehow in NLU...
    question                = 200 # dummy enum, may serve as other/general quest
    question_information    = 201 # perhaps a gneral between fact, exp, & pref.
    question_experience     = 202
    question_preference     = 203
    question_opinion        = 204
    question_desire         = 205
    question_plan           = 206

    # greeting, farewell, and silence, are not necessarily responses...
    response_action         = 300 # dummy enum, may need better name... misc.
    greeting                = 301 # greeting only, nothing else, no How are you?
    farewell                = 302
    thanks                  = 303
    apology                 = 304
    confirm                 = 305
    disconfirm              = 306
    agreement               = 307 # perhaps agreeance be a range?
    disagreement            = 308
    silence                 = 309

    backchannel             = 400 # Listening Oriented
    request_confirmation    = 401
    request_clarification   = 402
    repeat                  = 403
    paraphrase              = 404

    other                   = 000 # should record what user specifies as other.

class QuestionType(Enum):
    """
    The type of questions used in utterances for classification and better
    handling.
    """
    polar       = 100
    declarative = 101
    wh          = 200
    open_ended  = 300
    rhetorical  = 400
    other       = 000

def is_statement(da):
    """ checks if dialogue act is a statement."""
    return isinstance(da, DialogueAct) \
        and da.value >= DialogueAct.statement.value \
        and da.value < DialogueAct.statement.value + 100

def is_question(da):
    """ checks if dialogue act is a question."""
    return isinstance(da, DialogueAct) \
        and da.value >= DialogueAct.question.value \
        and da.value < DialogueAct.question.value + 100

def is_response_action(da):
    """ checks if dialogue act is a response_action."""
    return isinstance(da, DialogueAct) \
        and da.value >= DialogueAct.response_action.value \
        and da.value < DialogueAct.response_action.value + 100

def is_backchannel(da):
    """ checks if dialogue act is a backchannel."""
    return isinstance(da, DialogueAct) \
        and da.value >= DialogueAct.backchannel.value \
        and da.value < DialogueAct.backchannel.value + 100

class Utterance(object):
    """Defines an individual utterance with the specific NLU information"""
    #TODO add speaker of utterance for identification!
    # TODO add syntactic representation, esp. for questions!
    def __init__(self, speaker, dialogue_act, topic, sentiment, assertiveness,
            text=None):
        assert text is None or isinstance(text, str)
        #assert "[s]" in text and "[/s]" in text #Subject Tags, rest = prediacte
        assert isinstance(topic, str)
        assert isinstance(sentiment, int) and sentiment >= 1 and sentiment <= 10
        assert isinstance(assertiveness, int) and assertiveness >= 1 \
            and assertiveness <= 10
        assert isinstance(dialogue_act, DialogueAct)
        assert isinstance(speaker, str)

        if isinstance(text, str):
            self.__text = text.strip()
        else:
            self.__text = text
        self.__topic = topic.lower().strip()
        self.__sentiment = sentiment
        self.__assertiveness = assertiveness
        self.__dialogue_act = dialogue_act
        self.__speaker = speaker

    @property
    def text(self):
        """The string representation of the utterance's text"""
        return self.__text

    @property
    def topic(self):
        """The conversational topic of the utterance"""
        return self.__topic

    @property
    def sentiment(self):
        """The sentiment of the utterance"""
        return self.__sentiment

    @property
    def assertiveness(self):
        """The assertiveness of the utterance"""
        return self.__assertiveness

    @property
    def dialogue_act(self):
        """The dialogue act to depict the intent of the utterance"""
        return self.__dialogue_act

    @property
    def speaker(self):
        """The speaker of the utterance"""
        return self.__speaker

    def set_text(self, text):
        self.__text = text.strip() if isinstance(text, str) else None

    def print_out(self):
        print(
            "Speaker: ", self.speaker,
            "Topic: ", self.topic, "\n",
            "Dialogue Act: ", self.dialogue_act, "\n",
            "Sentiment: ", self.sentiment, "\n",
            "Aggressiveness: ", self.assertiveness, "\n",
            "Text: ", self.text, "\n"
        )

    def copy(self):
        return Utterance(
            self.__speaker,
            self.__dialogue_act,
            self.__topic,
            self.__sentiment,
            self.__assertiveness,
            self.__text
        )

class ConversationHistory(object):
    """Contains the conversation history with its NLU information."""
    def __init__(self, participants=[], utterances=OrderedDict()):
        """
        :param utterances: OrderedDict of datetime to Utterance objects
            detailing the conversation history.
        :param participants: list of personas participating in conversation
        """
        #TODO make participants dict of participant id's/hashes
        assert isinstance(participants, list)
        assert isinstance(utterances, OrderedDict) \
            and (len(utterances.values()) == 0
            or isinstance(utterances.values()[0], Utterance))

        self.__utterances = utterances
        self.__participants = participants

        self.__topic_to_utterances = {}
        for k,u in utterances.items():
            self.__add_utterance_to_topic(u, k)

    @property
    def utterances(self):
        return self.__utterances

    @property
    def participants(self):
        return self.__participants.copy()

    @property
    def topic_to_utterance(self):
        return self.__topic_to_utterances.copy()

    @property
    def last_utterance(self):
        """ Peeks at last entered utterance """
        return self.__utterances[next(reversed(self.__utterances))].copy()

    def add_utterance(self, utterance, date_time=None):
        assert isinstance(utterance, Utterance)
        if date_time is None:
            date_time = datetime.now()

        self.__utterances[date_time] = utterance
        self.__add_utterance_to_topic(utterance, date_time)

    def __add_utterance_to_topic(self, utterance, date_time):
        """Helper function to update topic_to_utterances dict"""
        if utterance.topic in self.__topic_to_utterances.keys():
            self.__topic_to_utterances[utterance.topic].append(date_time)
        else:
            self.__topic_to_utterances[utterance.topic] = [date_time]

    def add_participant(self, participant):
        self.__participants.append(participant)

    def print_out(self):
        print("Utterances:\n")
        for u in self.utterances:
            u.print_out()

        print("\nParticipants:\n")
        for p in self.participants:
            print(p.print_out())

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
        assert isinstance(topic_sentiment, dict) or topic_sentiment is None
        if topic_sentiment:
            # values ints [1,10]
            assert isinstance(list(topic_sentiment.values())[0], int)

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
