from typing import Type
from typing import Callable
from typing import TypeVar
from typing import Generic
from typing import Optional
from typing import List
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, inspect
from sqlalchemy import delete

from core.exceptions import ApiExistsError
from core.logger import logger
from modules.base_pydantic import BasePydanticModel
from modules.base_entity import BaseEntity

Entity = TypeVar("Entity", bound=BaseEntity)
Schema = TypeVar("Schema", bound=BasePydanticModel)


class BaseRepository(Generic[Entity, Schema]):
    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        entity: Type[Entity],
        model: Type[Schema],
    ):
        self.session_factory = session_factory
        self.entity = entity
        self.model = model

    def from_model(self, model: Schema) -> Entity:
        """
        Преобразует Pydantic модель в SQLAlchemy сущность.
        """
        try:
            data_values = {}
            columns = inspect(self.entity).mapper.column_attrs
            for column in columns:
                col_name = column.key
                if hasattr(model, col_name):  # Проверяем наличие поля в модели
                    data_values[col_name] = getattr(model, col_name)
            return self.entity(**data_values)
        except Exception as e:
            logger.error(f"Ошибка преобразования модели в сущность: {e}")
            raise ValueError(
                "Ошибка преобразования Pydantic модели в SQLAlchemy сущность."
            )

    def to_model(self, entity: Entity) -> Schema:
        """
        Преобразует SQLAlchemy сущность в Pydantic модель.
        """
        try:
            entity_data = {
                column.key: getattr(entity, column.key)
                for column in inspect(self.entity).mapper.column_attrs
            }
            return self.model(**entity_data)
        except Exception as e:
            logger.error(f"Ошибка преобразования сущности в модель: {e}")
            raise ValueError(
                "Ошибка преобразования SQLAlchemy сущности в Pydantic модель."
            )

    async def create(self, model: Schema) -> Schema:
        """Добавляет новую запись на основе Pydantic-модели."""
        async with self.session_factory() as session:
            try:
                entity = self.from_model(model)
                session.add(entity)
                await session.commit()

                await session.refresh(entity)
                return self.to_model(entity)
            except IntegrityError:
                await session.rollback()
                raise ApiExistsError()

    async def get_by_id(self, _id: Any) -> Optional[Schema]:
        """Возвращает запись по ID."""
        async with self.session_factory() as session:
            query = select(self.entity).where(self.entity.id == _id)
            entity = await session.scalar(query)
            return self.to_model(entity) if entity else None

    async def get_all(self) -> List[Schema]:
        """Возвращает все записи."""
        async with self.session_factory() as session:
            result = await session.execute(select(self.entity))
            entities = result.scalars().all()
            return [self.to_model(entity) for entity in entities]

    async def update(self, _id: Any, updated_data: dict) -> Optional[Schema]:
        """Обновляет запись."""
        async with self.session_factory() as session:
            query = (
                update(self.entity).where(self.entity.id == _id).values(**updated_data)
            )
            await session.execute(query)
            await session.commit()
            return await self.get_by_id(_id)

    async def delete(self, _id: Any):
        """Удаляет запись."""
        async with self.session_factory() as session:
            query = delete(self.entity).where(self.entity.id == _id)
            await session.execute(query)
            await session.commit()

    async def get_by_filter(self, **filters) -> Schema:
        """Возвращает записи по фильтру."""
        async with self.session_factory() as session:
            query = select(self.entity).filter_by(**filters).limit(1)
            entity = await session.scalar(query)
            return self.to_model(entity) if entity else None
