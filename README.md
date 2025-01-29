# DeltaSnap

A tool to capture any subset of database records and compare changes between captures. It is mainly used for functional testing and debugging.

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/vmaiasw/DeltaSnap.git
cd deltasnap
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
pip install -r requirements.txt
```

## Usage

```python
from src.deltasnap import capture_all_records, compare_capture

def test_start_game(test_session):
    initial_capture = capture_all_records(test_session)

    # Logic to test

    final_capture = capture_all_records(test_session)
    changes, created, deleted = compare_capture(initial_capture, final_capture)

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

## Requirements

- Python 3.6 or higher.

## License

This project is licensed under the MIT License.
