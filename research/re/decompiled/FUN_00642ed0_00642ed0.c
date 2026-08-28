
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4
FUN_00642ed0(int param_1,int param_2,int param_3,int param_4,float param_5,int param_6,int param_7,
            char param_8,int param_9,char param_10,char param_11,char param_12,char param_13,
            char param_14,int param_15,int param_16,char param_17,char param_18,int param_19,
            float *param_20,float *param_21,float *param_22,int param_23,int param_24,int param_25)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  int iVar13;
  float fVar14;
  float fVar15;
  float *pfVar16;
  int *piVar17;
  int iVar18;
  float *pfVar19;
  float *pfVar20;
  int iVar21;
  float10 fVar22;
  float10 fVar23;
  double dVar24;
  float local_74;
  float local_70;
  uint local_5c;
  uint local_58;
  float local_50;
  undefined4 local_44;
  int local_40;
  float local_34;
  uint local_1c;
  uint local_c;
  
  pfVar16 = (float *)FUN_00403e20();
  fVar1 = *pfVar16;
  piVar17 = (int *)FUN_0043d4d0();
  iVar18 = *piVar17;
  piVar17 = (int *)FUN_0043d4d0();
  iVar13 = *piVar17;
  piVar17 = (int *)FUN_0043d4d0();
  iVar18 = FUN_00647b70(iVar18 - param_24 * *piVar17,0);
  local_5c = (uint)(param_14 != '\0');
  local_1c = (uint)(param_13 != '\0');
  local_58 = (uint)(param_18 != '\0');
  local_50 = 0.0;
  if (param_19 == 1) {
    pfVar16 = (float *)FUN_00403e20();
    local_50 = *pfVar16;
  }
  else if ((NAN((double)param_19) || NAN(_DAT_01011590)) != ((double)param_19 == _DAT_01011590)) {
    pfVar16 = (float *)FUN_00403e20();
    local_50 = *pfVar16;
  }
  pfVar16 = (float *)FUN_00403e20();
  pfVar19 = (float *)FUN_00403e20();
  pfVar20 = (float *)FUN_00403e20();
  fVar2 = *pfVar19;
  fVar3 = *pfVar20;
  fVar15 = (float)_DAT_01020758;
  fVar4 = *pfVar16;
  pfVar16 = (float *)FUN_00403e20();
  fVar5 = *pfVar16;
  pfVar16 = (float *)FUN_00403e20();
  fVar6 = *pfVar16;
  pfVar16 = (float *)FUN_00403e20();
  fVar7 = *pfVar16;
  local_40 = param_4;
  if (param_8 != '\0') {
    local_40 = 0;
  }
  local_c = (uint)(param_11 != '\0');
  if (param_17 == '\0') {
    pfVar16 = (float *)FUN_00403e20();
    fVar8 = *pfVar16;
  }
  else {
    pfVar16 = (float *)FUN_00403e20();
    pfVar19 = (float *)FUN_00403e20();
    fVar8 = *pfVar16 * *pfVar19;
  }
  fVar22 = (float10)FUN_00404010((fVar8 - param_5) / fVar8,0);
  pfVar16 = (float *)FUN_00403e20();
  dVar24 = _pow((double)(float)fVar22,(double)*pfVar16);
  fVar8 = (float)dVar24;
  local_74 = fVar8;
  if ((param_3 < 1) && (param_19 != 1)) {
    pfVar16 = (float *)FUN_00403e20();
    local_74 = fVar8 * *pfVar16;
  }
  pfVar16 = (float *)FUN_00403e20();
  pfVar19 = (float *)FUN_00403e20();
  fVar9 = *pfVar19;
  fVar10 = *pfVar16;
  local_70 = 1.0;
  if (param_12 != '\0') {
    pfVar16 = (float *)FUN_00403e20();
    local_70 = *pfVar16;
  }
  FUN_00403e20();
  iVar21 = FUN_00ec62c0();
  pfVar16 = (float *)FUN_00403e20();
  fVar22 = (float10)FUN_00404010(((float)(iVar21 * param_15) +
                                 ((float)param_9 * fVar9 + fVar10) * (float)(param_10 != '\0') *
                                 local_70) * local_74 * *pfVar16);
  *param_20 = (float)fVar22;
  pfVar16 = (float *)FUN_00403e20();
  fVar9 = *pfVar16;
  pfVar16 = (float *)FUN_00403e20();
  fVar10 = *pfVar16;
  pfVar16 = (float *)FUN_00403e20();
  fVar11 = *pfVar16;
  pfVar16 = (float *)FUN_00403e20();
  fVar12 = *pfVar16;
  if (param_16 < 2) {
    fVar14 = 1.0;
  }
  else {
    dVar24 = (double)param_16 - _DAT_01012070;
    pfVar16 = (float *)FUN_00403e20();
    fVar14 = *pfVar16 * (float)dVar24 + 1.0;
  }
  fVar23 = (float10)FUN_00404010((float)local_40 * fVar8 *
                                 (fVar10 * (float)(param_12 != '\0') +
                                 fVar9 * (float)(param_10 != '\0') + 1.0) *
                                 fVar12 * ((float)param_6 + fVar11) * (float)((100 - param_7) / 100)
                                 * fVar14,0);
  local_34 = (float)fVar23;
  if (param_8 != '\0') {
    pfVar16 = (float *)FUN_00403e20();
    local_34 = local_34 * *pfVar16;
  }
  *param_21 = local_34;
  pfVar16 = (float *)FUN_00403e20();
  fVar2 = ((fVar7 * (float)local_58 + fVar6 * (float)local_1c + fVar5 * (float)local_5c + 1.0 +
           local_50) * (((float)param_1 / fVar15) * (fVar2 - fVar3) + fVar4) * fVar8 -
          (float)(int)(((iVar18 + (param_24 - param_23) * iVar13 + param_2) - param_25) * local_c))
          * *pfVar16;
  *param_22 = fVar2;
  fVar2 = fVar1 + (float)fVar22 + local_34 + fVar2;
  if ((fVar2 < (float)_DAT_01012070 == (NAN(fVar2) || NAN((float)_DAT_01012070))) ||
     (fVar2 <= (float)_DAT_01012060)) {
    local_44 = FUN_00ec62c0();
  }
  else {
    local_44 = 1;
  }
  return local_44;
}

