from tests.db.config import ORM


def __get_repository_adapter_class():
    match ORM:
        case "sqlalchemy":
            from tests.db.repository.adapters.SqlAlchemyRepository import (
                SqlAlchemyRepository,
            )

            return SqlAlchemyRepository
        case _:
            raise Exception(f"ORM {ORM} not supported")


Repository = __get_repository_adapter_class()
