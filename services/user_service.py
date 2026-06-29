from sqlalchemy.orm import Session
from models import User
from utils.security import hash_password


def create_user(
        db: Session,
        username: str,
        password: str
):

    hashed_password = hash_password(password)

    user = User(
        username=username,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
        db: Session,
        username: str,
        password: str
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        return None

    from utils.security import verify_password

    if not verify_password(
            password,
            user.password
    ):
        return None

    return user