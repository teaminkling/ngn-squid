# Technical Specification

> TalkDown is a specification for a highly-moddable custom game engine that is based on interactive narrative: dialogue, choices, characters, and setting.

The specification will be available at **inklinginteractive.com/talkdown.pdf**

## Top-Level Explanation

TalkDown is meant to solve two key problems:

1. Moddability should be a first-class feature to allow for maintainability and a "feature-focused" view of narrative game development.
2. Dialogue and writing in games is not easy to "debug," which in turn makes it difficult to write.

## Mod Structure

    <mod_name>/
        README.md
        characters/
            <short_character_name>.md
            ... [3]
        settings/
            <short_setting_name>.md
            ...
        chapters/
            0001_<your_description>/ [1]
                <short_page_name>.md
                ... [2]
            ...
        events/
            ... [3]
        assets/
            .... [3]

[1]: The "0001" shown here is anything used to sort the directories. You can use ABC, 123, or whatever you like. Just note that the directory is sorted in lexicographical order.

[2]: These directories can be arbitrarily nested, but the lexicographical ordering of the directory name (case insensitive) should be considered.

[3]: These directories can be arbitrarily nested without restriction.

Any of these directories can have assets associated with the Markdown files. You must put them in the top-level `assets/` directory but you can arbitrarily nest them.

## Implementation

The only important part of the specification for writers is above as the Markdown layout. Any TalkDown engine should be able to parse them and consume them the same way. However, there are some very important API endpoints needed by the game developers.

The API fundamentally states:

- At any time there is an internal state managed by the TalkDown API.
    - The state is a group of variables.
    - Variables have type inference.
        - `Set `example variable` to 123` will set it to an integer.
        - `Set `example variable` to 123.0` will set it to a number.
        - `Set `example variable` to "123"` will set it to text.
        - `Set `example flag` to true` will set it to a
    - It is **impossible** to mutate these variables using the TalkDown API.
        - Otherwise the developer of the engine can confuse their writer collaborators who are working with their own understanding of the state of a game at any one moment.
- There is a way to persist data and retrieve data from persistence.
- Resources can be accessed asynchronously across multiple (unlimited) streams.

### The TalkDown Debugger

This is also known as the Editor.

The Debugger is critically important to the TalkDown specification and also affects how your writers will interact with TalkDown.

Specifically, writers will start a TalkDown debugging session and see the temporary variables, text (live), memory management visualisations, story pathing (what connects to where), complexity, event triggers, and overall statistics of their game.

One important consideration is the ability to see all story paths at any time, and to modify flags/variables at any time. On activation of two-way writing, you can use the debugger to write to the file as well, especially to modify variables.

## Elements in Memory

### State

The state contains the scoped variables with types `map`, `list`, `int`, `float`, `bool`, and `str`. The programming language your engine is written in can deal with these types however you like. But mutation of state is determined by TalkDown itself.

State in TalkDown is not like what a programmer is used to. A story is literally all about change. In this sense, the concept of a `const` is not considered default as it would be in Rust. However, as you'll see later, there is still a way of defining constants.

- You can increment and decrement integers.
    - `Set `some integer` to 123`
    - `Decrement `some integer``
- You can add and subtract from `int` and `float`.
    - `Set `some float` to 123.0`
    - `Take 100.0 from `some float``
    - `Add 77.0 to `some float``
- You can push, pop, access `list`s by index, and more!
    - A `list` can have multiple internal data types.
    - `Set `some list``
    - `Add "some string" to the list`
    - `Add `some variable` to the list`
    - `Remove index 3 from `some list``
        - This is not recommended. Why does a writer need to access something by direct index? You would probably want a `map` data structure.
    - TODO: Map data structure.
- You can invert booleans.
    - `Set `some bool` to true`
    - `Flip `some bool``
- You can create constants.
    - `Set `some bool` to true, unchanging` or
    - `Set `some bool` to true, constant` or
    - `Set `some bool` to true, which won't change`

> I wrote the implementation first. How do I access the actual variables?

### Pages

A Page is the most important feature in TalkDown. It is a bunch of text that can be formatted with nearly arbitrary Markdown. This text can then be accessed by the implementation.

Pages are affected by the internal state of the system. You can see the internal state of the system using a TalkDown debugger as you are writing: as you reach the page you are editing, you can refresh the page as you save the file and access any variables available to you.

A Page can be arbitrarily categorised, contains references to the Page(s) and/or Event(s) that can call it, and contains references to the Page(s) and/or Event(s) it calls.

If assets are implemented in your engine, the Page should also contain references to any assets that are referenced. They should be categorised under the heading blocks.

### Events

An event can do two things:

- Set a variable.
- 

### Performance

This section is optional to implement.

A story can be massive. While loading the entire story into memory is not too difficult, it can be very inefficient. On the other hand, loading of data can negatively impact the user experience. There are a number of things to do to speed things up while optimising for precious RAM.

Unfortunately, there is an overhead in processing Markdown files. A game in production will still need to read these files as we go. The recommended process also obfuscates the files with some form of two-way encryption. I will investigate dealing with this as time goes, but it's likely that "lazy loading" can deal with this.

- Lazy Loading

> It's possible the numbers here are totally wrong. I wouldn't be surprised if `n` = `100` and `m = 1` were possible values. Sane defaults will be developed by engine implementations as development continues.

**Lazy Loading deals with loading times.**

A Page shall only load itself and travel, breath-first, `n` levels down links to collect and store Pages. A good value for `n` is dependent on the complexity of your game, but `5` is a good starting point.

Each page keeps track of the depth of this recursion. A value `m` where `m < n` is the "trigger" for lazy loading another `n` levels. If `n` = `5`, then `m` could be `2`. From `5` to `2`, the user will experience zero slowdown due to loading from disk. Once the depth hits `2`, the next page brings it up to `5`, but the next page can be instantly displayed at the same time. This buffer hopefully can remove loading times for resources completely.

> I need to look at how the Amethyst/Unity assets pipeline works and see if I can feed the idea into those engines. Having a game engine `inkengine` that can guarantee no loading times for large worlds would be really cool.

- Inactive Culling

**Inactive Culling deals with memory utilisation.**

If a page cannot be reached anymore, it shall be removed from the Pages in memory. This can be determined by knowing the Events that call a Page are no longer in scope. A Page has a two-way knowledge of the Event(s) and/or Page(s) that can call it to being. Once a Page is fully consumed (either by explicitly consuming it or consuming the next Page in an Event Stream), it checks if there are any other Pages that can call back to it

Inactive Culling is an extremely important feature of the debugger as well. The debugger should visibly show you which pages are in memory and will be loaded.

- Unreachability List

**Unreachability List deals with size of a binary.**

When "compiling" a TalkDown project, Pages that are not reachable without debugging (or cheating) will be listed. As shown in the user specification, you can configure a Page to not show up on this list by explicitly marking it as "internal." Also as stated before, this means the Page is not loadable, and any attempt to link to a page like this will result in a compilation error.

This is not necessarily an optimisation. Lazy Loading will ensure these pages are never loaded to begin with, which should be good enough. But you want to make sure your content is available to users and not take up too much unnecessary disk space. This feature can help with that.

- Asynchronous Operation

**Asynchronous Operation deals with avoiding thread/coroutine blocking.**

A call to an Event is asynchronous. Once it is read in, the results can be read 

### Persistence

There are two types of variable as determined by the TalkDown implementation you write:

- Scoped

A variable lives and dies after the start and/or before the end of the entire game.

- Unscoped

A variable lives for the entirety of the game.

Ideally, all variables will be scoped when you package for "production": the end user. When you save, you save the current scope of variables and the internal state of the game in a file (we prefer `JSON` compressed with `zlib`) to be read later.

You must have a way to bring scoped variables and stored Pages back into memory when loading from this file.

### Assets Pipeline

Above you learned that you can add assets to blocks of Markdown via an `assets/` directory in the top-level directory. Note that you do not need to use a resource in a Markdown file to load it in as an asset in the assets pipeline.

An API is provided to access these files.

> This section is incomplete and to be considered for a later version of the specification.