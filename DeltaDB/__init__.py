"""
DeltaDB library - A library for processing database records, capturing data, 
and viewing the differences between them.

This module exposes the main configuration, capturer, and types used in the library.
"""

__all__ = []

# Configurations
from DeltaDB.infrastructure.configurations.DBConfig import DBConfig

__all__ += ["DBConfig"]

# Features
from DeltaDB.presentation.DBCapturer import DBCapturer

__all__ += ["DBCapturer"]

# Types
from DeltaDB.domain.types import (
    RecordId,
    Info,
    Capture,
    RecordsChanges,
    DeletedRecords,
    CreatedRecords,
)

__all__ += [
    "RecordId",
    "Info",
    "Capture",
    "RecordsChanges",
    "DeletedRecords",
    "CreatedRecords",
]
