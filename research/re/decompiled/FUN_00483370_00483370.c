
undefined4 * __fastcall FUN_00483370(undefined4 *param_1)

{
  bool bVar1;
  char cVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  int *unaff_FS_OFFSET;
  uint local_1c;
  uint local_18;
  int local_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00eeefab;
  local_10 = *unaff_FS_OFFSET;
  uVar3 = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  *unaff_FS_OFFSET = (int)&local_10;
  FUN_00402d30(uVar3);
  *param_1 = &PTR_FUN_0101c794;
  Concurrency::details::QuickBitSet::QuickBitSet((QuickBitSet *)(param_1 + 4));
  local_8 = 0;
  if (DAT_011c54bc == 0) {
    FUN_00483a50();
  }
  DAT_011c54bc = DAT_011c54bc + 1;
  if (DAT_011c54b8 == '\0') {
    bVar1 = false;
    FUN_0043b2b0(1);
    for (local_18 = 0; local_18 < 0x79; local_18 = local_18 + 1) {
      *(int *)(&DAT_01187008 + local_18 * 0xc) =
           (int)(char)*(&PTR_s_NONE_01187004)[local_18 * 3] |
           (int)(char)(&PTR_s_NONE_01187004)[local_18 * 3][1] << 8 |
           (int)(char)(&PTR_s_NONE_01187004)[local_18 * 3][2] << 0x10 |
           (int)(char)(&PTR_s_NONE_01187004)[local_18 * 3][3] << 0x18;
      if ((byte)(&DAT_01187000)[local_18 * 0xc] != local_18) {
        FUN_005b5e40("FORMS: formEnumString[ %d ].cFormID in TESForm.cpp is out of order.",local_18)
        ;
        bVar1 = true;
      }
      for (local_1c = 0; local_1c < 0x79; local_1c = local_1c + 1) {
        if ((local_18 != local_1c) &&
           (*(int *)(&DAT_01187008 + local_18 * 0xc) == *(int *)(&DAT_01187008 + local_1c * 0xc))) {
          FUN_005b5e40("FORMS: formEnumString[ %d ] and formEnumString[ %d ] have the same iFormString %s in TESForm.cpp."
                       ,local_18,local_1c,(&PTR_s_NONE_01187004)[local_18 * 3]);
          bVar1 = true;
        }
      }
    }
    FUN_0043b2b0(0);
    if (bVar1) {
      FUN_0040fbe0("You must fix the problems in TESForm.cpp to run this game.");
    }
    DAT_011c54b8 = '\x01';
  }
  *(undefined *)(param_1 + 1) = 0;
  param_1[2] = 8;
  param_1[3] = 0;
  if (DAT_011c3f2c != 0) {
    cVar2 = FUN_00482f20();
    if (cVar2 == '\0') {
      uVar4 = FUN_00469800();
      param_1[3] = uVar4;
      iVar5 = FUN_004835e0();
      if (iVar5 != 0) {
        uVar4 = FUN_004835e0();
        FUN_00484f50(uVar4);
      }
      if ((uint)param_1[3] < 0x800) {
        FUN_00485c10(0x800,1);
      }
    }
  }
  if (param_1[3] != 0) {
    FUN_00844700(param_1[3],param_1);
  }
  *unaff_FS_OFFSET = local_10;
  return param_1;
}

