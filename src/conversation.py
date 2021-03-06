"""
All classes and functions related to engaging in a conversation.

:author: Derek S. Prijatelj
"""

# TODO Need better assertions/error throwing for controlling arg types in class
# TODO after prototype, figure out how to handle utterances @ same datetime,
#   esp. across Conversations in a ConversationHistory
# TODO Swap from OrderedDict to SortedSet, at least w/in Conversation
# TODO make all to_string() simple be to_string version of to_dict()/json_dump
#   use vars(self) to make dict of attributes. may help w/ json_dump^^^^
# TODO properly implement to_string and print, etc. __repr__, __str__, etc...

from collections import OrderedDict
from datetime import datetime
from enum import Enum
from functools import total_ordering
import copy
import json
#from sortedcontainers import SortedSet

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

def statement_to_question(da):
    """ returns respective question to statement dialogue act """
    if is_statement(da):
        return DialogueAct(da.value + DialogueAct.statement.value)
    else:
        return None # TODO perhaps throw error

def question_to_statement(da):
    """ returns respective question to statement dialogue act """
    if is_question(da):
        return DialogueAct(da.value - DialogueAct.statement.value)
    else:
        return None # TODO perhaps throw error

def topic_is_self(topic):
    """ Check if the topic is about the simulation/chatbot itself. """
    return topic in {"you", "yourself", "self_bot"}

def topic_is_user(topic):
    """ Check if the topic is about the user. """
    return topic in {"me", "myself", "self_user"}

# TODO split conversation.py into utterance.py, conversation.py, conversation_history.py, where the general helpr functions above are in the utterance.py. The below functions will be in conversation or conversation history

def find_conversation_histsory(personas, path="../data/conversation_logs/"):
    """
    Finds list of all existing conversation histories with all involved personas.

    :param personas: set of persona ids.
    :return: list of ConversationHistorys where all personas are involved,
        unless  if set of personas are not included in any ConversationHistory,
        then None is returned.
    """
    #TODO implement an actual Data Base that lets you find by persona ids.
    return None

@total_ordering
class Utterance(object):
    """
    Defines an individual utterance with the specific NLU information

    :param speaker: str of persona_id speaking the Utterance
    :param dialogue_act: DialogueAct of the Utterance
    :param topic: str topic of the utterance for placement in ontology
    :param sentiment: int [1,10] polar sentiment of the Utterance
    :param assertiveness: int [1,10] assertiveness of the Utterance
    :param text: str text of the Utterance, None if Utterance is placeholder
    :param question_type: QuestionType of Utterance if DialogueAct is question
    :param date_time: datetime of when the Utterance was spoken
    """
    # TODO if given only a persona, rather than a speaker name and personality
    #   traits, then infer those from the persona.
    def __init__(self, speaker, dialogue_act, topic, sentiment, assertiveness,
            text=None, question_type=None, date_time=None):
        assert text is None or isinstance(text, str)
        assert isinstance(topic, str)
        assert isinstance(sentiment, int) and sentiment >= 1 and sentiment <= 10
        assert isinstance(assertiveness, int) and assertiveness >= 1 \
            and assertiveness <= 10
        assert isinstance(dialogue_act, DialogueAct)
        assert isinstance(speaker, str)

        if date_time is None:
            date_time = datetime.now()

        if isinstance(text, str):
            self.__text = text.strip()
        else:
            self.__text = text
        self.__topic = topic.lower().strip()
        self.__sentiment = sentiment
        self.__assertiveness = assertiveness
        self.__dialogue_act = dialogue_act
        self.__speaker = speaker
        self.__date_time = date_time

        if question_type and isinstance(question_type, QuestionType) \
                and is_question(dialogue_act):
            self.__question_type = question_type
        else:
            self.__question_type = None

    @property
    def speaker(self):
        """The speaker of the utterance"""
        return self.__speaker

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
    def question_type(self):
        """The question type of the question dialogue act and utterance"""
        return self.__question_type

    @property
    def topic(self):
        """The conversational topic of the utterance"""
        return self.__topic

    @property
    def text(self):
        """The string representation of the utterance's text"""
        return self.__text

    @property
    def date_time(self):
        return self.__date_time

    def set_text(self, text):
        self.__text = text.strip() if isinstance(text, str) else None

    def __str__(self):
        return (
            "Utterance:\n" +
            "Speaker: " + self.speaker + "\n" +
            "Topic: " + self.topic + "\n" +
            "Dialogue Act: " + str(self.dialogue_act) + "\n" +
            "Question Type: " + str(self.question_type) + "\n" +
            "Sentiment: " + str(self.sentiment) + "\n" +
            "Assertiveness: " + str(self.assertiveness) + "\n" +
            "Text: " + self.text + "\n"
        )

    def __repr__(self):
        return self.__str__()

    def __copy__(self):
        return Utterance(
            self.speaker,
            self.dialogue_act,
            self.topic,
            self.sentiment,
            self.assertiveness,
            self.text,
            self.question_type,
            self.date_time
        )

    def copy(self):
        return self.__copy__()

    def __hash__(self):
        return hash((
            self.__speaker,
            self.__dialogue_act,
            self.__topic,
            self.__sentiment,
            self.__assertiveness,
            self.__text,
            self.__question_type,
            self.__date_time
        ))

    def __eq__(self, other):
        return (
            isinstance(other, Utterance)
            and self.__speaker == other.__speaker
            and self.__dialogue_act == other.__dialogue_act
            and self.__topic == other.__topic
            and self.__sentiment == other.__sentiment
            and self.__assertiveness == other.__assertiveness
            and self.__text == other.__text
            and self.__question_type == other.__question_type
            and self.__date_time == other.__date_time
        )

    def __lt__(self, other):
        return ((
            self.__date_time,
            self.__speaker,
            self.__dialogue_act,
            self.__topic,
            self.__sentiment,
            self.__assertiveness,
            self.__text,
            self.__question_type
        ) < (
            other.__date_time,
            other.__speaker,
            other.__dialogue_act,
            other.__topic,
            other.__sentiment,
            other.__assertiveness,
            other.__text,
            other.__question_type
        ))

    # TODO is this improper usage? missing __objclass__?
    def __dict__(self):
        return {
            "speaker": self.__speaker,
            "dialogue_act": vars(self.__dialogue_act),
            "topic": self.__topic,
            "sentiment": self.__sentiment,
            "assertiveness": self.__assertiveness,
            "text": self.__text,
            "question_type": vars(self.__question_type),
            "date_time": self.__date_time
        }

class Conversation(object):
    """ A representation of a single conversation """
    new_convo = True

    def __init__(self, participants=set(), utterances=OrderedDict(),
            topic_to_utterances=None):
        """
        :param utterances: OrderedDict of datetime to Utterance objects
            detailing the utterance history of the conversation.
        :param participants: set of persona_ids participating in conversation
        :param topic_to_utterances: Dict of str "topic" to list(datetime) of
            utterances under this topic in conversation history.
        """
        #TODO make participants dict of participant id's/hashes
        assert isinstance(participants, set)
        assert isinstance(utterances, OrderedDict) \
            and (len(utterances.values()) == 0
            or isinstance(utterances.values()[0], Utterance))

        self.__utterances = utterances
        self.__participants = participants

        if topic_to_utterances is None:
            self.__topic_to_utterances = {}
            for k,u in utterances.items():
                self.__add_utterance_to_topic(u, k)
        else:
            assert(isinstance(topic_to_utterances, dict))
            self.__topic_to_utterances = topic_to_utterances

    @property
    def utterances(self):
        return self.__utterances.copy()

    @property
    def participants(self):
        return self.__participants.copy()

    @property
    def topic_to_utterances(self):
        return self.__topic_to_utterances.copy()

    @property
    def last_utterance(self):
        """ Peeks at last entered utterance """
        #return self.__utterances[len(self.__utterances) - 1].copy()
        # for OrderedDict
        if len(self.__utterances) == 0:
            return None
        return self.__utterances[next(reversed(self.__utterances))].copy()

    # TODO datatime.now() in default only called once. Error...
    def add_utterance(self, utterance, date_time=None):
        assert isinstance(utterance, Utterance)
        if date_time is None:
            date_time = datetime.now()
        assert isinstance(date_time, datetime)
        self.__utterances[date_time] = utterance
        #self.__utterances.add(utterance)
        self.__add_utterance_to_topic(utterance)
        #self.__add_utterance_to_topic(utterance, date_time)

    #def __add_utterance_to_topic(self, utterance, date_time):
    def __add_utterance_to_topic(self, utterance):
        """Helper function to update topic_to_utterances dict"""
        if utterance.topic in self.__topic_to_utterances.keys():
            self.__topic_to_utterances[utterance.topic].append(
                utterance.date_time)
        else:
            self.__topic_to_utterances[utterance.topic] = [utterance.date_time]

    def add_participant(self, participant):
        self.__participants.add(participant)

    def __str__(self):
        s = "Utterances:\n"
        for u in self.__utterances:
            s += str(u)

        s += "\nParticipants:\n"
        for p in self.__participants:
            s += str(p) + " "

        return s.strip()

    def __repr__(self):
        return self.__str__()

    # TODO
    def topic_to_utterances_to_str(self):
        return

    def __copy__(self):
        return Conversation(
            self.participants,
            self.utterances,
            self.topic_to_utterances
        )

    def copy(self):
        return self.__copy__()

    def __eq__(self, other):
        return (
            isinstance(other, Conversation)
            and self.__participants == other.__participants
            and self.__utterances == other.__utterances
            and self.__topic_to_utterances == other.__topic_to_utterances
        )

    # Conversation is mutable, therefore not hashable by Python standards

    def __dict__(self):
        return {
            "participants": self.__participants,
            "utterances": self.__utterances,
            "topic_to_utterances": self.__topic_to_utterances
        }

class ConversationHistory(object):
    """ A history of conversations between participants and associated data """
    def __init__(self, conversations=OrderedDict(),
            topic_to_conversations=None):
        """
        :param conversations: OrderedDict of datetime to Conversation objects
        :param topic_to_conversations: Dict of str "topic" to list(datetime) of
            conversations under this topic in conversation history.
        """
        self.__conversations = conversations

        if topic_to_conversations is None:
            self.create_topic_to_conversations()
        else:
            assert(isinstance(topic_to_conversations, dict))
            self.__topic_to_conversations = topic_to_conversations

    @property
    def conversations(self):
        return self.__conversations.copy()

    @property
    def topic_to_conversations():
        return self.__topic_to_conversations.copy()

    @property
    def last_conversation(self):
        """ Peeks at last entered utterance """
        return self.__conversations[next(reversed(self.__conversations))].copy()

    def get_utterances_from_topic(self, topic):
        """ return all topic related utterances from all conversations
        :return OrderedDict<datetime, Utterance>: OrderedDict of datetime to
            Utterance.
        """
        # TODO handle duplicate time_stamps across and w/in Conversations
        utterances = OrderedDict()
        for conv in self.__topic_to_conversations[topic]:
            for u_date_time in conversations[conv].topic_to_utterances[topic]:
                utterances.update(
                    {u_date_time:conversations[conv].utterances[u_date_time]}
                )
        return utterances

    def add_conversation(self, conversation, date_time=None):
        assert isinstance(conversation, Conversation)
        if date_time is None:
            date_time = datetime.now()
        assert isinstance(date_time, datetime)
        self.__conversations[date_time] = conversation
        self.__add_conversation_to_topic(conversation, date_time)

    def __add_conversation_to_topic(self, conversation, date_time):
        """Helper function to update topic_to_conversations dict"""
        for utterance in conversation.utterances.values():
            if utterance.topic in self.__topic_to_conversations.keys():
                self.__topic_to_conversations[utterance.topic].append(date_time)
            else:
                self.__topic_to_conversations[utterance.topic] = [date_time]

    # TODO update_conversation_to_topic(self): update if conversations include new topics

    def create_topic_to_conversations(self):
        """ Helper function to create the topic_to_conversations dictionary """
        self.__topic_to_conversations = {}
        for k,u in self.__conversations.items():
            self.__add_conversation_to_topic(u, k)

    # TODO
    def topic_to_conversations_to_string(self):
        return

    def __str__(self):
        s = "Conversations:\n"
        for convo in self.conversations:
            s += str(convo)
        return s

    def __repr__(self):
        return self.__str__()

    def __copy__(self):
        return ConversationHistory(
            self.conversations,
            self.topic_to_conversations
        )

    def copy(self):
        return self.__copy__()

    # ConversationHistory is mutable, therefore not hashable by Python standards

    def __dict__(self):
        return{
            "conversations": self.__conversations,
            "topic_to_conversations": self.__topic_to_conversations
        }

    # TODO This extract_dict does not match that in Persona.py. Make them same
    def extract_dict(self, ch_dict):
        """
        Extracts the Conversation History from the provided dict,
        overwriting existing data.
        """
        # TODO make extract dict overwrite the ConversationHistory's data
        self.__conversations = ch_dict["conversations"]
        if "topic_to_conversations" in ch_dict.keys():
            topic_to_conversations = ch_dict["topic_to_conversations"]
        else:
            self.create_topic_to_conversations()


    def save_json(self, json_output_path):
        """ Save Conversation History as JSON at provided path """
        # TODO add unique name to each ConversationHistory when saved including:
        # str(date_time) + "_" + str(personas)
        #conversation_history_id = str(participants)
        with open(json_output_path, 'w', encoding='utf-8') as json_output:
            json.dump(
                {"conversation_history":vars(self)},
                json_output,
                ensure_ascii=False,
                indent=4,
                sort_keys=True
            )

    # TODO implement constructor with only str json path
    def load_json(self, json_path):
        """ Loads the ConversationHistory.json, overwrites existing data """
        with open(json_path, encoding='utf-8') as json_conversation_history:
            dict_conversation_history = json.load(json_conversation_history)
            self.extract_dict(dict_conversation_history)
