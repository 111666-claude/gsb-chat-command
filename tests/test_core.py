import unittest

from commands.core import Dispatcher


class BasicTest(unittest.TestCase):
    def test_text_without_slash_is_format_error(self):
        self.assertEqual(Dispatcher(0).run("p1", "hello", 0, 0), "error:format")

    def test_unknown_command(self):
        self.assertEqual(Dispatcher(0).run("p1", "/nope", 0, 0), "error:unknown")

    def test_registered_command_succeeds(self):
        world = Dispatcher(0)
        world.register("wave")
        self.assertEqual(world.run("p1", "/wave", 0, 0), "ok:wave")

    def test_aliases_table_starts_empty(self):
        self.assertEqual(Dispatcher(0).aliases, {})

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Dispatcher(0).scanned_count(), 0)


class AliasTest(unittest.TestCase):
    def test_alias_resolves_to_primary_name(self):
        world = Dispatcher(0)
        world.register("whisper", args_min=2, args_max=2, aliases=("w",))
        self.assertEqual(world.run("p1", "/w bob hi", 0, 0), "ok:whisper")

    def test_alias_shares_cooldown_with_primary(self):
        world = Dispatcher(5000)
        world.register("whisper", args_min=2, args_max=2, aliases=("w",))
        self.assertEqual(world.run("p1", "/w bob hi", 0, 0), "ok:whisper")
        self.assertEqual(world.run("p1", "/whisper bob hi", 0, 1),
                         "error:cooldown")

    def test_unknown_alias_still_unknown(self):
        world = Dispatcher(0)
        world.register("whisper", aliases=("w",))
        self.assertEqual(world.run("p1", "/ww", 0, 0), "error:unknown")


class ArgsTest(unittest.TestCase):
    def test_too_few_args(self):
        world = Dispatcher(0)
        world.register("whisper", args_min=2, args_max=2)
        self.assertEqual(world.run("p1", "/whisper bob", 0, 0), "error:args")

    def test_too_many_args(self):
        world = Dispatcher(0)
        world.register("whisper", args_min=2, args_max=2)
        self.assertEqual(world.run("p1", "/whisper a b c", 0, 0), "error:args")

    def test_arg_bounds_inclusive(self):
        world = Dispatcher(0)
        world.register("say", args_min=1, args_max=2)
        self.assertEqual(world.run("p1", "/say a", 0, 0), "ok:say")
        self.assertEqual(world.run("p1", "/say a b", 0, 1), "ok:say")

    def test_bad_args_do_not_start_cooldown(self):
        world = Dispatcher(5000)
        world.register("whisper", args_min=2, args_max=2)
        self.assertEqual(world.run("p1", "/whisper bob", 0, 0), "error:args")
        self.assertEqual(world.run("p1", "/whisper bob hi", 0, 1),
                         "ok:whisper")


class RankTest(unittest.TestCase):
    def test_low_rank_denied(self):
        world = Dispatcher(0)
        world.register("ban", args_min=1, args_max=1, min_rank=5)
        self.assertEqual(world.run("p1", "/ban bob", 1, 0), "error:denied")

    def test_sufficient_rank_allowed(self):
        world = Dispatcher(0)
        world.register("ban", args_min=1, args_max=1, min_rank=5)
        self.assertEqual(world.run("p1", "/ban bob", 5, 0), "ok:ban")
        self.assertEqual(world.run("p1", "/ban bob", 9, 1), "ok:ban")

    def test_denied_does_not_start_cooldown(self):
        world = Dispatcher(5000)
        world.register("ban", args_min=1, args_max=1, min_rank=5)
        self.assertEqual(world.run("p1", "/ban bob", 1, 0), "error:denied")
        self.assertEqual(world.run("p1", "/ban bob", 5, 1), "ok:ban")


class CooldownTest(unittest.TestCase):
    def test_second_call_within_cooldown(self):
        world = Dispatcher(5000)
        world.register("wave")
        self.assertEqual(world.run("p1", "/wave", 0, 0), "ok:wave")
        self.assertEqual(world.run("p1", "/wave", 0, 1), "error:cooldown")

    def test_call_after_cooldown_expires(self):
        world = Dispatcher(5000)
        world.register("wave")
        self.assertEqual(world.run("p1", "/wave", 0, 0), "ok:wave")
        self.assertEqual(world.run("p1", "/wave", 0, 5000), "ok:wave")

    def test_cooldown_is_per_player(self):
        world = Dispatcher(5000)
        world.register("wave")
        self.assertEqual(world.run("p1", "/wave", 0, 0), "ok:wave")
        self.assertEqual(world.run("p2", "/wave", 0, 1), "ok:wave")

    def test_cooldown_is_per_command(self):
        world = Dispatcher(5000)
        world.register("wave")
        world.register("dance")
        self.assertEqual(world.run("p1", "/wave", 0, 0), "ok:wave")
        self.assertEqual(world.run("p1", "/dance", 0, 1), "ok:dance")

    def test_cooldown_error_does_not_refresh_timer(self):
        world = Dispatcher(5000)
        world.register("wave")
        self.assertEqual(world.run("p1", "/wave", 0, 0), "ok:wave")
        self.assertEqual(world.run("p1", "/wave", 0, 4000), "error:cooldown")
        self.assertEqual(world.run("p1", "/wave", 0, 5000), "ok:wave")


class CostTest(unittest.TestCase):
    def test_scanned_does_not_grow_with_command_count(self):
        world = Dispatcher(0)
        for index in range(10000):
            world.register("c-%d" % index)
        for index in range(3000):
            world.run("p1", "/c-9999", 0, index)
        self.assertLessEqual(world.scanned_count(), 6000)

    def test_repeated_calls_are_deterministic(self):
        world = Dispatcher(0)
        world.register("wave")
        results = [world.run("p1", "/wave", 0, t) for t in range(100)]
        self.assertEqual(results, ["ok:wave"] * 100)


if __name__ == "__main__":
    unittest.main()
