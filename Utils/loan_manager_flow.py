from imports import *
from models.Client import Client
from models.Loan import Loan
from models.Loan import Status
from Utils.db import DB
from db_models.Client_db_model import ClientModel 
from db_models.Loan_db_model import LoanModel


def create_client(client: Client, db: Session) -> ClientModel:
    try:
        db_client = ClientModel(
            nombre=client.nombre,
            correo=client.correo,
            rfc=client.rfc,
            fecha_alta=client.fecha_alta
        )

        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear el cliente: {e}")
        raise Exception(f"loan_manager_flow::create_client: No se pudo crear el cliente {client} en la base de datos, error: {e}")

def create_loan(loan: Loan, db: Session):
    try:
        new_loan = LoanModel(
            client_id=loan.client_id,
            amount=loan.amount,
            fecha_otorgamiento=loan.fecha_otorgamiento,
            status=loan.status
        )

        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return new_loan

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear préstamo: {e}")
        raise Exception(f"loan_manager_flow::create_loan: No se pudo crear el Prestamo {loan} en la base de datos, error: {e}")


def main_flow():
    db = DB().session_db()
    
    cliente1 = Client(
        nombre="Jorge",
        correo="esparzajorge03@gmail.com",
        rfc="xxxxxxxxxxxxxx",
        fecha_alta="01/01/2025"
    )
    
    result_client = create_client(client=cliente1,db=db)

    print(f"Cliente creado: {result_client}")

    # Create loan directly in database model to avoid enum conversion issues
    new_loan = LoanModel(
        client_id=result_client.id,
        amount=100.00,
        fecha_otorgamiento=datetime.strptime("01/01/2025", "%d/%m/%Y"),
        status=Status.activo
    )

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    result_loan = new_loan
    
    print(f"Prestamo otorgado: {result_loan}")



    db.close()

