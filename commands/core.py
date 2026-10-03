"""聊天指令分发：别名解析、参数校验、权限与冷却。

缺陷：别名不解析、参数个数不校验、权限不检查、冷却不生效、
每次执行扫描全部已注册指令。
"""


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
        self.scanned += len(self.commands)
        if not text.startswith("/"):
            return "error:format"
        parts = text[1:].split()
        if not parts:
            return "error:format"
        name = parts[0]
        if name not in self.commands:
            return "error:unknown"
        args = parts[1:]
        self.last_used[(player, name)] = now_ms
        return "ok:%s" % name

    def scanned_count(self):
        return self.scanned
