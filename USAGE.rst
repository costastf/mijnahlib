=====
Usage
=====

To use mijnahlib in a project:

.. code-block:: python

    from mijnahlib import Server
    server=Server(AH_USERNAME, AH_PASSWORD)

    # add items to shopping cart by id
    server.shopping_cart.add_item_by_id('wi382975')

    # show shopping cart contents.
    print(server.shopping_cart.contents)