"""
MnemoScript — A DSL compiler for Fallout New Vegas game scripts.

Compiles a clean, Python-like scripting language to GECK-compatible
SCDA bytecode, producing SCPT records for ESP plugin injection.

Usage:
    from mnemoscript.compiler import compile_source, compile_file

    # From source string
    subrecords = compile_source('''
        script MyScript
        type effect
        use player 0x00000014
        on ScriptEffectUpdate
          player.ModAV Health 10.0
        end
    ''')

    # From .mns file
    subrecords = compile_file('path/to/script.mns')
"""
