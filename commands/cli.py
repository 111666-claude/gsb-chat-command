"""命令行入口：跑聊天指令样例。"""

import argparse

from .core import Dispatcher


def build_parser():
    parser = argparse.ArgumentParser(prog="chat-command", description="聊天指令分发")
    parser.add_argument("--sample", default="alias",
                        help="alias / args / rank / cooldown / scan")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "alias":
        world = Dispatcher(cooldown_ms=0)
        world.register("whisper", args_min=2, args_max=2, aliases=("w",))
        print("result=%s" % world.run("p1", "/w bob hi", 0, 0))
    elif args.sample == "args":
        world = Dispatcher(cooldown_ms=0)
        world.register("whisper", args_min=2, args_max=2)
        print("result=%s" % world.run("p1", "/whisper bob", 0, 0))
    elif args.sample == "rank":
        world = Dispatcher(cooldown_ms=0)
        world.register("ban", args_min=1, args_max=1, min_rank=5)
        print("result=%s" % world.run("p1", "/ban bob", 1, 0))
    elif args.sample == "cooldown":
        world = Dispatcher(cooldown_ms=5000)
        world.register("wave", args_min=0, args_max=0)
        world.run("p1", "/wave", 0, 0)
        print("second=%s" % world.run("p1", "/wave", 0, 1))
    elif args.sample == "scan":
        world = Dispatcher(cooldown_ms=0)
        for index in range(3000):
            world.register("c-%d" % index, args_min=0, args_max=0)
        for index in range(3000):
            world.run("p1", "/c-2999", 0, index)
        print("scanned=%d" % world.scanned_count())
    else:
        raise SystemExit("需要 --sample alias|args|rank|cooldown|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
