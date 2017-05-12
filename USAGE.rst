=====
Usage
=====

To use mijnahlib in a project:

.. code-block:: python

    from mijnahlib import Server as AH
    ah=AH(AH_USERNAME, AH_PASSWORD)

    # add items to shopping cart by id
    ah.shopping_cart.add_item_by_id('wi382975')

    # add items to shopping cart by description
    ah.shopping_cart.add_item_by_description('milk')

    # show shopping cart contents.
    print(ah.shopping_cart.contents)

    # There are two types of items. Products and UnspecifiedProducts.
    # UnspecifiedProducts have much less attributes exposed since they are
    # generic. If accessed, those attributes return None and log a warning so
    # they can be used like the Product items.
    # show internal attributes of items in the cart
    for item in ah.shopping_cart.contents:
        print(item.description)
        print(item.measurement_unit)
        print(item.price)
        print(item.quantity)
        print(item.has_discount)
        print(item.brand)
        print(item.category)
        print(item.price_previously)
        print(item.id)

    # get a list of items with discount
    discounted_items = ah.shopping_cart.get_items_with_discount()

    # get info over the stores
    for store in ah.stores:
        print(store.address)
        print(store.telephone)
        print(store.id)
        print(store.latitude)
        print(store.longtitude)
        print(store.opening_times_today)
        print(store.opens_sunday)
        print(store.opens_evenings)
