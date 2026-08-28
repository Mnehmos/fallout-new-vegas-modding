
/* WARNING: Function: __alloca_probe_16 replaced with injection: alloca_probe */

void FUN_004fd6f0(undefined4 param_1)

{
  char cVar1;
  int iVar2;
  int *local_34;
  int *local_30;
  int *local_2c;
  undefined *local_28;
  int local_24;
  int *local_20;
  uint local_1c;
  uint local_18;
  undefined *local_14;
  undefined *local_10;
  int local_c;
  char local_5;
  
  local_1c = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  local_5 = FUN_00472660();
  if (local_5 == '3') {
    (**(code **)(*local_20 + 0x18))();
    FUN_00485110(param_1);
    FUN_00484ab0(0);
    do {
      local_c = FUN_004726b0();
      if (local_c == 0) break;
      local_24 = local_c;
      if (local_c < 0x44545345) {
        if (local_c == 0x44545344) {
LAB_004fd8c5:
          if (local_20 == (int *)0x0) {
            local_34 = (int *)0x0;
          }
          else {
            local_34 = local_20 + 0x16;
          }
          FUN_004781e0(local_34,param_1);
        }
        else if (local_c < 0x41544145) {
          if (local_c == 0x41544144) {
            FUN_004861f0(param_1,local_20 + 0x18,0x54);
          }
          else if (local_c == 0x314d414e) {
            iVar2 = FUN_00401660();
            if (iVar2 != 0) {
              FUN_00401660();
              local_14 = (undefined *)&local_34;
              FUN_00472890(&local_34,0);
              (**(code **)(local_20[0x2d] + 0x18))(local_14);
            }
          }
          else if ((local_c == 0x324d414e) && (iVar2 = FUN_00401660(), iVar2 != 0)) {
            FUN_004893e0(local_20 + 0x2d,param_1);
          }
        }
        else if (local_c == 0x44494445) {
          FUN_00401660();
          local_28 = (undefined *)&local_34;
          local_10 = (undefined *)&local_34;
          FUN_00472890(&local_34,0x200);
          (**(code **)(*local_20 + 0x134))(local_10);
        }
        else if (local_c == 0x444e424f) {
          (**(code **)(*local_20 + 0xe0))(param_1);
        }
      }
      else if (local_c < 0x4d414e57) {
        if (local_c == 0x4d414e56) {
          FUN_004727f0(&local_18);
          if (local_18 < 4) {
            local_20[0x33] = local_18;
          }
          else {
            local_20[0x33] = 1;
          }
        }
        else {
          if (local_c == 0x4c444f4d) goto LAB_004fd898;
          if (local_c == 0x4c4c5546) {
            if (local_20 == (int *)0x0) {
              local_2c = (int *)0x0;
            }
            else {
              local_2c = local_20 + 0xc;
            }
            FUN_00487050(local_2c,param_1);
          }
        }
      }
      else if (local_c == 0x54444f4d) {
LAB_004fd898:
        if (local_20 == (int *)0x0) {
          local_30 = (int *)0x0;
        }
        else {
          local_30 = local_20 + 0xf;
        }
        FUN_004892d0(local_30,param_1);
      }
      else if (local_c == 0x54534544) goto LAB_004fd8c5;
      if ((local_c == 0x41544144) && (cVar1 = FUN_00401680(), cVar1 != '\0')) {
        FUN_004fccf0();
      }
      cVar1 = FUN_004726f0();
    } while (cVar1 != '\0');
  }
  ___security_check_cookie_4();
  return;
}

