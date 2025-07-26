from imports import *
from models.Client import Client
from models.Loan import Loan

Base = declarative_base()


class ClientModel(Base):
    __tablename__ = 'Clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    correo = Column(String(255), nullable=False)
    rfc = Column(String(20), nullable=False)
    fecha_alta = Column(DateTime, nullable=False)

