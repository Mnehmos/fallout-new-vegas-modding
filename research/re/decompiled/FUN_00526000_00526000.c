
undefined4 __thiscall FUN_00526000(int param_1_00,undefined4 param_1)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  
  iVar2 = ___RTDynamicCast(param_1,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011840dc,0);
  if (iVar2 == 0) {
    uVar3 = 1;
  }
  else {
    cVar1 = FUN_00485270(iVar2);
    if (cVar1 == '\0') {
      iVar2 = _memcmp((void *)(param_1_00 + 0x18),(void *)(iVar2 + 0x18),8);
      if (iVar2 == 0) {
        uVar3 = 0;
      }
      else {
        uVar3 = 1;
      }
    }
    else {
      uVar3 = 1;
    }
  }
  return uVar3;
}

