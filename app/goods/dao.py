from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import Goods
from .schemas import PaginationGoods


class GoodsDAO(BaseDAO):
    model = Goods

    @classmethod
    async def get_goods_objects_all_information(cls, **kwargs):
        """Возвращает все товары cо всей информацией."""
        try:
            async with async_session_maker() as session:
                goods = (
                    select(Goods)
                    .options(selectinload(Goods.purchases))
                    .options(joinedload(Goods.subcategory))
                )
                goods = await session.execute(goods)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return jsonable_encoder(goods.scalars().all())

    @classmethod
    async def get_pagination_goods(cls, **kwargs):
        if kwargs['page_size'] <= 0 or kwargs['page_size'] >= 100:
            kwargs['page_size'] = 2

        if kwargs['page'] <= 0:
            kwargs['page'] = 1

        try:
            async with async_session_maker() as session:
                length = (
                    select(func.count(Goods.id))
                )
                length = (await session.execute(length)).scalar_one()
                pages_count = length // kwargs['page_size'] + 1
                if pages_count > kwargs['page']:
                    page = kwargs['page'] - 1
                else:
                    page = pages_count - 1
                goods = (
                    select(Goods)
                    .offset(page*kwargs['page_size'])
                    .limit(kwargs['page_size'])
                    .options(joinedload(Goods.subcategory))
                )
                goods = (await session.execute(goods)).scalars().all()
                pagination = PaginationGoods(
                    total=len(goods),
                    page=page + 1,
                    page_size=kwargs['page_size'],
                    pages_count=pages_count,
                    data=jsonable_encoder(goods)
                )
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            print(message)
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return pagination
