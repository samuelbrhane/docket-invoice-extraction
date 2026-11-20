from app.db import Base
from app.models.mixins import CreatedAtMixin, UuidPkMixin


class Visitor(UuidPkMixin, CreatedAtMixin, Base):
    __tablename__ = "visitors"