import json
import math
import platform

import pytest

import correctionlib._core as core
from correctionlib import schemav2 as schema


def wrap(*corrs):
    cset = schema.CorrectionSet(
        schema_version=schema.VERSION,
        corrections=list(corrs),
    )
    return core.CorrectionSet.from_string(cset.json())


def test_evaluator():
    with pytest.raises(RuntimeError):
        cset = core.CorrectionSet.from_string("{")

    with pytest.raises(RuntimeError):
        cset = core.CorrectionSet.from_string("{}")

    with pytest.raises(RuntimeError):
        cset = core.CorrectionSet.from_string('{"schema_version": "blah"}')

    with pytest.raises(RuntimeError):
        cset = core.CorrectionSet.from_string('{"schema_version": 2, "description": 3}')

    cset = core.CorrectionSet.from_string(
        '{"schema_version": 2, "description": "something", "corrections": []}'
    )
    assert cset.schema_version == 2
    assert cset.description == "something"

    cset = wrap(
        schema.Correction(
            name="test corr",
            version=2,
            inputs=[],
            output=schema.Variable(name="a scale", type="real"),
            data=1.234,
        )
    )
    assert set(cset) == {"test corr"}
    sf = cset["test corr"]
    assert sf.version == 2
    assert sf.description == ""

    with pytest.raises(RuntimeError):
        sf.evaluate(0, 1.2, 35.0, 0.01)

    assert sf.evaluate() == 1.234

    cset = wrap(
        schema.Correction(
            name="test corr",
            version=2,
            inputs=[
                schema.Variable(name="pt", type="real"),
                schema.Variable(name="syst", type="string"),
            ],
            output=schema.Variable(name="a scale", type="real"),
            data=schema.Binning.parse_obj(
                {
                    "nodetype": "binning",
                    "input": "pt",
                    "edges": [0, 20, 40, float("inf")],
                    "flow": "error",
                    "content": [
                        schema.Category.parse_obj(
                            {
                                "nodetype": "category",
                                "input": "syst",
                                "content": [
                                    {"key": "blah", "value": 1.1},
                                    {"key": "blah2", "value": 2.2},
                                ],
                            }
                        ),
                        schema.Category.parse_obj(
                            {
                                "nodetype": "category",
                                "input": "syst",
                                "content": [
                                    {"key": "blah2", "value": 1.3},
                                    {
                                        "key": "blah3",
                                        "value": {
                                            "nodetype": "formula",
                                            "expression": "0.25*x + exp([0])",
                                            "parser": "TFormula",
                                            "variables": ["pt"],
                                            "parameters": [3.1],
                                        },
                                    },
                                ],
                            }
                        ),
                        1.0,
                    ],
                }
            ),
        )
    )
    assert set(cset) == {"test corr"}
    sf = cset["test corr"]
    assert sf.version == 2
    assert sf.description == ""

    with pytest.raises(RuntimeError):
        # too many inputs
        sf.evaluate(0, 1.2, 35.0, 0.01)

    with pytest.raises(RuntimeError):
        # not enough inputs
        sf.evaluate(1.2)

    with pytest.raises(RuntimeError):
        # wrong type
        sf.evaluate(5)

    with pytest.raises(RuntimeError):
        # wrong type
        sf.evaluate("asdf")

    assert sf.evaluate(12.0, "blah") == 1.1
    # Do we need pytest.approx? Maybe not
    assert sf.evaluate(31.0, "blah3") == 0.25 * 31.0 + math.exp(3.1)

    with pytest.raises(RuntimeError):
        # underflow
        sf.evaluate(-1.0, "blah")

    assert sf.evaluate(1000.0, "blah") == 1.0


@pytest.mark.skipif(
    platform.architecture() in {("32bit", "ELF"), ("32bit", "")},
    reason="cibuildwheel tests fail while building i686 wheels due to floating point rounding differences of order 1e-16",
)
def test_tformula():
    def evaluate(expr, variables, parameters):
        cset = {
            "schema_version": 2,
            "corrections": [
                {
                    "name": "test",
                    "version": 1,
                    "inputs": [
                        {"name": vname, "type": "real"}
                        for vname, _ in zip("xyzt", variables)
                    ],
                    "output": {"name": "f", "type": "real"},
                    "data": {
                        "nodetype": "formula",
                        "expression": expr,
                        "parser": "TFormula",
                        "variables": [vname for vname, _ in zip("xyzt", variables)],
                        "parameters": parameters or None,
                    },
                }
            ],
        }
        schema.CorrectionSet.parse_obj(cset)
        corr = core.CorrectionSet.from_string(json.dumps(cset))["test"]
        return corr.evaluate(*variables)

    test_values = [1.0, 32.0, -3.0, 1550.0]
    for x in test_values:
        assert evaluate("23.*x", [x], []) == 23.0 * x
        assert evaluate("23.*log(max(x, 0.1))", [x], []) == 23.0 * math.log(max(x, 0.1))
        assert evaluate("2.2e3 + x", [x], []) == 2.2e3 + x
        assert evaluate("-2e-3 * x", [x], []) == -2e-3 * x

    assert evaluate("5", [], []) == 5.0
    assert evaluate("3+2", [], []) == 5.0
    assert evaluate(" 3 + 2 ", [], []) == 5.0
    assert evaluate("3-2", [], []) == 1.0
    assert evaluate("3*2", [], []) == 6.0
    assert evaluate("6/2", [], []) == 3.0
    assert evaluate("3^2", [], []) == 9.0
    assert evaluate("4*3^2", [], []) == 36.0
    assert evaluate("3^2*4", [], []) == 36.0
    assert (
        evaluate("1+2*3^4+5*2+6*2", [], []) == 1 + 2 * (3 * 3 * 3 * 3) + 5 * 2 + 6 * 2
    )
    assert (
        evaluate("1+3^4*2+5*2+6*2", [], []) == 1 + 2 * (3 * 3 * 3 * 3) + 5 * 2 + 6 * 2
    )
    assert evaluate("3<=2", [], []) == 0.0
    assert evaluate("2<=3", [], []) == 1.0
    assert evaluate("3<=3", [], []) == 1.0
    assert evaluate("3>=2", [], []) == 1.0
    assert evaluate("2>=3", [], []) == 0.0
    assert evaluate("3>=3", [], []) == 1.0
    assert evaluate("3>2", [], []) == 1.0
    assert evaluate("2>3", [], []) == 0.0
    assert evaluate("3>3", [], []) == 0.0
    assert evaluate("3<2", [], []) == 0.0
    assert evaluate("2<3", [], []) == 1.0
    assert evaluate("3<3", [], []) == 0.0
    assert evaluate("2==3", [], []) == 0.0
    assert evaluate("3==3", [], []) == 1.0
    assert evaluate("2!=3", [], []) == 1.0
    assert evaluate("3!=3", [], []) == 0.0
    assert evaluate("1+2*3", [], []) == 7.0
    assert evaluate("(1+2)*3", [], []) == 9.0
    assert evaluate("2*3+1", [], []) == 7.0
    assert evaluate("2*(3+1)", [], []) == 8.0
    assert evaluate("4/2*3", [], []) == 6.0
    assert evaluate("1-2+3", [], []) == 2.0
    assert evaluate("(1+2)-(3+4)", [], []) == -4.0
    assert evaluate("3/2*4+1", [], []) == 3.0 / 2.0 * 4.0 + 1
    assert evaluate("1+3/2*4", [], []) == 1 + 3.0 / 2.0 * 4.0
    assert evaluate("1+4*(3/2+5)", [], []) == 1 + 4 * (3.0 / 2.0 + 5.0)
    assert evaluate("1+2*3/4*5", [], []) == 1 + 2.0 * 3.0 / 4.0 * 5
    assert evaluate("1+2*3/(4+5)+6", [], []) == 1 + 2.0 * 3.0 / (4 + 5) + 6
    assert evaluate("100./3.*2+1", [], []) == 100.0 / 3.0 * 2.0 + 1
    assert evaluate("100./3.*(4-2)+2*(3+1)", [], []) == 100.0 / 3.0 * (4 - 2) + 2 * (
        3 + 1
    )
    assert evaluate("2*(3*4*5)/6", [], []) == 2 * (3 * 4 * 5) / 6
    assert (
        evaluate("2*(2.5*3*3.5)*(4*4.5*5)/6", [], [])
        == 2 * (2.5 * 3 * 3.5) * (4 * 4.5 * 5) / 6
    )
    assert evaluate("x", [3.0], []) == 3.0
    assert evaluate("-x", [3.0], []) == -3.0
    assert evaluate("y", [0.0, 3.0], []) == 3.0
    assert evaluate("z", [0.0, 0.0, 3.0], []) == 3.0
    assert evaluate("t", [0.0, 0.0, 0.0, 3.0], []) == 3.0
    assert evaluate("[0]", [], [3.0]) == 3.0
    with pytest.raises(RuntimeError):
        evaluate("[0] + 3.", [], [])
    assert evaluate("[1]", [], [0.0, 3.0]) == 3.0
    assert evaluate("[0]+[1]*3", [], [1.0, 3.0]) == 10.0
    assert evaluate("log(2)", [], []) == math.log(2.0)
    # assert evaluate("TMath::Log(2)", [], []) == math.log(2.)
    assert evaluate("log10(2)", [], []) == math.log10(2.0)
    assert evaluate("exp(2)", [], []) == math.exp(2.0)
    assert evaluate("pow(2,0.3)", [], []) == pow(2.0, 0.3)
    # assert evaluate("TMath::Power(2,0.3)", [], []) == pow(2., 0.3)
    assert evaluate("erf(2.)", [], []) == math.erf(2.0)
    # assert evaluate("TMath::Erf(2.)", [], []) == math.erf(2.)
    # assert evaluate("TMath::Landau(3.)", [], []) == None
    assert evaluate("max(2,1)", [], []) == 2.0
    assert evaluate("max(1,2)", [], []) == 2.0
    # assert evaluate("TMath::Max(2,1)", [], []) == 2.
    # assert evaluate("TMath::Max(1,2)", [], []) == 2.
    assert evaluate("cos(0.5)", [], []) == math.cos(0.5)
    # assert evaluate("TMath::Cos(0.5)", [], []) == math.cos(0.5)
    assert evaluate("sin(0.5)", [], []) == math.sin(0.5)
    # assert evaluate("TMath::Sin(0.5)", [], []) == math.sin(0.5)
    assert evaluate("tan(0.5)", [], []) == math.tan(0.5)
    # assert evaluate("TMath::Tan(0.5)", [], []) == math.tan(0.5)
    assert evaluate("acos(0.5)", [], []) == math.acos(0.5)
    # assert evaluate("TMath::ACos(0.5)", [], []) == math.acos(0.5)
    assert evaluate("asin(0.5)", [], []) == math.asin(0.5)
    # assert evaluate("TMath::ASin(0.5)", [], []) == math.asin(0.5)
    assert evaluate("atan(0.5)", [], []) == math.atan(0.5)
    # assert evaluate("TMath::ATan(0.5)", [], []) == math.atan(0.5)
    assert evaluate("atan2(-0.5, 0.5)", [], []) == math.atan2(-0.5, 0.5)
    # assert evaluate("TMath::ATan2(-0.5, 0.5)", [], []) == math.atan2(-0.5, 0.5)
    assert evaluate("cosh(0.5)", [], []) == math.cosh(0.5)
    # assert evaluate("TMath::CosH(0.5)", [], []) == math.cosh(0.5)
    assert evaluate("sinh(0.5)", [], []) == math.sinh(0.5)
    # assert evaluate("TMath::SinH(0.5)", [], []) == math.sinh(0.5)
    assert evaluate("tanh(0.5)", [], []) == math.tanh(0.5)
    # assert evaluate("TMath::TanH(0.5)", [], []) == math.tanh(0.5)
    assert evaluate("acosh(2.0)", [], []) == math.acosh(2.0)
    # assert evaluate("TMath::ACosH(2.0)", [], []) == math.acosh(2.)
    assert evaluate("asinh(2.0)", [], []) == math.asinh(2.0)
    # assert evaluate("TMath::ASinH(2.0)", [], []) == math.asinh(2.)
    assert evaluate("atanh(0.5)", [], []) == math.atanh(0.5)
    # assert evaluate("TMath::ATanH(0.5)", [], []) == math.atanh(0.5)
    assert evaluate("max(max(5,3),2)", [], []) == 5.0
    assert evaluate("max(2,max(5,3))", [], []) == 5.0
    assert (
        evaluate("-(-2.36997+0.413917*log(208))/208", [], [])
        == -(-2.36997 + 0.413917 * math.log(208.0)) / 208.0
    )

    for x in [1.0, 2.0, 3.0]:
        assert evaluate("2*erf(4*(x-1))", [x], []) == 2 * math.erf(4 * (x - 1))
        # assert evaluate("2*TMath::Landau(2*(x-1))", [x], []) == None

    v = [1.0, 4.0, 2.0, 0.5, 2.0, 1.0]
    for x in [1.0, 10.0, 100.0]:
        assert evaluate(
            "([0]+([1]/((log10(x)^2)+[2])))+([3]*exp(-([4]*((log10(x)-[5])*(log10(x)-[5])))))",
            [x],
            v,
        ) == (
            v[0]
            + (
                v[1]
                / (((math.log(x) / math.log(10)) * (math.log(x) / math.log(10))) + v[2])
            )
        ) + (
            v[3]
            * math.exp(
                -1.0
                * (
                    v[4]
                    * (
                        (math.log(x) / math.log(10.0) - v[5])
                        * (math.log(x) / math.log(10.0) - v[5])
                    )
                )
            )
        )

    v = [1.3, 4.0, 2.0]
    for x in [1.0, 10.0, 100.0]:
        assert evaluate("[0]*([1]+[2]*log(x))", [x], v) == v[0] * (
            v[1] + v[2] * math.log(x)
        )

    v = [1.3, 4.0, 1.7, 1.0]
    for x in [1.0, 10.0, 100.0]:
        assert evaluate("[0]+([1]/((log10(x)^[2])+[3]))", [x], v) == v[0] + (
            v[1] / ((math.pow(math.log(x) / math.log(10.0), v[2])) + v[3])
        )

    v = [1.3, 5.0, 10.0]
    for x in [1.0, 10.0, 100.0]:
        y, z = 1.0, 0.5
        assert evaluate(
            "max(0.0001,1-y*([0]+([1]*z)*(1+[2]*log(x)))/x)", [x, y, z], v
        ) == max(0.0001, 1 - y * (v[0] + (v[1] * z) * (1 + v[2] * math.log(x))) / x)

    for x in [0.1, 1.0, 10.0, 100.0]:
        assert (
            evaluate(
                "(-2.36997+0.413917*log(x))/x-(-2.36997+0.413917*log(208))/208", [x], []
            )
            == (-2.36997 + 0.413917 * math.log(x)) / x
            - (-2.36997 + 0.413917 * math.log(208)) / 208
        )
        assert evaluate(
            "max(0.,1.03091-0.051154*pow(x,-0.154227))-max(0.,1.03091-0.051154*pow(208.,-0.154227))",
            [x],
            [],
        ) == max(0.0, 1.03091 - 0.051154 * math.pow(x, -0.154227)) - max(
            0.0, 1.03091 - 0.051154 * math.pow(208.0, -0.154227)
        )

    v = [1.0, 4.0, 2.0, 0.5, 2.0, 1.0, 1.0, -1.0]
    for x in [0.1, 1.0, 10.0, 100.0]:
        assert evaluate("[2]*([3]+[4]*log(max([0],min([1],x))))", [x], v) == v[2] * (
            v[3] + v[4] * math.log(max(v[0], min(v[1], x)))
        )
        assert evaluate(
            "((x>=[6])*(([0]+([1]/((log10(x)^2)+[2])))+([3]*exp(-([4]*((log10(x)-[5])*(log10(x)-[5])))))))+((x<[6])*[7])",
            [x],
            v,
        ) == (
            (x >= v[6])
            * (
                (
                    v[0]
                    + (
                        v[1]
                        / (
                            (
                                (math.log(x) / math.log(10))
                                * (math.log(x) / math.log(10))
                            )
                            + v[2]
                        )
                    )
                )
                + (
                    v[3]
                    * math.exp(
                        -1.0
                        * (
                            v[4]
                            * (
                                (math.log(x) / math.log(10.0) - v[5])
                                * (math.log(x) / math.log(10.0) - v[5])
                            )
                        )
                    )
                )
            )
        ) + (
            (x < v[6]) * v[7]
        )
        assert evaluate(
            "(max(0.,1.03091-0.051154*pow(x,-0.154227))-max(0.,1.03091-0.051154*pow(208.,-0.154227)))+[7]*((-2.36997+0.413917*log(x))/x-(-2.36997+0.413917*log(208))/208)",
            [x],
            v,
        ) == (
            max(0.0, 1.03091 - 0.051154 * math.pow(x, -0.154227))
            - max(0.0, 1.03091 - 0.051154 * math.pow(208.0, -0.154227))
        ) + v[
            7
        ] * (
            (-2.36997 + 0.413917 * math.log(x)) / x
            - (-2.36997 + 0.413917 * math.log(208)) / 208
        )
        assert evaluate(
            "[2]*([3]+[4]*log(max([0],min([1],x))))*1./([5]+[6]*100./3.*(max(0.,1.03091-0.051154*pow(x,-0.154227))-max(0.,1.03091-0.051154*pow(208.,-0.154227)))+[7]*((-2.36997+0.413917*log(x))/x-(-2.36997+0.413917*log(208))/208))",
            [x],
            v,
        ) == v[2] * (v[3] + v[4] * math.log(max(v[0], min(v[1], x)))) * 1.0 / (
            v[5]
            + v[6]
            * 100.0
            / 3.0
            * (
                max(0.0, 1.03091 - 0.051154 * math.pow(x, -0.154227))
                - max(0.0, 1.03091 - 0.051154 * math.pow(208.0, -0.154227))
            )
            + v[7]
            * (
                (-2.36997 + 0.413917 * math.log(x)) / x
                - (-2.36997 + 0.413917 * math.log(208)) / 208
            )
        )

    assert (
        evaluate("100./3.*0.154227+2.36997", [], []) == 100.0 / 3.0 * 0.154227 + 2.36997
    )

    v = [0.88524, 28.4947, 4.89135, -19.0245, 0.0227809, -6.97308]
    for x in [10.0]:
        assert evaluate("exp([4]*(log10(x)-[5])*(log10(x)-[5]))", [x], v) == math.exp(
            v[4]
            * (math.log(x) / math.log(10) - v[5])
            * (math.log(x) / math.log(10) - v[5])
        )
        # the following shows a small numerical error: 1.2512381067949132 - 1.251238106794914 == -8e-16
        assert evaluate(
            "max(0.0001,[0]+[1]/(pow(log10(x),2)+[2])+[3]*exp(-1*([4]*((log10(x)-[5])*(log10(x)-[5])))))",
            [x],
            v,
        ) == pytest.approx(
            max(
                0.0001,
                v[0]
                + v[1] / (math.pow(math.log(x) / math.log(10), 2) + v[2])
                + v[3]
                * math.exp(
                    -1
                    * v[4]
                    * (math.log(x) / math.log(10) - v[5])
                    * (math.log(x) / math.log(10) - v[5])
                ),
            ),
            abs=1e-15,
        )
        assert evaluate(
            "max(0.0001,[0]+[1]/(pow(log10(x),2)+[2])+[3]*exp(-[4]*(log10(x)-[5])*(log10(x)-[5])))",
            [x],
            v,
        ) == max(
            0.0001,
            v[0]
            + v[1] / (math.pow(math.log(x) / math.log(10), 2) + v[2])
            + v[3]
            * math.exp(
                -v[4]
                * (math.log(x) / math.log(10) - v[5])
                * (math.log(x) / math.log(10) - v[5])
            ),
        )

    v = [0.945459, 2.78658, 1.65054, -48.1061, 0.0287239, -10.8759]
    for x in [425.92155818]:
        assert evaluate("-[4]*(log10(x)-[5])*(log10(x)-[5])", [x], v) == -v[4] * (
            math.log10(x) - v[5]
        ) * (math.log10(x) - v[5])

    v = [55, 2510, 0.997756, 1.000155, 0.979016, 0.001834, 0.982, -0.048, 1.250]
    x = 100.0
    assert evaluate(
        "[2]*([3]*([4]+[5]*log(max([0],min([1],x))))*1./([6]+[7]*100./3.*(max(0.,1.03091-0.051154*pow(x,-0.154227))-max(0.,1.03091-0.051154*pow(208.,-0.154227)))+[8]*((1+0.04432-1.304*pow(max(30.,min(6500.,x)),-0.4624)+(0+1.724*log(max(30.,min(6500.,x))))/max(30.,min(6500.,x)))-(1+0.04432-1.304*pow(208.,-0.4624)+(0+1.724*log(208.))/208.))))",
        [100.0],
        v,
    ) == v[2] * (
        v[3]
        * (v[4] + v[5] * math.log(max(v[0], min(v[1], x))))
        * 1.0
        / (
            v[6]
            + v[7]
            * 100.0
            / 3.0
            * (
                max(0.0, 1.03091 - 0.051154 * math.pow(x, -0.154227))
                - max(0.0, 1.03091 - 0.051154 * math.pow(208.0, -0.154227))
            )
            + v[8]
            * (
                (
                    1
                    + 0.04432
                    - 1.304 * math.pow(max(30.0, min(6500.0, x)), -0.4624)
                    + (0 + 1.724 * math.log(max(30.0, min(6500.0, x))))
                    / max(30.0, min(6500.0, x))
                )
                - (
                    1
                    + 0.04432
                    - 1.304 * math.pow(208.0, -0.4624)
                    + (0 + 1.724 * math.log(208.0)) / 208.0
                )
            )
        )
    )

    assert evaluate("(1+0.04432+(1.724+100.))-1", [], []) == 101.76832
    assert evaluate("(1+(1.724+100.)+0.04432)-1", [], []) == 101.76832
    assert evaluate("((1.724+100.)+1+0.04432)-1", [], []) == 101.76832
    # Note: was 0.06156 in reco::formulaEvaluator (float vs. double)
    assert evaluate("(1+0.04432+1.724/100.)-1", [], []) == 0.06155999999999984
    assert evaluate("(1+1.724/100.+0.04432)-1", [], []) == 0.06155999999999984
    assert evaluate("(1.724/100.+1+0.04432)-1", [], []) == 0.06155999999999984
    assert (
        evaluate("(1+0.04432+(1.724/100.))-1", [], [])
        == (1 + 0.04432 + (1.724 / 100.0)) - 1
    )
    assert (
        evaluate("(1+(1.724/100.)+0.04432)-1", [], [])
        == (1 + 0.04432 + (1.724 / 100.0)) - 1
    )
    assert (
        evaluate("((1.724/100.)+1+0.04432)-1", [], [])
        == (1 + 0.04432 + (1.724 / 100.0)) - 1
    )
    assert evaluate(
        "0.997756*(1.000155*(0.979016+0.001834*log(max(55.,min(2510.,100.))))*1./(0.982+-0.048*100./3.*(max(0.,1.03091-0.051154*pow(100.,-0.154227))-max(0.,1.03091-0.051154*pow(208.,-0.154227)))+1.250*((1+0.04432-1.304*pow(max(30.,min(6500.,100.)),-0.4624)+(0+1.724*log(max(30.,min(6500.,100.))))/max(30.,min(6500.,100.)))-(1+0.04432-1.304*pow(208.,-0.4624)+(0+1.724*log(208.))/208.))))",
        [],
        [],
    ) == 0.997756 * (
        1.000155
        * (0.979016 + 0.001834 * math.log(max(55.0, min(2510.0, 100.0))))
        * 1.0
        / (
            0.982
            + -0.048
            * 100.0
            / 3.0
            * (
                max(0.0, 1.03091 - 0.051154 * math.pow(100.0, -0.154227))
                - max(0.0, 1.03091 - 0.051154 * pow(208.0, -0.154227))
            )
            + 1.250
            * (
                (
                    1
                    + 0.04432
                    - 1.304 * math.pow(max(30.0, min(6500.0, 100.0)), -0.4624)
                    + (0 + 1.724 * math.log(max(30.0, min(6500.0, 100.0))))
                    / max(30.0, min(6500.0, 100.0))
                )
                - (
                    1
                    + 0.04432
                    - 1.304 * math.pow(208.0, -0.4624)
                    + (0 + 1.724 * math.log(208.0)) / 208.0
                )
            )
        )
    )

    v = [0.006467, 0.02519, 77.08]
    for x in [100.0]:
        assert evaluate("[0]+[1]*exp(-x/[2])", [x], v) == v[0] + v[1] * math.exp(
            -x / v[2]
        )

    v = [1.4, 0.453645, -0.015665]
    x, y, z = 157.2, 0.5, 23.2
    assert evaluate(
        "max(0.0001,1-y/x*([1]*(z-[0])*(1+[2]*log(x/30.))))", [x, y, z], v
    ) == max(0.0001, 1 - y / x * (v[1] * (z - v[0]) * (1 + v[2] * math.log(x / 30.0))))

    v = [1.4, 0.453645, -0.015665]
    x, y, z = 157.2, 0.5, 23.2
    assert evaluate(
        "max(0.0001,1-y*[1]*(z-[0])*(1+[2]*log(x/30.))/x)", [x, y, z], v
    ) == max(0.0001, 1 - y / x * (v[1] * (z - v[0]) * (1 + v[2] * math.log(x / 30.0))))

    v = [1.4, 0.453645, -0.015665]
    x, y, z = 157.2, 0.5, 23.2
    assert evaluate(
        "max(0.0001,1-y*([1]*(z-[0])*(1+[2]*log(x/30.)))/x)", [x, y, z], v
    ) == max(0.0001, 1 - y * (v[1] * (z - v[0]) * (1 + v[2] * math.log(x / 30.0))) / x)

    v = [1.326, 0.4209, 0.02223, -0.6704]
    x = 100.0
    assert evaluate(
        "sqrt([0]*abs([0])/(x*x)+[1]*[1]*pow(x,[3])+[2]*[2])", [x], v
    ) == math.sqrt(
        v[0] * abs(v[0]) / (x * x) + v[1] * v[1] * math.pow(x, v[3]) + v[2] * v[2]
    )

    v = [2.3, 0.20, 0.009]
    x = 100.0
    assert evaluate("sqrt([0]*[0]/(x*x)+[1]*[1]/x+[2]*[2])", [x], v) == math.sqrt(
        v[0] * v[0] / (x * x) + v[1] * v[1] / x + v[2] * v[2]
    )

    v = [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0]
    for x in [224.0, 225.0, 226.0]:
        assert evaluate(
            "([0]+[1]*x+[2]*x^2)*(x<225)+([0]+[1]*225+[2]*225^2+[3]*(x-225)+[4]*(x-225)^2+[5]*(x-225)^3)*(x>225)",
            [x],
            v,
        ) == (v[0] + v[1] * x + v[2] * (x * x)) * (x < 225) + (
            v[0]
            + v[1] * 225
            + v[2] * (225 * 225)
            + v[3] * (x - 225)
            + v[4] * ((x - 225) * (x - 225))
            + v[5] * ((x - 225) * (x - 225) * (x - 225))
        ) * (
            x > 225
        )

    with pytest.raises(RuntimeError):
        evaluate("doesNotExist(2)", [], [])
    with pytest.raises(RuntimeError):
        evaluate("doesNotExist(2) + abs(-1)", [], [])
    with pytest.raises(RuntimeError):
        evaluate("abs(-1) + doesNotExist(2)", [], [])
    with pytest.raises(RuntimeError):
        evaluate("abs(-1) + ( 5 * doesNotExist(2))", [], [])
    with pytest.raises(RuntimeError):
        evaluate("( 5 * doesNotExist(2)) + abs(-1)", [], [])
    with pytest.raises(RuntimeError):
        evaluate("TMath::Exp(2)", [], [])
    with pytest.raises(RuntimeError):
        evaluate("1 + 2 * 3 + 5 * doesNotExist(2) ", [], [])

    # issue 40
    v = [
        -1.04614304,
        29.09992313,
        8.512377293,
        -2.773443989,
        4.913533881,
        2.780409657,
        0.2951616046,
        19.72651073,
        1.841689324,
        2.013020835,
    ]
    for x in [5.0, 15.0]:
        # would be nice to check output as well
        evaluate(
            "max(0.0001,((x<10)*([9]))+((x>=10)*([0]+([1]/(pow(log10(x),2)+[2]))+([3]*exp(-([4]*((log10(x)-[5])*(log10(x)-[5])))))+([6]*exp(-([7]*((log10(x)-[8])*(log10(x)-[8]))))))))",
            [x],
            v,
        )


def test_category():
    def make_cat(items, default):
        cset = wrap(
            schema.Correction(
                name="test",
                version=2,
                inputs=[
                    schema.Variable(
                        name="cat",
                        type="string" if isinstance(next(iter(items)), str) else "int",
                    )
                ],
                output=schema.Variable(name="a scale", type="real"),
                data=schema.Category(
                    nodetype="category",
                    input="cat",
                    content=[
                        {"key": key, "value": value} for key, value in items.items()
                    ],
                    default=default,
                ),
            )
        )
        return cset["test"]

    corr = make_cat({"blah": 1.2}, None)
    assert corr.evaluate("blah") == 1.2
    with pytest.raises(IndexError):
        corr.evaluate("asdf")

    corr = make_cat({"blah": 1.2}, 0.1)
    assert corr.evaluate("blah") == 1.2
    assert corr.evaluate("asdf") == 0.1
    assert corr.evaluate("def") == 0.1

    corr = make_cat({0: 1.2, 13: 1.4}, None)
    assert corr.evaluate(0) == 1.2
    assert corr.evaluate(13) == 1.4
    with pytest.raises(IndexError):
        corr.evaluate(1)
    with pytest.raises(RuntimeError):
        corr.evaluate("one")


def test_binning():
    def binning(flow):
        cset = wrap(
            schema.Correction(
                name="test",
                version=2,
                inputs=[schema.Variable(name="x", type="real")],
                output=schema.Variable(name="a scale", type="real"),
                data=schema.Binning(
                    nodetype="binning",
                    input="x",
                    edges=[0.0, 1.0, 3.0],
                    content=[1.0, 2.0],
                    flow=flow,
                ),
            )
        )
        return cset["test"]

    corr = binning(flow="error")
    with pytest.raises(RuntimeError):
        corr.evaluate(-1.0)
    assert corr.evaluate(0.0) == 1.0
    assert corr.evaluate(0.2) == 1.0
    assert corr.evaluate(1.0) == 2.0
    with pytest.raises(RuntimeError):
        corr.evaluate(3.0)

    corr = binning(flow="clamp")
    assert corr.evaluate(-1.0) == 1.0
    assert corr.evaluate(1.0) == 2.0
    assert corr.evaluate(3.0) == 2.0
    assert corr.evaluate(3000.0) == 2.0

    corr = binning(flow=42.0)
    assert corr.evaluate(-1.0) == 42.0
    assert corr.evaluate(0.0) == 1.0
    assert corr.evaluate(1.0) == 2.0
    assert corr.evaluate(2.9) == 2.0
    assert corr.evaluate(3.0) == 42.0

    def multibinning(flow):
        cset = wrap(
            schema.Correction(
                name="test",
                version=2,
                inputs=[
                    schema.Variable(name="x", type="real"),
                    schema.Variable(name="y", type="real"),
                ],
                output=schema.Variable(name="a scale", type="real"),
                data=schema.MultiBinning(
                    nodetype="multibinning",
                    inputs=["x", "y"],
                    edges=[
                        [0.0, 1.0, 3.0],
                        [10.0, 20.0, 30.0, 40.0],
                    ],
                    content=[float(i) for i in range(2 * 3)],
                    flow=flow,
                ),
            )
        )
        return cset["test"]

    corr = multibinning(flow="error")
    with pytest.raises(RuntimeError):
        corr.evaluate(0.0, 5.0)
    with pytest.raises(RuntimeError):
        corr.evaluate(-1.0, 5.0)
    assert corr.evaluate(0.0, 10.0) == 0.0
    assert corr.evaluate(0.0, 20.0) == 1.0
    assert corr.evaluate(0.0, 30.0) == 2.0
    with pytest.raises(RuntimeError):
        corr.evaluate(0.0, 40.0)
    assert corr.evaluate(1.0, 10.0) == 3.0
    assert corr.evaluate(1.0, 20.0) == 4.0
    assert corr.evaluate(1.0, 30.0) == 5.0
    with pytest.raises(RuntimeError):
        corr.evaluate(2.0, 5.0)

    corr = multibinning(flow="clamp")
    assert corr.evaluate(-1.0, 5.0) == 0.0
    assert corr.evaluate(-1.0, 25.0) == 1.0
    assert corr.evaluate(-1.0, 35.0) == 2.0
    assert corr.evaluate(-1.0, 45.0) == 2.0
    assert corr.evaluate(0.0, 45.0) == 2.0
    assert corr.evaluate(2.0, 45.0) == 5.0
    assert corr.evaluate(3.0, 45.0) == 5.0
    assert corr.evaluate(3.0, 35.0) == 5.0
    assert corr.evaluate(3.0, 25.0) == 4.0
    assert corr.evaluate(3.0, 15.0) == 3.0
    assert corr.evaluate(3.0, 5.0) == 3.0
    assert corr.evaluate(0.0, 5.0) == 0.0

    corr = multibinning(flow=42.0)
    assert corr.evaluate(-1.0, 5.0) == 42.0
    assert corr.evaluate(2.0, 45.0) == 42.0
    assert corr.evaluate(3.0, 5.0) == 42.0

    corr = multibinning(
        flow=schema.Formula(
            nodetype="formula",
            expression="2.*x + 5.*y",
            parser="TFormula",
            variables=["x", "y"],
        )
    )
    assert corr.evaluate(-1.0, 5.0) == 2.0 * -1 + 5.0 * 5.0
    assert corr.evaluate(0.0, 10.0) == 0.0


def test_formularef():
    cset = wrap(
        schema.Correction(
            name="reftest",
            version=2,
            inputs=[
                schema.Variable(name="x", type="real"),
            ],
            output=schema.Variable(name="a scale", type="real"),
            generic_formulas=[
                schema.Formula(
                    nodetype="formula",
                    expression="[0] + [1]*x",
                    parser="TFormula",
                    variables=["x"],
                ),
            ],
            data=schema.Binning(
                nodetype="binning",
                input="x",
                edges=[0, 1, 2, 3],
                content=[
                    schema.FormulaRef(
                        nodetype="formularef", index=0, parameters=[0.1, 0.2]
                    ),
                    schema.FormulaRef(
                        nodetype="formularef", index=0, parameters=[1.1, -0.2]
                    ),
                    schema.FormulaRef(
                        nodetype="formularef", index=0, parameters=[3.1, 0.5]
                    ),
                ],
                flow="error",
            ),
        )
    )
    corr = cset["reftest"]
    assert corr.evaluate(0.5) == 0.1 + 0.2 * 0.5
    assert corr.evaluate(1.5) == 1.1 + -0.2 * 1.5
    assert corr.evaluate(2.5) == 3.1 + 0.5 * 2.5


def test_transform():
    cset = wrap(
        schema.Correction(
            name="test",
            version=2,
            inputs=[
                schema.Variable(name="torewrite", type="real"),
            ],
            output=schema.Variable(name="a scale", type="real"),
            data=schema.Transform(
                nodetype="transform",
                input="torewrite",
                rule=0.1,
                content=schema.Formula(
                    nodetype="formula",
                    expression="x",
                    parser="TFormula",
                    variables=["torewrite"],
                ),
            ),
        )
    )
    corr = cset["test"]
    assert corr.evaluate(0.5) == 0.1
    assert corr.evaluate(1.5) == 0.1

    cset = wrap(
        schema.Correction(
            name="test",
            version=2,
            inputs=[
                schema.Variable(name="torewrite", type="int"),
            ],
            output=schema.Variable(name="a scale", type="real"),
            data=schema.Transform(
                nodetype="transform",
                input="torewrite",
                rule=schema.Category(
                    nodetype="category",
                    input="torewrite",
                    content=[
                        {"key": 0, "value": 0},
                        {"key": 1, "value": 4},
                        {"key": 2, "value": 0},
                        {"key": 9, "value": 3.000001},
                        {"key": 10, "value": 2.999999},
                    ],
                ),
                content=schema.Category(
                    nodetype="category",
                    input="torewrite",
                    content=[
                        {"key": 0, "value": 0.0},
                        {"key": 3, "value": 0.1},
                        {"key": 4, "value": 0.2},
                    ],
                ),
            ),
        )
    )
    corr = cset["test"]
    assert corr.evaluate(0) == 0.0
    assert corr.evaluate(1) == 0.2
    assert corr.evaluate(2) == 0.0
    with pytest.raises(IndexError):
        corr.evaluate(3)
    assert corr.evaluate(9) == 0.1
    assert corr.evaluate(10) == 0.1
