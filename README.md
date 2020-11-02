# TalkDown

The TalkDown interactive dialogue and narrative library tools.

> Talkdown is worse than [Ink](https://github.com/inkle/ink). Use that instead!

## This Repository

TalkDown consists of a few moving parts:

- The TalkDown Debugger.
- The TalkDown HTML Engine.
- The TalkDown Command Line Interface.

### The Debugger

The `chatterbug` tool opens a web browser with your initial game load "event". More on "events" later. All of the actual
story are told in "locations." A location is either "active" or "inactive." More on "locations" later.

With the debugger, you can see all variables, all events that can be triggered, all active locations, all at once. You
can see all of the events, sub events, the locations of all characters (should you use the characters feature), modify
variables, and so on.

Very importantly, you can save the state as just text: all events and variables. Auto-save is enabled by default since
the development server has live-reload turned on and you lose progress with every Markdown re-render.

You can essentially "play a game" with the debugger like a CYOA game where each event can also be triggered in a more
comprehensive engine. For instance, an event could be "killed the Mayor of the city" or "pulled the lever on this level
to call the elevator."

### The HTML Engine

You can also the debugger as a game engine in itself! You can export an HTML file with JavaScript in-line and a saves
feature to export to users. This can be therefore hosted easily on other platforms.

> This is just `chatterbug` but with debug features disabled and exported as a static site rather than a dynamic server
> with live reload.

### The Command Line Interface

The `hotwire` tool simply exports the Markdown files into a format that can be understood by some major game engines.
The preferred way to perform export is to perform code translation/transpilation and explicitly write code. But
implementation details are expected to vary even for the same engines.

Currently, `hotwire` supports:

- Nothing, as it's just a specification.

## Specification

> TalkDown is a specification for a highly-moddable custom game engine that is based on interactive narrative:
> dialogue, choices, characters, and setting.

TalkDown is meant to solve two key problems:

1. Moddability should be a first-class feature to allow for a "feature-focused" view of narrative game development.
2. Dialogue and writing in games is not easy to "debug," which in turn makes it difficult to write.
3. Twine is popular but slow, janky, and difficult to maintain for large games.

Now you know the "why", read on to understand the "how" and "what":

### Mod Structure

- `<mod_name>`
  - `README.md`
  - characters/
    - `<short_character_name>.md`
    - ...
  - locations/
    - `<short_location_name>.md`
    - ...
  - events/
    - `0000_<event_name>.md` [^1]
    - ...
  - assets/
    - ... [^2]

### Events, Characters, and Locations

There are three things to manage and write in TalkDown: events, characters, and locations. You should think about
"state":

- The state of a character.
- The state of a location setting.
- The state of the story.

You use "events" to set and mutate variables, make locations active or inactive, make events active or inactive, and
call other events. An event is like a choice that the player can make, or something that can just happen in the game
world.

Events are _always_ called externally. An "event" is the most analogous thing to a "page" in Twine we have in TalkDown
[^3]. Speaking of Twine, you can basically make an entire game out of "events" the same way that Twine would allow you
to navigate between pages. A significant difference is that an event can be _asynchronous_: many things can happen at
the same time and you can use _waiting_ to display multiple "threads" of events at the same time [^4].

You should consider location state as well. You can describe a location and have this be affected by mutations on the
game world's state. But you can also have significant story happening in a location as influenced by the location's
state. What I mean by this is: sometimes the location can and should be displayed to the player. If significant stuff
is happening actively to the location, then you should make that location active!

An active location is displayed as coloured-in/in-view while in the `chatterbug` debugger. You can click on it at any
time to see the description of the location. Imagine you are in a 2D game where you have entered a room: this activates
that location since you can see everything happening within it! And everywhere else you're expected to have "focus" on
should be activated.

You can use TalkDown without the "location activate" feature if you just want to use locations as concept writing and
world building. This actually just activates all locations by default so you can see what's going on at any time. But I
strongly recommend keeping it on to help with understanding how a story flows and where all of the set pieces are.

#### Inbuilt Events

There are some inbuilt events that can be called at any time:

- You can call an event that will move a character to a location.
- You can call an event that will label the character whose POV we are seeing.
  - Normally you would call this once to one player at the start of the story.
- You can call an event that activates the location the POV player is on and deactivates all other locations.

#### Sub-Events

Dialogue and choice makes heavy use of sub-events within event pages. Characters can have dialogue, and if you want to
be able to give a different response to anything that people say, you will need sub-events to handle that if you
don't want your project directory structure to explode.

A sub-event creates callable events at compile time that should be called within events themselves. They can set
variables and activate events like "proper" events can, but they are expected to "complete": calling a sub-event will
block the parent event until the sub-event is explicitly exited.

The linter will catch cases where sub-events are not possible to close. Handy, right?

[^1]: You should have lexicographical ordering enabled for events.

[^2]: These directories can be arbitrarily nested without restriction. TalkDown does not enforce the internal structure
      of the assets directory.

[^3]: There are significant differences, though. The biggest one is that Twine uses pages for _everything_ while we
      only use them to show action and reaction. Everything else happens in location settings.

[^4]: If you just want to use this like Twine, then I doubt you will need this. This is best used to handle dialogue
      and internal tracking of story state which is very handy when exporting to an external engine's format.
