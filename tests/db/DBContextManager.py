from typing import Any, Optional
from contextvars import ContextVar, Token

current_session: ContextVar[Optional[Any]] = ContextVar("current_session", default=None)


class DBContextManager:
    def __init__(self, session: Optional[Any] = None) -> None:
        """
        Initializes the context manager to handle transactions in a database.

        Args:
            session (Optional[Any]): The database session to be managed within the context.
                If not provided, the context will perform no action.
        """
        self._session = session
        self._token: Token[Any]

    def __enter__(self) -> None:
        """
        Starts the database session and sets it as the current context.
        """
        if self._session:
            self._session.begin()

        self._token = current_session.set(self._session)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Rolls back if an error occurred, or commits if everything went well, and closes the session when exiting the context.
        """
        if self._session:
            try:
                if exc_type:
                    print(f"Rollback due to: {exc_type} - {exc_val}")
                    self._session.rollback()
                else:
                    self._session.commit()
            finally:
                self._session.close()

        current_session.reset(self._token)


class DBTestContextManager(DBContextManager):
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Finalizes the session in test mode and always performs a rollback.
        """
        if self._session:
            try:
                self._session.rollback()
            finally:
                self._session.close()

        current_session.reset(self._token)
