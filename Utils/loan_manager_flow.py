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

def get_loans_by_client_id(client_id: int, db: Session) -> list[Loan]:
    try:
        loans = db.query(LoanModel).filter(LoanModel.client_id == client_id).all()
        if not loans:
            raise Exception(f"No se encontraron préstamos para el cliente con id={client_id}")
        
        return [Loan(
            id=loan.id,
            client_id=loan.client_id,
            amount=loan.amount,
            fecha_otorgamiento=loan.fecha_otorgamiento,
            status=loan.status
        ) for loan in loans]
    
    except Exception as e:
        raise Exception(f"loan_manager_flow::get_loans_by_client_id: Error al obtener préstamos del cliente {client_id}: {e}")



def update_loan_status(loan_id: int, new_status: Status, db: Session) -> Loan:
    try:
        loan = db.query(LoanModel).filter(LoanModel.id == loan_id).first()
        if not loan:
            raise Exception(f"No se encontró un préstamo con id={loan_id}")
        
        loan.status = new_status
        db.commit()
        db.refresh(loan)

        return Loan(
            id=loan.id,
            client_id=loan.client_id,
            amount=loan.amount,
            fecha_otorgamiento=loan.fecha_otorgamiento,
            status=loan.status
        )
    
    except Exception as e:
        raise Exception(f"loan_manager_flow::update_loan_status: Error al actualizar el estado del préstamo {loan_id}: {e}")


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

    result_loan = create_loan(loan=new_loan,db=db)
    
    print(f"Prestamo otorgado: {result_loan}")

    result_loans = get_loans_by_client_id(client_id=result_client.id,db=db)

    print(f"prestamos de cliente {result_client.id},\n{result_loans}")

    updated_loan = update_loan_status(loan_id=result_loan.id, new_status=Status.pagado, db=db)
    print(updated_loan)



    db.close()

