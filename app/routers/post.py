import redis
import json
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas
from ..database import get_db
from ..utils import get_expiration_seconds, get_datetime_now
# from ..cache import get_redis_inst

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

try:
    redis_cache_inst = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
except Exception as e:
    print(str(e))

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    result = redis_cache_inst.exists("all_posts")
    print(f"This is the result of redis: {result}")
    # print(f"This is the len: {len(result)}")
    if not result:
        posts = db.query(models.Post).all()
        posts_json = jsonable_encoder(posts)
        print(f"This is the result of post: {posts_json}")
        time_now = get_datetime_now()
        redis_cache_inst.set("all_posts", json.dumps(posts_json))
        expiration_secs = get_expiration_seconds(time_now)
        redis_cache_inst.expire("all_posts", expiration_secs)
    else:
        print(f"Entered Here")
        result = redis_cache_inst.get("all_posts")
        posts = json.loads(result)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()