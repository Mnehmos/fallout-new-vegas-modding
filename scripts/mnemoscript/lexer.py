"""
MnemoScript Lexer — tokenizes .mns source into a token stream.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class TokenType(Enum):
    # Keywords
    SCRIPT    = auto()
    TYPE      = auto()
    INT       = auto()
    FLOAT     = auto()
    REF       = auto()
    USE       = auto()
    OPCODE    = auto()
    ON        = auto()
    END       = auto()
    SET       = auto()
    TO        = auto()
    IF        = auto()
    ELSEIF    = auto()
    ELSE      = auto()
    ENDIF     = auto()
    RETURN    = auto()
    ACTORVALUE = auto()  # keyword in `use X actorvalue N`

    # Literals
    INTEGER   = auto()
    NUMBER    = auto()   # float literal
    STRING    = auto()
    HEXINT    = auto()   # 0xNNNNNNNN

    # Identifiers & operators
    IDENT     = auto()
    DOT       = auto()
    PLUS      = auto()
    MINUS     = auto()
    STAR      = auto()
    SLASH     = auto()
    PERCENT   = auto()
    EQ        = auto()   # ==
    NEQ       = auto()   # !=
    LT        = auto()
    LTE       = auto()   # <=
    GT        = auto()
    GTE       = auto()   # >=
    AND       = auto()   # &&
    OR        = auto()   # ||
    LPAREN    = auto()
    RPAREN    = auto()

    # Structural
    NEWLINE   = auto()
    EOF       = auto()


KEYWORDS = {
    'script':     TokenType.SCRIPT,
    'type':       TokenType.TYPE,
    'int':        TokenType.INT,
    'float':      TokenType.FLOAT,
    'ref':        TokenType.REF,
    'use':        TokenType.USE,
    'opcode':     TokenType.OPCODE,
    'on':         TokenType.ON,
    'end':        TokenType.END,
    'set':        TokenType.SET,
    'to':         TokenType.TO,
    'if':         TokenType.IF,
    'elseif':     TokenType.ELSEIF,
    'else':       TokenType.ELSE,
    'endif':      TokenType.ENDIF,
    'return':     TokenType.RETURN,
    'actorvalue': TokenType.ACTORVALUE,
}


@dataclass
class Token:
    type: TokenType
    value: str | int | float
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line})"


class LexError(Exception):
    def __init__(self, msg: str, line: int, col: int):
        super().__init__(f"Line {line}, col {col}: {msg}")
        self.line = line
        self.col = col


def tokenize(source: str) -> List[Token]:
    """Tokenize MnemoScript source into a list of tokens."""
    tokens: List[Token] = []
    lines = source.split('\n')

    for line_num, line_text in enumerate(lines, start=1):
        col = 0
        text = line_text

        # Strip comment
        semi = text.find(';')
        if semi >= 0:
            text = text[:semi]

        text = text.rstrip()
        if not text.strip():
            continue  # skip blank/comment-only lines

        i = 0
        line_has_tokens = False

        while i < len(text):
            ch = text[i]

            # Whitespace
            if ch in ' \t':
                i += 1
                continue

            col = i + 1

            # Two-char operators
            if i + 1 < len(text):
                two = text[i:i+2]
                if two == '==':
                    tokens.append(Token(TokenType.EQ, '==', line_num, col))
                    i += 2; line_has_tokens = True; continue
                if two == '!=':
                    tokens.append(Token(TokenType.NEQ, '!=', line_num, col))
                    i += 2; line_has_tokens = True; continue
                if two == '<=':
                    tokens.append(Token(TokenType.LTE, '<=', line_num, col))
                    i += 2; line_has_tokens = True; continue
                if two == '>=':
                    tokens.append(Token(TokenType.GTE, '>=', line_num, col))
                    i += 2; line_has_tokens = True; continue
                if two == '&&':
                    tokens.append(Token(TokenType.AND, '&&', line_num, col))
                    i += 2; line_has_tokens = True; continue
                if two == '||':
                    tokens.append(Token(TokenType.OR, '||', line_num, col))
                    i += 2; line_has_tokens = True; continue

            # Single-char operators
            if ch == '.':
                tokens.append(Token(TokenType.DOT, '.', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == '+':
                tokens.append(Token(TokenType.PLUS, '+', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == '-':
                # Could be negative number or subtraction
                # Peek ahead — if next char is digit and previous token is an operator or start of line, it's a negative literal
                if i + 1 < len(text) and text[i+1].isdigit():
                    if not tokens or tokens[-1].type in (
                        TokenType.NEWLINE, TokenType.SET, TokenType.TO,
                        TokenType.PLUS, TokenType.MINUS, TokenType.STAR,
                        TokenType.SLASH, TokenType.PERCENT, TokenType.EQ,
                        TokenType.NEQ, TokenType.LT, TokenType.LTE,
                        TokenType.GT, TokenType.GTE, TokenType.AND,
                        TokenType.OR, TokenType.LPAREN, TokenType.IF,
                        TokenType.ELSEIF,
                    ):
                        # Parse as negative number
                        j = i + 1
                        has_dot = False
                        while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                            if text[j] == '.':
                                has_dot = True
                            j += 1
                        num_str = text[i:j]
                        if has_dot:
                            tokens.append(Token(TokenType.NUMBER, float(num_str), line_num, col))
                        else:
                            tokens.append(Token(TokenType.INTEGER, int(num_str), line_num, col))
                        i = j; line_has_tokens = True; continue
                tokens.append(Token(TokenType.MINUS, '-', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == '*':
                tokens.append(Token(TokenType.STAR, '*', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == '/':
                tokens.append(Token(TokenType.SLASH, '/', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == '%':
                tokens.append(Token(TokenType.PERCENT, '%', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == '<':
                tokens.append(Token(TokenType.LT, '<', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == '>':
                tokens.append(Token(TokenType.GT, '>', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == '(':
                tokens.append(Token(TokenType.LPAREN, '(', line_num, col))
                i += 1; line_has_tokens = True; continue
            if ch == ')':
                tokens.append(Token(TokenType.RPAREN, ')', line_num, col))
                i += 1; line_has_tokens = True; continue

            # Hex integer (0xNNNN)
            if ch == '0' and i + 1 < len(text) and text[i+1] in 'xX':
                j = i + 2
                while j < len(text) and text[j] in '0123456789abcdefABCDEF':
                    j += 1
                hex_str = text[i:j]
                tokens.append(Token(TokenType.HEXINT, int(hex_str, 16), line_num, col))
                i = j; line_has_tokens = True; continue

            # Number (integer or float)
            if ch.isdigit():
                j = i
                has_dot = False
                while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                    if text[j] == '.':
                        has_dot = True
                    j += 1
                num_str = text[i:j]
                if has_dot:
                    tokens.append(Token(TokenType.NUMBER, float(num_str), line_num, col))
                else:
                    tokens.append(Token(TokenType.INTEGER, int(num_str), line_num, col))
                i = j; line_has_tokens = True; continue

            # Identifier or keyword
            if ch.isalpha() or ch == '_':
                j = i
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                word = text[i:j]
                lower = word.lower()
                if lower in KEYWORDS:
                    tokens.append(Token(KEYWORDS[lower], word, line_num, col))
                else:
                    tokens.append(Token(TokenType.IDENT, word, line_num, col))
                i = j; line_has_tokens = True; continue

            raise LexError(f"Unexpected character: {ch!r}", line_num, col)

        if line_has_tokens:
            tokens.append(Token(TokenType.NEWLINE, '\\n', line_num, len(text) + 1))

    tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 0))
    return tokens
