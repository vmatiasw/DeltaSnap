"""
DeltaDB Library - A library for processing database records, capturing data, 
and viewing the differences between them.

This module exposes the core components of the DeltaDB library, including:
- Main configuration (`DBConfig`)
- Data capturer (`DBCapturer`)
- Core data types used in the library (e.g., `RecordId`, `Info`, `Capture`)
"""

__all__ = [
    "DBConfig",              # Main configuration for database access
    "DBCapturer",            # Captures database records and differences
    "RecordId",              # Type for record identifiers
    "Info",                  # Metadata for records
    "Capture",               # Captured database records
    "RecordsChanges",        # Tracks changes between records
    "DeletedRecords",        # Deleted records in the capture
    "CreatedRecords",        # Newly created records in the capture
]

# Configurations
from DeltaDB.infrastructure.configurations.DBConfig import DBConfig

# Features
from DeltaDB.presentation.DBCapturer import DBCapturer

# Types
from DeltaDB.domain.types import (
    RecordId,
    Info,
    Capture,
    RecordsChanges,
    DeletedRecords,
    CreatedRecords,
)
