from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, utils, models

router = APIRouter(
    prefix="/account",
    tags=['account']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Account)
def createAccount(account: schemas.Account_Create, db:Session = Depends(database.get_db)):
    hassed_password = utils.hasher(account.password)
    account.password = hassed_password

    new_account = models.Account(**account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account