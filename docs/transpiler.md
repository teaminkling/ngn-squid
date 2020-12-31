# Transpiler Implementation

This document explains how to implement a Squid transpiler.

## Algorithm

### 1. Manifest

Read the manifest to find the files in this project in order. The manifest has the format:

```json
{
    "project": [
        "a.squid",
        "../b.squid",
        "foo/c.squid"
    ],
    "output": "squid.json"
}
```

Both keys `project` and `output` are mandatory.

### 2. Parse File

> This is understood by the maintainer but may be confusing to readers. It will be rewritten when the transpiler is
> complete for a more comprehensive view. On top of this, it may not be fully accurate (yet). Sorry!

In the manifest example above, we read the file, line by line, following the rules:

1. `--` prefix indicates the active library identifier.
2. All completely empty lines/whitespace-only lines are skipped over.
3. All lines that start with `#` are skipped over.
4. `>` prefix indicates the active character and mood. The character and mood information is added to the
   meta-information.
5. All lines that start with two whitespace characters or more are associated with the active mode. This
   enters a mode that allows special parsing of conditional statements with a (not regex) pattern `?{...}`.
6. These are turned into one continuous string where each newline is made into a single whitespace character and there
   may only be one whitespace character between any words.
7. `>`, `!`, `--` prefixes immediately set the active character and mood to "nothing."
8. If a line starts with anything other than the already presented prefixes, the transpilation must error.
9. If two or more whitespace characters are met with `>>`, everything after the `>>` is to be parsed as a "choice".
   Choices can wrap on multiple lines because they continue to be parsed with the same rules as a "passage" until the
   active character and mood are set to nothing.
10. The `!` prefix has some modes:
    1. `!{` prefix indicates an action is to be taken. Whatever is inside the brackets is simply added as an action.
       The action parsed is added to the meta-information.
    2. `![` prefix indicates that a variable is about to be assigned. The format is
       `! [type] name : with : categories = value or expression`. The variable is added to the variables
       meta-information for this file.
11. The `*[` prefix works in exactly the same way as the variable assignment except it is ephemeral; the variable is
    not added to the global meta-information list.
12. Anything that is a valid expression syntax (reminder: `?{...}`) is expected to be:
    1. Run an action and return its value.
    2. Fetch the value of a variable.
13. Anything in `?<...>` syntax calculates a variable and uses it in the name of a variable.
14. Anything in a `?(...)` syntax calculates a basic mathematical or logical expression. The `?` prefix is no longer
    necessary (but is optionally allowed) for special symbols inside it: `{}<>`.
15. In "choice mode", the choice may:
    1. Have a variable substitution using `?{...}` syntax. Note that `?<...>` is not valid here.

### 3. Output Parts

The JSON output is fairly literal and easy to read:

```json
{
    "data": [

    ],
    "meta": {
        "checksum": {
            "algorithm": "SHA256",
            "hash": "<--snip-->"
        },
        "actions": [],
        "characters": [],
        "variables": []
    }
}
```
