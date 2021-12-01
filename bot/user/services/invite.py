from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.user.models import Invite


async def get_invite_by_hash(session: AsyncSession, hash: str) -> Optional[Invite]:
    query = select(Invite).where(Invite.hash == hash)
    result = await session.execute(query)
    return result.scalars().first()


async def create_invite(session: AsyncSession, creator_id: int, hash: str, user_identifier: str) -> Invite:
    invite = Invite(creator=creator_id, hash=hash, user_identifier=user_identifier)
    session.add(invite)
    return invite


async def update_invited_user(session: AsyncSession, invite_id: int, invited_user_id: int) -> None:
    query = update(Invite.invited).where(Invite.id == invite_id).values(invited=invited_user_id)
    await session.execute(query)
