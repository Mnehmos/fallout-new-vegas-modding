
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 FUN_00646f70(int *param_1,int *param_2,int param_3,undefined4 param_4,undefined4 param_5,
                    float param_6,int param_7,int param_8,float param_9,float param_10,
                    float param_11,int *param_12)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  bool bVar6;
  char cVar7;
  char cVar8;
  byte bVar9;
  undefined4 *puVar10;
  int iVar11;
  float *pfVar12;
  float10 fVar13;
  float10 fVar14;
  undefined4 local_7c;
  char *local_74;
  char *local_70;
  int *local_64;
  int *local_60;
  float local_4c;
  float local_44;
  float local_40;
  float local_28;
  float local_18;
  float local_14;
  
  local_18 = 0.0;
  if (param_2 == (int *)0x0) {
    bVar6 = false;
  }
  else {
    cVar7 = FUN_00452370();
    if ((cVar7 == '\0') || (cVar7 = (**(code **)(*param_2 + 0x100))(), cVar7 != '\0')) {
      bVar6 = false;
    }
    else {
      bVar6 = true;
    }
  }
  cVar7 = (**(code **)(*param_2 + 0x224))();
  if ((param_2 == (int *)0x0) || (cVar8 = (**(code **)(*param_2 + 0x100))(), cVar8 == '\0')) {
    local_64 = (int *)0x0;
  }
  else {
    if (param_2 == (int *)0x0) {
      local_60 = (int *)0x0;
    }
    else {
      local_60 = param_2 + 0x29;
    }
    local_64 = local_60;
  }
  if (param_7 == 0) {
    if (param_8 == 0) {
      local_14 = 1.0;
    }
    else {
      bVar9 = FUN_00647730();
      local_14 = (float)bVar9;
    }
  }
  else {
    bVar9 = FUN_005dc980();
    local_14 = (float)bVar9;
  }
  if (cVar7 != '\0') {
    local_14 = 1.0;
  }
  if ((param_12 != (int *)0x0) && ((bVar6 || (cVar7 != '\0')))) {
    if (cVar7 == '\0') {
      local_70 = "";
    }
    else {
      local_70 = "Grenade Target";
    }
    if (bVar6) {
      local_74 = "Destructible Target ";
    }
    else {
      local_74 = "";
    }
    (**(code **)(*param_12 + 0x14))(param_12,1,3,&DAT_0101996c,local_74,local_70);
  }
  puVar10 = (undefined4 *)FUN_00403e20();
  fVar13 = (float10)FUN_0040ebd0(*puVar10);
  if ((param_3 == 0) || (cVar8 = FUN_006450c0(), cVar8 != '\0')) {
    pfVar12 = (float *)FUN_00403e20();
    if (*pfVar12 < param_10) {
      if (param_12 != (int *)0x0) {
        (**(code **)(*param_12 + 0x14))(param_12,1,3,"Melee weapon or unarmed -- out of range");
      }
    }
    else {
      if (param_12 != (int *)0x0) {
        (**(code **)(*param_12 + 0x14))(param_12,1,3,"Melee weapon or unarmed assume 100%");
      }
      local_18 = DAT_01016410;
    }
  }
  else {
    iVar11 = FUN_00525ae0();
    if (iVar11 != 0) {
      FUN_00525ae0();
      fVar14 = (float10)FUN_0045cd80();
      if ((NAN(fVar14) || NAN((float10)_DAT_01012060)) == (fVar14 == (float10)_DAT_01012060)) {
        if (param_12 != (int *)0x0) {
          (**(code **)(*param_12 + 0x14))(param_12,1,3,"Target out of explosion range");
        }
        return (float10)0;
      }
    }
    cVar8 = FUN_004c0bf0();
    if (cVar8 == '\0') {
      cVar8 = FUN_004c0c60();
      if (((cVar8 != '\0') && (cVar8 = FUN_00647790(), cVar8 != '\0')) &&
         (fVar14 = (float10)FUN_00646f50(), fVar14 < (float10)param_10)) {
        return (float10)0;
      }
      local_44 = 1.0;
      cVar8 = FUN_004c0c60();
      if (cVar8 != '\0') {
        fVar14 = (float10)FUN_00524b80();
        local_44 = (float)(fVar14 + (float10)param_6);
      }
      FUN_00403e20();
      fVar14 = (float10)FUN_0057dd70();
      fVar1 = (float)(fVar14 * (float10)param_10);
      fVar3 = fVar1 * fVar1 * (float)_DAT_0101ff40;
      local_40 = (param_11 / (float)_DAT_01021928) * param_11;
      if (cVar7 == '\0') {
        if (fVar1 + fVar1 < param_11) {
          local_40 = ((fVar1 + fVar1) / param_11) * local_40;
        }
        if (bVar6) {
          pfVar12 = (float *)FUN_00403e20();
          local_40 = local_40 * *pfVar12;
        }
      }
      else {
        pfVar12 = (float *)FUN_00403e20();
        local_40 = *pfVar12;
      }
      local_4c = 0.0;
      if ((float)_DAT_01012060 < fVar3) {
        puVar10 = (undefined4 *)FUN_00403e20();
        fVar14 = (float10)FUN_0040ebd0(local_40 / fVar3,*puVar10);
        local_4c = (float)fVar14;
      }
      pfVar12 = (float *)FUN_00403e20();
      local_18 = *pfVar12 * ((1.0 - (float)fVar13) + (float)fVar13 * param_9) * local_4c * local_14;
      if (param_12 != (int *)0x0) {
        (**(code **)(*param_12 + 0x14))
                  (param_12,1,3,"bound size: %.2f, base chance: %.2f",(double)param_11,
                   (double)local_14);
        (**(code **)(*param_12 + 0x14))
                  (param_12,1,3,"spread factor: %.2f, radius %.2f, area %.2f",(double)local_44,
                   (double)fVar1,(double)fVar3);
        (**(code **)(*param_12 + 0x14))
                  (param_12,1,3,"target area: %.2f, range spread: %.2f, final chance: %.2f",
                   (double)local_40,(double)local_4c,(double)local_18);
      }
    }
    else {
      fVar13 = (float10)FUN_00646f50();
      pfVar12 = (float *)FUN_00403e20();
      if ((float)fVar13 * *pfVar12 < param_10) {
        if (param_12 != (int *)0x0) {
          (**(code **)(*param_12 + 0x14))(param_12,1,3,"Target out of thrown weapon range");
        }
        return (float10)0;
      }
      pfVar12 = (float *)FUN_00403e20();
      fVar3 = (float)fVar13 * *pfVar12;
      pfVar12 = (float *)FUN_00403e20();
      fVar4 = fVar3 - *pfVar12;
      pfVar12 = (float *)FUN_00403e20();
      fVar13 = (float10)FUN_00404010(param_10 - *pfVar12);
      fVar1 = (float)((float10)1 - fVar13 / (float10)fVar4);
      if (param_3 == 0) {
        local_7c = 0;
      }
      else {
        local_7c = FUN_00446390();
      }
      fVar13 = (float10)FUN_00646880(param_1,local_7c);
      if ((float)fVar13 < (float)_DAT_01012060 == ((float)fVar13 == (float)_DAT_01012060)) {
        local_28 = 1.0;
      }
      else {
        pfVar12 = (float *)FUN_00403e20();
        local_28 = 1.0 - *pfVar12;
      }
      FUN_008d85e0();
      fVar13 = (float10)FUN_0066ef50();
      pfVar12 = (float *)FUN_00403e20();
      fVar2 = *pfVar12;
      fVar5 = (float)_DAT_01017a40;
      pfVar12 = (float *)FUN_00403e20();
      fVar2 = ((1.0 - *pfVar12) + (fVar2 * (float)fVar13) / fVar5) * local_28;
      pfVar12 = (float *)FUN_00403e20();
      local_18 = (fVar1 + fVar2) * *pfVar12 * (float)_DAT_01017a40;
      if (param_12 != (int *)0x0) {
        (**(code **)(*param_12 + 0x14))
                  (param_12,1,3,"mod max range: %.2f, range gap: %.2f, range odds: %.2f",
                   (double)fVar3,(double)fVar4,(double)fVar1);
        (**(code **)(*param_12 + 0x14))
                  (param_12,1,3,"arm condition: %.2f, skill calc %.2f, final chance %.2f",
                   (double)local_28,(double)fVar2,(double)local_18);
      }
    }
    if ((bVar6) || (cVar7 != '\0')) {
      local_18 = local_18 * (float)_DAT_01017a40;
      if (((float)_DAT_01012060 < local_18) &&
         (local_18 < (float)_DAT_01012070 != (NAN(local_18) || NAN((float)_DAT_01012070)))) {
        local_18 = 1.0;
      }
      if (param_12 != (int *)0x0) {
        (**(code **)(*param_12 + 0x14))
                  (param_12,1,3,"destructible/grenade target chance: %.2f",(double)local_18);
      }
    }
  }
  if ((local_64 != (int *)0x0) &&
     ((iVar11 = (**(code **)(*local_64 + 8))(), 0 < iVar11 ||
      (iVar11 = (**(code **)(*param_1 + 8))(), 0 < iVar11)))) {
    if (param_12 != (int *)0x0) {
      pfVar12 = (float *)FUN_00403e20();
      (**(code **)(*param_12 + 0x14))
                (param_12,1,3,"Stealth bonus: %f becomes %f",(double)local_18,
                 (double)(local_18 * *pfVar12));
    }
    FUN_005e58f0();
    if (0.0 < (float)_DAT_01012060 != ((float)_DAT_01012060 == 0.0)) {
      pfVar12 = (float *)FUN_00403e20();
      local_18 = local_18 * *pfVar12;
    }
  }
  puVar10 = (undefined4 *)FUN_00403e20();
  fVar13 = (float10)FUN_0040ebd0(local_18,*puVar10);
  return (float10)((float)fVar13 / (float)_DAT_01017a40);
}

