from fastapi import APIRouter, Form

from config import conf

from .handlers import ver_recaptcha

recaptcha_router = APIRouter(
    prefix='/api/recaptcha',
    tags=['Роутер Google reCaptcha']
)


@recaptcha_router.post('/verify-recaptcha')
async def verify_recaptcha(token: str | None = Form()):
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
