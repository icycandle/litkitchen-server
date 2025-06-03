import pytest
from fastapi.testclient import TestClient
from litkitchen_server.main import app
from litkitchen_server.infrastructure.repository_provider import (
    get_main_dish_text_repo,
    get_side_dish_media_repo,
    get_drink_style_repo,
)
from litkitchen_server.infrastructure.main_dish_text_repository import (
    MainDishTextRepository,
)
from litkitchen_server.infrastructure.side_dish_media_repository import (
    SideDishMediaRepository,
)
from litkitchen_server.infrastructure.drink_style_repository import DrinkStyleRepository
from litkitchen_server.infrastructure.repository_provider import engine
from sqlmodel import Session

session = Session(engine)


def override_main_dish_text_repo():
    return MainDishTextRepository(session)


def override_side_dish_media_repo():
    return SideDishMediaRepository(session)


def override_drink_style_repo():
    return DrinkStyleRepository(session)


app.dependency_overrides[get_main_dish_text_repo] = override_main_dish_text_repo
app.dependency_overrides[get_side_dish_media_repo] = override_side_dish_media_repo
app.dependency_overrides[get_drink_style_repo] = override_drink_style_repo

client = TestClient(app)


@pytest.mark.e2e
def test_get_options_maindish(options_fixture):
    resp = client.get("/api/options/maindish")
    assert resp.status_code == 200
    assert resp.json() == [
        {
            "id": 1,
            "author_name": "寺尾哲也",
            "work_title": "子彈是餘生",
            "main_dish": "洋芋片",
            "publisher": "聯經",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 2,
            "author_name": "張嘉祥",
            "work_title": "夜官巡場 Iā-Kuan Sûn-Tiûnn",
            "main_dish": "虱目魚粥",
            "publisher": "九歌",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 3,
            "author_name": "薛西斯",
            "work_title": "K.I.N.G.：天災對策室",
            "main_dish": "馬鈴薯",
            "publisher": "獨步",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 4,
            "author_name": "楊双子",
            "work_title": "臺灣漫遊錄",
            "main_dish": "咖哩飯",
            "publisher": "春山",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 5,
            "author_name": "邱常婷",
            "work_title": "獸靈之詩",
            "main_dish": "山芋",
            "publisher": "獨步",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 6,
            "author_name": "李昂",
            "work_title": "殺夫",
            "main_dish": "鴨肉飯",
            "publisher": "聯經",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 7,
            "author_name": "張貴興",
            "work_title": "野豬渡河",
            "main_dish": "肉絲炒飯",
            "publisher": "時報",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 8,
            "author_name": "楊千鶴",
            "work_title": "花開時節",
            "main_dish": "和式麵包",
            "publisher": "前衛",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 9,
            "author_name": "葉石濤",
            "work_title": "台灣男子簡阿淘",
            "main_dish": "地瓜粥",
            "publisher": "草根",
            "genre": "小說",
            "description": "",
        },
        {
            "id": 10,
            "author_name": "謝宜安",
            "work_title": "必修！臺灣校園鬼故事考",
            "main_dish": "營養麵條",
            "publisher": "蓋亞",
            "genre": "非虛構",
            "description": "",
        },
        {
            "id": 11,
            "author_name": "房慧真",
            "work_title": "夜遊：解嚴前夕一個國中女生的身體時代記",
            "main_dish": "榴槤糯米飯",
            "publisher": "春山",
            "genre": "散文",
            "description": "",
        },
        {
            "id": 12,
            "author_name": "程廷 Apyang Imiq",
            "work_title": "我長在打開的樹洞",
            "main_dish": "小米粥",
            "publisher": "九歌",
            "genre": "散文",
            "description": "",
        },
        {
            "id": 13,
            "author_name": "白萩",
            "work_title": "香頌",
            "main_dish": "炒米粉",
            "publisher": "黑眼睛",
            "genre": "詩",
            "description": "",
        },
    ]


@pytest.mark.e2e
def test_get_options_sidedish(options_fixture):
    resp = client.get("/api/options/sidedish")
    assert resp.status_code == 200
    assert resp.json() == [
        {"id": 1, "media_type": "電影／劇集", "side_dish": "爆米花"},
        {"id": 2, "media_type": "戲劇", "side_dish": "生菜沙拉"},
        {"id": 3, "media_type": "電玩", "side_dish": "茶葉蛋"},
        {"id": 4, "media_type": "虛擬實境", "side_dish": "分子料理"},
        {"id": 5, "media_type": "音樂概念專輯", "side_dish": "三色豆"},
    ]


@pytest.mark.e2e
def test_get_options_drinkstyle(options_fixture):
    resp = client.get("/api/options/drinkstyle")
    assert resp.status_code == 200
    assert resp.json() == [
        {"id": 1, "style": "蒙太奇", "drink": "烏龍茶"},
        {"id": 2, "style": "懸疑", "drink": "咖啡"},
        {"id": 3, "style": "後設", "drink": "紅茶"},
        {"id": 4, "style": "黑色喜劇", "drink": "可樂"},
        {"id": 5, "style": "歌德", "drink": "提神飲料"},
        {"id": 6, "style": "推理", "drink": "鐵觀音"},
        {"id": 7, "style": "魂系", "drink": "抹茶"},
        {"id": 8, "style": "八點檔", "drink": "蔬果汁"},
    ]
