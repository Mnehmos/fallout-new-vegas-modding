
undefined4 __thiscall FUN_00432dd0(int param_1_00,undefined4 param_1)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  
  iVar2 = ___RTDynamicCast(param_1,0,&PTR_PTR__scalar_deleting_destructor__01183b2c,
                           &PTR_PTR__scalar_deleting_destructor__01184cd4,0);
  if (iVar2 == 0) {
    uVar3 = 1;
  }
  else {
    cVar1 = FUN_0040f700(param_1);
    if (cVar1 == '\0') {
      if (*(int *)(param_1_00 + 0xc) == 0) {
        if (*(int *)(iVar2 + 0xc) != 0) {
          return 1;
        }
      }
      else {
        cVar1 = FUN_004d9780(*(undefined4 *)(iVar2 + 0xc));
        if (cVar1 != '\0') {
          return 1;
        }
      }
      uVar3 = 0;
    }
    else {
      uVar3 = 1;
    }
  }
  return uVar3;
}

