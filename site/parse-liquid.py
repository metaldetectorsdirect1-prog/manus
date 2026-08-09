#!/usr/bin/env python3
"""Parse every HIVOLT template with a real Liquid engine.

check-liquid.py enforces house rules and catches unbalanced blocks by counting
tags. This is stronger: python-liquid actually parses each template, so it
rejects malformed filters, bad operators, unterminated strings and tag-syntax
misuse that tag-counting cannot see.

Shopify-specific tags (form, paginate, schema, style, javascript, section,
render) are not in the base dialect, so they are registered here as
pass-through tags that still parse their bodies. A parse error is therefore a
genuine syntax fault in our code, not a dialect gap.

Run:  python3 site/parse-liquid.py [files...]
"""
import glob
import pathlib
import sys

from liquid import Environment
from liquid.ast import Node
from liquid.parser import get_parser
from liquid.tag import Tag
from liquid.token import TOKEN_EOF, TOKEN_EXPRESSION, TOKEN_TAG


class _BodyNode(Node):
    """Holds a parsed block body; renders it straight through."""

    __slots__ = ("block",)

    def __init__(self, token, block):
        super().__init__(token)
        self.block = block

    def render_to_output(self, context, buffer):
        return self.block.render(context, buffer)


class _EmptyNode(Node):
    __slots__ = ()

    def render_to_output(self, context, buffer):
        return False


def _block_tag(tag_name, end_name):
    """A Shopify block tag whose body must still parse."""

    class _T(Tag):
        name = tag_name
        end = end_name
        block = True

        def parse(self, stream):
            token = stream.eat(TOKEN_TAG)
            # drain the tag's own expression tokens; we don't evaluate them,
            # but they must be consumed or the block parser sees them as content
            # into_inner() lifts the tag's expression tokens off the outer
            # stream. We don't evaluate them — only the body must parse.
            stream.into_inner(tag=token)
            body = get_parser(self.env).parse_block(
                stream, frozenset((end_name, TOKEN_EOF))
            )
            stream.expect(TOKEN_TAG, value=end_name)
            return _BodyNode(token, body)

    _T.__name__ = f"{tag_name.title()}Tag"
    return _T


def _inline_tag(tag_name):
    class _T(Tag):
        name = tag_name
        block = False

        def parse(self, stream):
            token = stream.eat(TOKEN_TAG)
            # eat=False is the convention every built-in inline tag follows
            # (see liquid.builtin.tags.include_tag): the tag leaves the stream
            # ON its expression token and the enclosing block parser advances.
            # Consuming it here instead puts the outer stream one token ahead,
            # which is invisible at top level — EOF forgives it — and breaks
            # the moment the tag appears inside a block, where the parser then
            # reads the expression as the block's terminator and reports
            # "expected tag endunless, found end of expression".
            if stream.current.kind == TOKEN_EXPRESSION:
                stream.into_inner(tag=token, eat=False)
            return _EmptyNode(token)

    _T.__name__ = f"{tag_name.title()}Tag"
    return _T


def make_env():
    env = Environment()
    for name, end in (("form", "endform"),
                      ("paginate", "endpaginate"),
                      ("schema", "endschema"),
                      ("style", "endstyle"),
                      ("javascript", "endjavascript"),
                      ("stylesheet", "endstylesheet")):
        env.add_tag(_block_tag(name, end))
    for name in ("section", "sections", "render", "layout"):
        env.add_tag(_inline_tag(name))
    return env


# (source, should_parse). A harness that only ever says "ok" proves nothing —
# these run before the templates do, so a green report means the parser both
# accepts valid Shopify Liquid AND still rejects broken Liquid.
SELFTEST = [
    ("{% render 'x' %}", True),
    # The shape that exposed the eat=True bug: an inline pass-through tag
    # nested inside a block.
    ("{% unless a == 'b' %}{% render 'x' %}{% endunless %}", True),
    ("{% if a %}{% section 'y' %}{% endif %}", True),
    ("{% form 'customer', id: 'z' %}{% render 'x' %}{% endform %}", True),
    # Genuinely broken: unterminated block, unknown filter syntax, bad operator.
    ("{% unless a %}no end", False),
    ("{{ a | | b }}", False),
    ("{% if a =! b %}x{% endif %}", False),
]


def selftest(env):
    bad = 0
    for src, should_parse in SELFTEST:
        try:
            env.from_string(src)
            parsed = True
        except Exception:                             # noqa: BLE001
            parsed = False
        if parsed != should_parse:
            bad += 1
            want = "parse" if should_parse else "be rejected"
            print(f"SELFTEST FAILED — expected {want}: {src}")
    if bad:
        print(f"\nharness is unsound ({bad}/{len(SELFTEST)}); "
              f"template results below cannot be trusted")
    return bad


def main():
    env = make_env()
    if selftest(env):
        return 2
    paths = sys.argv[1:] or sorted(
        glob.glob("site/*.liquid") + glob.glob("site/theme/*.liquid"))
    bad = 0
    for p in paths:
        try:
            env.from_string(pathlib.Path(p).read_text())
            print(f"  ok  {p}")
        except Exception as e:                      # noqa: BLE001
            bad += 1
            print(f"FAIL  {p}\n      {type(e).__name__}: "
                  f"{str(e).replace(chr(10), ' ')[:170]}")
    print(f"\n{len(paths) - bad}/{len(paths)} templates parse cleanly")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
