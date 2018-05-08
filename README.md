Persona Simulation
==

This is my senior project as a Bachelor's of Science Computer Science Major at Duquesne University.
The project is focused on exploring and implementing (in a prototype) the simulation of persona in open-domain conversational agents (chatbots).
This work aims to put forth a framework for persona simulation that is modular and easily scalable.
The parts of the framework, including the Natural Language Understanding, Personality Profile, and Natural Language Generation modules, are all to be easily swappable.
The entire framework itself is also meant to be a modular entity that can be used in any other system.

Modularity in the Personality Profile means that the personality behind the personas should be easily swappable such that by simply loading a different personality from a file or in memory, the current chatbot will change to simulate that persona.
This makes the personality profiles to serve as off-the-shelf data that is easily hot-swappable (borrowing a term related to that of Hard Drives or Solid State Drives in a computer for being able to be removed and replaced while the machine is on).
In this version the Personality Profile is very simple, as a static and coherent persona is the primary focus of this prototype.

Pyschological Background
--
This work looks at personas and personalities from a psychological point of view.
As such, the distinction between persona and personality must be defined.

**Persona**:

noun: persona; plural noun: personae, personas

1. the aspect of someone's character that is presented to or perceived by others.

"her public persona"

- a role or character adopted by an author or an actor

**Personality**:

noun: personality; plural noun: personalities

1. the combination of characteristics or qualities that form an individual's distinctive character.

- the set of habitual behaviors, cognitions and emotional patterns that evolve from biological and environmental factors 

The key difference is that the persona is shallow, while the personality is complex and defines the personas the person may depict.
This work focuses specifically on simulating a static persona that is used to make an impression on the user in hopes of changing the user's mood to match that depicted by the persona.

The reason this is persona simulation, not personality simulation is because the personality is barely defined and the personas is static per personality profile.
In this prototype the personality profile is so limited that it basically serves as a placeholder for the future personality profiles.

Personality Simulation: PerSim Version 0.1
--
This prototype is to serve as the basis for creating the framework for simulating the more complicated personalities.
We have to first ensure that a static persona can be simulated so that when the personalities we want to simulate decide to change their persona, we will be able be certain that each change is distinct in someway from the other.

The goal for v0.1 is to build a chatbot that is capable of holding short conversations and has a noticeable, static persona.
The persona depicted will be a modular component that can be swapped to change the persona of the chatbot.
This version is also meant to establish the fundamental framework for persona/personality simulation which will be further developed in future versions.

The goal for this version is to aim for an open-domain, generative model with a coherent persona for short conversations only (eg. small-talk).

Requirements
--
- Python 3+
- Numpy
- Scikit-Learn (not currently needed, but will be in future?)
- NLTK

Usage
--
Inside src:

    python main.py [path/to/personality_profile]

For example to run the default neutral personality profile:

    python main.py ../data/personality_profiles/neutral.json

TODO
==
ASAP:
- Unit Test. Do them. Do ALL of them.

After the proof of concept version (0.1):
- Decide if JSON or YAML is better for Personality Profiles.
    + YAML much easier to read(how certain?) and __write__ (ensure this difference is great enough to warrant a change)
    + JSON is a standard (pointless point in itself without reasoning) and is known for its speed, if YAML can  be read as efficiently as JSON, then use YAML, esp. given the readability and writability of YAML over JSON.
    + May end up using YAML for Personality Profiles, but JSON for Conversations, and Conversation Histories, because it only needs serialized and stored, not edited by humans.
    + (could use JSON entirely, if a GUI/CLI was made to edit and create Personality Profiles, but thats more overhead than may be necessary)
