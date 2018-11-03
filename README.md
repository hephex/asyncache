# asyncache

Helpers to use cachetools with asyncio.

[![Build Status](https://www.travis-ci.org/hephex/asyncache.svg?branch=master)](https://www.travis-ci.org/hephex/asyncache)
[![Coverage Status](https://coveralls.io/repos/github/hephex/asyncache/badge.svg?branch=master)](https://coveralls.io/github/hephex/asyncache?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Example

```python
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
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


## Acknowledgments

* [cachetools](https://github.com/tkem/cachetools)
