from correctionlib.JSONEncoder import dumps, json


def test_jsonencode():
    data = {
        "layer1": {
            "layer2_1": {
                "layer3_1": [
                    {"x": 1, "y": 7},
                    {"x": 0, "y": 4},
                    {"x": 5, "y": 3},
                    {"x": 6, "y": 9},
                    {"key": "foo", "value": 1},
                    {"key": "foo", "value": {k: v for v, k in enumerate("abcd")}},
                    {k: v for v, k in enumerate("ab")},
                    {k: v for v, k in enumerate("abc")},
                    {k: v for v, k in enumerate("abcd")},
                    {k: {k2: v2 for v2, k2 in enumerate("ab")} for k in "ab"},
                ],
                "layer3_2": "string",
                "layer3_3": [
                    {"x": 2, "y": 8, "z": 3},
                    {"x": 1, "y": 5, "z": 4},
                    {"x": 6, "y": 9, "z": 8},
                ],
            },
            "layer2_2": {
                "layer3_4": [
                    ["a", "b", "c"],
                    [c for c in "abcdefghijklmnopqrstuvwxyz"],
                    [c for c in "abcdefghijklmnopqrstuvwxyz123"],
                    [c for c in "abcdefghijklmnopqrstuvwxyz" * 2],
                    [
                        "this is short",
                        "very short",
                    ],
                    ["this is medium long", "verily, can you see?"],
                    ["this one is a bit longer,", "in order to find the edge..."],
                    [
                        "this",
                        "list of",
                        "strings",
                        "is a bit",
                        "longer",
                        "in order",
                        "to find",
                        "the edge",
                        "but the",
                        "words",
                        "are short",
                    ],
                    [
                        "this",
                        1,
                        2,
                        "list of",
                        45,
                        "also",
                        66,
                        "contains",
                        "some",
                        "numbers",
                        "for the",
                        100,
                        "heck of",
                        "it",
                        "see if",
                        "it splits",
                    ],
                    [
                        "this",
                        "list of strings is",
                        "a bit longer,",
                        "in order",
                        "to find the edge...",
                    ],
                    [
                        "this is a very, very long string to test line break",
                        "and this is another very long string",
                    ],
                ],
                "layer3_5": [
                    list(range(1, 10 + 1)),
                    list(range(1, 20 + 1)),
                    list(range(1, 24 + 1)),
                    list(range(1, 25 + 1)),
                    list(range(1, 26 + 1)),
                    list(range(1, 27 + 1)),
                    list(range(1, 30 + 1)),
                    list(range(1, 40 + 1)),
                    list(range(1, 50 + 1)),
                    list(range(1, 51 + 1)),
                    list(range(1, 52 + 1)),
                ],
                "layer3_6": list(range(1, 20 + 1)),
                "layer3_7": list(range(1, 40 + 1)),
                "layer3_8": [
                    {
                        "key": "this is short",
                        "value": "very short",
                    },
                    {
                        "key": "this is medium long",
                        "value": "verily, can you see?",
                    },
                    {
                        "key": "this is one is a bit longer",
                        "value": "to find the edge",
                    },
                    {
                        "key": "this is a very long string to test line break",
                        "value": "another very long string",
                    },
                ],
            },
        }
    }

    formatted = dumps(
        data,
        sort_keys=True,
        indent=2,
        maxlistlen=25,
        maxdictlen=3,
        breakbrackets=False,
    )

    retrieved = json.loads(formatted)

    expected = """\
{
  "layer1": {
    "layer2_1": {
      "layer3_1": [
        { "x": 1, "y": 7 },
        { "x": 0, "y": 4 },
        { "x": 5, "y": 3 },
        { "x": 6, "y": 9 },
        { "key": "foo", "value": 1 },
        { "key": "foo",
          "value": {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3
          }
        },
        { "a": 0, "b": 1 },
        { "a": 0, "b": 1, "c": 2 },
        { "a": 0,
          "b": 1,
          "c": 2,
          "d": 3
        },
        { "a": { "a": 0, "b": 1 },
          "b": { "a": 0, "b": 1 }
        }
      ],
      "layer3_2": "string",
      "layer3_3": [
        { "x": 2, "y": 8, "z": 3 },
        { "x": 1, "y": 5, "z": 4 },
        { "x": 6, "y": 9, "z": 8 }
      ]
    },
    "layer2_2": {
      "layer3_4": [
        [ "a", "b", "c" ],
        [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
          "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ],
        [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
          "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3"
        ],
        [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
          "s", "t", "u", "v", "w", "x", "y", "z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
          "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ],
        [ "this is short", "very short" ],
        [ "this is medium long", "verily, can you see?" ],
        [ "this one is a bit longer,",
          "in order to find the edge..."
        ],
        [ "this", "list of", "strings", "is a bit", "longer",
          "in order", "to find", "the edge", "but the", "words",
          "are short"
        ],
        [ "this", 1, 2, "list of", 45, "also", 66, "contains", "some",
          "numbers", "for the", 100, "heck of", "it", "see if",
          "it splits"
        ],
        [ "this",
          "list of strings is",
          "a bit longer,",
          "in order",
          "to find the edge..."
        ],
        [ "this is a very, very long string to test line break",
          "and this is another very long string"
        ]
      ],
      "layer3_5": [
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24 ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
          14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
        ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
          15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
        ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
          16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
        ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
          21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40
        ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
          26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50
        ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
          18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
          35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51
        ],
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
          19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
          37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52
        ]
      ],
      "layer3_6": [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ],
      "layer3_7": [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40
      ],
      "layer3_8": [
        { "key": "this is short", "value": "very short" },
        { "key": "this is medium long", "value": "verily, can you see?" },
        { "key": "this is one is a bit longer",
          "value": "to find the edge"
        },
        { "key": "this is a very long string to test line break",
          "value": "another very long string"
        }
      ]
    }
  }
}"""
    assert (
        formatted == expected
    ), f"Formatted does not match expected:\nExpected: {expected}\nFormatted: {formatted}"
    assert (
        retrieved == data
    ), f"Data before and after encoding do not match:\nBefore: {data}\nFormatted: {formatted}"
