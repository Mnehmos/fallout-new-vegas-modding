
void FUN_005b1ba0(ushort param_1,int param_2,int param_3,undefined4 param_4)

{
  short sVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  int *piVar5;
  int iVar6;
  long lVar7;
  double dVar8;
  int local_2c4;
  byte local_2b9;
  int local_2b4;
  int local_2b0;
  undefined2 local_298;
  undefined2 local_290;
  short local_288;
  short local_280;
  short local_278;
  undefined2 local_270;
  undefined2 local_230;
  char local_22c [512];
  int local_2c;
  char local_28;
  int local_20;
  int *local_1c;
  uint local_10;
  ushort local_c;
  ushort *local_8;
  
  local_10 = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  *(undefined4 *)(param_3 + 0x208) = 0;
  local_8 = (ushort *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c));
  *local_8 = param_1;
  *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
  local_c = 0;
  do {
    if ((int)(uint)param_1 <= (int)(short)local_c) {
      if (*(uint *)(param_3 + 0x208) < *(uint *)(param_3 + 0x204)) {
        FUN_005aea90(param_4,"Expected end of line.\r\nCompiled script not saved!",
                     *(undefined4 *)(param_2 + (short)local_c * 0xc));
      }
LAB_005b3ab4:
      ___security_check_cookie_4();
      return;
    }
    cVar2 = (&DAT_0118cdd4)[*(int *)(param_2 + 4 + (short)local_c * 0xc) * 8];
    FUN_005af310();
    iVar3 = FUN_005af5f0(param_4,local_22c,param_3 + 4,param_3 + 0x208,cVar2,0);
    if (iVar3 == 0) {
      if (*(char *)(param_2 + 8 + (short)local_c * 0xc) == '\0') {
        FUN_005aea90(param_4,"Missing parameter %s.\r\nCompiled script not saved!",
                     *(undefined4 *)(param_2 + (short)local_c * 0xc));
      }
      else {
        *local_8 = local_c;
      }
      goto LAB_005b3ab4;
    }
    if ((cVar2 == '\0') && ((local_2c != 0 || (local_28 != '\0')))) {
      FUN_005aea90(param_4,"Parameter %s may not be a variable.\r\nCompiled script not saved!",
                   *(undefined4 *)(param_2 + (short)local_c * 0xc));
      goto LAB_005b3ab4;
    }
    if (((&DAT_0118cdd5)[*(int *)(param_2 + 4 + (short)local_c * 0xc) * 8] != '\0') &&
       ((cVar2 = FUN_005afad0(local_22c,0,0), cVar2 == '\0' || (local_2c == 0)))) {
      FUN_005aea90(param_4,"Item \'%s\' not found for parameter %s.\r\nCompiled script not saved!",
                   local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
      goto LAB_005b3ab4;
    }
    if ((&DAT_0118cdd5)[*(int *)(param_2 + 4 + (short)local_c * 0xc) * 8] == '\0') {
      switch(*(undefined4 *)(param_2 + 4 + (short)local_c * 0xc)) {
      case 0:
        local_230 = (undefined2)iVar3;
        *(undefined2 *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = local_230;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        FUN_00401460(param_3 + 0x20c + *(int *)(param_3 + 0x40c),local_22c,iVar3);
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + iVar3;
        break;
      case 1:
      case 2:
      case 0x17:
        iVar3 = param_3 + 0x20c;
        if (local_2c != 0) {
          if (local_28 == 'G') {
            *(undefined *)(iVar3 + *(int *)(param_3 + 0x40c)) = 0x47;
            *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 1;
          }
          else {
            *(undefined *)(iVar3 + *(int *)(param_3 + 0x40c)) = 0x72;
            *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 1;
          }
          *(undefined2 *)(iVar3 + *(int *)(param_3 + 0x40c)) = (undefined2)local_2c;
          *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        }
        if (local_28 != 'G') {
          if (local_20 == 0) {
            if ((*(int *)(param_2 + 4 + (short)local_c * 0xc) == 1) ||
               (*(int *)(param_2 + 4 + (short)local_c * 0xc) == 0x17)) {
              iVar6 = FUN_004b1230(local_22c);
              if (iVar6 == 0) {
                FUN_005aea90(param_4,
                             "Unknown variable \'%s\' for parameter %s.\r\nCompiled script not saved!"
                             ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
                goto LAB_005b3ab4;
              }
              *(undefined *)(iVar3 + *(int *)(param_3 + 0x40c)) = 0x6e;
              *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 1;
              lVar7 = _atol(local_22c);
              *(long *)(iVar3 + *(int *)(param_3 + 0x40c)) = lVar7;
              *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 4;
            }
            else {
              iVar6 = FUN_004b12d0(local_22c);
              if (iVar6 == 0) {
                FUN_005aea90(param_4,
                             "Unknown variable \'%s\' for parameter %s.\r\nCompiled script not saved!"
                             ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
                goto LAB_005b3ab4;
              }
              *(undefined *)(iVar3 + *(int *)(param_3 + 0x40c)) = 0x7a;
              *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 1;
              dVar8 = _atof(local_22c);
              *(double *)(iVar3 + *(int *)(param_3 + 0x40c)) = dVar8;
              *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 8;
            }
          }
          else {
            *(char *)(iVar3 + *(int *)(param_3 + 0x40c)) = local_28;
            *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 1;
            *(undefined2 *)(iVar3 + *(int *)(param_3 + 0x40c)) = (undefined2)local_20;
            *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
          }
        }
        break;
      default:
        FUN_005b5e40("SCRIPTS: Param type \'%d\' unimplemented in ScriptCompiler::StandardCompile.",
                     *(undefined4 *)(param_2 + 4 + (short)local_c * 0xc));
        goto LAB_005b3ab4;
      case 5:
        iVar3 = FUN_0066eb40(local_22c);
        if (iVar3 == 0x4d) {
          FUN_005aea90(param_4,
                       "Invalid actor value \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        local_270 = (undefined2)iVar3;
        *(undefined2 *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = local_270;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        break;
      case 8:
        iVar3 = _toupper((int)local_22c[0]);
        cVar2 = (char)iVar3;
        if (((cVar2 != 'X') && (cVar2 != 'Y')) && (cVar2 != 'Z')) {
          FUN_005aea90(param_4,
                       "Axis (X,Y,Z) required for parameter %s.\r\nCompiled script not saved!",
                       *(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        *(char *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = cVar2;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 1;
        break;
      case 10:
        local_2b0 = 0xff;
        for (local_2b4 = 0; local_2b4 < 0xf5; local_2b4 = local_2b4 + 1) {
          iVar3 = FUN_00404dc0(local_22c,(&PTR_DAT_011977d8)[local_2b4 * 9]);
          if (iVar3 == 0) {
            local_2b0 = local_2b4;
            break;
          }
        }
        if (local_2b0 == 0xff) {
          FUN_005aea90(param_4,
                       "Animation group \"%s\" not found for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        *(undefined2 *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = (undefined2)local_2b0;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        break;
      case 0x12:
        sVar1 = 2;
        iVar3 = FUN_00404dc0(local_22c,PTR_DAT_01199e8c);
        if (iVar3 == 0) {
          sVar1 = 0;
        }
        else {
          iVar3 = FUN_00404dc0(local_22c,PTR_s_Female_01199e90);
          if (iVar3 == 0) {
            sVar1 = 1;
          }
        }
        if (sVar1 == 2) {
          FUN_005aea90(param_4,
                       "Sex (Male, Female) required for parameter %s.\r\nCompiled script not saved!"
                       ,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        *(short *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = sVar1;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        break;
      case 0x1c:
        iVar3 = FUN_004b1230(local_22c);
        if (iVar3 == 0) {
          FUN_005aea90(param_4,
                       "Invalid crime type \'%s\' for parameter %s.  Crime type must be a numeric value from 0-%d.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc),4);
          goto LAB_005b3ab4;
        }
        lVar7 = _atol(local_22c);
        if ((lVar7 < 0) || (4 < lVar7)) {
          FUN_005aea90(param_4,
                       "Invalid crime type \'%s\' for parameter %s.  Crime type must be a numeric value from 0-%d.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc),4);
          goto LAB_005b3ab4;
        }
        local_298 = (undefined2)lVar7;
        *(undefined2 *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = local_298;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        break;
      case 0x20:
        local_2b9 = 0;
        for (local_2c4 = 0; local_2c4 < 0x57; local_2c4 = local_2c4 + 1) {
          iVar3 = FUN_00404dc0(local_22c,(&PTR_s_Activator_0118a2d8)[local_2c4]);
          if (iVar3 == 0) {
            local_2b9 = (&DAT_0118a598)[local_2c4];
            break;
          }
        }
        if (local_2b9 == 0) {
          FUN_005aea90(param_4,
                       "Form Type \"%s\" not found for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        *(ushort *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = (ushort)local_2b9;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        break;
      case 0x29:
        iVar3 = FUN_004d5eb0(local_22c);
        if (iVar3 == 0x2b) {
          FUN_005aea90(param_4,
                       "Invalid misc stat \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        local_290 = (undefined2)iVar3;
        *(undefined2 *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = local_290;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        break;
      case 0x33:
        local_278 = 0;
        while ((local_278 < 5 &&
               (iVar3 = FUN_00404dc0((&PTR_DAT_01186cf4)[local_278],local_22c), iVar3 != 0))) {
          local_278 = local_278 + 1;
        }
        if (local_278 == 5) {
          FUN_005aea90(param_4,
                       "Invalid alignment \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        *(short *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = local_278;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        break;
      case 0x34:
        local_288 = 0;
        while ((local_288 < 0xe &&
               (iVar3 = FUN_00404dc0((&PTR_s_BigGuns_011869bc)[local_288],local_22c), iVar3 != 0)))
        {
          local_288 = local_288 + 1;
        }
        if (local_288 == 0xe) {
          FUN_005aea90(param_4,
                       "Invalid EquipType \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        *(short *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = local_288;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
        break;
      case 0x37:
        local_280 = 0;
        while ((local_280 < 5 &&
               (iVar3 = FUN_00404dc0((&PTR_DAT_0119bbb0)[local_280],local_22c), iVar3 != 0))) {
          local_280 = local_280 + 1;
        }
        if (local_280 == 5) {
          FUN_005aea90(param_4,
                       "Invalid CriticalStage \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        *(short *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = local_280;
        *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
      }
    }
    else {
      switch(*(undefined4 *)(param_2 + 4 + (short)local_c * 0xc)) {
      case 3:
        if (local_20 == 0) {
          if (local_1c != (int *)0x0) {
            uVar4 = FUN_00401170();
            cVar2 = FUN_00481f30(uVar4);
            if (cVar2 != '\0') break;
          }
          FUN_005aea90(param_4,
                       "Invalid inventory object \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 4:
      case 6:
      case 0x18:
      case 0x1a:
        if (local_20 == 0) {
          piVar5 = (int *)___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028
                                           ,&PTR_PTR__scalar_deleting_destructor__011841cc,0);
          if (piVar5 == (int *)0x0) {
            FUN_005aea90(param_4,
                         "Invalid object reference \'%s\' for parameter %s.\r\nCompiled script not saved!"
                         ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
            goto LAB_005b3ab4;
          }
          iVar3 = *(int *)(param_2 + 4 + (short)local_c * 0xc);
          if (iVar3 == 6) {
            cVar2 = (**(code **)(*piVar5 + 0x100))();
            if (cVar2 == '\0') {
              FUN_005aea90(param_4,
                           "Invalid actor \'%s\' for parameter %s.\r\nCompiled script not saved!",
                           local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
              goto LAB_005b3ab4;
            }
          }
          else if (iVar3 == 0x18) {
            iVar3 = FUN_007af430();
            if (iVar3 != DAT_011ca224) {
              FUN_005aea90(param_4,
                           "Invalid map marker \'%s\' for parameter %s.\r\nCompiled script not saved!"
                           ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
              goto LAB_005b3ab4;
            }
          }
          else if ((iVar3 == 0x1a) && (iVar3 = FUN_0055d310(), iVar3 == 0)) {
            FUN_005aea90(param_4,
                         "Invalid container reference \'%s\' for parameter %s.\r\nCompiled script not saved!"
                         ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
            goto LAB_005b3ab4;
          }
        }
        break;
      default:
        FUN_005b5e40("SCRIPTS: Param type \'%d\' (referenced object) unimplemented in ScriptCompiler::StandardCompile."
                     ,*(undefined4 *)(param_2 + 4 + (short)local_c * 0xc));
        goto LAB_005b3ab4;
      case 7:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            ((iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                       &PTR_PTR__scalar_deleting_destructor__01183060,0), iVar3 == 0
             && (iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                          &PTR_PTR__scalar_deleting_destructor__0118a650,0),
                iVar3 == 0)))))) {
          FUN_005aea90(param_4,
                       "Invalid spell item \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 9:
        iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                 &PTR_PTR__scalar_deleting_destructor__01183fb4,0);
        if ((local_20 == 0) && ((iVar3 == 0 || (cVar2 = FUN_00425fd0(), cVar2 == '\0')))) {
          FUN_005aea90(param_4,
                       "Invalid interior cell \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0xb:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            (iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                      &PTR_PTR__scalar_deleting_destructor__01183140,0), iVar3 == 0)
            ))) {
          FUN_005aea90(param_4,
                       "Invalid magic item \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0xc:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0xd))))
        {
          FUN_005aea90(param_4,
                       "Invalid sound \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0xd:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x45)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid topic \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0xe:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x47)))
           ) {
          FUN_005aea90(param_4,"Invalid info \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0xf:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0xc))))
        {
          FUN_005aea90(param_4,"Invalid race \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x10:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 7)))) {
          FUN_005aea90(param_4,
                       "Invalid class \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x11:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 8)))) {
          FUN_005aea90(param_4,
                       "Invalid faction \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x13:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 6)))) {
          FUN_005aea90(param_4,
                       "Invalid global \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x14:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            ((iVar3 = FUN_00401170(), iVar3 != 0x27 && (iVar3 = FUN_00401170(), iVar3 != 0x55))))))
        {
          FUN_005aea90(param_4,
                       "Invalid furniture object/list \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x15:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            (iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                      &PTR_PTR__scalar_deleting_destructor__01183128,0), iVar3 == 0)
            ))) {
          FUN_005aea90(param_4,
                       "Invalid object \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x19:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            (iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                      &PTR_PTR__scalar_deleting_destructor__011846e8,0), iVar3 == 0)
            ))) {
          FUN_005aea90(param_4,
                       "Invalid actor base \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x1b:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            (iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                      &PTR_PTR__scalar_deleting_destructor__01183fd0,0), iVar3 == 0)
            ))) {
          FUN_005aea90(param_4,
                       "Invalid worldspace \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x1d:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            (iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                      &PTR_PTR__scalar_deleting_destructor__011846a0,0), iVar3 == 0)
            ))) {
          FUN_005aea90(param_4,
                       "Invalid package \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x1e:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            (iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                      &PTR_PTR__scalar_deleting_destructor__0118627c,0), iVar3 == 0)
            ))) {
          FUN_005aea90(param_4,
                       "Invalid combat style \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x1f:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            (iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                      &PTR_PTR__scalar_deleting_destructor__011837c4,0), iVar3 == 0)
            ))) {
          FUN_005aea90(param_4,
                       "Invalid effect setting \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x21:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x35)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid weather \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x22:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x2a)))
           ) {
          FUN_005aea90(param_4,"Invalid NPC \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x23:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            ((iVar3 = FUN_00401170(), iVar3 != 0x2a && (iVar3 = FUN_00401170(), iVar3 != 8)))))) {
          FUN_005aea90(param_4,
                       "Invalid owner \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x24:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x4f)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid Effect Shader \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x25:
        iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                 &PTR_PTR__scalar_deleting_destructor__011863d4,0);
        if ((local_20 == 0) && (iVar3 == 0)) {
          FUN_005aea90(param_4,
                       "Invalid form list \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x26:
        iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                 &PTR_PTR__scalar_deleting_destructor__011863f0,0);
        if ((local_20 == 0) && (iVar3 == 0)) {
          FUN_005aea90(param_4,
                       "Invalid menu icon \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x27:
        iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                 &PTR_PTR__scalar_deleting_destructor__011861dc,0);
        if ((local_20 == 0) && (iVar3 == 0)) {
          FUN_005aea90(param_4,"Invalid perk \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x28:
        iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                 &PTR_PTR__scalar_deleting_destructor__0118640c,0);
        if ((local_20 == 0) && (iVar3 == 0)) {
          FUN_005aea90(param_4,"Invalid note \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x2a:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x54)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid Imagespace Modifier \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x2b:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x53)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid Imagespace \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x2f:
        iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                 &PTR_PTR__scalar_deleting_destructor__011840dc,0);
        if ((local_20 == 0) && (iVar3 == 0)) {
          FUN_005aea90(param_4,
                       "Invalid encounter zone \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x30:
        iVar3 = ___RTDynamicCast(local_1c,0,&PTR_PTR__scalar_deleting_destructor__01183028,
                                 &PTR_PTR__scalar_deleting_destructor__01186a18,0);
        if ((local_20 == 0) && (iVar3 == 0)) {
          FUN_005aea90(param_4,
                       "Invalid Idle form\'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x31:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x62)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid message \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x32:
        if (local_20 == 0) {
          if (local_1c != (int *)0x0) {
            uVar4 = FUN_00401170();
            cVar2 = FUN_00481f30(uVar4);
            if ((cVar2 != '\0') || (iVar3 = FUN_00401170(), iVar3 == 0x55)) break;
          }
          FUN_005aea90(param_4,
                       "Invalid inventory object \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x35:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            ((cVar2 = (**(code **)(*local_1c + 0xe8))(), cVar2 == '\0' &&
             (iVar3 = FUN_00401170(), iVar3 != 0x55)))))) {
          FUN_005aea90(param_4,
                       "Invalid object \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x36:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x66)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid music type \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x38:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            ((iVar3 = FUN_00401170(), iVar3 != 0x2a && (iVar3 = FUN_00401170(), iVar3 != 0x2d))))))
        {
          FUN_005aea90(param_4,
                       "Invalid NPC or LeveledCharacter \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x39:
        if ((local_20 == 0) &&
           ((local_1c == (int *)0x0 ||
            ((iVar3 = FUN_00401170(), iVar3 != 0x2b && (iVar3 = FUN_00401170(), iVar3 != 0x2c))))))
        {
          FUN_005aea90(param_4,
                       "Invalid Creature or LeveledCreature \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x3a:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x2d)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid LeveledCharacter \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x3b:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x2c)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid LeveledCreature \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x3c:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x34)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid LeveledItem \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x3d:
        if ((local_20 == 0) && (local_1c == (int *)0x0)) {
          FUN_005aea90(param_4,"Invalid form \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x3e:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x68)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid reputation \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x3f:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x6d)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid casino \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x40:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x6c)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid casino chip \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x41:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x71)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid challenge \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x42:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x74)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid caravan money \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x43:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x73)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid caravan card \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x44:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x75)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid caravan card \'%s\' for parameter %s.\r\nCompiled script not saved!"
                       ,local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
        break;
      case 0x45:
        if ((local_20 == 0) && ((local_1c == (int *)0x0 || (iVar3 = FUN_00401170(), iVar3 != 0x37)))
           ) {
          FUN_005aea90(param_4,
                       "Invalid region \'%s\' for parameter %s.\r\nCompiled script not saved!",
                       local_22c,*(undefined4 *)(param_2 + (short)local_c * 0xc));
          goto LAB_005b3ab4;
        }
      }
      *(undefined *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = 0x72;
      *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 1;
      *(undefined2 *)(param_3 + 0x20c + *(int *)(param_3 + 0x40c)) = (undefined2)local_2c;
      *(int *)(param_3 + 0x40c) = *(int *)(param_3 + 0x40c) + 2;
    }
    local_c = local_c + 1;
  } while( true );
}

