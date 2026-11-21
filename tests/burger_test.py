from unittest.mock import Mock
import pytest
import praktikum.ingredient_types as types


class TestBurger:
    def test_set_buns(self, burger):
        mock_bun = Mock(**{"get_name.return_value": "black bun", "get_price.return_value": 100.0})
        burger.set_buns(mock_bun)
        assert "(==== black bun ====)" in burger.get_receipt()

    @pytest.mark.parametrize(
        "ing_type, ing_name",
        [
            (types.INGREDIENT_TYPE_SAUCE, "hot sauce"),
            (types.INGREDIENT_TYPE_FILLING, "cutlet"),
        ],
    )
    def test_add_ingredient(self, burger, ing_type, ing_name):
        burger.set_buns(Mock(**{"get_name.return_value": "black bun", "get_price.return_value": 100.0}))
        mock_ing = Mock(
            **{
                "get_type.return_value": ing_type,
                "get_name.return_value": ing_name,
                "get_price.return_value": 50.0,
            }
        )
        burger.add_ingredient(mock_ing)
        assert f"= {ing_type.lower()} {ing_name} =" in burger.get_receipt()

    def test_remove_ingredient(self, burger):
        burger.set_buns(Mock(**{"get_name.return_value": "black bun", "get_price.return_value": 100.0}))
        mock_1 = Mock(
            **{
                "get_type.return_value": types.INGREDIENT_TYPE_SAUCE,
                "get_name.return_value": "sauce 1",
                "get_price.return_value": 50.0,
            }
        )
        mock_2 = Mock(
            **{
                "get_type.return_value": types.INGREDIENT_TYPE_FILLING,
                "get_name.return_value": "cutlet 2",
                "get_price.return_value": 100.0,
            }
        )
        burger.add_ingredient(mock_1)
        burger.add_ingredient(mock_2)

        burger.remove_ingredient(0)
        assert "sauce 1" not in burger.get_receipt()

    def test_move_ingredient(self, burger):
        burger.set_buns(Mock(**{"get_name.return_value": "black bun", "get_price.return_value": 100.0}))
        mock_1 = Mock(
            **{
                "get_type.return_value": types.INGREDIENT_TYPE_SAUCE,
                "get_name.return_value": "sauce 1",
                "get_price.return_value": 50.0,
            }
        )
        mock_2 = Mock(
            **{
                "get_type.return_value": types.INGREDIENT_TYPE_FILLING,
                "get_name.return_value": "cutlet 2",
                "get_price.return_value": 100.0,
            }
        )
        burger.add_ingredient(mock_1)
        burger.add_ingredient(mock_2)

        burger.move_ingredient(0, 1)
        receipt = burger.get_receipt()
        assert receipt.index("cutlet 2") < receipt.index("sauce 1")

    @pytest.mark.parametrize(
        "bun_price, ing_prices, expected_price",
        [
            (100.0, [100.0, 50.0], 350.0),
            (150.0, [], 300.0),
        ],
    )
    def test_get_price(self, burger, bun_price, ing_prices, expected_price):
        burger.set_buns(Mock(**{"get_price.return_value": bun_price}))
        for price in ing_prices:
            burger.add_ingredient(Mock(**{"get_price.return_value": price}))
        assert burger.get_price() == expected_price

    @pytest.mark.parametrize(
        "bun_name, bun_price, ing_type, ing_name, ing_price, expected_total",
        [
            ("black bun", 100.0, types.INGREDIENT_TYPE_SAUCE, "hot sauce", 100.0, "300.0"),
            ("white bun", 150.0, types.INGREDIENT_TYPE_FILLING, "cutlet", 200.0, "500.0"),
        ],
    )
    def test_get_receipt(
        self, burger, bun_name, bun_price, ing_type, ing_name, ing_price, expected_total
    ):
        mock_bun = Mock(**{"get_name.return_value": bun_name, "get_price.return_value": bun_price})
        mock_ing = Mock(
            **{
                "get_type.return_value": ing_type,
                "get_name.return_value": ing_name,
                "get_price.return_value": ing_price,
            }
        )
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ing)

        expected_receipt = (
            f"(==== {bun_name} ====)\n"
            f"= {ing_type.lower()} {ing_name} =\n"
            f"(==== {bun_name} ====)\n\n"
            f"Price: {expected_total}"
        )
        assert burger.get_receipt() == expected_receipt
        