
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_005623d0(int *param_1_00,uint *param_1)

{
  char cVar1;
  int iVar2;
  float10 fVar3;
  int *piVar4;
  undefined4 uVar5;
  uint *puVar6;
  undefined4 uVar7;
  undefined local_28 [4];
  undefined local_24 [4];
  undefined local_20 [4];
  undefined local_1c [4];
  undefined local_18 [4];
  undefined local_14 [4];
  undefined4 local_10;
  char local_9;
  int local_8;
  
  FUN_00484da0(param_1);
  local_9 = (**(code **)(*param_1_00 + 0x100))();
  if (local_9 == '\0') {
    uVar5 = 0x200000;
    FUN_00428110(local_14);
    cVar1 = FUN_004280f0(uVar5);
    if (cVar1 != '\0') {
      FUN_00484580(1);
    }
  }
  uVar5 = 0x10;
  FUN_00428110(local_18);
  cVar1 = FUN_004280f0(uVar5);
  if (cVar1 != '\0') {
    FUN_00864980(param_1_00 + 0xf,4);
    FUN_00567490(param_1_00[0xf]);
  }
  iVar2 = (-(uint)(local_9 != '\0') & 0x3fc00) + 0xa4021c40;
  local_8 = iVar2;
  FUN_00428110(local_1c);
  cVar1 = FUN_004280f0(iVar2);
  if (cVar1 != '\0') {
    puVar6 = param_1;
    FUN_005d43c0(param_1);
    FUN_00428150(puVar6);
  }
  uVar5 = 0x8000020;
  FUN_00428110(local_20);
  cVar1 = FUN_004280f0(uVar5);
  if (cVar1 != '\0') {
    FUN_005d43c0();
    FUN_0041aeb0();
    local_10 = FUN_004bf220(param_1_00);
    FUN_004d4160(param_1);
  }
  uVar5 = 0x10000000;
  FUN_00428110(local_24);
  cVar1 = FUN_004280f0(uVar5);
  if (cVar1 != '\0') {
    cVar1 = (**(code **)(*param_1_00 + 0x100))();
    if (cVar1 == '\0') {
      Concurrency::details::SchedulerResourceManagement::Statistics
                (DAT_011ddf38,(uint *)0x0,param_1,(uint *)0x0);
    }
  }
  cVar1 = (**(code **)(*param_1_00 + 0x100))();
  if (cVar1 == '\0') {
    uVar5 = 0x400000;
    FUN_00428110(local_28);
    cVar1 = FUN_004280f0(uVar5);
    if (cVar1 != '\0') {
      uVar5 = 8;
      FUN_005d43c0(8);
      cVar1 = FUN_0041b3a0(uVar5);
      if (cVar1 == '\0') {
        uVar5 = 8;
        FUN_005d43c0(8);
        FUN_0041b440(uVar5);
      }
      else {
        uVar5 = 8;
        FUN_005d43c0(8);
        FUN_0041b470(uVar5);
      }
    }
  }
  cVar1 = FUN_00452370();
  if ((cVar1 != '\0') && (param_1_00[0x19] != 0)) {
    iVar2 = FUN_00559450();
    if (iVar2 != 0) {
      FUN_005d43c0();
      fVar3 = (float10)FUN_0041b6b0();
      if ((NAN(fVar3) || NAN((float10)_DAT_0101a6b0)) == (fVar3 == (float10)_DAT_0101a6b0)) {
        iVar2 = FUN_007af430();
        if (iVar2 != 0) {
          uVar7 = 0;
          piVar4 = param_1_00;
          uVar5 = FUN_007af430(param_1_00,0);
          FUN_00475400(uVar5);
          cVar1 = FUN_00476f50(piVar4,uVar7);
          if (cVar1 != '\0') {
            FUN_0057a3c0(0);
          }
        }
      }
    }
  }
  uVar5 = (**(code **)(*param_1_00 + 0x1d0))();
  FUN_0055d6d0(param_1_00,uVar5);
  return;
}

