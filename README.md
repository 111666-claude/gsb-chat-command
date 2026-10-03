# chat-command

聊天指令分发：别名解析、参数校验、权限与冷却，只用 Python 标准库。

```
python3 -m commands.cli --sample alias
python3 -m commands.cli --sample args
python3 -m commands.cli --sample rank
python3 -m commands.cli --sample cooldown
python3 -m commands.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **解析**：文本必须以 `/` 开头，否则 `error:format`；指令名与参数用空白分隔。
- **别名**：别名解析到主指令名，返回结果里用主名。
- **参数个数**：参数少于 `args_min` 或多于 `args_max` 返回 `error:args`，
  不执行、不进冷却。
- **权限**：调用者等级低于 `min_rank` 返回 `error:denied`，不执行、不进冷却。
- **冷却**：成功执行后该玩家这条指令进入 `cooldown_ms` 冷却，冷却期内返回
  `error:cooldown`；不同玩家、不同指令互不影响。
- **未知指令**：返回 `error:unknown`。
- **不变量**：失败调用不改变冷却计时；同一串调用重复执行结果相同。
- **查询代价**：执行一条指令不许扫描全部已注册指令，`scanned_count`
  不随指令数线性增长。
- **规模**：1 万条指令、每秒 10 万次调用，单次摊还 O(1)。

## 输出契约（不改格式）

```
result=..
second=..
scanned=..
```

## 目录

```
commands/core.py   解析、别名、权限与冷却
commands/cli.py    命令行入口
tests/             unittest 用例
```
