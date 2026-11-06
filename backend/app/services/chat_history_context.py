
from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


active_session_context: ContextVar[
    tuple["Session", str] | None
] = ContextVar(
    "learnfirst_active_tutor_session",
    default=None,
)
