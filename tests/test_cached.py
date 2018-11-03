import asyncio
import functools
import unittest

from asyncache import cached

import cachetools


def sync(func):
    """
    Helper to force an function/method to run synchronously.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return wrapped


class SyncMixin:
    def cache(self):
        raise NotImplementedError

    def func(self, *args, **kwargs):
        if hasattr(self, "count"):
            self.count += 1
        else:
            self.count = 0
        return self.count

    def test_decorator(self):
        cache = self.cache()
        wrapper = cached(cache)(self.func)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.func)

        self.assertEqual(wrapper(0), 0)
        self.assertEqual(len(cache), 1)
        self.assertIn(cachetools.keys.hashkey(0), cache)
        self.assertNotIn(cachetools.keys.hashkey(1), cache)
        self.assertNotIn(cachetools.keys.hashkey(1.0), cache)

        self.assertEqual(wrapper(1), 1)
        self.assertEqual(len(cache), 2)
        self.assertIn(cachetools.keys.hashkey(0), cache)
        self.assertIn(cachetools.keys.hashkey(1), cache)
        self.assertIn(cachetools.keys.hashkey(1.0), cache)

        self.assertEqual(wrapper(1), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual(wrapper(1.0), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual(wrapper(1.0), 1)
        self.assertEqual(len(cache), 2)

    def test_decorator_typed(self):
        cache = self.cache()
        key = cachetools.keys.typedkey
        wrapper = cached(cache, key=key)(self.func)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.func)

        self.assertEqual(wrapper(0), 0)
        self.assertEqual(len(cache), 1)
        self.assertIn(cachetools.keys.typedkey(0), cache)
        self.assertNotIn(cachetools.keys.typedkey(1), cache)
        self.assertNotIn(cachetools.keys.typedkey(1.0), cache)

        self.assertEqual(wrapper(1), 1)
        self.assertEqual(len(cache), 2)
        self.assertIn(cachetools.keys.typedkey(0), cache)
        self.assertIn(cachetools.keys.typedkey(1), cache)
        self.assertNotIn(cachetools.keys.typedkey(1.0), cache)

        self.assertEqual(wrapper(1), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual(wrapper(1.0), 2)
        self.assertEqual(len(cache), 3)
        self.assertIn(cachetools.keys.typedkey(0), cache)
        self.assertIn(cachetools.keys.typedkey(1), cache)
        self.assertIn(cachetools.keys.typedkey(1.0), cache)

        self.assertEqual(wrapper(1.0), 2)
        self.assertEqual(len(cache), 3)

    def test_decorator_lock(self):
        class Lock(object):

            count = 0

            def __enter__(self):
                Lock.count += 1

            def __exit__(self, *exc):
                pass

        cache = self.cache()
        wrapper = cached(cache, lock=Lock())(self.func)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.func)
        self.assertEqual(wrapper(0), 0)
        self.assertEqual(Lock.count, 2)
        self.assertEqual(wrapper(1), 1)
        self.assertEqual(Lock.count, 4)
        self.assertEqual(wrapper(1), 1)
        self.assertEqual(Lock.count, 5)


class AsyncMixin:
    def cache(self):
        raise NotImplementedError

    async def coro(self, *args, **kwargs):
        if hasattr(self, "count"):
            self.count += 1
        else:
            self.count = 0

        await asyncio.sleep(0)

        return self.count

    @sync
    async def test_decorator_async(self):
        cache = self.cache()
        wrapper = cached(cache)(self.coro)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.coro)

        self.assertEqual((await wrapper(0)), 0)
        self.assertEqual(len(cache), 1)
        self.assertIn(cachetools.keys.hashkey(0), cache)
        self.assertNotIn(cachetools.keys.hashkey(1), cache)
        self.assertNotIn(cachetools.keys.hashkey(1.0), cache)

        self.assertEqual((await wrapper(1)), 1)
        self.assertEqual(len(cache), 2)
        self.assertIn(cachetools.keys.hashkey(0), cache)
        self.assertIn(cachetools.keys.hashkey(1), cache)
        self.assertIn(cachetools.keys.hashkey(1.0), cache)

        self.assertEqual((await wrapper(1)), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual((await wrapper(1.0)), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual((await wrapper(1.0)), 1)
        self.assertEqual(len(cache), 2)

    @sync
    async def test_decorator_typed_async(self):
        cache = self.cache()
        key = cachetools.keys.typedkey
        wrapper = cached(cache, key=key)(self.coro)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.coro)

        self.assertEqual((await wrapper(0)), 0)
        self.assertEqual(len(cache), 1)
        self.assertIn(cachetools.keys.typedkey(0), cache)
        self.assertNotIn(cachetools.keys.typedkey(1), cache)
        self.assertNotIn(cachetools.keys.typedkey(1.0), cache)

        self.assertEqual((await wrapper(1)), 1)
        self.assertEqual(len(cache), 2)
        self.assertIn(cachetools.keys.typedkey(0), cache)
        self.assertIn(cachetools.keys.typedkey(1), cache)
        self.assertNotIn(cachetools.keys.typedkey(1.0), cache)

        self.assertEqual((await wrapper(1)), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual((await wrapper(1.0)), 2)
        self.assertEqual(len(cache), 3)
        self.assertIn(cachetools.keys.typedkey(0), cache)
        self.assertIn(cachetools.keys.typedkey(1), cache)
        self.assertIn(cachetools.keys.typedkey(1.0), cache)

        self.assertEqual((await wrapper(1.0)), 2)
        self.assertEqual(len(cache), 3)

    @sync
    async def test_decorator_lock_async(self):
        class Lock(object):

            count = 0

            async def __aenter__(self):
                Lock.count += 1

            async def __aexit__(self, *exc):
                pass

        cache = self.cache()
        wrapper = cached(cache, lock=Lock())(self.coro)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.coro)
        self.assertEqual((await wrapper(0)), 0)
        self.assertEqual(Lock.count, 2)
        self.assertEqual((await wrapper(1)), 1)
        self.assertEqual(Lock.count, 4)
        self.assertEqual((await wrapper(1)), 1)
        self.assertEqual(Lock.count, 5)


class DictWrapperTest(unittest.TestCase, SyncMixin, AsyncMixin):
    def cache(self):
        return dict()


class LFUTest(unittest.TestCase, SyncMixin, AsyncMixin):
    def cache(self):
        return cachetools.LFUCache(10)


class LRUTest(unittest.TestCase, SyncMixin, AsyncMixin):
    def cache(self):
        return cachetools.LRUCache(10)


class RRTest(unittest.TestCase, SyncMixin, AsyncMixin):
    def cache(self):
        return cachetools.RRCache(10)


class TTLTest(unittest.TestCase, SyncMixin, AsyncMixin):
    def cache(self):
        return cachetools.TTLCache(maxsize=10, ttl=10.0)
