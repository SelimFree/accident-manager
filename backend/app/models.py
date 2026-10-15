"""Register every SQLAlchemy ORM model before any ORM query.

SQLAlchemy relationships like relationship("Comment") resolve via the
registry only after the model defining that class has been imported.
"""
from app.features.users.models import User, UserRole
from app.features.accidents.models import Accident, AccidentStatus, IncidentConfirmation, NotificationEvent
from app.features.comments.models import Comment

__all__ = [
    "User", "UserRole", "Accident", "AccidentStatus",
    "IncidentConfirmation", "NotificationEvent", "Comment",
]
