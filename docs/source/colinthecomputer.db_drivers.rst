colinthecomputer.db\_drivers package
====================================

Auto imported db drivers.
When importing the package, it will expose the available database drivers as a dictionary.

i.e:

.. code-block:: python

    import db_drivers
    driver = db_drivers['postgresql']


Adding a file named ``"duckguy_driver"`` to the pacakge 
will automaticaly expose the driver via ``db_drivers['duckguy']``.

A db_driver has ``savers``, ``getters`` attributes, which enable saving and acessing data.
i.e:

.. code-block:: python

    # in this example, driver.savers['character'] saves character information
    driver.savers['character'](name='roy', color='yellow', age='?')
    # saves data
    # in this example, driver.getters['character'] gets the existing characters in the db
    driver.getters['characters']()
    > ['roy']

The savers and getters are automatically collected, and must be written in ``savers.py`` and ``getters.py`` modules
and be named ``save_field`` and ``get_field`` respectively.

To support the working project, a driver must support the following savers (but can expose more savers):

.. method:: save_user(user_id, username, birthday, gender)

.. method:: save_pose(user_id, datetime, data)

.. method:: save_color_image(user_id, datetime, data)

.. method:: save_depth_image(user_id, datetime, data)

.. method:: save_feelings(user_id, datetime, data)


And the following getters:

.. method:: get_users()

.. method:: get_user_info(user_id)

.. method:: get_snapshot_exists(user_id, snapshot_id)

.. method:: get_snapshots(user_id)

.. method:: get_snapshot_info(snapshot_id)

.. method:: get_result(snapshot_id, result_name)

Submodules
----------

colinthecomputer.db\_drivers.postgresql\_driver module
------------------------------------------------------

Supports the above methods.

Uses postgresql for the implementation.
