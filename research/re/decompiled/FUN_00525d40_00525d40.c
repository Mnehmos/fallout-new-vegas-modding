
/* WARNING: Function: __alloca_probe_16 replaced with injection: alloca_probe */

void FUN_00525d40(undefined4 param_1)

{
  char cVar1;
  int local_1c;
  int *local_18;
  uint local_14;
  undefined *local_10;
  int local_c;
  char local_5;
  
  local_14 = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  local_5 = FUN_00472660();
  if (local_5 == 'a') {
    FUN_00485110(param_1);
    FUN_00484ab0(0);
    do {
      local_c = FUN_004726b0();
      if (local_c == 0) break;
      local_1c = local_c;
      if (local_c == 0x41544144) {
        FUN_00472890(local_18 + 6,8);
        cVar1 = FUN_00401680();
        if (cVar1 != '\0') {
          FUN_00503210();
        }
      }
      else if (local_c == 0x44494445) {
        FUN_00401660();
        local_10 = (undefined *)&local_1c;
        FUN_00472890(&local_1c,0x200);
        (**(code **)(*local_18 + 0x134))(local_10);
      }
      else if (local_c == 0x444e424f) {
        (**(code **)(*local_18 + 0xe0))(param_1);
      }
      cVar1 = FUN_004726f0();
    } while (cVar1 != '\0');
  }
  ___security_check_cookie_4();
  return;
}

