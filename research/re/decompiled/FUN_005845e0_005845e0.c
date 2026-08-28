
void __fastcall FUN_005845e0(int *param_1)

{
  char cVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  int *unaff_FS_OFFSET;
  int local_50;
  undefined local_40 [4];
  int *local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int *local_18;
  int local_14;
  int local_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00ef7deb;
  local_10 = *unaff_FS_OFFSET;
  uVar2 = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  *unaff_FS_OFFSET = (int)&local_10;
  cVar1 = FUN_004013e0(uVar2);
  if (cVar1 == '\0') {
    local_1c = param_1[0x10];
    if (local_1c != 0) {
      uVar3 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_1c,uVar3);
      uVar3 = FUN_004839c0(local_1c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01184170,0);
      local_20 = ___RTDynamicCast(uVar3,0);
      if (local_20 == 0) {
        iVar4 = FUN_00474cb0();
        if (iVar4 == 0) {
          uVar3 = FUN_0084e3a0();
          FUN_005b5e40("MASTERFILE: Unable to find climate (%08X) on owner worldspace (%08X).",
                       local_1c,uVar3);
        }
        else {
          uVar3 = (**(code **)(*param_1 + 0x130))();
          FUN_005b5e40("MASTERFILE: Unable to find climate (%08X) on owner worldspace \"%s\".",
                       local_1c,uVar3);
        }
      }
      FUN_0087ce80(local_20);
    }
    local_1c = param_1[0x11];
    if (local_1c != 0) {
      uVar3 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_1c,uVar3);
      uVar3 = FUN_004839c0(local_1c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01184154,0);
      local_24 = ___RTDynamicCast(uVar3,0);
      if (local_24 == 0) {
        iVar4 = FUN_00474cb0();
        if (iVar4 == 0) {
          uVar3 = FUN_0084e3a0();
          FUN_005b5e40("MASTERFILE: Unable to find imagespace (%08X) on owner worldspace (%08X).",
                       local_1c,uVar3);
        }
        else {
          uVar3 = (**(code **)(*param_1 + 0x130))();
          FUN_005b5e40("MASTERFILE: Unable to find imagespace (%08X) on owner worldspace \"%s\".",
                       local_1c,uVar3);
        }
      }
      FUN_008d8040(local_24);
    }
    local_1c = param_1[0x34];
    if (local_1c != 0) {
      uVar3 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_1c,uVar3);
      uVar3 = FUN_004839c0(local_1c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011840dc,0);
      local_28 = ___RTDynamicCast(uVar3,0);
      if (local_28 == 0) {
        iVar4 = FUN_00474cb0();
        if (iVar4 == 0) {
          uVar3 = FUN_0084e3a0();
          FUN_005b5e40("Unable to find encounter zone (%08X) on owner worldspace (%08X).",local_1c,
                       uVar3);
        }
        else {
          uVar3 = (**(code **)(*param_1 + 0x130))();
          FUN_005b5e40("Unable to find encounter zone (%08X) on owner worldspace \"%s\".",local_1c,
                       uVar3);
        }
      }
      FUN_00584bc0(local_28);
    }
    local_1c = param_1[0x1d];
    if (local_1c != 0) {
      uVar3 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_1c,uVar3);
      uVar3 = FUN_004839c0(local_1c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01184118,0);
      local_2c = ___RTDynamicCast(uVar3,0);
      if (local_2c == 0) {
        iVar4 = FUN_00474cb0();
        if (iVar4 == 0) {
          uVar3 = FUN_0084e3a0();
          FUN_005b5e40("MASTERFILE: Unable to find water type (%08X) on owner worldspace (%08X).",
                       local_1c,uVar3);
        }
        else {
          uVar3 = (**(code **)(*param_1 + 0x130))();
          FUN_005b5e40("MASTERFILE: Unable to find water type (%08X) on owner worldspace \"%s\".",
                       local_1c,uVar3);
        }
      }
      FUN_004febb0(local_2c);
    }
    local_1c = param_1[0x1e];
    if (local_1c != 0) {
      uVar3 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_1c,uVar3);
      uVar3 = FUN_004839c0(local_1c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01184118,0);
      local_30 = ___RTDynamicCast(uVar3,0);
      if (local_30 == 0) {
        iVar4 = FUN_00474cb0();
        if (iVar4 == 0) {
          uVar3 = FUN_0084e3a0();
          FUN_005b5e40("MASTERFILE: Unable to find lod water type (%08X) on owner worldspace (%08X)."
                       ,local_1c,uVar3);
        }
        else {
          uVar3 = (**(code **)(*param_1 + 0x130))();
          FUN_005b5e40("MASTERFILE: Unable to find lod water type (%08X) on owner worldspace \"%s\"."
                       ,local_1c,uVar3);
        }
      }
      FUN_00442a80(local_30);
    }
    local_1c = param_1[0x27];
    if (local_1c != 0) {
      uVar3 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_1c,uVar3);
      uVar3 = FUN_004839c0(local_1c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011840fc,0);
      local_34 = ___RTDynamicCast(uVar3,0);
      if (local_34 == 0) {
        iVar4 = FUN_00474cb0();
        if (iVar4 == 0) {
          uVar3 = FUN_0084e3a0();
          FUN_005b5e40("MASTERFILE: Unable to find music type (%08X) on owner worldspace (%08X).",
                       local_1c,uVar3);
        }
        else {
          uVar3 = (**(code **)(*param_1 + 0x130))();
          FUN_005b5e40("MASTERFILE: Unable to find music type (%08X) on owner worldspace \"%s\".",
                       local_1c,uVar3);
        }
      }
      FUN_00810570(local_34);
    }
    local_1c = param_1[0x1c];
    if (local_1c != 0) {
      uVar3 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_1c,uVar3);
      uVar3 = FUN_004839c0(local_1c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01183fd0,0);
      local_38 = ___RTDynamicCast(uVar3,0);
      if (local_38 == 0) {
        iVar4 = FUN_00474cb0();
        if (iVar4 == 0) {
          uVar3 = FUN_0084e3a0();
          FUN_005b5e40("MASTERFILE: Unable to find landscape world (%08X) on owner worldspace (%08X)."
                       ,local_1c,uVar3);
        }
        else {
          uVar3 = (**(code **)(*param_1 + 0x130))();
          FUN_005b5e40("MASTERFILE: Unable to find landscape world (%08X) on owner worldspace \"%s\"."
                       ,local_1c,uVar3);
        }
      }
      FUN_005863d0(local_38);
    }
    if (param_1[0x12] != 0) {
      FUN_0058f210(param_1);
    }
    FUN_00484ab0(1);
  }
  local_14 = FUN_004b9ba0();
  while (local_14 != 0) {
    local_3c = (int *)0x0;
    FUN_006b7f20(&local_14,local_40,&local_3c);
    if (local_3c != (int *)0x0) {
      (**(code **)(*local_3c + 0x88))();
    }
  }
  local_18 = (int *)FUN_005f36f0();
  if (local_18 != (int *)0x0) {
    (**(code **)(*local_18 + 0x88))();
  }
  iVar4 = FUN_00401000(0x3c);
  local_8 = 0;
  if (iVar4 == 0) {
    local_50 = 0;
  }
  else {
    local_50 = FUN_006fc490(param_1);
  }
  param_1[0xf] = local_50;
  *unaff_FS_OFFSET = local_10;
  return;
}

