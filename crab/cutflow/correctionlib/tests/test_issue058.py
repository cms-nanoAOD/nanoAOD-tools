import pytest

from correctionlib import schemav2 as schema


def test_categoryitem_coercion():
    x = schema.CategoryItem(key="30", value=1.0)
    assert x.key == "30"
    x = schema.CategoryItem(key=30, value=1.0)
    assert x.key == 30
    with pytest.raises(ValueError):
        x = schema.CategoryItem(key=30.0, value=1.0)
    with pytest.raises(ValueError):
        x = schema.CategoryItem(key=b"30", value=1.0)
    x = schema.CategoryItem(key="30xyz", value=1.0)
    assert x.key == "30xyz"


def test_cat_valid():
    with pytest.raises(ValueError):
        schema.Category(
            nodetype="category",
            input="x",
            content=[
                schema.CategoryItem(key="30xyz", value=1.0),
                schema.CategoryItem(key=30, value=1.0),
            ],
        )

    with pytest.raises(ValueError):
        schema.Category(
            nodetype="category",
            input="x",
            content=[
                schema.CategoryItem(key="30xyz", value=1.0),
                schema.CategoryItem(key="30xyz", value=1.0),
            ],
        )
