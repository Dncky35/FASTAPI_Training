from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import database, schemas, models,oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Post"],
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.Post_Create, db:Session = Depends(database.get_db), curr_account = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.model_dump())
    new_post.account_id = curr_account.id

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/", status_code=status.HTTP_302_FOUND, response_model=List[schemas.Post_Out])
async def get_posts(db:Session = Depends(database.get_db), curr_account = Depends(oauth2.get_current_user),
                    owner_id:int = 0, limit:int = 20, offset:int = 0, search:Optional[str] = ""):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    
    if owner_id != 0:

        if search == "":
            posts = results.filter(models.Post.account_id == owner_id).limit(limit).offset(offset).all()
        else:
            posts = results.filter(models.Post.account_id == owner_id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    else:
        if search == "":
            posts = results.limit(limit).offset(offset).all()
        else:
            posts = results.filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    return posts

@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.Post_Out)
async def get_post_by_id(id, db:Session = Depends(database.get_db), curr_account = Depends(oauth2.get_current_user)):
    
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    post = result.filter(models.Post.id == id).first()
    
    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"There is no post with id:{id}"
            )

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_post(id, db:Session = Depends(database.get_db), curr_account = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"There is no post with id:{id}"
            )
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return{ "data":"Has been Deleted"}
    
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(id, post:schemas.Post_Create, response: Response, db:Session = Depends(database.get_db), curr_account = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_found = post_query.first()

    if not post_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with id:{id}"
            )
    
    elif curr_account.id != post_found.account_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"UNAUTHORIZED"
        )
    
    else: 
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()