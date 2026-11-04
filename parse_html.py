
import json
from html.parser import HTMLParser


class EquipmentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.current_row = []
        elif tag == "td":
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag == "td":
            self.in_cell = False
        elif tag == "tr":
            if self.current_row:
                self.rows.append(self.current_row)

    def handle_data(self, data):
        if self.in_cell:
            value = data.strip()
            if value:
                self.current_row.append(value)


def main():
    with open("equipment.html", "r", encoding="utf-8") as file:
        html = file.read()

    parser = EquipmentParser()
    parser.feed(html)

    equipment_list = []

    for row in parser.rows:
        if len(row) >= 3:
            equipment = {
                "inventory_number": row[0],
                "name": row[1],
                "status": row[2]
            }
            equipment_list.append(equipment)

    print("Распознанное оборудование:")

    for equipment in equipment_list:
        print(equipment)

    with open("parsed_equipment.json", "w", encoding="utf-8") as file:
        json.dump(
            equipment_list,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("\nДанные сохранены в parsed_equipment.json")


if __name__ == "__main__":
    main()
