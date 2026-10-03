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


if __name__ == "__main__":
    unittest.main()
