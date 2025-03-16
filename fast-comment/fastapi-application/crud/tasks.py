#
# from core.schemas.user import UserCheck
#
# from typing import Sequence
# from core.models import User, Panels, Panel
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession


# async def get_panel_by_number(session: AsyncSession, check_user: UserCheck):
#     result = await session.execute(select(Panel).where(Panel.number_panels == check_user.number_panels))
#     return result.scalars().first()
#
# async def check_user(session: AsyncSession, check_user: UserCheck):
#     result = await session.execute(
#         select(User).where(
#             User.username == check_user.username,
#             User.password == check_user.password)
#     )
#
#     user = result.scalars().first()
#
#     result = await session.execute(
#         select(Panels, User).where(
#             Panels.number_panels == check_user.number_panels,
#             Panels.check == True,
#             Panels.id ==User.id_user
#         )
#     )
#
#     panel = result.scalars().first()
#
#     return user, panel