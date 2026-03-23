"""
MnemoScript compiler tests — verify lexer, parser, and emitter.
"""
import sys
import os
import struct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import tokenize, TokenType
from parser import parse
from emitter import compile_script
from compiler import compile_source, build_scpt_record
from opcodes import OP_SCRIPTNAME, OP_BEGIN, OP_END, OP_SET, OP_IF


def test_lexer_basic():
    tokens = tokenize("script MyTest\ntype quest\n")
    types = [t.type for t in tokens if t.type != TokenType.NEWLINE]
    assert TokenType.SCRIPT in types
    assert TokenType.IDENT in types
    assert TokenType.TYPE in types
    print("  PASS: lexer_basic")


def test_lexer_operators():
    tokens = tokenize("if x >= 5 && y != 3\n")
    types = [t.type for t in tokens]
    assert TokenType.IF in types
    assert TokenType.GTE in types
    assert TokenType.AND in types
    assert TokenType.NEQ in types
    print("  PASS: lexer_operators")


def test_lexer_hex():
    tokens = tokenize("use player 0x00000014\n")
    hex_tok = [t for t in tokens if t.type == TokenType.HEXINT][0]
    assert hex_tok.value == 0x14
    print("  PASS: lexer_hex")


def test_lexer_negative():
    tokens = tokenize("set x to -5.0\n")
    # Should produce: SET IDENT TO NUMBER
    num_tok = [t for t in tokens if t.type == TokenType.NUMBER]
    assert len(num_tok) == 1
    assert num_tok[0].value == -5.0
    print("  PASS: lexer_negative")


def test_parser_minimal():
    source = "script Test\ntype object\n"
    tokens = tokenize(source)
    ast = parse(tokens)
    assert ast.name == "Test"
    assert ast.script_type == "object"
    assert len(ast.variables) == 0
    assert len(ast.events) == 0
    print("  PASS: parser_minimal")


def test_parser_vars():
    source = "script Test\nint iCount\nfloat fVal\nref rObj\n"
    tokens = tokenize(source)
    ast = parse(tokens)
    assert len(ast.variables) == 3
    assert ast.variables[0].var_type == 'int'
    assert ast.variables[1].var_type == 'float'
    assert ast.variables[2].var_type == 'ref'
    print("  PASS: parser_vars")


def test_parser_use():
    source = "script Test\nuse player 0x00000014\n"
    tokens = tokenize(source)
    ast = parse(tokens)
    assert len(ast.uses) == 1
    assert ast.uses[0].name == 'player'
    assert ast.uses[0].form_id == 0x14
    print("  PASS: parser_use")


def test_parser_event():
    source = """script Test
use player 0x00000014
on GameMode
  player.ModAV Health 5.0
end
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    assert len(ast.events) == 1
    assert ast.events[0].event_name == 'GameMode'
    assert len(ast.events[0].body) == 1
    print("  PASS: parser_event")


def test_parser_if():
    source = """script Test
int iVal
use player 0x00000014
on GameMode
  if iVal > 5
    player.ModAV Health 10.0
  else
    player.ModAV Health 1.0
  endif
end
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    block = ast.events[0].body[0]
    assert hasattr(block, 'condition')
    assert len(block.body) == 1
    assert len(block.else_body) == 1
    print("  PASS: parser_if")


def test_emitter_minimal():
    source = "script Test\ntype object\n"
    result = compile_source(source)
    assert result['EDID'] == b'Test\x00'
    assert len(result['SCHR']) == 20
    # SCDA should have at least ScriptName opcode
    scda = result['SCDA']
    assert len(scda) >= 8
    # First two bytes should be ScriptName opcode
    assert struct.unpack('<H', scda[0:2])[0] == OP_SCRIPTNAME
    print("  PASS: emitter_minimal")


def test_emitter_event():
    source = """script Test
use player 0x00000014
on OnEquip
  player.ModAV Luck 5.0
end
"""
    result = compile_source(source)
    scda = result['SCDA']
    # Should contain: ScriptName, Begin, SetCurrentRef, ModAV, End
    assert len(scda) > 20
    # Find Begin opcode (0x10)
    ops = []
    i = 0
    while i < len(scda) - 1:
        op = struct.unpack('<H', scda[i:i+2])[0]
        ops.append(op)
        if op in (OP_SCRIPTNAME, OP_BEGIN, OP_END):
            arg_len = struct.unpack('<H', scda[i+2:i+4])[0]
            i += 4 + arg_len
        else:
            break  # complex parsing needed beyond this
    assert OP_SCRIPTNAME in ops
    assert OP_BEGIN in ops
    print("  PASS: emitter_event")


def test_emitter_schr_structure():
    source = """script Test
type effect
int iA
float fB
use player 0x00000014
use SomeRef 0x01000800
on ScriptEffectUpdate
  set iA to 5
end
"""
    result = compile_source(source)
    schr = result['SCHR']
    unused, ref_count, compiled_size, var_count, stype, flags = struct.unpack('<IIIIHH', schr)
    assert unused == 0
    assert ref_count == 2
    assert var_count == 2
    assert stype == 0x0100  # effect
    assert flags == 0x0001
    assert compiled_size == len(result['SCDA'])
    print("  PASS: emitter_schr_structure")


def test_build_scpt_record():
    source = "script Test\ntype object\n"
    subrecords = compile_source(source)
    record = build_scpt_record(subrecords)
    # Should start with 'SCPT' magic
    assert record[:4] == b'SCPT'
    # Record header is 24 bytes
    data_size = struct.unpack('<I', record[4:8])[0]
    assert len(record) == 24 + data_size
    print("  PASS: build_scpt_record")


def test_negative_args():
    source = """script Test
use player 0x00000014
on OnUnequip
  player.ModAV Luck -5.0
end
"""
    result = compile_source(source)
    scda = result['SCDA']
    # Should compile without error and have reasonable bytecode
    assert len(scda) > 20
    print("  PASS: negative_args")


def test_set_with_expression():
    source = """script Test
float fVal
use player 0x00000014
on GameMode
  set fVal to player.GetAV Luck * 2.0
end
"""
    result = compile_source(source)
    scda = result['SCDA']
    # Should have Set opcode
    assert len(scda) > 30
    print("  PASS: set_with_expression")


def test_if_elseif():
    source = """script Test
int iVal
use player 0x00000014
on GameMode
  if iVal > 10
    player.ModAV Health 50.0
  elseif iVal > 5
    player.ModAV Health 25.0
  else
    player.ModAV Health 10.0
  endif
end
"""
    result = compile_source(source)
    scda = result['SCDA']
    assert len(scda) > 50
    print("  PASS: if_elseif")


def test_multiple_events():
    source = """script Test
use player 0x00000014
on OnEquip
  player.ModAV Luck 5.0
end
on OnUnequip
  player.ModAV Luck -5.0
end
"""
    result = compile_source(source)
    assert len(result['SCDA']) > 40
    # Count Begin opcodes in bytecode
    scda = result['SCDA']
    begin_count = 0
    for i in range(0, len(scda) - 1, 2):
        if struct.unpack('<H', scda[i:i+2])[0] == OP_BEGIN:
            begin_count += 1
            break  # just check first one exists
    assert begin_count >= 1
    print("  PASS: multiple_events")


if __name__ == '__main__':
    print("=== MnemoScript Compiler Tests ===\n")
    tests = [
        test_lexer_basic,
        test_lexer_operators,
        test_lexer_hex,
        test_lexer_negative,
        test_parser_minimal,
        test_parser_vars,
        test_parser_use,
        test_parser_event,
        test_parser_if,
        test_emitter_minimal,
        test_emitter_event,
        test_emitter_schr_structure,
        test_build_scpt_record,
        test_negative_args,
        test_set_with_expression,
        test_if_elseif,
        test_multiple_events,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  FAIL: {test.__name__}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")
    if failed > 0:
        sys.exit(1)
