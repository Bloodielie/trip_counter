from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.user.models import Role, users_roles


async def get_role_by_codename(session: AsyncSession, codename: str) -> Optional[Role]:
    query = select(Role).where(Role.codename == codename)
    result = await session.execute(query)
    return result.scalars().first()


async def create_role(session: AsyncSession, codename: str, description: Optional[str] = None) -> Role:
    role = Role(codename=codename, description=description)
    session.add(role)
    return role


async def add_role_to_user(session: AsyncSession, codename: str, user_id: int) -> None:
    role_id_subquery = select(Role.id).where(Role.codename == codename).subquery()
    query = insert(users_roles).values(user=user_id, role=role_id_subquery)
    await session.execute(query)
