from fastapi import APIRouter
from .handlers import ver_recaptcha
from config import conf

recaptcha_router = APIRouter(
    prefix='/recaptcha',
    tags=['Роутер Google reCaptcha']
)


@recaptcha_router.post('/verify-recaptcha')
async def verify_recaptcha(token: str):
    if ver_recaptcha(
        token,
        conf.google_recaptcha.gsk,
        conf.google_recaptcha.google_url
    ):
        return {'success': True}
    else:
        return {'success': False}


@recaptcha_router.get('/pbc')
async def give_pbc() -> str:
    return conf.google_recaptcha.gpk
