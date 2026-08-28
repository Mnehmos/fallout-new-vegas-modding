
undefined4 __thiscall FUN_004d9780(byte *param_1_00,byte *param_1)

{
  char cVar1;
  undefined4 uVar2;
  int iVar3;
  
  if (param_1 == (byte *)0x0) {
    uVar2 = 1;
  }
  else if (*param_1_00 == *param_1) {
    cVar1 = FUN_00439090(param_1 + 8);
    if (cVar1 == '\0') {
      if ((*param_1_00 != 0) &&
         (iVar3 = _memcmp(*(void **)(param_1_00 + 4),*(void **)(param_1 + 4),
                          (uint)*param_1_00 * 0x1c), iVar3 != 0)) {
        return 1;
      }
      uVar2 = 0;
    }
    else {
      uVar2 = 1;
    }
  }
  else {
    uVar2 = 1;
  }
  return uVar2;
}

