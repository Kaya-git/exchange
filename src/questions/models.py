from database.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

class QuestionAnswers(Base):
    __tablename__ = "questions_answers"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    question: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True
    )
    answer: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True
    )
