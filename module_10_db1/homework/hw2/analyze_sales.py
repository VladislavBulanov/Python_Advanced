import sqlite3
from typing import Dict, List, Tuple


def get_statistic() -> None:
    """The function analyzes database of phone's sales
    and prints statistic about phone's colors."""

    with sqlite3.connect("hw_2_database.db") as conn:
        cursor = conn.cursor()

        # Get all phone's models:
        cursor.execute("SELECT `phone_id` FROM `table_checkout`")
        phone_ids = cursor.fetchall()

        # Get how much sales each model has:
        sales_stats_by_model: Dict[int, int] = dict()
        for elem in phone_ids:
            sales_stats_by_model[elem[0]] = sales_stats_by_model.get(elem[0], 0) + 1
        # print(sales_stats_by_model)  # Debug print

        # Get all existing colors:
        cursor.execute("SELECT `id`, `colour` FROM `table_phones`")
        colors_by_models: List[Tuple[int, str]] = cursor.fetchall()
        # print(colors_by_models)  # Debug print

        # Get stats of sales by colors:
        sales_by_color: Dict[str, int] = dict()
        for i_id in sales_stats_by_model:
            for model in colors_by_models:
                if i_id in model:
                    sales_by_color[model[1]] = (sales_by_color.get(model[1], 0)
                                                + sales_stats_by_model[i_id])
        print(sales_by_color)


if __name__ == "__main__":
    get_statistic()
