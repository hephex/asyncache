asyncache
#########

Helpers to use cachetools with asyncio.

.. image:: https://img.shields.io/pypi/v/asyncache
   :target: https://pypi.org/project/asyncache/
   :alt: Latest PyPI version

.. image:: https://travis-ci.org/hephex/asyncache.svg?branch=master
    :target: https://travis-ci.org/hephex/asyncache

.. image:: https://coveralls.io/repos/github/hephex/asyncache/badge.svg?branch=master
    :target: https://coveralls.io/github/hephex/asyncache?branch=master

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

Installation
============

asyncache is available from PyPI_ and can be installed by running::

  pip install asyncache

Example
=======

.. code-block:: python

    from asyncache import cached
    from cachetools import TTLCache
    
    pool = ...
    
    @cached(TTLCache(1024, 60))
    async def get_username(user_id):
        rec = await pool.fetchrow(
            """
            SELECT
                username
            FROM
                users
            WHERE
                id = $1
            """,
            user_id,
        )
        return rec and rec["username"]

License
=======

This project is licensed under the MIT License - see the LICENSE_ file for details.


Acknowledgments
===============

- `cachetools`_


.. _LICENSE: LICENSE
.. _cachetools: https://github.com/tkem/cachetools
.. _PyPI: https://pypi.org/project/asyncache/


