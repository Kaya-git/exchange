# from passlib.context import CryptContext
# from sqlalchemy.ext.asyncio import AsyncSession


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





# class Hasher:
#     @staticmethod
#     def verify_password(plain_password, hashed_password):
#         return pwd_context.verify(plain_password, hashed_password)

#     @staticmethod
#     def get_password_hash(password: str) -> str:
#         return pwd_context.hash(password)

# async def authenticate_user(
#         email: str,
#         password: str,
#         session: AsyncSession
# ):
#     user = get_user_by_email_for_auth(email=email, session=session)
#     if user is None:
#         return False
#     if not Hasher.verify_password(password, user.hashed_password):
#         return False
#     return user
