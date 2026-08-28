
undefined4 FUN_0040f700(int param_1)

{
  char cVar1;
  char cVar2;
  undefined4 uVar3;
  
  if (param_1 == 0) {
    uVar3 = 1;
  }
  else {
    cVar1 = FUN_004f1540();
    cVar2 = FUN_004f1540();
    if (cVar1 == cVar2) {
      uVar3 = 0;
    }
    else {
      uVar3 = 1;
    }
  }
  return uVar3;
}

