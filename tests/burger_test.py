import pytest
from unittest.mock import Mock
import praktikum.ingredient_types as types
from praktikum.burger import Burger

class TestBurger:

    @pytest.fixture
    def burger(self):
        return Burger()

    def test_init_bun_is_none(self, burger):
        assert burger.bun is None

    def test_init_ingredients_is_empty_list(self, burger):
        assert burger.ingredients == []

    def test_set_buns(self, burger):
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    @pytest.mark.parametrize("ing_type", [types.INGREDIENT_TYPE_SAUCE, types.INGREDIENT_TYPE_FILLING])
    def test_add_ingredient(self, burger, ing_type):
        mock_ing = Mock(**{"get_type.return_value": ing_type})
        burger.add_ingredient(mock_ing)
        assert burger.ingredients == [mock_ing]

    def test_remove_ingredient(self, burger):
        mock_1, mock_2, mock_3 = Mock(), Mock(), Mock()
        burger.ingredients = [mock_1, mock_2, mock_3]
        burger.remove_ingredient(1)
        assert burger.ingredients == [mock_1, mock_3]

    @pytest.mark.parametrize("start_idx, new_idx", [(0, 1), (1, 0)])
    def test_move_ingredient(self, burger, start_idx, new_idx):
        mock_1, mock_2, mock_3 = Mock(), Mock(), Mock()
        burger.ingredients = [mock_1, mock_2, mock_3]
        target = burger.ingredients[start_idx]
        burger.move_ingredient(start_idx, new_idx)
        assert burger.ingredients[new_idx] == target

    @pytest.mark.parametrize(
        "bun_price, ing_prices, expected_price",
        [
            (100.0, [100.0, 50.0], 350.0),
            (150.0, [], 300.0),
        ]
    )
    def test_get_price(self, burger, bun_price, ing_prices, expected_price):
        burger.set_buns(Mock(**{"get_price.return_value": bun_price}))
        burger.ingredients = [Mock(**{"get_price.return_value": price}) for price in ing_prices]
        assert burger.get_price() == expected_price

    @pytest.mark.parametrize(
        "bun_name, bun_price, ing_type, ing_name, ing_price, expected_total",
        [
            ("black bun", 100.0, types.INGREDIENT_TYPE_SAUCE, "hot sauce", 100.0, "300.0"),
            ("white bun", 150.0, types.INGREDIENT_TYPE_FILLING, "cutlet", 200.0, "500.0"),
        ]
    )
    def test_get_receipt(self, burger, bun_name, bun_price, ing_type, ing_name, ing_price, expected_total):
        mock_bun = Mock(**{"get_name.return_value": bun_name, "get_price.return_value": bun_price})
        mock_ing = Mock(**{
            "get_type.return_value": ing_type,
            "get_name.return_value": ing_name,
            "get_price.return_value": ing_price,
        })
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ing)

        expected_receipt = (
            f"(==== {bun_name} ====)\n"
            f"= {ing_type.lower()} {ing_name} =\n"
            f"(==== {bun_name} ====)\n\n"
            f"Price: {expected_total}"
        )
        assert burger.get_receipt() == expected_receipt
        