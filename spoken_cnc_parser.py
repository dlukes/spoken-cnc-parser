import re

from pypeg2 import Enum, Keyword, K, List, attr, contiguous, csl, some, parse
from pypeg2.xmlast import thing2xml


class Token(str):
    grammar = re.compile(r"\w+|[\-\+\?&]|[\.@]{1,2}")


class UnclearSpan(List):
    grammar = "(", some(Token), ")"


class OverlapSpan(List):
    grammar = "[", some([Token, UnclearSpan]), "]"


class ParaType(Keyword):
    # NOTE: ``regex`` defines the regular expression to scan when searching for valid input; the
    # default is "\w+", but we need to exclude "_", which is used as separator
    regex = re.compile(r"[A-Z]{2}")
    # TODO: add remaining para types, perhaps in a config file...?
    grammar = Enum(K("SM"), K("CP"), K("MZ"))


class ParaTypes(List):
    grammar = csl(ParaType, separator="_")


class ParaSpan(List):
    grammar = "<", attr("type", contiguous(ParaTypes)), some([Token, UnclearSpan, OverlapSpan]), ">"


class Transcription(List):
    grammar = some([Token, UnclearSpan, OverlapSpan, ParaSpan])


t = parse("běžela @ magda @@ kaňonem <SM_CP srážela .. [banány & (velkým)]> rádiem ?", Transcription)
print(thing2xml(t, pretty=True).decode())
print(t[5].type)
