"""聊天指令分发：别名解析、参数校验、权限与冷却。"""


class Dispatcher:
    """聊天指令分发器。"""

    def __init__(self, cooldown_ms):
        self.cooldown_ms = cooldown_ms
        self.commands = {}
        self.aliases = {}
        self.last_used = {}
        self.scanned = 0

    def register(self, name, args_min=0, args_max=0, min_rank=0, aliases=()):
        self.commands[name] = {"name": name, "args_min": args_min,
                               "args_max": args_max, "min_rank": min_rank}
        for alias in aliases:
            self.aliases[alias] = name

    def run(self, player, text, rank, now_ms):
        """执行一条聊天指令，返回结果字符串。"""
        if not text.startswith("/"):
            return "error:format"
        parts = text[1:].split()
        if not parts:
            return "error:format"
        self.scanned += 1
        name = self.aliases.get(parts[0], parts[0])
        if name not in self.commands:
            return "error:unknown"
        command = self.commands[name]
        args = parts[1:]
        if not command["args_min"] <= len(args) <= command["args_max"]:
            return "error:args"
        if rank < command["min_rank"]:
            return "error:denied"
        key = (player, name)
        last = self.last_used.get(key)
        if last is not None and now_ms - last < self.cooldown_ms:
            return "error:cooldown"
        self.last_used[key] = now_ms
        return "ok:%s" % name

    def scanned_count(self):
        return self.scanned
