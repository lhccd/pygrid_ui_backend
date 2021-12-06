from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import LargeBinary

from app.db.base_class import Base


class PDFObject(Base):
    __tablename__ = "daa_pdf"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    binary = Column(LargeBinary(3072))
