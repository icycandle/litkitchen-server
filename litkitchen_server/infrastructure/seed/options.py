from sqlmodel import Session, select
from litkitchen_server.infrastructure.repository_provider import engine
from litkitchen_server.infrastructure.models import (
    MainDishTextOrm,
    SideDishMediaOrm,
    DrinkStyleOrm,
)


def insert_options_fixture():
    session = Session(engine)
    # 若已存在資料則跳過
    if (
        session.exec(select(MainDishTextOrm)).first()
        or session.exec(select(SideDishMediaOrm)).first()
        or session.exec(select(DrinkStyleOrm)).first()
    ):
        session.close()
        return

    # MainDishTextOrm fixture
    main_dishes = [
        MainDishTextOrm(
            id=1,
            author_name="寺尾哲也",
            work_title="子彈是餘生",
            main_dish="洋芋片",
            publisher="聯經",
            genre="小說",
        ),
        MainDishTextOrm(
            id=2,
            author_name="張嘉祥",
            work_title="夜官巡場 Iā-Kuan Sûn-Tiûnn",
            main_dish="虱目魚粥",
            publisher="九歌",
            genre="小說",
        ),
        MainDishTextOrm(
            id=3,
            author_name="薛西斯",
            work_title="K.I.N.G.：天災對策室",
            main_dish="馬鈴薯",
            publisher="獨步",
            genre="小說",
        ),
        MainDishTextOrm(
            id=4,
            author_name="楊双子",
            work_title="臺灣漫遊錄",
            main_dish="咖哩飯",
            publisher="春山",
            genre="小說",
        ),
        MainDishTextOrm(
            id=5,
            author_name="李昂",
            work_title="殺夫",
            main_dish="鴨肉飯",
            publisher="聯經",
            genre="小說",
        ),
        MainDishTextOrm(
            id=6,
            author_name="黃麗群",
            work_title="海邊的房間",
            main_dish="麻油雞湯",
            publisher="未提供",
            genre="小說",
        ),
        MainDishTextOrm(
            id=7,
            author_name="陳千武",
            work_title="獵女犯",
            main_dish="爪哇烤雞飯",
            publisher="未提供",
            genre="小說",
        ),
        MainDishTextOrm(
            id=8,
            author_name="呂赫若",
            work_title="呂赫若全集",
            main_dish="豬肉乾",
            publisher="未提供",
            genre="小說",
        ),
        MainDishTextOrm(
            id=9,
            author_name="賴和",
            work_title="新編賴和全集",
            main_dish="燒肉圓",
            publisher="未提供",
            genre="小說",
        ),
        MainDishTextOrm(
            id=10,
            author_name="謝宜安",
            work_title="必修！臺灣校園鬼故事考",
            main_dish="營養麵條",
            publisher="蓋亞",
            genre="非虛構",
        ),
        MainDishTextOrm(
            id=11,
            author_name="房慧真",
            work_title="夜遊：解嚴前夕一個國中女生的身體時代記",
            main_dish="榴槤糯米飯",
            publisher="春山",
            genre="散文",
        ),
        MainDishTextOrm(
            id=12,
            author_name="程廷 Apyang Imiq",
            work_title="我長在打開的樹洞",
            main_dish="小米粥",
            publisher="九歌",
            genre="散文",
        ),
        MainDishTextOrm(
            id=13,
            author_name="白萩",
            work_title="香頌",
            main_dish="炒米粉",
            publisher="黑眼睛",
            genre="詩",
        ),
    ]

    side_dishes = [
        SideDishMediaOrm(id=1, media_type="電影／劇集", side_dish="爆米花"),
        SideDishMediaOrm(id=2, media_type="戲劇", side_dish="生菜沙拉"),
        SideDishMediaOrm(id=3, media_type="電玩", side_dish="茶葉蛋"),
        SideDishMediaOrm(id=4, media_type="虛擬實境", side_dish="分子料理"),
        SideDishMediaOrm(id=5, media_type="音樂概念專輯", side_dish="三色豆"),
    ]

    drink_styles = [
        DrinkStyleOrm(id=1, style="蒙太奇", drink="烏龍茶"),
        DrinkStyleOrm(id=2, style="懸疑", drink="咖啡"),
        DrinkStyleOrm(id=3, style="後設", drink="紅茶"),
        DrinkStyleOrm(id=4, style="黑色喜劇", drink="可樂"),
        DrinkStyleOrm(id=5, style="歌德", drink="提神飲料"),
        DrinkStyleOrm(id=6, style="推理", drink="鐵觀音"),
        DrinkStyleOrm(id=7, style="魂系", drink="抹茶"),
        DrinkStyleOrm(id=8, style="八點檔", drink="可爾必思"),
    ]

    for obj in main_dishes + side_dishes + drink_styles:
        session.add(obj)
    session.commit()
    session.close()
