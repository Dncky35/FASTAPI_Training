from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth2

router = APIRouter(
    prefix="/login",
    tags=["Authenticate"],
)

@router.post("/", response_model=schemas.Token)
async def login(credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    
    account = db.query(models.Account).filter(models.Account.email == credentials.username).first()

    if not account:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    elif not utils.verifyer(credentials.password, account.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    else:
        access_token = oauth2.create_access_token(data = {"account_id":account.id})
        return {"access_token": access_token, "token_type":"Bearer"}