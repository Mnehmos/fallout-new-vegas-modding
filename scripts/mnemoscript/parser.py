"""
MnemoScript Parser — builds AST from token stream.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union
from lexer import Token, TokenType


# --- AST Nodes ---

@dataclass
class VarDecl:
    """Variable declaration: int/float/ref name"""
    var_type: str        # 'int', 'float', 'ref'
    name: str
    index: int = 0       # assigned during compilation

@dataclass
class UseDecl:
    """External reference: use name formid [actorvalue N]"""
    name: str
    form_id: int
    is_actor_value: bool = False
    av_index: int = 0

@dataclass
class OpcodeDecl:
    """Custom opcode registration: opcode FuncName 0xNNNN"""
    name: str
    opcode: int

@dataclass
class IntLiteral:
    value: int

@dataclass
class FloatLiteral:
    value: float

@dataclass
class VarRef:
    name: str

@dataclass
class FuncCall:
    """ref.Function args  OR  Function args"""
    ref_name: Optional[str]   # None = self/no ref
    func_name: str
    args: List[Union[IntLiteral, FloatLiteral, VarRef, str]]  # str = identifier (ActorValue name, etc.)

@dataclass
class BinOp:
    left: 'Expr'
    op: str              # '+', '-', '*', '/', '%', '==', '!=', '<', '<=', '>', '>=', '&&', '||'
    right: 'Expr'

@dataclass
class UnaryOp:
    op: str
    operand: 'Expr'

# Expression = any of the above expression nodes
Expr = Union[IntLiteral, FloatLiteral, VarRef, FuncCall, BinOp, UnaryOp]

@dataclass
class SetStmt:
    target: str          # variable name
    expr: Expr

@dataclass
class CallStmt:
    call: FuncCall

@dataclass
class IfBlock:
    condition: Expr
    body: List['Stmt']
    elseif_blocks: List[tuple]   # list of (condition, body) pairs
    else_body: List['Stmt']

@dataclass
class ReturnStmt:
    pass

Stmt = Union[SetStmt, CallStmt, IfBlock, ReturnStmt]

@dataclass
class EventBlock:
    event_name: str
    body: List[Stmt]

@dataclass
class Script:
    name: str
    script_type: str     # 'object', 'quest', 'effect'
    variables: List[VarDecl] = field(default_factory=list)
    uses: List[UseDecl] = field(default_factory=list)
    opcodes: List[OpcodeDecl] = field(default_factory=list)
    events: List[EventBlock] = field(default_factory=list)


# --- Parser ---

class ParseError(Exception):
    def __init__(self, msg: str, token: Token):
        super().__init__(f"Line {token.line}: {msg} (got {token.type.name} = {token.value!r})")
        self.token = token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, tt: TokenType) -> Token:
        tok = self.advance()
        if tok.type != tt:
            raise ParseError(f"Expected {tt.name}", tok)
        return tok

    def skip_newlines(self):
        while self.peek().type == TokenType.NEWLINE:
            self.advance()

    def at(self, *types: TokenType) -> bool:
        return self.peek().type in types

    def parse(self) -> Script:
        self.skip_newlines()

        # script name
        self.expect(TokenType.SCRIPT)
        name_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.NEWLINE)
        self.skip_newlines()

        # type declaration
        script_type = 'object'
        if self.at(TokenType.TYPE):
            self.advance()
            type_tok = self.expect(TokenType.IDENT)
            script_type = type_tok.value.lower()
            self.expect(TokenType.NEWLINE)
            self.skip_newlines()

        script = Script(name=name_tok.value, script_type=script_type)

        # Declarations and event blocks
        while not self.at(TokenType.EOF):
            self.skip_newlines()
            if self.at(TokenType.EOF):
                break

            tok = self.peek()

            if tok.type == TokenType.INT:
                script.variables.append(self._parse_var_decl('int'))
            elif tok.type == TokenType.FLOAT:
                script.variables.append(self._parse_var_decl('float'))
            elif tok.type == TokenType.REF:
                script.variables.append(self._parse_var_decl('ref'))
            elif tok.type == TokenType.USE:
                script.uses.append(self._parse_use_decl())
            elif tok.type == TokenType.OPCODE:
                script.opcodes.append(self._parse_opcode_decl())
            elif tok.type == TokenType.ON:
                script.events.append(self._parse_event_block())
            else:
                raise ParseError("Expected declaration or event block", tok)

        return script

    def _parse_var_decl(self, vtype: str) -> VarDecl:
        self.advance()  # consume int/float/ref
        name_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.NEWLINE)
        return VarDecl(var_type=vtype, name=name_tok.value)

    def _parse_use_decl(self) -> UseDecl:
        self.advance()  # consume 'use'
        name_tok = self.expect(TokenType.IDENT)

        # FormID
        form_tok = self.advance()
        if form_tok.type == TokenType.HEXINT:
            form_id = form_tok.value
        elif form_tok.type == TokenType.INTEGER:
            form_id = form_tok.value
        else:
            raise ParseError("Expected FormID (hex or int)", form_tok)

        # Optional: actorvalue N
        is_av = False
        av_idx = 0
        if self.at(TokenType.ACTORVALUE):
            self.advance()
            av_tok = self.advance()
            if av_tok.type in (TokenType.INTEGER, TokenType.HEXINT):
                av_idx = av_tok.value
            else:
                raise ParseError("Expected actor value index", av_tok)
            is_av = True

        self.expect(TokenType.NEWLINE)
        return UseDecl(name=name_tok.value, form_id=form_id,
                       is_actor_value=is_av, av_index=av_idx)

    def _parse_opcode_decl(self) -> OpcodeDecl:
        self.advance()  # consume 'opcode'
        name_tok = self.expect(TokenType.IDENT)
        op_tok = self.advance()
        if op_tok.type == TokenType.HEXINT:
            opcode = op_tok.value
        elif op_tok.type == TokenType.INTEGER:
            opcode = op_tok.value
        else:
            raise ParseError("Expected opcode value", op_tok)
        self.expect(TokenType.NEWLINE)
        return OpcodeDecl(name=name_tok.value, opcode=opcode)

    def _parse_event_block(self) -> EventBlock:
        self.advance()  # consume 'on'
        event_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.NEWLINE)

        body = self._parse_body()

        self.expect(TokenType.END)
        self.expect(TokenType.NEWLINE)

        return EventBlock(event_name=event_tok.value, body=body)

    def _parse_body(self) -> List[Stmt]:
        """Parse statements until 'end', 'else', 'elseif', or 'endif'."""
        stmts = []
        while True:
            self.skip_newlines()
            tok = self.peek()
            if tok.type in (TokenType.END, TokenType.ELSE, TokenType.ELSEIF,
                            TokenType.ENDIF, TokenType.EOF):
                break
            stmts.append(self._parse_stmt())
        return stmts

    def _parse_stmt(self) -> Stmt:
        tok = self.peek()

        if tok.type == TokenType.SET:
            return self._parse_set()
        elif tok.type == TokenType.IF:
            return self._parse_if()
        elif tok.type == TokenType.RETURN:
            self.advance()
            self.expect(TokenType.NEWLINE)
            return ReturnStmt()
        elif tok.type == TokenType.IDENT:
            return self._parse_call_stmt()
        else:
            raise ParseError("Expected statement", tok)

    def _parse_set(self) -> SetStmt:
        self.advance()  # consume 'set'
        target_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.TO)
        expr = self._parse_expr()
        self.expect(TokenType.NEWLINE)
        return SetStmt(target=target_tok.value, expr=expr)

    def _parse_call_stmt(self) -> CallStmt:
        """Parse: [ref.]FuncName args..."""
        call = self._parse_func_call_or_ref()
        self.expect(TokenType.NEWLINE)
        return CallStmt(call=call)

    def _parse_func_call_or_ref(self) -> FuncCall:
        """Parse ident[.ident] [args...]"""
        first = self.expect(TokenType.IDENT)

        ref_name = None
        func_name = first.value

        # Check for ref.func
        if self.at(TokenType.DOT):
            self.advance()  # consume '.'
            func_tok = self.expect(TokenType.IDENT)
            ref_name = first.value
            func_name = func_tok.value

        # Parse arguments (everything until NEWLINE or binary operator)
        args = []
        while not self.at(TokenType.NEWLINE, TokenType.EOF,
                          TokenType.PLUS, TokenType.STAR,
                          TokenType.SLASH, TokenType.PERCENT,
                          TokenType.EQ, TokenType.NEQ,
                          TokenType.LT, TokenType.LTE,
                          TokenType.GT, TokenType.GTE,
                          TokenType.AND, TokenType.OR,
                          TokenType.RPAREN,
                          TokenType.ELSE, TokenType.ELSEIF, TokenType.ENDIF):
            arg_tok = self.peek()
            if arg_tok.type == TokenType.INTEGER:
                args.append(IntLiteral(self.advance().value))
            elif arg_tok.type == TokenType.NUMBER:
                args.append(FloatLiteral(self.advance().value))
            elif arg_tok.type == TokenType.HEXINT:
                args.append(IntLiteral(self.advance().value))
            elif arg_tok.type == TokenType.IDENT:
                args.append(self.advance().value)  # could be ActorValue name or var ref
            elif arg_tok.type == TokenType.MINUS:
                # Negative number argument: -5.0, -10, etc.
                self.advance()  # consume '-'
                next_tok = self.peek()
                if next_tok.type == TokenType.INTEGER:
                    args.append(IntLiteral(-self.advance().value))
                elif next_tok.type == TokenType.NUMBER:
                    args.append(FloatLiteral(-self.advance().value))
                else:
                    raise ParseError("Expected number after '-' in argument", next_tok)
            else:
                break

        return FuncCall(ref_name=ref_name, func_name=func_name, args=args)

    def _parse_if(self) -> IfBlock:
        self.advance()  # consume 'if'
        condition = self._parse_expr()
        self.expect(TokenType.NEWLINE)
        body = self._parse_body()

        elseif_blocks = []
        else_body = []

        while self.at(TokenType.ELSEIF):
            self.advance()
            elif_cond = self._parse_expr()
            self.expect(TokenType.NEWLINE)
            elif_body = self._parse_body()
            elseif_blocks.append((elif_cond, elif_body))

        if self.at(TokenType.ELSE):
            self.advance()
            self.expect(TokenType.NEWLINE)
            else_body = self._parse_body()

        self.expect(TokenType.ENDIF)
        self.expect(TokenType.NEWLINE)

        return IfBlock(condition=condition, body=body,
                       elseif_blocks=elseif_blocks, else_body=else_body)

    # --- Expression parser (precedence climbing) ---

    def _parse_expr(self) -> Expr:
        return self._parse_or()

    def _parse_or(self) -> Expr:
        left = self._parse_and()
        while self.at(TokenType.OR):
            op = self.advance().value
            right = self._parse_and()
            left = BinOp(left, op, right)
        return left

    def _parse_and(self) -> Expr:
        left = self._parse_comparison()
        while self.at(TokenType.AND):
            op = self.advance().value
            right = self._parse_comparison()
            left = BinOp(left, op, right)
        return left

    def _parse_comparison(self) -> Expr:
        left = self._parse_additive()
        while self.at(TokenType.EQ, TokenType.NEQ, TokenType.LT,
                      TokenType.LTE, TokenType.GT, TokenType.GTE):
            op = self.advance().value
            right = self._parse_additive()
            left = BinOp(left, op, right)
        return left

    def _parse_additive(self) -> Expr:
        left = self._parse_multiplicative()
        while self.at(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self._parse_multiplicative()
            left = BinOp(left, op, right)
        return left

    def _parse_multiplicative(self) -> Expr:
        left = self._parse_unary()
        while self.at(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.advance().value
            right = self._parse_unary()
            left = BinOp(left, op, right)
        return left

    def _parse_unary(self) -> Expr:
        if self.at(TokenType.MINUS):
            op_tok = self.advance()
            operand = self._parse_primary()
            return UnaryOp('-', operand)
        return self._parse_primary()

    def _parse_primary(self) -> Expr:
        tok = self.peek()

        if tok.type == TokenType.INTEGER:
            self.advance()
            return IntLiteral(tok.value)

        if tok.type == TokenType.HEXINT:
            self.advance()
            return IntLiteral(tok.value)

        if tok.type == TokenType.NUMBER:
            self.advance()
            return FloatLiteral(tok.value)

        if tok.type == TokenType.LPAREN:
            self.advance()
            expr = self._parse_expr()
            self.expect(TokenType.RPAREN)
            return expr

        if tok.type == TokenType.IDENT:
            # Could be: variable, ref.func, or bare func
            first = self.advance()

            if self.at(TokenType.DOT):
                # ref.func(args)
                self.advance()
                func_tok = self.expect(TokenType.IDENT)
                args = self._parse_func_args_in_expr()
                return FuncCall(ref_name=first.value, func_name=func_tok.value, args=args)

            # Check if this looks like a function call (next token is an ident or number, not an operator)
            if self.at(TokenType.IDENT, TokenType.INTEGER, TokenType.NUMBER, TokenType.HEXINT):
                # Bare function call with args
                args = self._parse_func_args_in_expr()
                return FuncCall(ref_name=None, func_name=first.value, args=args)

            # Simple variable reference
            return VarRef(first.value)

        raise ParseError("Expected expression", tok)

    def _parse_func_args_in_expr(self) -> list:
        """Parse function arguments within an expression context (limited)."""
        args = []
        while self.at(TokenType.IDENT, TokenType.INTEGER, TokenType.NUMBER, TokenType.HEXINT):
            arg_tok = self.peek()
            # Stop if this ident could be a variable in the outer expression
            # Heuristic: if the next-next token is an operator, this ident is a var, not an arg
            if arg_tok.type == TokenType.IDENT:
                # Peek ahead: is the token AFTER this one an operator?
                save = self.pos
                self.advance()
                if self.at(TokenType.PLUS, TokenType.MINUS, TokenType.STAR,
                           TokenType.SLASH, TokenType.PERCENT,
                           TokenType.EQ, TokenType.NEQ,
                           TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE,
                           TokenType.AND, TokenType.OR, TokenType.RPAREN,
                           TokenType.NEWLINE, TokenType.EOF):
                    # This ident might be a var in outer context — check if it's a known AV first
                    # For now, take it as an arg (single arg functions like GetAV)
                    args.append(arg_tok.value)
                    break  # Only take one ident arg in expression context
                else:
                    self.pos = save
                    args.append(self.advance().value)
            elif arg_tok.type == TokenType.INTEGER:
                args.append(IntLiteral(self.advance().value))
            elif arg_tok.type == TokenType.NUMBER:
                args.append(FloatLiteral(self.advance().value))
            elif arg_tok.type == TokenType.HEXINT:
                args.append(IntLiteral(self.advance().value))
            else:
                break
        return args


def parse(tokens: List[Token]) -> Script:
    """Convenience wrapper."""
    return Parser(tokens).parse()
