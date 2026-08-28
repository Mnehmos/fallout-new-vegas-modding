
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

int __fastcall FUN_006c02c0(int param_1)

{
  uint uVar1;
  int *unaff_FS_OFFSET;
  int local_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00f034f5;
  local_10 = *unaff_FS_OFFSET;
  uVar1 = DAT_011c16bc ^ (uint)&stack0xfffffffc;
  *unaff_FS_OFFSET = (int)&local_10;
  FUN_0044fae0(uVar1);
  local_8 = 0;
  FUN_006c5fc0(0x25);
  local_8._0_1_ = 1;
  Concurrency::details::QuickBitSet::QuickBitSet((QuickBitSet *)(param_1 + 0x2c));
  local_8._0_1_ = 2;
  Concurrency::details::QuickBitSet::QuickBitSet((QuickBitSet *)(param_1 + 0x34));
  local_8._0_1_ = 3;
  FUN_004ee810();
  local_8._0_1_ = 4;
  FUN_006c6450(7,8);
  local_8._0_1_ = 5;
  FUN_006c6450(7,8);
  local_8._0_1_ = 6;
  FUN_006c6070(0x25);
  local_8._0_1_ = 7;
  Concurrency::details::QuickBitSet::QuickBitSet((QuickBitSet *)(param_1 + 0xf0));
  local_8._0_1_ = 8;
  Concurrency::details::QuickBitSet::QuickBitSet((QuickBitSet *)(param_1 + 0xf8));
  local_8._0_1_ = 9;
  FUN_006c5fc0(0x25);
  local_8._0_1_ = 10;
  FUN_006c5fc0(0x25);
  local_8._0_1_ = 0xb;
  FUN_0044dee0();
  local_8._0_1_ = 0xc;
  FUN_006c60a0(0x25);
  local_8._0_1_ = 0xd;
  FUN_006c6c10();
  local_8._0_1_ = 0xe;
  FUN_006c6c10();
  local_8._0_1_ = 0xf;
  Concurrency::details::QuickBitSet::QuickBitSet((QuickBitSet *)(param_1 + 0x160));
  Concurrency::details::QuickBitSet::QuickBitSet((QuickBitSet *)(param_1 + 0x180));
  local_8._0_1_ = 0x10;
  Concurrency::details::QuickBitSet::QuickBitSet((QuickBitSet *)(param_1 + 0x188));
  local_8._0_1_ = 0x11;
  FUN_00633c90(0);
  local_8 = CONCAT31(local_8._1_3_,0x12);
  FUN_0045d260("Pathing","Obstacle Manager Update",1,1);
  FUN_0045d260("Pathing","Navmesh Background Update",0,1);
  FUN_00404eb0(0x2e,1,
               "D:\\_Fallout3\\Platforms\\Common\\Code\\Fallout Shared\\Pathfinding\\NavMeshObstacleManager.cpp"
               ,0xb8);
  *(undefined4 *)(param_1 + 0x120) = 0;
  *(undefined4 *)(param_1 + 0x124) = 0;
  *(undefined *)(param_1 + 0x198) = 0;
  *(undefined4 *)(param_1 + 400) = 0;
  *(undefined4 *)(param_1 + 0x194) = _DAT_0106c398;
  *(undefined *)(param_1 + 0x18) = 0;
  FUN_00404ee0();
  *unaff_FS_OFFSET = local_10;
  return param_1;
}

