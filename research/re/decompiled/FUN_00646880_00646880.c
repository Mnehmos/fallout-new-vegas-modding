
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 FUN_00646880(undefined4 param_1,undefined4 param_2)

{
  float10 fVar1;
  float10 fVar2;
  float local_8;
  
  switch(param_2) {
  case 0:
  case 2:
  case 5:
  case 6:
  case 7:
  case 8:
  case 9:
    fVar2 = (float10)FUN_00646800(param_1,0x1b,0);
    fVar1 = (float10)FUN_00646800(param_1,0x1c,0);
    fVar2 = (fVar1 + (float10)(double)fVar2) / (float10)_DAT_01011590;
    break;
  default:
    fVar2 = (float10)FUN_00646800(param_1,0x1c,0);
  }
  local_8 = (float)fVar2;
  return (float10)local_8;
}

