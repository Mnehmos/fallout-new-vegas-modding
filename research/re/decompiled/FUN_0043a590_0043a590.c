
undefined4 __fastcall FUN_0043a590(int *param_1)

{
  undefined4 uVar1;
  int iVar2;
  int *piVar3;
  int local_8;
  
  local_8 = *param_1;
  uVar1 = FUN_00484e60();
  FUN_00485d50(&local_8,uVar1);
  uVar1 = FUN_004839c0(local_8,&PTR_PTR__scalar_deleting_destructor__01183028,
                       &PTR_PTR__scalar_deleting_destructor__011841cc,0);
  iVar2 = ___RTDynamicCast(uVar1,0);
  *param_1 = iVar2;
  if (*param_1 == 0) {
    FUN_005b5e40("MASTERFILE: Could not find linked door (%08X) in teleport data init.",local_8);
    return 0;
  }
  FUN_007af430();
  iVar2 = FUN_00401170();
  if (iVar2 == 0x1c) {
    iVar2 = FUN_00ec7595((double)(float)param_1[1]);
    if ((((iVar2 == 0) || (iVar2 = FUN_00ec7595((double)(float)param_1[2]), iVar2 == 0)) ||
        (iVar2 = FUN_00ec7595((double)(float)param_1[3]), iVar2 == 0)) ||
       (((iVar2 = __isnan((double)(float)param_1[1]), iVar2 != 0 ||
         (iVar2 = __isnan((double)(float)param_1[2]), iVar2 != 0)) ||
        (iVar2 = __isnan((double)(float)param_1[3]), iVar2 != 0)))) {
      FUN_005b5e40();
      param_1[1] = DAT_011f426c;
      param_1[2] = DAT_011f4270;
      param_1[3] = DAT_011f4274;
    }
    iVar2 = FUN_00ec7595((double)(float)param_1[4]);
    if (((iVar2 == 0) || (iVar2 = FUN_00ec7595((double)(float)param_1[5]), iVar2 == 0)) ||
       ((iVar2 = FUN_00ec7595((double)(float)param_1[6]), iVar2 == 0 ||
        (((iVar2 = __isnan((double)(float)param_1[4]), iVar2 != 0 ||
          (iVar2 = __isnan((double)(float)param_1[5]), iVar2 != 0)) ||
         (iVar2 = __isnan((double)(float)param_1[6]), iVar2 != 0)))))) {
      FUN_005b5e40();
      param_1[4] = DAT_011f426c;
      param_1[5] = DAT_011f4270;
      param_1[6] = DAT_011f4274;
    }
    return 1;
  }
  piVar3 = (int *)FUN_007af430();
  FUN_007af430();
  FUN_0084e3a0();
  uVar1 = (**(code **)(*piVar3 + 0x130))();
  FUN_007af430(uVar1);
  iVar2 = FUN_00401170();
  FUN_005b5e40("MASTERFILE: Linked door (%08X) in teleport data points to invalid object (%s %s(%08X))."
               ,local_8,(&PTR_s_NONE_01187004)[iVar2 * 3]);
  *param_1 = 0;
  return 0;
}

