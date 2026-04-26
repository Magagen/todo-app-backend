from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category import CategoryNotFoundError, CategoryService


def test_get_categories_returns_pydantic_models(
    category_service: CategoryService,
    category_repository_mock: Mock,
) -> None:
    # Имитируем, что метод get_all репозитория вернет эти задачи
    category_repository_mock.get_all.return_value = [
        CategoryORM(id="1", name="Категория1"),
        CategoryORM(id="2", name="Категория2"),
    ]

    result = category_service.get_categories()

    assert result == [
        CategoryRead(id="1", name="Категория1"),
        CategoryRead(id="2", name="Категория2"),
    ]


def test_create_category_commits_created_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    created_category = CategoryORM(id="task-1", name="new category")
    category_repository_mock.create.return_value = created_category

    result = category_service.create_category(CategoryCreate(name="new category"))

    category_repository_mock.create.assert_called_once_with(name="new category")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "name": "new category",
    }


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdate(name="Обновить имя"),  # payload
            "Обновить имя",  # expected_name
        ),
        pytest.param(
            CategoryUpdate(name="new name"),  # payload
            "new name",  # expected_name
        ),
        pytest.param(
            CategoryUpdate(name="dada"),  # payload
            "dada",  # expected_name
        ),
    ],
)
def test_update_task_updates_only_passed_fields(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
    payload: CategoryUpdate,
    expected_name: str,
) -> None:
    category = CategoryORM(id="category-1", name="category-1")
    category_repository_mock.get_by_id.return_value = category

    result = category_service.update_category("category-1", payload)

    category_repository_mock.get_by_id.assert_called_once_with("category-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": expected_name,
    }


def test_update_category_raises_when_category_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):  # Должна произойти указанная ошибка
        category_service.update_category(
            "missing-category", CategoryUpdate(name="Неважно")
        )

    db_mock.commit.assert_not_called()


def test_delete_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    created_category = CategoryORM(id="category-1", name="Новая категория")
    category_repository_mock.get_by_id.return_value = created_category
    category_service.delete_category("category-1")

    category_repository_mock.get_by_id.assert_called_once_with("category-1")
    category_repository_mock.delete.assert_called_once_with(created_category)
    db_mock.commit.assert_called_once_with()
