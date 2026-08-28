
undefined4 FUN_0040ff60(undefined4 param_1)

{
  undefined uVar1;
  char cVar2;
  int iVar3;
  int iVar4;
  undefined4 uVar5;
  int extraout_var;
  int iVar6;
  
  FUN_0040fbf0("BaseExtraList::AddExtra()");
  iVar6 = extraout_var;
  uVar1 = FUN_004f1540();
  cVar2 = FUN_0040f980(uVar1);
  if (cVar2 == '\0') {
    iVar4 = *(int *)(iVar6 + 4);
    if (iVar4 == 0) {
      *(undefined4 *)(iVar6 + 4) = param_1;
    }
    else {
      while( true ) {
        iVar3 = FUN_0044ddc0(iVar6,iVar4);
        if (iVar3 == 0) break;
        iVar4 = FUN_0044ddc0(iVar6,iVar4);
      }
      FUN_00403550(param_1);
    }
  }
  else {
    if (*(int *)(iVar6 + 4) != 0) {
      FUN_00403550(*(undefined4 *)(iVar6 + 4));
    }
    *(undefined4 *)(iVar6 + 4) = param_1;
  }
  uVar5 = 1;
  uVar1 = FUN_004f1540(1);
  FUN_0040fee0(uVar1,uVar5);
  FUN_0040fba0();
  return param_1;
}

