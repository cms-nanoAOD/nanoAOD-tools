"""A custom JSON encoder for corrections
Author: Izaak Neutelings (March 2021)
Description: Write JSON with indents more compactly by collapsing some lists and dictionaries
Instructions: Print or write JSON dictionary 'data' as
  import JSONEncoder
  print(JSONEncoder.write(data,sort_keys=True,indent=2,maxlistlen=25,maxdictlen=3,breakbrackets=False))
  print(JSONEncoder.dumps(data,sort_keys=True,indent=2,maxlistlen=25,maxdictlen=3,breakbrackets=False))
Adapted from:
  https://stackoverflow.com/questions/16264515/json-dumps-custom-formatting
"""
import gzip
import json
import math
from typing import Any, List, Type

import pydantic


def write(data: Any, fname: str, **kwargs: Any) -> None:
    """Help function to quickly write JSON file formatted by JSONEncoder."""
    if fname.endswith(".json.gz"):
        with gzip.open(fname, "wt") as fout:
            fout.write(dumps(data, **kwargs))
    else:
        with open(fname, "w") as fout:
            fout.write(dumps(data, **kwargs))


def dumps(data: Any, sort_keys: bool = False, **kwargs: Any) -> str:
    """Help function to quickly dump dictionary formatted by JSONEncoder."""
    if isinstance(data, pydantic.BaseModel):  # for pydantic
        return data.json(cls=JSONEncoder, exclude_unset=True, **kwargs)
    else:  # for standard data structures
        return json.dumps(data, cls=JSONEncoder, sort_keys=sort_keys, **kwargs)


class JSONEncoder(json.JSONEncoder):
    """
    Encoder to make correctionlib JSON more compact, but still readable:
    - keep list of primitives (int, float, str) on one line,
      or split over several if the length is longer than a given maxlen
    - do not break line for short dictionary if all values are primitive
    - do not break line after bracket for first key of dictionary,
      unless itself nested in dictionary
    """

    def __init__(self, *args: Any, **kwargs: Any):
        if kwargs.get("indent", None) is None:
            kwargs["indent"] = 2
        # maximum of primitive elements per list, before breaking lines
        self.maxlistlen = kwargs.pop("maxlistlen", 25)
        # maximum of primitive elements per dict, before breaking lines
        self.maxdictlen = kwargs.pop("maxdictlen", 2)
        # maximum length of strings in short dict, before breaking lines
        self.maxstrlen = kwargs.pop("maxstrlen", 2 * self.maxlistlen)
        # break after opening bracket
        self.breakbrackets = kwargs.pop("breakbrackets", False)
        super().__init__(*args, **kwargs)
        self._indent = 0  # current indent
        self.parent = type(None)  # type of parent for recursive use

    def encode(self, obj: Any) -> str:
        grandparent = self.parent  # type: Type[Any]
        self.parent = type(obj)
        retval = ""
        if isinstance(obj, (list, tuple)):  # lists, tuples
            output = []
            if all(
                isinstance(x, (int, float, str)) for x in obj
            ):  # list of primitives only
                strlen = sum(len(s) for s in obj if isinstance(s, str))
                indent_str = " " * (self._indent + self.indent)
                if strlen > self.maxstrlen and any(
                    len(s) > 3 for s in obj if isinstance(s, str)
                ):
                    obj = [
                        json.dumps(s) for s in obj
                    ]  # convert everything into a string
                    if any(
                        len(s) > self.maxstrlen / 4 for s in obj
                    ):  # break list of long strings into multiple lines
                        output = obj
                    else:  # group strings into several lines
                        line = []  # type: List[str]
                        nchars = 0
                        for item in obj:
                            if len(line) == 0 or nchars + len(item) < self.maxstrlen:
                                line.append(item)
                                nchars += len(item)
                            else:  # new line
                                output.append(", ".join(line))
                                line = [item]
                                nchars = len(item)
                        if line:
                            output.append(", ".join(line))
                elif len(obj) <= self.maxlistlen:  # write short list on one line
                    for item in obj:
                        output.append(json.dumps(item))
                    retval = "[ " + ", ".join(output) + " ]"
                else:  # break long list into multiple lines
                    nlines = math.ceil(
                        len(obj) / float(self.maxlistlen)
                    )  # number of lines
                    maxlen = int(
                        math.ceil(len(obj) / nlines)
                    )  # divide evenly over nlines
                    for i in range(0, nlines):
                        line = []
                        for item in obj[i * maxlen : (i + 1) * maxlen]:
                            line.append(json.dumps(item))
                        if line:
                            output.append(", ".join(line))
                if not retval:
                    lines = (",\n" + indent_str).join(output)  # lines between brackets
                    if (
                        grandparent == dict or self.breakbrackets
                    ):  # break first line after opening bracket
                        retval = (
                            "[\n" + indent_str + lines + "\n" + " " * self._indent + "]"
                        )
                    else:  # do not break first line
                        retval = (
                            "["
                            + " " * (self.indent - 1)
                            + lines
                            + "\n"
                            + " " * self._indent
                            + "]"
                        )
            else:  # list of lists, tuples, dictionaries
                self._indent += self.indent
                indent_str = " " * self._indent
                for item in obj:
                    output.append(indent_str + self.encode(item))
                self._indent -= self.indent
                indent_str = " " * self._indent
                retval = "[\n" + ",\n".join(output) + "\n" + indent_str + "]"
        elif isinstance(obj, dict):  # dictionaries
            output = []
            if (
                len(obj) <= self.maxdictlen
                and all(isinstance(obj[k], (int, float, str)) for k in obj)
                and sum(len(k) + len(obj[k]) for k in obj if isinstance(obj[k], str))
                <= self.maxstrlen
            ):  # write short dict on one line
                retval = (
                    "{ "
                    + ", ".join(json.dumps(k) + ": " + self.encode(obj[k]) for k in obj)
                    + " }"
                )
            else:  # break long dict into multiple line
                self._indent += self.indent
                indent_str = " " * self._indent
                first = (
                    grandparent not in (type(None), dict) and not self.breakbrackets
                )  # break after opening brace
                for key, value in obj.items():
                    valstr = self.encode(value)
                    if (
                        first and "\n" not in valstr
                    ):  # no break between opening brace and first key
                        row = " " * (self.indent - 1) + json.dumps(key) + ": " + valstr
                    else:  # break before key
                        row = "\n" + indent_str + json.dumps(key) + ": " + valstr
                    output.append(row)
                    first = False
                self._indent -= self.indent
                indent_str = " " * self._indent
                retval = "{" + ",".join(output) + "\n" + indent_str + "}"
        else:  # use default formatting
            retval = json.dumps(obj)
        self.parent = grandparent
        return retval
