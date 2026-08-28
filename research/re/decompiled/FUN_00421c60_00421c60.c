
void FUN_00421c60(int param_1)

{
  uint uVar1;
  int iVar2;
  int *unaff_FS_OFFSET;
  int local_24;
  int local_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00eeb0fb;
  local_10 = *unaff_FS_OFFSET;
  uVar1 = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  *unaff_FS_OFFSET = (int)&local_10;
  if (param_1 == 0) {
    FUN_00410140(0x74);
  }
  else {
    iVar2 = FUN_00410220(0x74);
    if (iVar2 == 0) {
      iVar2 = FUN_00401000(0x10,uVar1);
      local_8 = 0;
      if (iVar2 == 0) {
        local_24 = 0;
      }
      else {
        local_24 = FUN_00432e60();
      }
      local_8 = 0xffffffff;
      *(int *)(local_24 + 0xc) = param_1;
      FUN_0040ff60(local_24);
    }
    else {
      *(int *)(iVar2 + 0xc) = param_1;
    }
  }
  *unaff_FS_OFFSET = local_10;
  return;
}

