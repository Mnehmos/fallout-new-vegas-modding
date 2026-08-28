
void __thiscall FUN_004bee00(int *param_1_00,undefined4 param_1)

{
  uint uVar1;
  undefined4 uVar2;
  int iVar3;
  QuickBitSet *this;
  int *unaff_FS_OFFSET;
  undefined4 local_38;
  int local_34;
  undefined4 local_1c;
  uint local_18;
  uint local_14;
  int local_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00f00b76;
  local_10 = *unaff_FS_OFFSET;
  uVar1 = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  *unaff_FS_OFFSET = (int)&local_10;
  uVar2 = FUN_008648a0(&PTR_PTR__scalar_deleting_destructor__01183028,
                       &PTR_PTR__scalar_deleting_destructor__01183108,0,uVar1);
  uVar2 = FUN_004839c0(uVar2);
  iVar3 = ___RTDynamicCast(uVar2,0);
  param_1_00[2] = iVar3;
  FUN_00864980(param_1_00 + 1,4);
  FUN_004bc780();
  local_14 = FUN_00864a60();
  if (local_14 != 0) {
    if (*param_1_00 == 0) {
      this = (QuickBitSet *)FUN_00401000(8);
      local_8 = 0;
      if (this == (QuickBitSet *)0x0) {
        local_34 = 0;
      }
      else {
        local_34 = Concurrency::details::QuickBitSet::QuickBitSet(this);
      }
      local_8 = 0xffffffff;
      *param_1_00 = local_34;
    }
    for (local_18 = 0; local_18 < local_14; local_18 = local_18 + 1) {
      iVar3 = FUN_00401000(0x20);
      local_8 = 1;
      if (iVar3 == 0) {
        local_38 = 0;
      }
      else {
        local_38 = FUN_00410360();
      }
      local_8 = 0xffffffff;
      local_1c = local_38;
      FUN_00428150(param_1);
      FUN_00905820(&local_1c);
    }
  }
  *unaff_FS_OFFSET = local_10;
  return;
}

