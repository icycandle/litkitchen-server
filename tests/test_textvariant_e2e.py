import pytest
from fastapi.testclient import TestClient
from litkitchen_server.main import app
from litkitchen_server.infrastructure.models import (
    TextVariant,
)  # 假設有 models 可直接操作

from litkitchen_server.infrastructure.repository_provider import engine, get_session
from sqlmodel import Session
from litkitchen_server.infrastructure.text_variant_repository import (
    TextVariantRepository,
)
from litkitchen_server.infrastructure.main_dish_text_repository import (
    MainDishTextRepository,
)
from litkitchen_server.infrastructure.side_dish_media_repository import (
    SideDishMediaRepository,
)
from litkitchen_server.infrastructure.drink_style_repository import DrinkStyleRepository
from litkitchen_server.domain.models import MainDishText, SideDishMedia, DrinkStyle

# 測試共用 session
session = Session(engine)


def override_get_session():
    yield session


app.dependency_overrides[get_session] = override_get_session

# Debug: 列印 app routes
for route in app.routes:
    print(f"ROUTE: {getattr(route, 'path', None)} {getattr(route, 'methods', None)}")

client = TestClient(app)


@pytest.mark.e2e
def test_get_text_variant_by_id(monkeypatch):
    global session
    # Setup: 直接寫入資料庫 fixture

    repo = TextVariantRepository(session)
    tv = TextVariant(
        main_dish_text_id=1,
        side_dish_media_id=1,
        drink_style_id=1,
        content="e2e test",
        variant_index=0,
        length=10,
        approved=True,
        print_count=0,
    )
    created = repo.create(tv)
    print(f"DEBUG created: {created}, id: {created.id}")
    db_tv = repo.get(created.id)
    print(f"DEBUG DB get({created.id}):", db_tv, type(db_tv))

    # Act
    resp = client.get(f"/api/text-variants/{created.id}")
    print(
        "DEBUG /text-variants/{id}:",
        resp.status_code,
        resp.json() if resp.status_code == 200 else resp.text,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == created.id
    assert data["content"] == "e2e test"

    # Teardown: 清除 fixture
    repo.delete(created.id)


@pytest.mark.e2e
def test_get_text_variants_filter(monkeypatch):
    global session

    repo = TextVariantRepository(session)
    # 清理舊資料，確保只測剛建立的那一筆
    for old in repo.get_all():
        if (
            old.main_dish_text_id == 2
            and old.side_dish_media_id == 2
            and old.drink_style_id == 2
        ):
            repo.delete(old.id)

    tv = TextVariant(
        main_dish_text_id=2,
        side_dish_media_id=2,
        drink_style_id=2,
        content="filter test",
        variant_index=1,
        length=11,
        approved=True,
        print_count=0,
    )
    created = repo.create(tv)

    resp = client.get(
        "/api/text-variants/pick-best",
        params={"main_dish_text_id": 2, "side_dish_media_id": 2, "drink_style_id": 2},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == created.id
    assert data["content"] == "filter test"
    repo.delete(created.id)


@pytest.mark.e2e
def test_print_count_pick_best_happy_path():
    # 建立 option fixture
    main_repo = MainDishTextRepository(session)
    side_repo = SideDishMediaRepository(session)
    drink_repo = DrinkStyleRepository(session)
    main = main_repo.create(
        MainDishText(
            author_name="A",
            work_title="B",
            main_dish="C",
            publisher="D",
            genre="E",
            description="",
        )
    )
    side = side_repo.create(SideDishMedia(media_type="電影", side_dish="爆米花"))
    drink = drink_repo.create(DrinkStyle(style="懸疑", drink="咖啡"))
    # 建立 textvariant
    tv_repo = TextVariantRepository(session)
    tv = tv_repo.create(
        TextVariant(
            main_dish_text_id=main.id,
            side_dish_media_id=side.id,
            drink_style_id=drink.id,
            content="test content",
            variant_index=0,
            length=12,
            approved=True,
            print_count=0,
        )
    )
    session.commit()

    client = TestClient(app)
    resp = client.get(f"/api/text-variants/print/{main.id}/{side.id}/{drink.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert "ok" in data

    # 清理
    tv_repo.delete(tv.id)
    main_repo.delete(main.id)
    side_repo.delete(side.id)
    drink_repo.delete(drink.id)
    session.commit()
    session.close()
