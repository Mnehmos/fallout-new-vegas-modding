
void __thiscall FUN_00416be0(int param_1_00,int *param_1)

{
  undefined uVar1;
  char cVar2;
  undefined4 uVar3;
  int iVar4;
  int *piVar5;
  undefined4 *puVar6;
  undefined4 local_128;
  int local_124;
  int local_120;
  int local_11c;
  undefined4 local_118;
  int local_114;
  undefined4 local_110;
  int local_10c;
  undefined4 local_108;
  int local_104;
  undefined4 local_100;
  int local_fc;
  undefined4 local_f8;
  int local_f4;
  int *local_f0;
  int local_ec;
  int local_e8;
  int local_e4;
  int local_e0;
  int local_dc;
  int local_d8;
  int local_d4;
  int local_d0;
  int local_cc;
  int local_c8;
  int local_c4;
  int local_c0;
  int local_bc;
  int local_b8;
  int local_b4;
  int local_b0;
  undefined4 local_ac;
  int *local_a8;
  int local_a4;
  undefined4 local_a0;
  int local_9c;
  int local_98;
  undefined4 local_94;
  int local_90;
  undefined4 local_8c;
  int local_88;
  undefined4 local_84;
  int local_80;
  undefined4 local_7c;
  int local_78;
  undefined4 local_74;
  int local_70;
  int local_6c;
  undefined4 local_68;
  int local_64;
  undefined4 local_60;
  int local_5c;
  undefined4 local_58;
  int local_54;
  undefined4 local_50;
  int local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  int local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined local_25;
  undefined4 local_24;
  int local_20;
  char local_19;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  FUN_0040fbf0(0);
  local_c = *(int *)(param_1_00 + 4);
  local_8 = FUN_00484e60(0xffffffff);
  do {
    if (local_c == 0) {
      FUN_0040fba0();
      return;
    }
    local_10 = FUN_0044ddc0();
    uVar1 = FUN_004f1540();
    iVar4 = local_c;
    switch(uVar1) {
    case 3:
      local_80 = local_c;
      local_7c = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_7c,local_8);
      uVar3 = FUN_004839c0(local_7c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01184118,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_80 + 0xc) = uVar3;
      if (*(int *)(local_80 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find cell water type %08X. Water data will be removed.",
                     local_7c);
        FUN_00410020(local_80,1);
      }
      break;
    case 7:
      local_88 = local_c;
      local_84 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_84,local_8);
      uVar3 = FUN_004839c0(local_84,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011840fc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_88 + 0xc) = uVar3;
      if (*(int *)(local_88 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find cell music type %08X. Music data will be removed.",
                     local_84);
        FUN_00410020(local_88,1);
      }
      break;
    case 8:
      local_64 = local_c;
      local_60 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_60,local_8);
      uVar3 = FUN_004839c0(local_60,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01184170,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_64 + 0xc) = uVar3;
      if (*(int *)(local_64 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find cell climate %08X. Climate data will be removed.",
                     local_60);
        FUN_00410020(local_64,1);
      }
      break;
    case 0x14:
      cVar2 = (**(code **)(*param_1 + 0x100))();
      if (cVar2 != '\0') {
        local_a8 = param_1;
        iVar4 = FUN_004181e0();
        if (iVar4 != 0) {
          FUN_004181e0();
          iVar4 = FUN_005f0b00();
          if (0 < iVar4) {
            uVar3 = FUN_0084e3a0();
            FUN_005b5e40("MASTERFILE: Ragdoll data found on alive actor %08X. Ragdoll data will be removed."
                         ,uVar3);
          }
        }
      }
      break;
    case 0x18:
      local_90 = local_c;
      local_8c = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_8c,local_8);
      uVar3 = FUN_004839c0(local_8c);
      *(undefined4 *)(local_90 + 0xc) = uVar3;
      if (*(int *)(local_90 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find package start location cell %08X. Package start location extra data will be removed."
                     ,local_8c);
        FUN_00410020(local_90,1);
      }
      break;
    case 0x21:
      local_4c = local_c;
      local_48 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_48,local_8);
      uVar3 = FUN_004839c0(local_48);
      *(undefined4 *)(local_4c + 0xc) = uVar3;
      if (*(int *)(local_4c + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find ownership owner form %08X. Ownership will be removed."
                     ,local_48);
        FUN_00410020(local_4c,1);
      }
      break;
    case 0x22:
      local_54 = local_c;
      local_50 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_50,local_8);
      uVar3 = FUN_004839c0(local_50,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01183ad4,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_54 + 0xc) = uVar3;
      if (*(int *)(local_54 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find ownership condition global %08X. Ownership will be removed."
                     ,local_50);
        FUN_00410020(local_54,1);
      }
      break;
    case 0x2a:
      local_20 = *(int *)(local_c + 0xc);
      local_19 = '\0';
      if (*(int *)(local_20 + 4) != 0) {
        local_24 = *(undefined4 *)(local_20 + 4);
        FUN_00485d50(&local_24,local_8);
        uVar3 = FUN_004839c0(local_24,&PTR_PTR__scalar_deleting_destructor__01183028,
                             &PTR_PTR__scalar_deleting_destructor__011841b4,0);
        uVar3 = ___RTDynamicCast(uVar3,0);
        *(undefined4 *)(local_20 + 4) = uVar3;
        if (*(int *)(local_20 + 4) == 0) {
          FUN_005b5e40("MASTERFILE: Unable to find key %08X for lock data. Lock will be removed.",
                       local_24);
          local_19 = '\x01';
        }
      }
      if (local_19 != '\0') {
        FUN_00410020(local_c,1);
      }
      break;
    case 0x2b:
      local_25 = 0;
      local_2c = *(undefined4 *)(local_c + 0xc);
      cVar2 = FUN_0043a590(param_1);
      if (cVar2 == '\0') {
        FUN_00410020(local_c,1);
      }
      break;
    case 0x2c:
      local_30 = *(undefined4 *)(local_c + 0xc);
      cVar2 = FUN_00438ef0();
      if ((cVar2 != '\0') && (cVar2 = FUN_00438ed0(), cVar2 == '\0')) {
        FUN_0044de80(0);
      }
      local_34 = FUN_0044edb0();
      if (local_34 != 0) {
        local_38 = FUN_00461630(local_34);
        FUN_00437730(local_38);
      }
      break;
    case 0x37:
      local_98 = local_c;
      local_94 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_94,local_8);
      uVar3 = FUN_004839c0(local_94,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011841cc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_98 + 0xc) = uVar3;
      if (*(int *)(local_98 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find enable state parent %08X. Enable state parent data will be removed."
                     ,local_94);
        FUN_00410020(local_98,1);
      }
      else {
        local_9c = ___RTDynamicCast(param_1,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                    &PTR_PTR__scalar_deleting_destructor__011841cc,0);
        if ((local_9c == 0) || (cVar2 = FUN_0056aac0(), cVar2 == '\0')) {
          FUN_005b5e40("MASTERFILE: Enable state parent loop detected. Parent removed.");
          FUN_00410020(local_98,1);
        }
        else {
          iVar4 = local_9c;
          FUN_005d43c0(local_9c);
          FUN_0041dcd0(iVar4);
        }
      }
      break;
    case 0x3b:
      local_a4 = local_c;
      local_a0 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_a0,local_8);
      uVar3 = FUN_004839c0(local_a0,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011841cc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_a4 + 0xc) = uVar3;
      if (*(int *)(local_a4 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find random door teleport marker %08X. Random door teleport marker data will be removed."
                     ,local_a0);
        FUN_00410020(local_a4,1);
      }
      break;
    case 0x3c:
      local_fc = local_c;
      local_f8 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_f8,local_8);
      uVar3 = FUN_004839c0(local_f8,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011841cc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_fc + 0xc) = uVar3;
      if (*(int *)(local_fc + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find merchant container %08X. Merchant container data will be removed."
                     ,local_f8);
        FUN_00410020(local_fc,1);
      }
      break;
    case 0x3f:
      local_5c = local_c;
      local_58 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_58,local_8);
      uVar3 = FUN_004839c0(local_58,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011830cc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_5c + 0xc) = uVar3;
      if (*(int *)(local_5c + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find poison %08X. Poison data will be removed.",local_58
                    );
        FUN_00410020(local_5c,1);
      }
      break;
    case 0x44:
      local_104 = local_c;
      local_100 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_100,local_8);
      uVar3 = FUN_004839c0(local_100,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011841cc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_104 + 0xc) = uVar3;
      if (*(int *)(local_104 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find XMarker target %08X. XMarker target data will be removed."
                     ,local_100);
        FUN_00410020(local_104,1);
      }
      break;
    case 0x51:
      local_b0 = local_c;
      local_ac = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_ac,local_8);
      uVar3 = FUN_004839c0(local_ac,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011841cc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_b0 + 0xc) = uVar3;
      if (*(int *)(local_b0 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find linked reference %08X. Linked reference data will be removed."
                     ,local_ac);
        FUN_00410020(local_b0,1);
      }
      else {
        piVar5 = param_1;
        FUN_005d43c0(param_1);
        FUN_0041e530(piVar5);
      }
      break;
    case 0x53:
      local_e4 = local_c;
      local_e8 = local_c + 0xc;
      local_e0 = 0;
      while ((local_e8 != 0 && (cVar2 = FUN_008256d0(), cVar2 == '\0'))) {
        puVar6 = (undefined4 *)FUN_006815c0();
        local_f0 = (int *)*puVar6;
        local_ec = *local_f0;
        FUN_00485d50(&local_ec,local_8);
        uVar3 = FUN_004839c0(local_ec,&PTR_PTR__scalar_deleting_destructor__01183028,
                             &PTR_PTR__scalar_deleting_destructor__011841cc,0);
        iVar4 = ___RTDynamicCast(uVar3,0);
        *local_f0 = iVar4;
        if (*local_f0 == 0) {
          FUN_005b5e40("MASTERFILE: Unable to find activate reference %08X.",local_ec);
          if (local_e0 == 0) {
            FUN_0063f7b0();
          }
          else {
            FUN_00905330(&local_f0);
            local_e8 = FUN_00726070();
          }
          FUN_00401030(local_f0);
        }
        else {
          piVar5 = param_1;
          FUN_005d43c0(param_1);
          FUN_0041edd0(piVar5);
          local_e0 = local_e8;
          local_e8 = FUN_00726070();
        }
      }
      cVar2 = FUN_008256d0();
      if (((cVar2 != '\0') && (*(char *)(local_e4 + 0x14) == '\0')) &&
         (iVar4 = FUN_004048e0(), iVar4 == 0)) {
        FUN_005b5e40("MASTERFILE: Removing empty activate parent extra.");
        FUN_00410020(local_e4,1);
      }
      break;
    case 0x57:
      local_f4 = local_c;
      FUN_00433db0(param_1);
      cVar2 = FUN_008256d0();
      if (cVar2 != '\0') {
        FUN_005b5e40("MASTERFILE: Removing empty decal extra.");
        FUN_00410020(local_f4,1);
      }
      break;
    case 0x59:
      local_6c = local_c;
      local_68 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_68,local_8);
      uVar3 = FUN_004839c0(local_68,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01184154,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_6c + 0xc) = uVar3;
      if (*(int *)(local_6c + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find cell imagespace %08X. ImageSpace data will be removed."
                     ,local_68);
        FUN_00410020(local_6c,1);
      }
      break;
    case 99:
      local_11c = local_c;
      local_118 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_118,local_8);
      uVar3 = FUN_004839c0(local_118,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011841cc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_11c + 0xc) = uVar3;
      if (*(int **)(local_11c + 0xc) == param_1) {
        *(undefined4 *)(local_11c + 0xc) = 0;
      }
      if (*(int *)(local_11c + 0xc) == 0) {
        uVar3 = FUN_0084e3a0();
        FUN_005b5e40("MASTERFILE: Unable to find multibound ref %08X used by reference %08X. Multibound ref data will be removed."
                     ,local_118,uVar3);
        FUN_00410020(local_11c,1);
      }
      break;
    case 0x66:
      local_120 = local_c;
      FUN_00433ed0(param_1);
      cVar2 = FUN_008256d0();
      if (cVar2 != '\0') {
        FUN_005b5e40("MASTERFILE: Removing empty reflector water extra.");
        FUN_00410020(local_120,1);
      }
      break;
    case 0x67:
      local_114 = local_c;
      local_110 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_110,local_8);
      uVar3 = FUN_004839c0(local_110);
      *(undefined4 *)(local_114 + 0xc) = uVar3;
      if (((*(int *)(local_114 + 0xc) != 0) && (iVar4 = FUN_00401170(), iVar4 != 0x1e)) &&
         (iVar4 != 0x37)) {
        *(undefined4 *)(local_114 + 0xc) = 0;
      }
      if (*(int *)(local_114 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find emittance source %08X. Emittance source data will be removed."
                     ,local_110);
        FUN_00410020(local_114,1);
      }
      break;
    case 0x68:
      local_14 = local_c + 0xc;
      local_18 = *(int *)(local_c + 0x18);
      if (local_18 != 0) {
        uVar3 = FUN_00484e60(0xffffffff);
        FUN_00485d50(&local_18,uVar3);
        uVar3 = FUN_004839c0(local_18,&PTR_PTR__scalar_deleting_destructor__01183028,
                             &PTR_PTR__scalar_deleting_destructor__011841cc,0);
        uVar3 = ___RTDynamicCast(uVar3,0);
        *(undefined4 *)(local_14 + 0xc) = uVar3;
        if (*(int *)(local_14 + 0xc) == 0) {
          FUN_005b5e40("MASTERFILE: Could not find radio range position ref (%08X).",local_18);
        }
        else {
          cVar2 = FUN_00575d10();
          if (cVar2 != '\0') {
            FUN_005b5e40("MASTERFILE: Invalid radio range position ref (%08X). Exteriors only.",
                         local_18);
          }
        }
      }
      break;
    case 0x6e:
      local_128 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_128,local_8);
      uVar3 = FUN_004839c0(local_128,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011840c4,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(iVar4 + 0xc) = uVar3;
      if (*(int *)(iVar4 + 0xc) == 0) {
        FUN_005b5e40("Unable to find ammo %08X. Ammo data will be removed.",local_128);
        FUN_00410020(iVar4,1);
      }
      break;
    case 0x6f:
      iVar4 = FUN_0041fe90();
      if (iVar4 != 0) {
        FUN_0067c6c0(param_1);
      }
      break;
    case 0x74:
      local_10c = local_c;
      local_108 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_108,local_8);
      uVar3 = FUN_004839c0(local_108,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__011840dc,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_10c + 0xc) = uVar3;
      if (*(int *)(local_10c + 0xc) == 0) {
        FUN_005b5e40("Unable to find encounter zone %08X. Encounter zone data will be removed.",
                     local_108);
        FUN_00410020(local_10c,1);
      }
      break;
    case 0x76:
      local_b4 = local_c;
      for (local_b8 = 0; local_b8 < 4; local_b8 = local_b8 + 1) {
        local_c0 = 0;
        FUN_00485d50(&local_c0,local_8);
        uVar3 = FUN_004839c0(local_c0,&PTR_PTR__scalar_deleting_destructor__01183028,
                             &PTR_PTR__scalar_deleting_destructor__011841cc,0);
        uVar3 = ___RTDynamicCast(uVar3,0);
        *(undefined4 *)(*(int *)(local_b4 + 0xc) + local_b8 * 4) = uVar3;
        if ((local_c0 != 0) && (*(int *)(*(int *)(local_b4 + 0xc) + local_b8 * 4) == 0)) {
          FUN_005b5e40("MASTERFILE: Unable to find occlusion plane reference %08X. Occlusion plane reference data will be removed."
                       ,local_c0);
          FUN_00410020(local_b4,1);
          break;
        }
        local_bc = FUN_00422120();
        if (local_bc == 0) {
          FUN_005b5e40("No occlusion plane for occlusion plane ref extra.");
        }
        else if (*(int *)(*(int *)(local_b4 + 0xc) + local_b8 * 4) != 0) {
          FUN_005d43c0();
          uVar3 = FUN_00422120();
          FUN_004181c0(local_b8,uVar3);
        }
      }
      break;
    case 0x77:
      local_c4 = local_c;
      for (local_c8 = 0; local_c8 < 2; local_c8 = local_c8 + 1) {
        local_cc = *(int *)(*(int *)(local_c4 + 0xc) + local_c8 * 4);
        FUN_00485d50(&local_cc,local_8);
        uVar3 = FUN_004839c0(local_cc,&PTR_PTR__scalar_deleting_destructor__01183028,
                             &PTR_PTR__scalar_deleting_destructor__011841cc,0);
        uVar3 = ___RTDynamicCast(uVar3,0);
        *(undefined4 *)(*(int *)(local_c4 + 0xc) + local_c8 * 4) = uVar3;
        if ((local_cc != 0) && (*(int *)(*(int *)(local_c4 + 0xc) + local_c8 * 4) == 0)) {
          FUN_005b5e40("MASTERFILE: Unable to find portal linked reference %08X. Portal linked reference data will be removed."
                       ,local_cc);
          FUN_00410020(local_c4,1);
          break;
        }
      }
      if (**(int **)(local_c4 + 0xc) == *(int *)(*(int *)(local_c4 + 0xc) + 4)) {
        if (**(int **)(local_c4 + 0xc) == 0) {
          uVar3 = FUN_0084e3a0();
          FUN_005b5e40("MASTERFILE: Both of portal %08X\'s linked rooms are NULL.",uVar3);
        }
        else {
          uVar3 = FUN_0084e3a0();
          uVar3 = FUN_0084e3a0(uVar3);
          FUN_005b5e40("MASTERFILE: Both of portal %08X\'s linked rooms are the same (%08X). Attempting to fix."
                       ,uVar3);
          *(undefined4 *)(*(int *)(local_c4 + 0xc) + 4) = 0;
        }
      }
      if (**(int **)(local_c4 + 0xc) != 0) {
        piVar5 = param_1;
        FUN_005d43c0(param_1);
        FUN_00420ce0(piVar5);
      }
      if (*(int *)(*(int *)(local_c4 + 0xc) + 4) != 0) {
        piVar5 = param_1;
        FUN_005d43c0(param_1);
        FUN_00420ce0(piVar5);
      }
      break;
    case 0x7b:
      local_d4 = local_c;
      local_d0 = *(int *)(local_c + 0xc) + 8;
      while( true ) {
        if ((local_d0 == 0) || (piVar5 = (int *)FUN_006815c0(), *piVar5 == 0))
        goto switchD_00416c66_caseD_4;
        piVar5 = (int *)FUN_006815c0();
        local_dc = *piVar5;
        FUN_00485d50(&local_dc,local_8);
        uVar3 = FUN_004839c0(local_dc,&PTR_PTR__scalar_deleting_destructor__01183028,
                             &PTR_PTR__scalar_deleting_destructor__011841cc,0);
        local_d8 = ___RTDynamicCast(uVar3,0);
        if ((local_dc != 0) && (local_d8 == 0)) break;
        if (local_dc != 0) {
          FUN_00726c60(&local_d8);
        }
        local_d0 = FUN_00726070();
      }
      FUN_005b5e40("MASTERFILE: Unable to find room linked reference %08X. Room linked reference data will be removed."
                   ,local_dc);
      FUN_00410020(local_d4,1);
      break;
    case 0x81:
      local_78 = local_c;
      local_74 = *(undefined4 *)(local_c + 0xc);
      FUN_00485d50(&local_74,local_8);
      uVar3 = FUN_004839c0(local_74,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__01184134,0);
      uVar3 = ___RTDynamicCast(uVar3,0);
      *(undefined4 *)(local_78 + 0xc) = uVar3;
      if (*(int *)(local_78 + 0xc) == 0) {
        FUN_005b5e40("MASTERFILE: Unable to find cell acoustic space %08X. AcousticSpace data will be removed."
                     ,local_74);
        FUN_00410020(local_78,1);
      }
      break;
    case 0x85:
      local_124 = local_c;
      FUN_00434050(param_1);
      cVar2 = FUN_008256d0();
      if (cVar2 != '\0') {
        FUN_005b5e40("MASTERFILE: Removing empty lit water extra.");
        FUN_00410020(local_124,1);
      }
      break;
    case 0x8c:
      local_70 = local_c;
      if (*(int *)(local_c + 0xc) != 0) {
        FUN_0058f210(param_1);
      }
      break;
    case 0x90:
      local_40 = *(undefined4 *)(local_c + 0xc);
      local_3c = FUN_0059bb30();
      uVar3 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_3c,uVar3);
      uVar3 = FUN_004839c0(local_3c,&PTR_PTR__scalar_deleting_destructor__01183028,
                           &PTR_PTR__scalar_deleting_destructor__0118418c,0);
      iVar4 = ___RTDynamicCast(uVar3,0);
      if (iVar4 == 0) {
        FUN_005b5e40("MASTERFILE: Could not find MediaLocationController (%08X) for a AudioMarker in extra data list."
                     ,local_3c);
      }
      else {
        FUN_007037c0(local_3c);
      }
      break;
    case 0x91:
      local_44 = *(undefined4 *)(local_c + 0xc);
    }
switchD_00416c66_caseD_4:
    local_c = local_10;
  } while( true );
}

