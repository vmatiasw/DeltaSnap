# DeltaSnap

A tool to capture any subset of database records and compare changes between captures. It is mainly used for functional testing and debugging.

## Installation

```bash
pip install deltasnap
```

## Requirements

- Python 3.6 or higher.

DeltaSnap works with any database or ORM that can interact with a database. You must have a database connection and an ORM such as SQLAlchemy or Django to use this tool effectively.

**Supported ORMs:**

- SQLAlchemy (any version >= 1.3)
- Django (any version >= 3.0)

Ensure that your project is properly connected to a database before using DeltaSnap.

## Usage

```python
from deltasnap import DBCapturer, DBConfig

# Set up the DBCapturer with the appropriate configuration
db_capturer = DBCapturer(
        DBConfig(
            db_source="sqlalchemy",  # Choose "sqlalchemy" or "django"
            test_session=test_session,  # Provide your test session (SQLAlchemy or Django session)
            base=base, # Provide the SQLAlchemy Base model. Django does not require this.
        )
    )


def test_start_game(test_session):
    initial_capture = db_capturer.capture_all_records(test_session)

    # Logic to test
    start_game()

    final_capture = db_capturer.capture_all_records(test_session)
    changes, created, deleted = db_capturer.compare_capture(initial_capture, final_capture)

    # Assertions to validate the changes
    assert not deleted.data # No records were deleted
    assert created.data == {
            ("cards", 1),
            ("cards", 2),
            ("cards", 3)
        } # 3 records were created in the 'cards' table
    assert changes.data == {
        ('games', 1): {
            'started': (False, True),
            'turn_start': (None, '2021-10-10T10:00:00Z')
            }
        } # There were changes in 2 columns of the record with id 1 from the 'games' table. For example, the 'started' field changed from False to True.
```

## Advantages

- **Full coverage**: Automatically validates all changes in the database.
- **Simplification**: Reduces the use of fixed `asserts` that may be missed by the tester.
- **Automatic evolution**: Adapts to changes in the database schema.
- **Complete comparisons**: Validates both previous and current values.

## License

This project is licensed under the MIT License.
