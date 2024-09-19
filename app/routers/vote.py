from fastapi import APIRouter, Depends, HTTPException, status
from .. import oauth2, database, schemas, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=["Vote"],
)

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_acct: int = Depends(oauth2.get_current_user)):
    
    print(f"post ID: {vote.post_id}, Acct ID: {current_acct.id}")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.account_id == current_acct.id)
    vote_found = vote_query.first()

    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post_found = post_query.first()

    # CHECK IF THE POST EXIST OR NOT
    if post_found:
        # CHECK IF USER ALREADY LIKED THE POST
        if vote.dir == 1:
            if vote_found:
                raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail=f"user {current_acct.id} has already voted that post {vote.post_id}")
            else:
                vote_new = models.Vote(post_id = vote.post_id, account_id = current_acct.id)
                db.add(vote_new)
                db.commit()
                return {"result": "Successfully added Vote"}
        else:
            if vote_found:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
            else:
                vote_query.delete(synchronize_session=False)
                db.commit()

                return {"Result" : "Successfully deleted Vote"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no post")