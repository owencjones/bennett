import pytest

from optool import validate_bnf_code, OPToolException_BNF_Code_was_invalid


class TestValidateBnfCode:

    def test_validates_correct_code(self) -> None:
        ...

    @pytest.mark.parametrize("code", [
        "A",                # Too short
        "040702",           # Partial, but valid, code
        "AABB00000AA00AA",  #Full, but invalid code
        "1304000H0AAAAAA4", #"Too long"
    ])
    def test_raises_correct_exception_for_incorrect_code(self, code: str) -> None:
        with pytest.raises(OPToolException_BNF_Code_was_invalid):
            validate_bnf_code(code) 

    def test_passes_with_valid_code(self) -> None:
        validate_bnf_code("1304000H0AAAAAA")

