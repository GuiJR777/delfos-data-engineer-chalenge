# Python Development Rules

This document defines mandatory coding standards for Python projects.

These rules must always be followed unless explicitly stated otherwise.

------------------------------------------------------------------------

## 1. Core Principles

### 1.1 SOLID

-   Always follow SOLID principles.
-   Classes must have a single responsibility.
-   Favor composition over inheritance.
-   Depend on abstractions, not concretions.

------------------------------------------------------------------------

### 1.2 DRY

-   Never duplicate logic.
-   Extract shared behavior into reusable methods or classes.

------------------------------------------------------------------------

## 2. Typing

### 2.1 Mandatory Type Hints

-   All functions and methods MUST be fully typed.
-   All return types must be explicit.

------------------------------------------------------------------------

## 3. Object-Oriented Programming

### 3.1 Default to OOP

-   Always use Object-Oriented Programming.
-   Functional style is allowed ONLY for:
    -   Simple scripts
    -   One-off utilities

Everything else must be class-based.

------------------------------------------------------------------------

## 4. Control Flow

### 4.1 Early Return

-   Prefer early returns over `if/else`.

------------------------------------------------------------------------

### 4.2 Complex Conditions

-   Never place complex logical expressions directly in `if`.
-   Store them in a well-named variable.

------------------------------------------------------------------------

## 5. Naming Conventions

### 5.1 Method Naming

Use semantic prefixes:

-   do_something → performs actions (no return)
-   is_something → returns boolean
-   get_something → getters
-   set_something → setters

------------------------------------------------------------------------

### 5.2 Parameters Must Match Method Intent

Parameter names must relate directly to what the method does.

Code should read like English.

------------------------------------------------------------------------

### 5.3 No Abbreviations

-   Never abbreviate variable names.
-   Variables must describe exactly what they represent.

------------------------------------------------------------------------

## 6. File Header Documentation

Every file must start with a comment describing its purpose.

------------------------------------------------------------------------

## 7. Line Length (PEP8)

-   Maximum line length: 79 characters.
-   If unavoidable, append \# noqa at the end of the line.

------------------------------------------------------------------------

## 8. Magic Numbers

-   Never use magic numbers.
-   Always extract them into named constants.

------------------------------------------------------------------------

## 9. Constants

-   Constants must be:
    -   Uppercase
    -   Typed
    -   Declared at module level

------------------------------------------------------------------------

## 10. Exception Handling & Logging

-   Every try/except block MUST contain informative logs.
-   Never swallow exceptions silently.
-   Logs must explain:
    -   What failed
    -   Why it failed (if known)
    -   Context data

------------------------------------------------------------------------

## 11. Imports

Imports must follow this exact order:

1.  Built-in Python imports
2.  External libraries
3.  Internal project modules

Rules:

-   Each group separated by one blank line.
-   Inside each group, imports must be alphabetical.

------------------------------------------------------------------------

## 12. File Ending

-   Every file MUST end with exactly one blank line.

------------------------------------------------------------------------

## 13. General Rules

-   Favor readability over cleverness.
-   Code should read like documentation.
-   Every class must have a clear responsibility.
-   Every method must have a clear intention.
-   Avoid side effects.
-   Prefer composition.
-   Keep methods small.

------------------------------------------------------------------------

## 14. Philosophy

The goal is:

-   Predictable code
-   Self-documenting logic
-   Easy onboarding
-   Easy maintenance
-   Production-grade architecture

If a solution violates clarity, it is wrong.

Simple \> Clever\
Explicit \> Implicit\
Readable \> Short
