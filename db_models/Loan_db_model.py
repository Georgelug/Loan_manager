from imports import *
from models.Client import Client
from models.Loan import Loan, Status


Base = declarative_base()

class LoanModel(Base):
    __tablename__ = 'Loans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("Clients.id"), nullable=False)
    amount = Column(Float, nullable=False)
    fecha_otorgamiento = Column(DateTime, nullable=False)
    status = Column(SQLEnum(Status), nullable=False)