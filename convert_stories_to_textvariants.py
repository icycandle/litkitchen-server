import json
import csv
import re

# combo 對應表
main_dish_map = {f"a{i}": i for i in range(1, 14)}
side_dish_map = {f"b{i}": i for i in range(1, 6)}
drink_style_map = {f"c{i}": i for i in range(1, 9)}

with open("stories.json", "r", encoding="utf-8") as f:
    stories = json.load(f)

rows = []
for item in stories:
    combo = item["combo"]
    m = re.match(r"a(\d+) × b(\d+) × c(\d+)", combo)
    if not m:
        print(f"combo 格式錯誤: {combo}")
        continue
    a, b, c = m.groups()
    main_dish_text_id = int(a)
    side_dish_media_id = int(b)
    drink_style_id = int(c)
    content = item["story"].replace("\r\n", "\n").replace("\r", "\n")
    variant_index = 0
    length = len(content)
    approved = False
    print_count = 0
    rows.append(
        {
            "main_dish_text_id": main_dish_text_id,
            "side_dish_media_id": side_dish_media_id,
            "drink_style_id": drink_style_id,
            "content": content,
            "variant_index": variant_index,
            "length": length,
            "approved": approved,
            "print_count": print_count,
        }
    )

with open("textvariants_import.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "main_dish_text_id",
            "side_dish_media_id",
            "drink_style_id",
            "content",
            "variant_index",
            "length",
            "approved",
            "print_count",
        ],
    )
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print("已產生 textvariants_import.csv，可用於批次匯入 textvariants！")
