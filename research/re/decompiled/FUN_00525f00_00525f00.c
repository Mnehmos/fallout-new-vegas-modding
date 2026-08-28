
void __fastcall FUN_00525f00(int *param_1)

{
  char cVar1;
  undefined4 uVar2;
  int local_c;
  int local_8;
  
  cVar1 = FUN_004013e0();
  if (cVar1 == '\0') {
    if (param_1[6] != 0) {
      local_c = param_1[6];
      uVar2 = FUN_00484e60(0xffffffff);
      FUN_00485d50(&local_c,uVar2);
      local_8 = FUN_004839c0(local_c);
      if (local_8 == 0) {
        uVar2 = FUN_0084e3a0();
        uVar2 = (**(code **)(*param_1 + 0x130))(uVar2);
        FUN_005b5e40("Unable to find owner form (%08X) on encounter zone \'%s\' (%08X).",local_c,
                     uVar2);
      }
      param_1[6] = local_8;
    }
    FUN_00484ab0(1);
  }
  return;
}

