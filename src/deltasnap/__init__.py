"""
DeltaSnap Library - A library for processing database records, capturing data, 
and viewing the differences between them.

This module exposes the core components of the DeltaSnap library, including:
- Main configuration (`DBConfig`)
- Data capturer (`DBCapturer`)
- Core data types used in the library (e.g., `RecordId`, `Info`, `Capture`)
"""

__all__ = [
    "DBConfig",  # Main configuration for database access
    "DBCapturer",  # Captures database records and differences
    "Deleted",  # Represents deleted records
    "Created",  # Represents created records
    "Changes",  # Represents changes between records
    "RecordId",  # Type for record identifiers
    "Info",  # Metadata for records
    "Capture",  # Captured database records
    "RecordsChanges",  # Tracks changes between records
    "DeletedRecords",  # Deleted records in the capture
    "CreatedRecords",  # Newly created records in the capture
]

# Configurations
from src.deltasnap.infrastructure.configurations.DBConfig import DBConfig

# Features
from src.deltasnap.presentation.DBCapturer import DBCapturer

# Classes
from src.deltasnap.domain.data_classes.Changes import Changes
from src.deltasnap.domain.data_classes.data_sets import Deleted, Created

# Types
from src.deltasnap.domain.types import (
    RecordId,
    Info,
    Capture,
    RecordsChanges,
    DeletedRecords,
    CreatedRecords,
)
