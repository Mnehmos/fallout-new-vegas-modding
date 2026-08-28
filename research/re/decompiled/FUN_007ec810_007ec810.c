
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_007ec810(int *param_1)

{
  char cVar1;
  undefined uVar2;
  uint uVar3;
  int iVar4;
  int *piVar5;
  float *pfVar6;
  char *pcVar7;
  uint uVar8;
  int *unaff_FS_OFFSET;
  float10 fVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  undefined *puVar14;
  undefined8 uVar15;
  ulonglong uVar16;
  undefined local_2d1;
  float local_2cc;
  undefined4 local_2bc;
  int local_2b8;
  undefined4 local_2b0;
  int *local_2a8;
  char local_2a0;
  char local_290;
  char local_278;
  int local_274;
  undefined local_250 [12];
  undefined local_244 [12];
  undefined local_238 [12];
  undefined local_22c [12];
  int local_220;
  int *local_21c;
  undefined4 local_20c;
  undefined4 local_1f0;
  int local_1e0;
  int local_1dc;
  char local_1d5;
  int local_1d4;
  int local_1d0;
  undefined4 local_1cc;
  int local_1c8;
  float local_1c4;
  int local_1c0;
  int local_1bc;
  float local_1b8;
  int local_1b4;
  undefined4 local_1b0;
  float local_1ac;
  char local_1a5;
  float local_1a4;
  float local_1a0;
  int local_19c;
  int *local_198;
  undefined4 local_194;
  int local_190;
  int local_18c;
  byte local_185;
  int local_184;
  char local_17e;
  char local_17d;
  float local_17c;
  int local_178;
  float local_174;
  undefined4 local_170;
  undefined4 local_16c;
  undefined4 local_168;
  float local_164;
  char local_160 [260];
  uint local_5c;
  float local_58;
  float local_54;
  float local_50;
  float local_4c;
  undefined4 local_48;
  int local_44;
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  char local_2d;
  float local_2c;
  int local_28;
  uint local_24;
  int local_20;
  uint local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00f0f6bc;
  local_10 = *unaff_FS_OFFSET;
  uVar3 = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  *unaff_FS_OFFSET = (int)&local_10;
  local_5c = uVar3;
  if ((*(char *)((int)param_1 + 0xfb) != '\0') || (iVar4 = FUN_00a09030(), iVar4 != 0))
  goto LAB_007eeb26;
  if ((DAT_011f21cc == (int *)0x0) ||
     (((iVar4 = (**(code **)(*DAT_011f21cc + 0x1d0))(uVar3), iVar4 == 0 ||
       (cVar1 = (**(code **)(*DAT_011f21cc + 0x22c))(), cVar1 != '\0')) ||
      (cVar1 = (**(code **)(*DAT_011dea3c + 0x22c))(), cVar1 != '\0')))) {
    FUN_007ebd50();
    goto LAB_007eeb26;
  }
  if ((((DAT_011db0d4 == 0) || (iVar4 = FUN_0044ddc0(), iVar4 == 0)) ||
      (iVar4 = FUN_0044ddc0(), iVar4 == 4)) || (cVar1 = FUN_00702450(), cVar1 == '\0')) {
    cVar1 = FUN_00702450();
    if ((cVar1 == '\0') && (DAT_011a0b68 != '\0')) {
      DAT_011a0b68 = '\0';
      uVar15 = 0xffffffff;
      uVar12 = 0;
      FUN_00705910(0,0xffffffff,0);
      FUN_00800ac0(uVar12,uVar15);
    }
    FUN_00a07dc0();
    FUN_0073ac90();
    FUN_00a07dc0();
    FUN_00a07dc0();
    goto LAB_007eeb26;
  }
  FUN_007f3c90();
  FUN_006815c0();
  piVar5 = (int *)FUN_006815c0();
  if (*(int *)(*piVar5 + 0x30) == 0) {
    FUN_007f3c90();
    FUN_007f6e50();
  }
  if (DAT_011a0b68 == '\0') {
    FUN_007ec3a0();
  }
  DAT_011a0b68 = '\x01';
  cVar1 = FUN_00703d50();
  if (cVar1 != '\0') goto LAB_007eeb26;
  FUN_007f07a0();
  local_14 = FUN_00877720();
  FUN_004b7210();
  cVar1 = FUN_004b71d0();
  if (cVar1 != '\0') {
    iVar4 = FUN_0044ddc0();
    local_40 = (-(uint)(iVar4 != 1) & 0x348) + 0x1ea9;
    local_48 = FUN_00a23390(0,7);
    local_3c = FUN_00a23390(0,8);
    local_38 = FUN_00a23390(0,9);
    local_44 = FUN_00a23390(0,10);
    local_3c = -local_3c;
    local_44 = -local_44;
    if (local_38 < 0x21f2) {
      if (local_38 < -0x21f1) {
        if (*(char *)((int)param_1 + 0x10f) == '\0') {
          iVar4 = FUN_00825c00();
          param_1[0x45] = iVar4;
          *(undefined *)((int)param_1 + 0x10f) = 1;
        }
      }
      else {
        iVar4 = FUN_00ec7d40();
        if ((iVar4 < 0x21f1) && (iVar4 = FUN_00ec7d40(), iVar4 < 0x21f1)) {
          cVar1 = FUN_007f4c00();
          if (cVar1 == '\0') {
            if (*(char *)(param_1 + 0x44) == '\0') {
              cVar1 = FUN_007f4bb0();
              if (cVar1 == '\0') {
                if (*(char *)((int)param_1 + 0x10f) != '\0') {
                  (**(code **)(*param_1 + 0xc))(2,0);
                }
              }
              else {
                *(undefined *)(DAT_011db0d4 + 0x10f) = 0;
                (**(code **)(*param_1 + 0xc))(2,0);
              }
            }
            else {
              (**(code **)(*param_1 + 0xc))(3,0);
            }
          }
          else {
            *(undefined *)(DAT_011db0d4 + 0x110) = 0;
            (**(code **)(*param_1 + 0xc))(3,0);
          }
          *(undefined *)((int)param_1 + 0x10d) = 1;
        }
      }
    }
    else if (*(char *)(param_1 + 0x44) == '\0') {
      iVar4 = FUN_00825c00();
      param_1[0x45] = iVar4;
      *(undefined *)(param_1 + 0x44) = 1;
    }
  }
  if ((DAT_011f21cc == (int *)0x0) ||
     (cVar1 = (**(code **)(*DAT_011f21cc + 0x100))(), cVar1 == '\0')) {
    FUN_00700320(0xfa3,0);
    FUN_00700320(0xfa3,0);
    FUN_00700320(0xfa3,0);
    FUN_00700320(0xfa3,0);
    FUN_00700320(0xfa3,0);
  }
  else {
    iVar4 = (**(code **)(DAT_011f21cc[0x29] + 0x1c))();
    local_164 = (float)iVar4;
    iVar4 = (**(code **)(DAT_011f21cc[0x29] + 8))(0x10);
    local_54 = (float)iVar4;
    local_4c = 0.0;
    if ((float)_DAT_01012060 < local_164) {
      local_4c = local_54 / local_164;
    }
    cVar1 = (**(code **)(*DAT_011f21cc + 0x22c))(0);
    if (cVar1 == '\0') {
      FUN_00774b00(param_1[0x24],param_1[0x26],local_4c - (float)param_1[0x3f],local_4c,2,2);
    }
    else {
      FUN_00774b00(param_1[0x24],param_1[0x26],local_4c - (float)param_1[0x3f],local_4c,2,0);
    }
    uVar10 = 1;
    uVar12 = FUN_0055d520();
    FUN_00a01350(0xfc4,uVar12,uVar10);
    FUN_00700320(0xfa3,1);
    FUN_00700320(0xfa3,1);
    FUN_00700320(0xfa3,1);
    FUN_00700320(0xfa3,1);
    FUN_00700320(0xfa3,1);
    fVar9 = (float10)FUN_007700f0(DAT_011dea3c,DAT_011f21cc);
    local_50 = (float)fVar9;
    local_58 = 0.0;
    FUN_005e58f0(0x2f,DAT_011dea3c,&local_58);
    if (local_58 <= (float)_DAT_01012060) {
      uVar10 = 1;
      uVar12 = FUN_0055d520();
      FUN_00a01350(0xfc4,uVar12,uVar10);
    }
    else {
      uVar12 = FUN_00403df0((double)local_50);
      uVar12 = FUN_00ec62c0(uVar12);
      uVar12 = FUN_00403df0(uVar12);
      uVar12 = FUN_0055d520(uVar12);
      _sprintf(local_160,"%s\n %s:%d %s:%.2f",uVar12);
      FUN_00a01350(0xfc4,local_160,1);
    }
    iVar4 = FUN_00967090();
    if ((iVar4 == 0) || (iVar4 = FUN_00967090(), *(char *)(iVar4 + 4) == '\0')) {
      FUN_00700320(0xff4,1);
      FUN_00700320(0xff4,1);
      FUN_00700320(0xff4,1);
      FUN_00700320(0xff4,1);
      FUN_00700320(0xff4,1);
    }
    else {
      FUN_00700320(0xff4,2);
      FUN_00700320(0xff4,2);
      FUN_00700320(0xff4,2);
      FUN_00700320(0xff4,2);
      FUN_00700320(0xff4,2);
    }
  }
  uVar12 = (**(code **)(DAT_011dea3c[0x29] + 0x1c))();
  iVar4 = FUN_00647b70(0,uVar12);
  local_2c = (float)iVar4;
  if ((NAN(local_2c) || NAN((float)_DAT_01012060)) == (local_2c == (float)_DAT_01012060)) {
    uVar12 = (**(code **)(DAT_011dea3c[0x29] + 8))();
    iVar4 = FUN_00647b70(0,uVar12);
    local_2c = (float)iVar4 / local_2c;
  }
  FUN_007748b0(param_1[0x1c],local_2c,0,0,0);
  FUN_00779070(param_1[0x21],param_1[0x1e],param_1[0x1f],param_1[0x20]);
  local_1c = FUN_00a24f10();
  local_18 = (int)local_1c >> 0x10;
  local_34 = (int)(local_1c & 0xff00) >> 8;
  local_24 = local_1c & 0xff;
  iVar4 = FUN_0044ddc0();
  if (iVar4 != 4) {
    iVar4 = FUN_00a24660(0x10,1);
    if ((iVar4 == 0) || (iVar4 = FUN_0044ddc0(), iVar4 == 1)) {
      iVar4 = FUN_00a24660(0x10,0);
      if ((iVar4 == 0) && (iVar4 = FUN_0044ddc0(), iVar4 == 1)) {
        FUN_009c6c30(2,0);
        *(undefined *)((int)param_1 + 0xfa) = 1;
      }
    }
    else {
      cVar1 = FUN_004b71d0();
      if ((cVar1 == '\0') || (((local_24 != 10 && (local_24 != 0xb)) && (local_24 != 0x11)))) {
        FUN_009c6c30(1,0);
        *(undefined *)((int)param_1 + 0xfa) = 0;
      }
    }
  }
  uVar15 = 0;
  uVar12 = 0;
  fVar9 = (float10)FUN_0084d030(0,0,0);
  FUN_009445b0((float)fVar9,uVar12,uVar15);
  cVar1 = FUN_00709d40();
  if (((cVar1 != '\0') &&
      ((iVar4 = FUN_00717a40(10,1), iVar4 == 1 || (iVar4 = FUN_00717a40(6,1), iVar4 == 1)))) ||
     ((iVar4 = FUN_00a23a50(1,1), iVar4 != 0 && (local_34 != 1)))) {
    FUN_004b7210();
    cVar1 = FUN_004b71d0();
    if ((cVar1 != '\0') || (*(char *)((int)param_1 + 0x10e) != '\0')) {
      FUN_004b7210();
      cVar1 = FUN_004b71d0();
      if ((cVar1 == '\0') || (iVar4 = FUN_00717a40(10,1), iVar4 != 1)) goto LAB_007ed343;
    }
    iVar4 = FUN_0044ddc0();
    if ((iVar4 == 2) && (*(char *)(param_1 + 0x3e) != '\0')) {
      FUN_007efa10(0,0,0);
      fVar9 = (float10)FUN_007f48e0();
      *(float *)(DAT_011db0d4 + 0xfc) = (float)fVar9;
    }
    FUN_007f0ea0();
  }
LAB_007ed343:
  cVar1 = FUN_007f3e00();
  if (cVar1 == '\0') goto LAB_007eeb26;
  piVar5 = (int *)FUN_008d8520();
  local_20 = (**(code **)(*piVar5 + 0x148))();
  if (local_20 == 0) {
    local_274 = 0;
  }
  else {
    local_274 = FUN_0044ddc0();
  }
  local_28 = local_274;
  if (local_274 == 0) {
    local_278 = '\0';
  }
  else {
    local_278 = FUN_00474a80();
  }
  local_2d = local_278;
  FUN_007f3070();
  iVar4 = FUN_0044ddc0();
  if (iVar4 == 4) goto LAB_007eeb26;
  DAT_011dea34 = 0;
  FUN_00964260();
  FUN_0084d030();
  FUN_008d3550();
  uVar10 = 0;
  uVar12 = (**(code **)(*DAT_011dea3c + 0x1e4))();
  FUN_008885e0(uVar12,uVar10);
  FUN_0094ae40(0,0);
  FUN_00950290();
  FUN_007ec3a0();
  local_16c = FUN_004b7210();
  local_168 = FUN_00747d00();
  local_170 = FUN_0073b020();
  if ((DAT_011db194 & 1) == 0) {
    DAT_011db194 = DAT_011db194 | 1;
    local_8 = 0;
    FUN_00715d40();
    _DAT_011db190 = FUN_00ec62c0();
    local_8 = 0xffffffff;
  }
  if ((DAT_011db194 & 2) == 0) {
    DAT_011db194 = DAT_011db194 | 2;
    local_8 = 1;
    FUN_00715da0();
    _DAT_011db18c = FUN_00ec62c0();
    local_8 = 0xffffffff;
  }
  if ((DAT_011db194 & 4) == 0) {
    DAT_011db194 = DAT_011db194 | 4;
    local_8 = 2;
    FUN_007177c0();
    _DAT_011db188 = FUN_00ec62c0();
    local_8 = 0xffffffff;
  }
  if ((DAT_011db194 & 8) == 0) {
    DAT_011db194 = DAT_011db194 | 8;
    local_8 = 3;
    FUN_00717820();
    _DAT_011db184 = FUN_00ec62c0();
    local_8 = 0xffffffff;
  }
  iVar4 = FUN_00a24180(0x12,0);
  if ((iVar4 != 0) && (local_18 != 0x12)) {
LAB_007ed5d8:
    FUN_00705780();
    goto LAB_007eeb26;
  }
  FUN_004b7210();
  cVar1 = FUN_004b71d0();
  if ((cVar1 != '\0') && (iVar4 = FUN_00717a40(9,1), iVar4 == 2)) {
    FUN_006815c0();
    iVar4 = FUN_005ae380();
    if ((iVar4 != 0) && (iVar4 = FUN_0044ddc0(), iVar4 == 2)) goto LAB_007ed5d8;
  }
  local_178 = 0;
  if (DAT_011f21cc == (int *)0x0) {
    DAT_011db180 = 0;
  }
  else {
    cVar1 = FUN_007eeb50(1,0,local_34);
    if (cVar1 == '\0') {
      cVar1 = FUN_007eeb50(2,0,local_34);
      if (cVar1 == '\0') {
        cVar1 = FUN_007eeb50(3,0,local_34);
        if (cVar1 == '\0') {
          if ((DAT_011db180 != 0) && (cVar1 = FUN_007eeb50(DAT_011db180,1,local_34), cVar1 == '\0'))
          {
            DAT_011db180 = 0;
          }
        }
        else {
          local_178 = 3;
          DAT_011db180 = 3;
        }
      }
      else {
        local_178 = 2;
        DAT_011db180 = 2;
      }
    }
    else {
      local_178 = 1;
      DAT_011db180 = 1;
    }
  }
  DAT_011db0b2 = 0;
  DAT_011db0b3 = 0;
  cVar1 = FUN_00a040a0();
  if (cVar1 == '\0') {
    if (local_178 == 2) {
      local_178 = 0;
    }
  }
  else if ((float)param_1[0x38] < _DAT_011db0b8 == (NAN((float)param_1[0x38]) || NAN(_DAT_011db0b8))
          ) {
    FUN_00700320(0xfaf,1);
  }
  else {
    FUN_00700320(0xfaf,0);
  }
  cVar1 = FUN_00a040a0();
  if (cVar1 == '\0') {
    if (local_178 == 3) {
      local_178 = 0;
    }
  }
  else if ((float)param_1[0x38] < _DAT_011db0c0 == (NAN((float)param_1[0x38]) || NAN(_DAT_011db0c0))
          ) {
    FUN_00700320(0xfaf,1);
  }
  else {
    FUN_00700320(0xfaf,0);
  }
  fVar9 = (float10)FUN_0066dce0(local_28,1,0);
  local_174 = (float)fVar9;
  if (local_178 == 2) {
    local_17c = _DAT_011db0b8;
  }
  else {
    local_17c = local_174;
    if (local_178 == 3) {
      local_17c = _DAT_011db0c0;
    }
  }
  if (DAT_011db180 == 2) {
    local_174 = _DAT_011db0b8;
  }
  else if (DAT_011db180 == 3) {
    local_174 = _DAT_011db0c0;
  }
  cVar1 = FUN_009526b0();
  if (cVar1 != '\0') {
    local_17c = 0.0;
    local_174 = 0.0;
  }
  FUN_007f28d0();
  if ((DAT_011db194 & 0x10) == 0) {
    DAT_011db194 = DAT_011db194 | 0x10;
    local_8 = 4;
    _DAT_011db17c = FUN_00a00940("_Brightness",0xffffffff);
    local_8 = 0xffffffff;
  }
  if (((DAT_011f21cc == (int *)0x0) ||
      ((float)param_1[0x38] < local_174 == (NAN((float)param_1[0x38]) || NAN(local_174)))) ||
     (DAT_011db180 == 0)) {
    FUN_00774b00(param_1[0x13],param_1[0x14],
                 ((float)param_1[0x38] - local_174) / (float)param_1[0x39],
                 (float)param_1[0x38] / (float)param_1[0x39],1,0);
    FUN_00700320(0xfa3,0);
  }
  else {
    FUN_00774b00(param_1[0x13],param_1[0x14],local_174 / (float)param_1[0x39],0,1,0);
  }
  if ((DAT_011f21cc == (int *)0x0) || (local_178 == 0)) {
    FUN_004b7210();
    cVar1 = FUN_004b71d0();
    if (((cVar1 == '\0') &&
        ((iVar4 = FUN_00a24180(0x1e,1), iVar4 != 0 && (iVar4 = FUN_00a24180(0x1e,3), iVar4 != 0))))
       && (local_18 != 0x1e)) {
      (**(code **)(*param_1 + 0xc))(2,0);
    }
    else {
      FUN_004b7210();
      cVar1 = FUN_004b71d0();
      if ((((cVar1 == '\0') && (iVar4 = FUN_00a24180(0x20,1), iVar4 != 0)) &&
          (iVar4 = FUN_00a24180(0x20,3), iVar4 != 0)) && (local_18 != 0x20)) {
        (**(code **)(*param_1 + 0xc))(3,0);
      }
    }
    goto LAB_007eeb26;
  }
  cVar1 = FUN_004b71d0();
  if ((cVar1 == '\0') && (cVar1 = FUN_007f6af0(), cVar1 != '\0')) {
    local_290 = '\x01';
  }
  else {
    local_290 = '\0';
  }
  local_17d = local_290;
  if ((local_290 != '\0') || (*(float *)(param_1[0x40] + 0x28) <= (float)_DAT_01012060)) {
    if ((local_290 == '\0') &&
       (((*(char *)(param_1[0x40] + 0x2d) != '\0' && (iVar4 = FUN_0044ddc0(), iVar4 == 2)) &&
        (*(char *)(param_1 + 0x3e) != '\0')))) {
      local_20c = FID_conflict__Immortalize<class_std::_Generic_error_category>();
      FUN_0041a250();
      local_8 = 0xc;
      FUN_00ae5680(local_250,"UIVATSInsufficientAP",0x121);
      local_8._0_1_ = 0xd;
      FUN_00418900();
      local_8 = CONCAT31(local_8._1_3_,0xc);
      FUN_00483710();
      FUN_00ad8830();
      if ((NAN(*(float *)(param_1[0x40] + 0x28)) || NAN((float)_DAT_01012060)) !=
          (*(float *)(param_1[0x40] + 0x28) == (float)_DAT_01012060)) {
        uVar16 = (ulonglong)_DAT_010162c0;
        uVar13 = 0;
        uVar11 = 0;
        uVar10 = 2;
        uVar12 = FUN_00403df0(2,0,0,_DAT_010162c0,0);
        FUN_00775380(uVar12,uVar10,uVar11,uVar13,uVar16);
      }
      local_8 = 0xffffffff;
      FUN_00483710();
    }
    goto LAB_007eeb26;
  }
  FUN_004b7210();
  cVar1 = FUN_004b71d0();
  if ((cVar1 == '\0') || (iVar4 = FUN_0044ddc0(), iVar4 != 2)) {
    FUN_004b7210();
    cVar1 = FUN_004b71d0();
    if (((cVar1 != '\0') || (iVar4 = FUN_0044ddc0(), iVar4 != 2)) ||
       ((*(char *)((int)param_1 + 0x10e) != '\0' && (local_178 == 1)))) {
      FUN_004b7210();
      cVar1 = FUN_004b71d0();
      if ((cVar1 == '\0') &&
         ((iVar4 = FUN_0044ddc0(), iVar4 == 1 && (*(char *)((int)param_1 + 0x10e) == '\0')))) {
        FUN_007f6af0();
      }
      goto LAB_007eeb26;
    }
  }
  if (local_28 != 0) {
    FUN_00446390();
  }
  local_18c = FUN_0066dba0();
  local_185 = FUN_007f5050(local_18c,0);
  if (((((float)param_1[0x3c] < (float)local_185 != ((float)param_1[0x3c] == (float)local_185)) &&
       (local_28 != 0)) && (iVar4 = FUN_00525980(), iVar4 != 0)) &&
     (iVar4 = FUN_004fe160(), 1 < iVar4)) {
    fVar9 = (float10)FUN_0066dca0(9,1,0,0);
    local_17c = (float)(fVar9 + (float10)local_17c);
  }
  piVar5 = (int *)FUN_008d8520();
  local_184 = (**(code **)(*piVar5 + 0x14c))();
  if (local_28 == 0) {
    local_2a0 = '\0';
  }
  else {
    iVar4 = FUN_00446390();
    if ((iVar4 == 10) || (iVar4 = FUN_00446390(), iVar4 == 0xd)) {
      if (local_184 != 0) {
        uVar3 = FUN_00726070();
        FUN_006815c0();
        uVar8 = FUN_005ae380();
        if (uVar8 < uVar3) goto LAB_007edbfb;
      }
      local_2a0 = '\0';
    }
    else {
LAB_007edbfb:
      local_2a0 = '\x01';
    }
  }
  local_17e = local_2a0;
  if (((((local_28 != 0) &&
        ((iVar4 = FUN_00446390(), iVar4 == 10 || (iVar4 = FUN_00446390(), iVar4 == 0xd)))) &&
       (local_17e == '\0')) ||
      (((((local_2d != '\0' && ((float)param_1[0x3d] + (float)param_1[0x3c] <= (float)_DAT_01012060)
          ) || (local_18c == 0x16)) ||
        (local_17c < (float)param_1[0x38] == (local_17c == (float)param_1[0x38]))) ||
       (((local_28 != 0 && (iVar4 = FUN_00525980(), iVar4 != 0)) &&
        ((float)param_1[0x3d] + (float)param_1[0x3c] <= (float)_DAT_01012060)))))) ||
     (((local_28 != 0 && (iVar4 = FUN_00525980(), iVar4 != 0)) &&
      ((local_184 == 0 || (iVar4 = FUN_00726070(), iVar4 < 1)))))) {
LAB_007ee652:
    iVar4 = FUN_007f3cf0();
    if (iVar4 != 0) {
      FUN_007f3cf0();
      FUN_006815c0();
      iVar4 = FUN_00ec62c0();
      if (((iVar4 < 1) && (iVar4 = FUN_0044ddc0(), iVar4 == 2)) &&
         (*(char *)(param_1 + 0x3e) != '\0')) {
        FUN_0041a250();
        local_8 = 6;
        uVar15 = 0x12101077d84;
        puVar14 = local_22c;
        FUN_00453a70(puVar14,"UIVATSEnterFail",0x121);
        FUN_00ad7550(puVar14,uVar15);
        local_8._0_1_ = 7;
        FUN_00418900();
        local_8 = CONCAT31(local_8._1_3_,6);
        FUN_00483710();
        FUN_00ad8830();
        uVar16 = (ulonglong)_DAT_010162c0;
        uVar13 = 0;
        uVar11 = 0;
        uVar10 = 2;
        uVar12 = FUN_00403df0(2,0,0,_DAT_010162c0,0);
        FUN_00775380(uVar12,uVar10,uVar11,uVar13,uVar16);
        local_8 = 0xffffffff;
        FUN_00483710();
        goto LAB_007ee907;
      }
    }
    if (local_17c <= (float)param_1[0x38]) {
      if ((NAN((float)param_1[0x3d] + (float)param_1[0x3c]) || NAN((float)_DAT_01012060)) !=
          ((float)param_1[0x3d] + (float)param_1[0x3c] == (float)_DAT_01012060)) {
        uVar16 = (ulonglong)_DAT_010162c0;
        uVar13 = 0;
        uVar11 = 0;
        uVar10 = 2;
        uVar12 = FUN_00403df0(2,0,0,_DAT_010162c0,0);
        FUN_00775380(uVar12,uVar10,uVar11,uVar13,uVar16);
        FUN_0041a250();
        local_8 = 10;
        uVar15 = 0x12101077d84;
        puVar14 = local_244;
        FUN_00453a70(puVar14,"UIVATSEnterFail",0x121);
        FUN_00ad7550(puVar14,uVar15);
        local_8._0_1_ = 0xb;
        FUN_00418900();
        local_8 = CONCAT31(local_8._1_3_,10);
        FUN_00483710();
        FUN_00ad8830();
        local_8 = 0xffffffff;
        FUN_00483710();
      }
    }
    else {
      local_1f0 = FID_conflict__Immortalize<class_std::_Generic_error_category>();
      FUN_0041a250();
      local_8 = 8;
      FUN_00ae5680(local_238,"UIVATSInsufficientAP",0x121);
      local_8._0_1_ = 9;
      FUN_00418900();
      local_8 = CONCAT31(local_8._1_3_,8);
      FUN_00483710();
      FUN_00ad8830();
      FUN_00700320(0xfa3,1);
      local_8 = 0xffffffff;
      FUN_00483710();
    }
  }
  else {
    iVar4 = FUN_007f3cf0();
    if (iVar4 != 0) {
      FUN_007f3cf0();
      FUN_006815c0();
      iVar4 = FUN_00ec62c0();
      if (iVar4 < 1) goto LAB_007ee652;
    }
    local_220 = FUN_00401000();
    local_8 = 5;
    if (local_220 == 0) {
      local_2a8 = (int *)0x0;
    }
    else {
      local_2a8 = (int *)FUN_009ca4a0();
    }
    local_21c = local_2a8;
    local_8 = 0xffffffff;
    local_198 = local_2a8;
    cVar1 = (**(code **)(*DAT_011f21cc + 0x100))();
    if (cVar1 == '\0') {
      local_2b0 = 0;
    }
    else {
      piVar5 = (int *)FUN_004181e0();
      (**(code **)(*piVar5 + 0x180))();
      local_2b0 = FUN_005e5130();
    }
    local_1b0 = local_2b0;
    cVar1 = (**(code **)(*DAT_011f21cc + 0x100))();
    if (cVar1 == '\0') {
      local_2b8 = 0;
    }
    else {
      piVar5 = (int *)FUN_008d8520();
      local_2b8 = (**(code **)(*piVar5 + 0x148))();
    }
    local_19c = local_2b8;
    if (local_2b8 == 0) {
      local_2bc = 0;
    }
    else {
      local_2bc = FUN_0044ddc0();
    }
    local_194 = local_2bc;
    iVar4 = FUN_007f3cf0();
    if (iVar4 != 0) {
      FUN_007f3cf0();
      piVar5 = (int *)FUN_006815c0();
      param_1[0x42] = *piVar5;
    }
    local_1a5 = '\0';
    if ((local_28 == 0) || (cVar1 = FUN_006450c0(), cVar1 != '\0')) {
      fVar9 = (float10)FUN_00476b70(0,DAT_01016410);
      local_1b8 = (float)fVar9;
      local_1c0 = 0;
      local_1b4 = -1;
      FUN_007f3c90();
      piVar5 = (int *)FUN_006815c0();
      local_1bc = *piVar5 + 8;
      while ((local_1bc != 0 && (cVar1 = FUN_008256d0(), cVar1 == '\0'))) {
        piVar5 = (int *)FUN_006815c0();
        switch(*(undefined4 *)(*piVar5 + 0x20)) {
        case 0:
        case 3:
        case 4:
        case 5:
        case 6:
          local_1c0 = local_1c0 + 1;
          break;
        case 1:
        case 2:
          piVar5 = (int *)FUN_006815c0();
          local_1b4 = *(int *)(*piVar5 + 0x20);
          local_1c0 = local_1c0 + 1;
        }
        local_1bc = FUN_00726070();
      }
      if (((local_28 == 0) && (local_178 == 2)) && (local_1b4 != -1)) {
        iVar4 = FUN_007f3bf0();
        local_198[4] = iVar4;
        local_1a5 = '\x01';
      }
      else if (0 < local_1c0) {
        local_1c4 = (float)_DAT_01017a40 / (float)local_1c0;
        FUN_00404010(local_1b8,0x3f800000);
        local_1c8 = FUN_00ec62c0();
        local_1c0 = 0;
        FUN_007f3c90();
        piVar5 = (int *)FUN_006815c0();
        local_1bc = *piVar5 + 8;
        while ((local_1bc != 0 && (cVar1 = FUN_008256d0(), cVar1 == '\0'))) {
          piVar5 = (int *)FUN_006815c0();
          if ((-1 < *(int *)(*piVar5 + 0x20)) && (*(int *)(*piVar5 + 0x20) < 7)) {
            if (local_1c0 == local_1c8) {
              FUN_006815c0();
              iVar4 = FUN_007f3bf0();
              local_198[4] = iVar4;
              local_1a5 = '\x01';
            }
            local_1c0 = local_1c0 + 1;
          }
          local_1bc = FUN_00726070();
        }
      }
    }
    if (local_1a5 == '\0') {
      iVar4 = FUN_007f3bf0();
      local_198[4] = iVar4;
    }
    uVar2 = FUN_007f5050(local_18c,0);
    *(undefined *)(local_198 + 2) = uVar2;
    uVar3 = FUN_007f5050(local_18c,1,0);
    uVar2 = FUN_00647b70((uVar3 & 0xff) - (uint)*(byte *)(local_198 + 2));
    *(undefined *)((int)local_198 + 9) = uVar2;
    if (local_178 == 2) {
      if ((local_28 == 0) || (fVar9 = (float10)FUN_007ebd10(), fVar9 <= (float10)_DAT_01012060)) {
        cVar1 = (**(code **)(*DAT_011f21cc + 0x230))();
        if (cVar1 == '\0') {
          *local_198 = 0x11;
        }
        else {
          *local_198 = 0x15;
        }
      }
      else {
        *local_198 = 0x10;
      }
    }
    else if (local_178 == 3) {
      *local_198 = 0x14;
    }
    else {
      *local_198 = local_18c;
    }
    local_198[3] = (int)DAT_011f21cc;
    local_198[8] = (int)local_17c;
    pfVar6 = (float *)FUN_00403e20();
    local_1a4 = *pfVar6 * (float)_DAT_01017a40;
    fVar9 = (float10)FUN_00476b70(0,DAT_01016410);
    local_1a0 = (float)fVar9;
    if (((DAT_011db0b0 != '\0') && (local_18c == 0)) && (local_1a0 <= local_1a4)) {
      *(undefined *)((int)local_198 + 7) = 1;
    }
    cVar1 = FUN_009c9f60();
    if (((cVar1 != '\0') && (cVar1 = (**(code **)(*DAT_011f21cc + 0x100))(), cVar1 != '\0')) &&
       (local_1a5 == '\0')) {
      piVar5 = (int *)FUN_004181e0();
      local_1cc = (**(code **)(*piVar5 + 0x180))();
      local_1d0 = FUN_005e5130();
      if (local_1d0 == 0) {
        local_1d0 = FUN_005e5130();
        if (local_1d0 == 0) {
          local_1d4 = FUN_006a9540();
          local_1d5 = '\0';
          local_1dc = 0;
          while ((local_1dc < 0xf && (local_1d5 == '\0'))) {
            if (*(int *)(local_1d4 + local_1dc * 4) != 0) {
              cVar1 = FUN_005e5190();
              local_198[4] = (int)cVar1;
              local_1d5 = '\x01';
            }
            local_1dc = local_1dc + 1;
          }
        }
        else {
          local_198[4] = 0x1a;
        }
      }
      else {
        local_198[4] = 0x19;
      }
    }
    FUN_009c71a0();
    local_190 = FUN_007f3cf0();
    if (local_190 == 0) {
      local_2cc = 0.0;
    }
    else {
      FUN_007f3cf0();
      piVar5 = (int *)FUN_006815c0();
      local_2cc = *(float *)(*piVar5 + 0x28);
    }
    local_1ac = local_2cc;
    if (*(char *)(param_1 + 0x41) != '\0') {
      local_1e0 = FUN_007ef930();
      piVar5 = (int *)FUN_0043d4d0();
      local_1ac = (float)(*piVar5 * local_1e0) / (float)_DAT_01017a40 + local_1ac;
    }
    pcVar7 = (char *)FUN_00408d60();
    if ((*pcVar7 == '\0') || (iVar4 = FUN_007f3cf0(), iVar4 == 0)) {
      local_2d1 = FUN_004dff00();
    }
    else {
      local_2d1 = 1;
    }
    *(undefined *)(local_198 + 1) = local_2d1;
    FUN_007f1840();
    cVar1 = FUN_007f28d0();
    if ((((cVar1 == '\0') || (local_28 == 0)) || (iVar4 = FUN_00446390(), iVar4 == 10)) ||
       (iVar4 = FUN_00446390(), iVar4 == 0xd)) {
LAB_007ee5f0:
      FUN_007efa10(local_198,0,local_178 != 1);
    }
    else {
      uVar3 = FUN_004fe160();
      uVar8 = FUN_00524b60();
      if ((uVar3 == (uVar8 & 0xff)) ||
         ((float)param_1[0x3d] + (float)param_1[0x3c] <= (float)_DAT_01012060)) goto LAB_007ee5f0;
      FUN_007efa10(local_198,1,local_178 != 1);
    }
    if ((float)param_1[0x38] < local_17c) {
      FUN_00700320(0xfaf,0);
    }
    FUN_007f0ea0();
  }
LAB_007ee907:
  fVar9 = (float10)FUN_007f48e0();
  *(float *)(DAT_011db0d4 + 0xfc) = (float)fVar9;
LAB_007eeb26:
  *unaff_FS_OFFSET = local_10;
  ___security_check_cookie_4();
  return;
}

