from asyncio import sleep

from database.db import Database
from pendings.models import PendingAdmin

from .schemas import ReviewDTO


async def check_review_verif(
       db: Database,
       review: ReviewDTO
) -> None:

    while True:
        print('Ожидаю подтверждения')
        check_review = None 
        check_review = await db.review.get(ident=review.id)

        if check_review.moderated is True or check_review is None:
            await db.pending_admin.delete(
                PendingAdmin.review_id == check_review.id
            )
            await db.session.commit()
            return

        await sleep(3)
