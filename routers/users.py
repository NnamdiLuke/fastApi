from fastapi import APIRouter, HTTPException, status, Depends
from backend.schemas.users import UserCreate, UserRead
from backend.crud.database import get_session
from backend.crud.users import get_user_by_email, create_user
from sqlmodel import Session
from backend.utils.email import send_email_async
from fastapi import BackgroundTasks


router = APIRouter(prefix="/api")

# @router.post('/register/', response_model=UserRead)
# async def register(background_tasks:BackgroundTasks,user_in: UserCreate,session: Session = Depends(get_session),):
#     # verify that user doesn't already exist
#     user = get_user_by_email(session,user_in.email)
#     if user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Email already registered')
#     #save the user in db
#     user = create_user(session,email=user_in.email,password=user_in.password)

#     # send email
#     subject = 'Welcome to Aero Bound Ventures'
#     recipient = [user_in.email]
#     body_text = f'Hello {user_in.email},\n\n Thank you for registering.'
#     background_tasks.add_task(
#         send_email_async(subject, recipient, body_text)
#     )
#     return user


@router.post("/register/", response_model=UserRead)
async def register(
    background_tasks: BackgroundTasks,
    user_in: UserCreate,
    session: Session = Depends(get_session),
):
    user = get_user_by_email(session, user_in.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user = create_user(session, email=user_in.email, password=user_in.password)

    subject = "Welcome to Aero Bound Ventures"
    recipient = [user_in.email]
    body_text = f"Hello {user_in.email},\n\nThank you for registering."

    background_tasks.add_task(send_email_async, subject, recipient, body_text)

    return user
