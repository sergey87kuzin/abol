import datetime
import json
from http import HTTPStatus

import pytest
from sqlalchemy import select

from models import User, Book
from settings import TEST_PASSWORD

user_data = {
    "username": "johndoe@gmail.com",
    "password": TEST_PASSWORD,
}

correct_data = {
    "title": "some title",
    "author": "some author",
    "publish_date": "2020-01-01"
}
incorrect_title = {
    "title": "some title +-;&?#",
    "author": "some author )(&%#@",
    "publish_date": "2020-01-01"
}
too_big_date = {
    "title": "some title new",
    "author": "some author new",
    "publish_date": (datetime.date.today() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
}
too_early_date = {
    "title": "some title old",
    "author": "some author old",
    "publish_date": "1200-01-01"
}


class TestBooks:
    @pytest.fixture(autouse=True)
    async def setup(self, client, create_user, async_session_test):
        await create_user("some_test_user", TEST_PASSWORD)
        access_data = {"username": "some_test_user", "password": TEST_PASSWORD}
        tokens = client.post("api/users/token", data=access_data).json()
        token = tokens.get("access_token")
        self.headers = {"Authorization": f"Bearer {token}"}

    async def result_check(
            self,
            response,
            response_status,
            async_session_test,
            data_dict
    ):
        assert response.status_code == response_status
        if response_status != HTTPStatus.OK:
            return
        object_from_db_id = response.json()["id"]

        async with async_session_test() as session:
            results = await session.execute(select(Book).where(Book.id == object_from_db_id))
            if results := results.fetchone():
                result = results[0]
            else:
                raise AssertionError("Object not found")
        for key, value in data_dict.items():
            if key == "publish_date":
                assert value == result.publish_date.strftime("%Y-%m-%d")
            else:
                assert getattr(result, key) == value, "Неверное сохранение объекта в бд"

    @pytest.mark.parametrize(
        "data_dict,response_status", [
            (correct_data, HTTPStatus.OK),
            (incorrect_title, HTTPStatus.BAD_REQUEST),
            (too_big_date, HTTPStatus.BAD_REQUEST),
            (too_early_date, HTTPStatus.BAD_REQUEST),
        ]
    )
    async def test_create_books(
            self,
            data_dict,
            response_status,
            client,
            async_session_test,
    ):
        response = client.post(f"api/books/", content=json.dumps(data_dict), headers=self.headers)
        await self.result_check(response, response_status, async_session_test, data_dict)

    @pytest.mark.parametrize(
        "data_dict,response_status", [
            (correct_data, HTTPStatus.OK),
            (incorrect_title, HTTPStatus.BAD_REQUEST),
            (too_big_date, HTTPStatus.BAD_REQUEST),
            (too_early_date, HTTPStatus.BAD_REQUEST),
        ]
    )
    async def test_update_books(
            self,
            data_dict,
            response_status,
            client,
            create_book,
            async_session_test,
    ):
        new_book = await create_book(
            "update_test_title",
            "update_test_author",
            datetime.date.today()
        )
        response = client.patch(
            f"api/books/{new_book.id}/",
            content=json.dumps(data_dict),
            headers=self.headers
        )
        await self.result_check(response, response_status, async_session_test, data_dict)

    async def test_get_book(self, client, create_book):
        data_dict = {
            "title": "get_test_title",
            "author": "get_test_author",
            "publish_date": datetime.date.today()
        }
        new_book = await create_book(**data_dict)
        response = client.get(f"api/books/{new_book.id}/", headers=self.headers)
        assert response.status_code == HTTPStatus.OK
        response = response.json()
        for key, value in data_dict.items():
            if key == "publish_date":
                assert value.strftime("%Y-%m-%d") == response.get(key)
            else:
                assert response.get(key) == value

    async def test_delete_book(self, client, create_book, async_session_test):
        data_dict = {
            "title": "delete_test_title",
            "author": "delete_test_author",
            "publish_date": datetime.date.today()
        }
        new_book = await create_book(**data_dict)
        response = client.delete(f"api/books/{new_book.id}/", headers=self.headers)
        assert response.status_code == HTTPStatus.NO_CONTENT
        async with async_session_test() as session:
            query = select(Book).where(Book.id == new_book.id)
            results = await session.execute(query)
            assert results.fetchall() == []

    async def test_admin_pagination(self, create_book, client, async_session_test):
        for index in range(25):
            await create_book(
                title=f"title_{index}",
                author=f"author_{index}",
                publish_date=datetime.date.today()
            )
        list_response = client.get(url=f"api/books/?page=2&limit=10", headers=self.headers)
        assert list_response.status_code == HTTPStatus.OK, "Неверный статус запроса при наличии пагинации"
        resp_data = list_response.json()
        assert resp_data.get("objects_count") >= 25
        assert len(resp_data.get("objects")) == 10
