
void __fastcall FUN_00525e70(int param_1)

{
  int iVar1;
  char cVar2;
  undefined4 uVar3;
  
  FUN_004855a0();
  iVar1 = *(int *)(param_1 + 0x18);
  if (iVar1 != 0) {
    uVar3 = FUN_0084e3a0();
    *(undefined4 *)(param_1 + 0x18) = uVar3;
  }
  cVar2 = FUN_00401500();
  if (cVar2 != '\0') {
    FUN_00503210();
  }
  FUN_00485990(0x41544144,param_1 + 0x18,8);
  cVar2 = FUN_00401500();
  if (cVar2 != '\0') {
    FUN_00503210();
  }
  *(int *)(param_1 + 0x18) = iVar1;
  FUN_00485680();
  return;
}

