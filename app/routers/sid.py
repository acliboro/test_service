from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List, Union
from .. import models, schemas
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/sids",
    tags=["Sids"]
)

# @router.get("/", response_model=List[schemas.Post])
# def get_sids(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_sids(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# @router.get("/{full_cusip}", response_model=List[schemas.SecMaster])
# def get_security_master(full_cusip: str, full_sedol: Union[str, None] = None,
#         ticker: Union[str, None] = None, exch_symbol: Union[str, None] = None, 
#         isin: Union[str, None] = None, symbol: Union[str, None] = None, db: Session = Depends(get_db)):

#     results = None
#     print("Query Security Master DB")
#     query_start_time = datetime.utcnow()
#     if full_cusip:
#         results = db.query(models.SecMaster).filter(models.SecMaster.full_cusip == full_cusip).all()
#     elif full_sedol:
#         results = db.query(models.SecMaster).filter(models.SecMaster.full_sedol == full_sedol).all()
#     query_end_time = datetime.utcnow()
#     print(f"Time elapsed: {query_end_time-query_start_time}")
#     if not results:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"data with ticker: {full_cusip} was not found")
#     return results

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_sid(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id)

#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id: {id} does not exist")
    
#     post.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.put("/{id}", response_model=schemas.Post)
# def update_sid(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

#     post_query = db.query(models.Post).filter(models.Post.id == id)

#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} does not exist")

#     post_query.update(updated_post.dict(), synchronize_session=False)
#     db.commit()

#     return post_query.first()