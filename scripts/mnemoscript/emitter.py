"""
MnemoScript Bytecode Emitter — compiles AST to SCPT record subrecords.

Output: dict with keys 'EDID', 'SCHR', 'SCDA', 'SCTX', 'SLSD_SCVR', 'SCRO'
Each value is raw bytes ready for ESP injection.
"""
from __future__ import annotations
import struct
from typing import Dict, List, Optional, Union
from parser import (Script, VarDecl, UseDecl, EventBlock, Stmt,
                    SetStmt, CallStmt, IfBlock, ReturnStmt,
                    Expr, IntLiteral, FloatLiteral, VarRef,
                    FuncCall, BinOp, UnaryOp)
from opcodes import (OP_BEGIN, OP_END, OP_SHORT, OP_FLOAT, OP_SET,
                     OP_IF, OP_ELSE, OP_ELSEIF, OP_SETCURRENTREF,
                     OP_SCRIPTNAME, OP_RETURN, OP_REF,
                     resolve_function, resolve_actor_value, resolve_event,
                     FUNCTION_REGISTRY)


class EmitError(Exception):
    pass


class BytecodeEmitter:
    """Compiles a parsed Script AST into SCPT subrecord data."""

    def __init__(self, script: Script, source_text: str = ''):
        self.script = script
        self.source_text = source_text

        # Variable name → (index, type)
        self.var_map: Dict[str, tuple] = {}
        # Reference name → 1-based SCRO index
        self.ref_map: Dict[str, int] = {}
        # SCRO FormIDs in order
        self.scro_list: List[int] = []
        # Custom opcode overrides
        self.custom_opcodes: Dict[str, int] = {}

        # Bytecode output buffer
        self.code = bytearray()

    def emit(self) -> dict:
        """Compile the script and return all SCPT subrecords."""
        self._build_tables()
        self._emit_script()
        return self._build_subrecords()

    def _build_tables(self):
        """Build variable and reference lookup tables."""
        # Variables — assigned indices in declaration order
        for i, var in enumerate(self.script.variables):
            var.index = i
            self.var_map[var.name.lower()] = (i, var.var_type)

        # References — 1-based indexing for SCRO
        for use in self.script.uses:
            idx = len(self.scro_list) + 1
            self.ref_map[use.name.lower()] = idx
            self.scro_list.append(use.form_id)

        # Custom opcodes
        for op in self.script.opcodes:
            self.custom_opcodes[op.name.lower()] = op.opcode

    def _w16(self, val: int):
        self.code += struct.pack('<H', val & 0xFFFF)

    def _w32(self, val: int):
        self.code += struct.pack('<I', val & 0xFFFFFFFF)

    def _w8(self, val: int):
        self.code += struct.pack('<B', val & 0xFF)

    def _wdouble(self, val: float):
        self.code += struct.pack('<d', val)

    def _resolve_func(self, name: str) -> int:
        """Resolve function name to opcode."""
        lower = name.lower()
        if lower in self.custom_opcodes:
            return self.custom_opcodes[lower]
        op = resolve_function(lower)
        if op is None:
            raise EmitError(f"Unknown function: {name}")
        return op

    def _resolve_ref(self, name: str) -> int:
        """Resolve reference name to 1-based SCRO index."""
        lower = name.lower()
        if lower in self.ref_map:
            return self.ref_map[lower]
        # Check if it's a local ref variable
        if lower in self.var_map:
            return 0  # handled differently
        raise EmitError(f"Unknown reference: {name}. Add a 'use {name} 0xFormID' declaration.")

    def _resolve_var(self, name: str) -> tuple:
        """Resolve variable name to (index, type)."""
        lower = name.lower()
        if lower in self.var_map:
            return self.var_map[lower]
        raise EmitError(f"Unknown variable: {name}")

    # --- Top-level emission ---

    def _emit_script(self):
        """Emit the full bytecode stream."""
        # ScriptName opcode
        self._w16(OP_SCRIPTNAME)
        self._w16(4)  # argLen
        self._w32(0)  # unused

        # Variable declarations (in order)
        for var in self.script.variables:
            if var.var_type == 'int':
                self._w16(OP_SHORT)
            elif var.var_type == 'float':
                self._w16(OP_FLOAT)
            elif var.var_type == 'ref':
                self._w16(OP_REF)
            # argLen = 0 for declarations in bytecode
            self._w16(0)

        # Event blocks
        for event in self.script.events:
            self._emit_event_block(event)

    def _emit_event_block(self, event: EventBlock):
        """Emit a Begin...End block."""
        event_opcode = resolve_event(event.event_name)
        if event_opcode is None:
            raise EmitError(f"Unknown event: {event.event_name}")

        # Begin header
        self._w16(OP_BEGIN)

        # We need to know blockLen before we emit the body.
        # Strategy: emit body to a temp buffer, measure it, then splice.
        begin_args_pos = len(self.code)

        # Placeholder: argLen(2) + paramCount(2) + eventOpcode(2) + blockLen(4)
        self._w16(0)  # argLen — will patch
        self._w16(0)  # paramCount (0 for most events)
        self._w16(event_opcode)
        block_len_pos = len(self.code)
        self._w32(0)  # blockLen — will patch

        body_start = len(self.code)

        # Emit body statements
        for stmt in event.body:
            self._emit_stmt(stmt)

        body_end = len(self.code)
        block_len = body_end - body_start

        # Patch blockLen
        struct.pack_into('<I', self.code, block_len_pos, block_len)
        # Patch argLen = paramCount(2) + eventOpcode(2) + blockLen(4) = 8
        struct.pack_into('<H', self.code, begin_args_pos, 8)

        # End
        self._w16(OP_END)
        self._w16(0)

    def _emit_stmt(self, stmt: Stmt):
        """Emit a single statement."""
        if isinstance(stmt, SetStmt):
            self._emit_set(stmt)
        elif isinstance(stmt, CallStmt):
            self._emit_call(stmt)
        elif isinstance(stmt, IfBlock):
            self._emit_if(stmt)
        elif isinstance(stmt, ReturnStmt):
            self._w16(OP_RETURN)
            self._w16(0)
        else:
            raise EmitError(f"Unknown statement type: {type(stmt)}")

    def _emit_set(self, stmt: SetStmt):
        """Emit: set varName to expr"""
        var_idx, var_type = self._resolve_var(stmt.target)

        self._w16(OP_SET)

        # Build the expression bytes first
        expr_bytes = self._compile_expr(stmt.expr)

        # argLen = var_ref(3) + exprLen(2) + expression
        var_marker = 0x66 if var_type in ('float', 'ref') else 0x73
        arg_len = 3 + 2 + len(expr_bytes)

        self._w16(arg_len)
        self._w8(var_marker)
        self._w16(var_idx)
        self._w16(len(expr_bytes))
        self.code += expr_bytes

    def _emit_call(self, stmt: CallStmt):
        """Emit a standalone function call."""
        call = stmt.call
        opcode = self._resolve_func(call.func_name)

        # If called on a reference, emit SetCurrentRef prefix
        if call.ref_name:
            ref_lower = call.ref_name.lower()
            if ref_lower in self.var_map:
                # ref variable — emit differently
                var_idx, _ = self.var_map[ref_lower]
                self._w16(OP_SETCURRENTREF)
                self._w16(var_idx)
            else:
                ref_idx = self._resolve_ref(call.ref_name)
                self._w16(OP_SETCURRENTREF)
                self._w16(ref_idx)

        # Emit function opcode + args
        arg_bytes = self._compile_call_args(call)
        self._w16(opcode)
        self._w16(len(arg_bytes))
        if arg_bytes:
            self.code += arg_bytes

    def _emit_if(self, stmt: IfBlock):
        """Emit if/elseif/else/endif chain with jump patching."""
        # Strategy: emit each branch, track positions for jump patching.
        # Jump offsets count "operations" (4-byte instruction units) not bytes.
        # For simplicity in v0.1, we use byte offsets and accept the approximation.
        # Real GECK counts "number of opcodes to skip" — we'll refine later.

        # IF
        expr_bytes = self._compile_expr(stmt.condition)
        self._w16(OP_IF)
        if_args_pos = len(self.code)
        self._w16(0)  # argLen — patch later
        jump_pos = len(self.code)
        self._w16(0)  # jumpOps — patch later
        self._w16(len(expr_bytes))
        self.code += expr_bytes
        # Patch argLen
        arg_len = 2 + 2 + len(expr_bytes)  # jumpOps + exprLen + expr
        struct.pack_into('<H', self.code, if_args_pos, arg_len)

        if_body_start = len(self.code)
        for s in stmt.body:
            self._emit_stmt(s)
        if_body_end = len(self.code)

        # We need to patch the If's jumpOps to skip past the body
        # For now, use byte count / 4 as approximate opcode count
        jump_bytes = if_body_end - if_body_start

        # If there's an else or elseif, the if-body needs to jump past the else too
        # We'll need a second pass. For v0.1, use a simple approach:
        # Each branch emits an Else/ElseIf with its own jump target.

        # ELSEIF blocks
        elseif_jump_patches = []
        for elif_cond, elif_body in stmt.elseif_blocks:
            # The previous branch's jump target should land here
            # But first, emit an Else-style jump (to skip remaining branches)
            # Actually, GECK uses ElseIf opcode directly
            else_jump_pos = len(self.code)
            # Emit else jump to skip past the whole chain (patch later)
            self._w16(OP_ELSE)
            self._w16(2)
            elif_chain_jump = len(self.code)
            self._w16(0)  # patch later
            elseif_jump_patches.append(elif_chain_jump)

            # Now patch previous if/elseif jump to land HERE
            branch_bytes = len(self.code) - if_body_end
            total_jump = jump_bytes + branch_bytes
            struct.pack_into('<H', self.code, jump_pos, total_jump // 4)

            # Emit ElseIf
            elif_expr_bytes = self._compile_expr(elif_cond)
            self._w16(OP_ELSEIF)
            elif_args_pos = len(self.code)
            self._w16(0)  # argLen
            jump_pos = len(self.code)
            self._w16(0)  # jumpOps
            self._w16(len(elif_expr_bytes))
            self.code += elif_expr_bytes
            elif_arg_len = 2 + 2 + len(elif_expr_bytes)
            struct.pack_into('<H', self.code, elif_args_pos, elif_arg_len)

            elif_body_start = len(self.code)
            for s in elif_body:
                self._emit_stmt(s)
            jump_bytes = len(self.code) - elif_body_start
            if_body_end = len(self.code)

        # ELSE block
        if stmt.else_body:
            else_start = len(self.code)
            self._w16(OP_ELSE)
            self._w16(2)
            else_chain_jump = len(self.code)
            self._w16(0)  # patch later
            elseif_jump_patches.append(else_chain_jump)

            branch_bytes = len(self.code) - if_body_end
            total_jump = jump_bytes + branch_bytes
            struct.pack_into('<H', self.code, jump_pos, total_jump // 4)

            else_body_start = len(self.code)
            for s in stmt.else_body:
                self._emit_stmt(s)

            # Patch all else/elseif chain jumps to point to end
            for patch_pos in elseif_jump_patches:
                chain_jump = (len(self.code) - patch_pos - 2) // 4
                struct.pack_into('<H', self.code, patch_pos, chain_jump)
        else:
            # No else — patch the last if/elseif jump
            remaining = len(self.code) - if_body_end
            total_jump = jump_bytes + remaining
            struct.pack_into('<H', self.code, jump_pos, total_jump // 4)

            # Patch all chain jumps
            for patch_pos in elseif_jump_patches:
                chain_jump = (len(self.code) - patch_pos - 2) // 4
                struct.pack_into('<H', self.code, patch_pos, chain_jump)

    # --- Expression compilation (RPN) ---

    def _compile_expr(self, expr: Expr) -> bytearray:
        """Compile an expression to RPN bytecode."""
        buf = bytearray()
        self._expr_to_rpn(expr, buf)
        return buf

    def _expr_to_rpn(self, expr: Expr, buf: bytearray):
        """Recursively emit RPN tokens for an expression."""
        if isinstance(expr, IntLiteral):
            buf += b'\x20'  # push separator
            buf += b'\x6E'  # 'n' = int constant
            buf += struct.pack('<i', expr.value)

        elif isinstance(expr, FloatLiteral):
            buf += b'\x20'  # push separator
            buf += b'\x7A'  # 'z' = double constant
            buf += struct.pack('<d', expr.value)

        elif isinstance(expr, VarRef):
            lower = expr.name.lower()
            if lower in self.var_map:
                idx, vtype = self.var_map[lower]
                buf += b'\x20'  # push separator
                marker = 0x66 if vtype in ('float', 'ref') else 0x73
                buf += bytes([marker])
                buf += struct.pack('<H', idx)
            else:
                raise EmitError(f"Unknown variable in expression: {expr.name}")

        elif isinstance(expr, FuncCall):
            # Emit reference prefix if needed
            if expr.ref_name:
                ref_lower = expr.ref_name.lower()
                if ref_lower in self.var_map:
                    # ref variable
                    idx, _ = self.var_map[ref_lower]
                    buf += b'\x72'
                    buf += struct.pack('<H', idx)
                else:
                    ref_idx = self._resolve_ref(expr.ref_name)
                    buf += b'\x72'
                    buf += struct.pack('<H', ref_idx)

            # Function call token
            opcode = self._resolve_func(expr.func_name)
            param_bytes = self._compile_func_params(expr)
            buf += b'\x58'  # 'X' = function call
            buf += struct.pack('<H', opcode)
            buf += struct.pack('<H', len(param_bytes))
            if param_bytes:
                # param count prefix
                buf += param_bytes

        elif isinstance(expr, BinOp):
            self._expr_to_rpn(expr.left, buf)
            self._expr_to_rpn(expr.right, buf)
            buf += b'\x20'  # separator before operator
            buf += self._encode_operator(expr.op)

        elif isinstance(expr, UnaryOp):
            self._expr_to_rpn(expr.operand, buf)
            buf += b'\x7E'  # unary negation

        else:
            raise EmitError(f"Cannot compile expression: {type(expr)}")

    def _encode_operator(self, op: str) -> bytes:
        """Encode an operator as ASCII bytes."""
        mapping = {
            '+':  b'+',
            '-':  b'-',
            '*':  b'*',
            '/':  b'/',
            '%':  b'%',
            '==': b'==',
            '!=': b'!=',
            '<':  b'<',
            '<=': b'<=',
            '>':  b'>',
            '>=': b'>=',
            '&&': b'&&',
            '||': b'||',
        }
        if op not in mapping:
            raise EmitError(f"Unknown operator: {op}")
        return mapping[op]

    def _compile_call_args(self, call: FuncCall) -> bytearray:
        """Compile function call arguments for standalone calls."""
        if not call.args:
            return bytearray()

        buf = bytearray()
        # Param count
        buf += struct.pack('<H', len(call.args))

        for arg in call.args:
            if isinstance(arg, str):
                # Could be an actor value name
                av = resolve_actor_value(arg)
                if av is not None:
                    buf += struct.pack('<H', av)
                else:
                    # Treat as a reference name
                    lower = arg.lower()
                    if lower in self.ref_map:
                        buf += struct.pack('<H', self.ref_map[lower])
                    elif lower in self.var_map:
                        idx, _ = self.var_map[lower]
                        buf += struct.pack('<H', idx)
                    else:
                        raise EmitError(f"Cannot resolve argument: {arg}")
            elif isinstance(arg, IntLiteral):
                buf += struct.pack('<i', arg.value)
            elif isinstance(arg, FloatLiteral):
                buf += struct.pack('<d', arg.value)
            else:
                raise EmitError(f"Unknown arg type: {type(arg)}")

        return buf

    def _compile_func_params(self, call: FuncCall) -> bytearray:
        """Compile function parameters for in-expression calls."""
        if not call.args:
            return bytearray()

        buf = bytearray()
        buf += struct.pack('<H', len(call.args))

        for arg in call.args:
            if isinstance(arg, str):
                av = resolve_actor_value(arg)
                if av is not None:
                    buf += struct.pack('<H', av)
                else:
                    lower = arg.lower()
                    if lower in self.ref_map:
                        buf += struct.pack('<H', self.ref_map[lower])
                    elif lower in self.var_map:
                        idx, _ = self.var_map[lower]
                        buf += struct.pack('<H', idx)
                    else:
                        raise EmitError(f"Cannot resolve param: {arg}")
            elif isinstance(arg, IntLiteral):
                buf += struct.pack('<i', arg.value)
            elif isinstance(arg, FloatLiteral):
                buf += struct.pack('<d', arg.value)
        return buf

    # --- Build final subrecords ---

    def _build_subrecords(self) -> dict:
        """Package compiled data into SCPT subrecords."""
        edid = self.script.name.encode('ascii') + b'\x00'

        # SCHR
        type_map = {'object': 0x0000, 'quest': 0x0001, 'effect': 0x0100}
        script_type = type_map.get(self.script.script_type, 0x0000)

        schr = struct.pack('<IIIIHH',
            0,                          # unused (4 bytes)
            len(self.scro_list),        # refCount (4 bytes)
            len(self.code),             # compiledSize (4 bytes)
            len(self.script.variables), # variableCount (4 bytes)
            script_type,                # type (2 bytes)
            0x0001,                     # flags: enabled (2 bytes)
        )

        # SCDA
        scda = bytes(self.code)

        # SCTX
        sctx = self.source_text.encode('utf-8') if self.source_text else b''

        # SLSD + SCVR pairs
        slsd_scvr_list = []
        for var in self.script.variables:
            # SLSD: 24 bytes
            flags = 0x01 if var.var_type == 'int' else 0x00
            slsd = struct.pack('<I', var.index)
            slsd += b'\x00' * 12  # unused
            slsd += struct.pack('<B', flags)
            slsd += b'\x00' * 7  # unused

            # SCVR: variable name as cstring
            scvr = var.name.encode('ascii') + b'\x00'
            slsd_scvr_list.append((slsd, scvr))

        # SCRO list
        scro_entries = [struct.pack('<I', fid) for fid in self.scro_list]

        return {
            'EDID': edid,
            'SCHR': schr,
            'SCDA': scda,
            'SCTX': sctx,
            'SLSD_SCVR': slsd_scvr_list,
            'SCRO': scro_entries,
        }


def compile_script(script: Script, source_text: str = '') -> dict:
    """Convenience wrapper: compile parsed AST to SCPT subrecords."""
    return BytecodeEmitter(script, source_text).emit()
