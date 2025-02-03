from utils import formatAmountToString, formatAmountToFloat, formatTimestampToDateStr, formatDateStrToTimestamp


def test_formatAmountToString():
    assert formatAmountToString(100) == "100,00"
    assert formatAmountToString(-100) == "100,00"
    assert formatAmountToString(1.23) == "1,23"
    assert formatAmountToString(1.234) == "1,23"

def test_formatAmountToFloat():
    assert formatAmountToFloat("100,00") == 100.0
    assert formatAmountToFloat("-100,00") == -100.0
    assert formatAmountToFloat("1,23") == 1.23
    assert formatAmountToFloat("1,234") == 1.234

def test_formatTimestampToDateStr():
    assert formatTimestampToDateStr(1640995200) == "31/12/2021"
    assert formatTimestampToDateStr(1640995201) == "31/12/2021"
    assert formatTimestampToDateStr(1640995202) == "31/12/2021"

def test_formatDateStrToTimestamp():
    assert formatDateStrToTimestamp("31/12/2021") == 1640919600
    assert formatDateStrToTimestamp("31/12/2021") == 1640919600
    assert formatDateStrToTimestamp("31/12/2021") == 1640919600
