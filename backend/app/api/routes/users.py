from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.models import User
from ...services.redis_service import RedisService
from ..schemas.users import UserCreate, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    active_users = await RedisService.get_active_users_count()
    if active_users >= 100:
        raise HTTPException(status_code=400, detail="Server at capacity")

    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await RedisService.add_active_user(str(new_user.id))

    return UserResponse(id=new_user.id, username=new_user.username)


@router.delete("/users/{user_id}")
async def remove_active_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await RedisService.remove_active_user(str(user_id))

    return {"detail": "User session ended"}
