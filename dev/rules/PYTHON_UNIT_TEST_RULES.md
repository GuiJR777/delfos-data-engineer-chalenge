# Python Unit Test Rules

This document defines mandatory standards for Python unit testing.

These rules must always be followed unless explicitly stated otherwise.

------------------------------------------------------------------------

## 1. Folder Structure

### 1.1 Mirror Production Code

-   The project folder structure MUST be replicated inside the `tests`
    folder.
-   Skip folders that do not contain code.

Example:

src/api/main.py\
tests/src/api/main/

------------------------------------------------------------------------

### 1.2 File-Level Mapping

-   For every `.py` file, a folder with the same name MUST exist inside
    `tests`.

Example:

src/api/main.py\
tests/src/api/main/

------------------------------------------------------------------------

## 2. Test File Naming

### 2.1 One Test File Per Class

-   For each class, create one test file.
-   Test file name must be:

test_class_name_in_snake_case.py

Example:

Class: DataBaseHandler\
File:

tests/src/databases/database_handler/test_data_base_handler.py

------------------------------------------------------------------------

## 3. Test Class Structure

### 3.1 One Test Class Per Method

-   Each method of the tested class MUST have its own test class.

Example:

Methods:

-   get_date_with_bar_code
-   set_user_name

Expected test classes:

-   TestGetDateWithBarCode
-   TestSetUserName

------------------------------------------------------------------------

## 4. Test Method Naming

### 4.1 Declarative Test Names

Test methods MUST describe behavior and follow this pattern:

test_when_condition_should_expected_result

Examples:

test_when_we_send_a\_bar_code_with_a\_string_should_return_correctly_date\
test_when_we_send_a\_bar_code_with_a\_float_should_raise_an_exception

------------------------------------------------------------------------

## 5. Arrange / Act / Assert

Each test method MUST be divided into three sections:

-   Arrange
-   Act
-   Assert

Each section MUST be explicitly commented.

Example:
```python

def test_when_we_send_a_bar_code_with_a_string_should_return_correctly_date():
    # Arrange

    database = FakeDatabase()
    database_handler = DataBaseHandler(database)

    bar_code = "123456789"
    expected = "01/01/2020"

    # Act

    response = database_handler.get_date_with_bar_code(bar_code)

    # Assert

    assert response == expected

```

------------------------------------------------------------------------

## 6. Behavioral Testing Only

-   Unit tests MUST validate behavior.
-   NEVER test integrations.

Forbidden in unit tests:

-   APIs
-   Databases
-   External services
-   Other real classes

Everything MUST be mocked.

------------------------------------------------------------------------

## 7. No Logic Inside Tests

Tests must be deterministic and dumb.

Forbidden:

-   if statements
-   loops
-   conditionals

Never write tests for your tests.

------------------------------------------------------------------------

## 8. Async Control

-   Sleeps, awaits and async calls MUST always be mocked.
-   Test suites should run in milliseconds.

------------------------------------------------------------------------

## 9. Test Data

-   NEVER use real data.
-   Always use fake or generated values.

------------------------------------------------------------------------

## 10. Parameterized Tests

-   Use pytest.parametrize whenever multiple cases exist for the same
    behavior.

------------------------------------------------------------------------

## 11. Fixtures

-   Use pytest fixtures when necessary.
-   Avoid overusing fixtures.
-   Fixtures must be simple and explicit.

------------------------------------------------------------------------

## 12. Coverage

-   Target 100% coverage whenever possible.
-   Every branch must be exercised.

------------------------------------------------------------------------

## 13. Philosophy

Unit tests exist to guarantee behavior, not implementation.

They must be:

-   Fast
-   Isolated
-   Predictable
-   Explicit
-   Easy to read

Bad tests are worse than no tests.

Behavior \> Coverage\
Clarity \> Cleverness\
Speed \> Complexity
