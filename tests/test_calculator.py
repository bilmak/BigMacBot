from app.calculator import Calculator
from app.menu import Menu, MenuUpsell
from app.menu import Menu, MenuUpsell
from app.calculator import Calculator
import pytest
from app.menu import Menu, MenuUpsell
from app.calculator import Calculator


def test_single_burger():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [
        {"name": "Big Mac"}
    ]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 5.99


def test_two_cheeseburgers():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "Cheeseburger",
        "quantity": 2
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 4.98


def test_meal_combo_mcchicken_meal():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "McChicken Meal"
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 6.79


def test_burger_with_additionals():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "Cheeseburger",
        "additionals": [{"name": "Bacon", "number": 2},],
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 3.99


def test_multiple_additional():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_input = [{
        "name": "Double Cheeseburger",
        "additionals": [
            {"name": "Bacon", "number": 1},
            {"name": "Tomato", "number": 2}
        ]
    }]
    total = calc.calculate_total(user_input)
    assert round(total, 2) == 5.14


def test_unknown_ingredient():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)
    user_order = [{
        "name": "Cheeseburger", "additionals": [{
            "name": "bober", "number": 20
        },],
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 2.49


def test_remove_default_ing():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "Cheeseburger", "removed": [{
            "name": "Onion"},
            {"name": "Pickles"},],
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 2.49


def test_mix_order_meal_and_custom_burgers():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "Big Mac Meal"},
        {"name": "Cheeseburger",
         "additionals": [
             {"name": "Bacon", "number": 1},], },
        {"name": "Apple Pie"},]

    total = calc.calculate_total(user_order)
    assert round(total, 2) == 12.52


def test_size_fries_small():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "French Fries", "size": "small"
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 1.39


def test_size_fries_large():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "French Fries", "size": "large"
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 2.49


def test_large_cola():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "Coca-Cola", "size": "large"
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 1.61


def test_no_size_cola():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)

    user_order = [{
        "name": "Coca-Cola"
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 1.29


def test_meal_with_sauce():
    menu = Menu("data/menu_ingredients.yaml")
    menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, menu_upsell)
    user_order = [{
        "name": "Big Mac Meal",
        "fries": "French Fries",
        "drinks": "Coca-Cola"
    }, {
        "name": "Ketchup"
    }]
    total = calc.calculate_total(user_order)
    assert round(total, 2) == 8.24


def test_double_deal_simple_case():
    menu = Menu("data/menu_ingredients.yaml")
    ups = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, ups)
    pr = {}
    for it in menu.data["items"]:
        pr[it["name"]] = it["price"]

    order = [
        {"name": "Hamburger", "quantity": 1, "double_deal": True},
        {"name": "Cheeseburger", "quantity": 1, "double_deal": True}
    ]

    got = calc.calculate_total(order)

    expect = (pr["Hamburger"] + pr["Cheeseburger"]) * 0.8

    assert round(got, 2) == round(expect, 2)


def test_double_deal_plus_regular_item():
    menu = Menu("data/menu_ingredients.yaml")
    upsell = MenuUpsell("data/menu_upsells.yaml")
    calc = Calculator(menu, upsell)

    prices = {i["name"]: i["price"] for i in menu.data["items"]}

    order = [
        {"name": "Hamburger", "quantity": 1, "double_deal": True},
        {"name": "Cheeseburger", "quantity": 1, "double_deal": True},
        {"name": "Filet-O-Fish", "quantity": 1}
    ]

    expected_total = (prices["Hamburger"] + prices["Cheeseburger"]) * 0.8
    expected_total += prices["Filet-O-Fish"]

    result = calc.calculate_total(order)

    assert abs(result - expected_total) < 0.01
