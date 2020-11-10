# Squid

> This repository is work-in-progress.

Squid refers to:

- Squid Language.
- Squid Transpiler.
- Squid Engine.
- Squid Editor.
  - Contains a JavaScript Squid Implementation.

Squid Language is a lightweight and relatively simple (simpler than [ink](https://github.com/inkle/ink)) markup language
for writing narrative-driven games. It is typed and is very easy to integrate to any programming language as it defines
a simple API.

## The Specification

This is an example `test.squid` file:

```squid
-- Library Identifier --

> Character Name [mood]
    This is a character talking. When the lines get too long, they get wrapped.

    This line is considered without the newline characters. This can be used for multi-line dialogue.

    Newlines get turned into spaces. Multiple spaces together get turned into single spaces. Like HTML!

> Character Name [mood]
    This is short but it does not wrap the next dialogue.

> Character Name [mood]
    This is the text for a choice. A choice is indicated by the >> characters.

    >> A ! action(arguments)
    >> B
    >> C -> Library Identifier

# This is a line-level comment and it is ignored.

# Choice A will execute a custom function defined by the game engine.
# Choice A and B will continue the execution flow to the action below.
# Choice C will jump back to the top of the file because it links to "Library Identifier".

?{ action(arguments) }
!{ action(arguments) }

# Above, we executed an action twice. Actions are provided by name by the game engine.
# It is important to know what actions are available before you use them.
# Note that both statements are the same.

> Character Name [mood]
    You can display variables with this syntax: ?{ Location Name : Flag Name }.

    You can display the return result of actions (if any) with the same syntax: ?{ action(arguments) }.

    Variables have types but are stored as strings. They can be a string, a float, an integer, and a boolean.

    Don't do math using this. If you must, the engine should define stuff like add(a, b) etc.

# You can set arbitrary flags easily with custom whitespace.

! [string] Location Name : Flag Name = New Value
! [float]  NPC Name      : Flag Name = New Value
! [int]    Flag Name                 = New Value
! [bool]   Flag Name                 = New Value

# Including using evaluated actions (as the return is calculated):

! [int] Flag Name = ?{ action(arguments) }

# And expression assignments (note all expressions of equality are done with ?() syntax):

! [int] Flag Name = ?( ?{ Location Name : Flag Name } == Something )

# All of this works for ephemeral/local variables. But these are destroyed when the next library is activated.
# Use them sparingly!

* [int]  Variable Name  = New Value
* [bool] Variable Name  = ?{ action(arguments) }

# You can perform basic evaluations except there really isn't any inbuilt string manipulation syntax.

> Character Name [mood]
    Choices can be conditionally locked if there's a ?(...) after the choice name.

    The expression inside the ?(...) calculate the predicate.

    Note that it should be 

    >> Choice A ?( ?{ NPC Name : Flag Name } < Something )  !  action(arguments)
    >> Choice B ?( Flag Name == Something Else )           ->  Another Library Identifier
    >> Choice C                                            ->  Library Identifier

    # If the expressions in choice A or B are not present, they will be disabled.

-- Another Library Identifier --

# You can have one or more libraries per file.
# Library identifiers are a bit like an "anchor."
# Libraries may be empty to act as placeholders.
```

## Transpiler

Any compiler for Squid should export to a single Squid JSON file. The default one is written in TypeScript
and takes a JSON manifest:

```json
{
  "manifest": ["a.squid", "../b.squid", "foo/c.squid"],
  "output": "squid.json"
}
```

Simply run `squid manifest.json`. The linter will spit out some warnings or errors if it finds any.

You may want to know [how to implement a parser/transpiler for Squid](docs/transpiler.md).

### Linter

The linter is part of the transpiler. It will detect:

- [ERR] Syntax error; story not well-formed.
- [ERR] Not exactly one main-level library call.
- [ERR] Flag read but never set.
- [ERR] Illegal assignment to given type.
- [ERR] Illegal expression for given type.
- [INF] Flag set but never read.
- [INF] Library is not accessed.

These [INF] messages are probably fine because the game itself can activate libraries or read flags.

## Editor

Squid Editor is an HTML5 editor and debugger that runs on Squid JSON. If you run the app locally, you can just do
`squid-editor --in squid.json --actions actions.js` or similar.

You can also hot-reload it: `squid-editor --manifest manifest.json --actions actions.js` which will compile your story
at will.

- You get a graph view of the libraries.
- You can jump to any library at any time.
- You can see and edit any of the flags at any time.
- You can see any of the engine's actions.
  - You can write JavaScript actions in the inbuilt Squid Engine.
- You can save and load states at whim.
- You can execute actions at whim.

It allows you to fully play through the game you have written.

## Engines

You can read on how to [implement Squid Engine here](docs/engine.md). The gist is this:

1. Implement an engine and API and create a map/dictionary data structure from string to callable. This gives a
   string-based interface to execute tasks in-game at whim.
2. Implement a way to read the JSON output (or deserialise the `.squid` file) and load in the files to memory on
   load.
3. Implement a way to execute each node in-engine.

## Modding

If your game wants narrative mods and you have a deserializer for the `.squid` format then it should be
fairly easy for people to make their own stories.

Essentially your method for making your game is now:

1. Implement Squid.
2. Implement parts of your engine.
3. Write Squid narrative files.
4. Test your game.
5. Go to 2 until the game is done.

Engine development and level development is now separate.
