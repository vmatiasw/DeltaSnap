from collections import Counter
from typing import Any, Dict, List, Tuple

# TODO: agregar estas funciones a CaptureDiff
# luego, borrar las carpetas y dejar solo los archivos de las fases

# Type aliases for readability
TupleList = List[Tuple[str, ...]]
StringDict = Dict[str, Any]

def validate_tuples(input_list: TupleList, valid_keys: List[str]) -> bool:
    """
    Validates that the first element of each tuple in the input list matches the provided valid keys.

    Args:
        input_list (TupleList): A list of tuples where the first element is a string and remaining elements are optional.
        valid_keys (List[str]): A list of valid strings that the tuples' first elements should match.

    Returns:
        bool: True if all tuples in the input list have their first element in valid_keys 
              and all valid_keys are represented in the input list. False otherwise.
    """
    input_keys = {tup[0] for tup in input_list}
    valid_keys_set = set(valid_keys)

    if input_keys != valid_keys_set:
        difference = input_keys.symmetric_difference(valid_keys_set)
        print(f"Error: The keys {difference} are invalid or missing.")
        return False

    return True


def validate_tuple_counts(input_list: TupleList, valid_keys_counts: List[Tuple[str, int]]) -> bool:
    """
    Validates that the frequency of each key in the input list matches the expected counts provided.

    Args:
        input_list (TupleList): A list of tuples where the first element is a string and remaining elements are optional.
        valid_keys_counts (List[Tuple[str, int]]): A list of tuples containing a key and its expected frequency.

    Returns:
        bool: True if all keys in the input list match the expected frequencies and all expected keys are present.
              False otherwise.
    """
    input_counts = Counter(tup[0] for tup in input_list)
    expected_keys = {key for key, _ in valid_keys_counts}

    # Check for missing or extra keys
    if not expected_keys.issubset(input_counts.keys()):
        missing_keys = expected_keys - input_counts.keys()
        print(f"Error: Missing keys {missing_keys} in the input list.")
        return False

    # Validate frequencies
    for key, expected_count in valid_keys_counts:
        if input_counts[key] != expected_count:
            print(f"Error: Key '{key}' appears {input_counts[key]} times, expected {expected_count}.")
            return False

    return True


def validate_nested_dicts(input_dict: StringDict, valid_schema: Dict[str, List[str]]) -> bool:
    """
    Validates that the keys and values in a nested dictionary follow the specified schema.

    Args:
        input_dict (StringDict): A dictionary where keys are strings and values are lists of tuples.
        valid_schema (Dict[str, List[str]]): A schema dictionary specifying valid keys and their allowed sub-keys.

    Returns:
        bool: True if all keys and their respective values follow the schema. False otherwise.
    """
    input_keys = set(input_dict.keys())
    schema_keys = set(valid_schema.keys())

    # Check if keys match schema
    if input_keys != schema_keys:
        missing_keys = schema_keys - input_keys
        extra_keys = input_keys - schema_keys
        if missing_keys:
            print(f"Error: Missing keys in input: {missing_keys}")
        if extra_keys:
            print(f"Error: Extra keys in input: {extra_keys}")
        return False

    # Validate values for each key using validate_tuples
    for key, tuples in input_dict.items():
        if not validate_tuples(tuples, valid_schema[key]):
            print(f"Error: Invalid values for key '{key}' based on the schema.")
            return False

    return True
