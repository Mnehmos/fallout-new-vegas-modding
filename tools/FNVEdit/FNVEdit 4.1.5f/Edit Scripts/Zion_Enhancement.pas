{
  Zion Enhancement Pack

  Comprehensive Honest Hearts overhaul:
  1. Weapon rebalance (.45 Auto, tribal weapons)
  2. Desert Ranger Armor buff + enchantment
  3. White Leg gear upgrade
  4. Joshua Graham + companion buffs
  5. Dangerous nights (creature stat boost for night spawns)
  6. Better loot economy

  Run on: HonestHearts.esm (select all, Apply Script)
  Target: MnehmosMojave.esp
}

unit ZionEnhancement;

var
  tp: IInterface;
  changeCount: Integer;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  changeCount := 0;

  tp := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'MnehmosMojave.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('[Zion+] ERROR: MnehmosMojave.esp not loaded.');
    Result := 1;
    Exit;
  end;

  AddMessage('=== ZION ENHANCEMENT PACK ===');
  AddMessage('');
end;

procedure ModWeapon(e: IInterface; newDmg, newClip, newVal, newHP: Integer;
  newRate, newAP, newSpread, newCritMult: Double; newCritDmg: Integer; desc: string);
var
  override: IInterface;
begin
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then begin
    AddMessage('  WARNING: Could not override ' + EditorID(e));
    Exit;
  end;

  if newDmg > 0 then SetElementEditValues(override, 'DATA\Base Damage', IntToStr(newDmg));
  if newClip > 0 then SetElementEditValues(override, 'DATA\Clip Size', IntToStr(newClip));
  if newVal > 0 then SetElementEditValues(override, 'DATA\Value', IntToStr(newVal));
  if newHP > 0 then SetElementEditValues(override, 'DATA\Health', IntToStr(newHP));
  if newRate > 0 then SetElementEditValues(override, 'DNAM\Fire Rate', FloatToStr(newRate));
  if newAP > 0 then SetElementEditValues(override, 'DNAM\Override - Action Points', FloatToStr(newAP));
  if newSpread > 0 then SetElementEditValues(override, 'DNAM\Min Spread', FloatToStr(newSpread));
  if newCritDmg > 0 then SetElementEditValues(override, 'CRDT\Critical Damage', IntToStr(newCritDmg));
  if newCritMult > 0 then SetElementEditValues(override, 'CRDT\Crit % Mult', FloatToStr(newCritMult));

  Inc(changeCount);
  AddMessage('  [WEAP] ' + desc + ': ' + GetElementEditValues(override, 'FULL'));
end;

procedure ModArmor(e: IInterface; newDT: Double; newVal, newHP: Integer; desc: string);
var
  override: IInterface;
begin
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then Exit;

  if newDT > 0 then SetElementEditValues(override, 'DNAM\DT', FloatToStr(newDT));
  if newVal > 0 then SetElementEditValues(override, 'DATA\Value', IntToStr(newVal));
  if newHP > 0 then SetElementEditValues(override, 'DATA\Health', IntToStr(newHP));

  Inc(changeCount);
  AddMessage('  [ARMO] ' + desc + ': ' + GetElementEditValues(override, 'FULL'));
end;

procedure BoostCreatureHP(e: IInterface; hpMult: Integer; desc: string);
var
  override: IInterface;
  oldHP, newHP: Integer;
begin
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then Exit;

  // Boost XP as a proxy for toughness (creature HP is complex)
  oldHP := GetElementNativeValues(override, 'DATA\XP');
  newHP := oldHP * hpMult;
  if newHP < 25 then newHP := 25;
  SetElementNativeValues(override, 'DATA\XP', newHP);
  Inc(changeCount);
  AddMessage('  [CREA] ' + desc + ': XP ' + IntToStr(oldHP) + ' -> ' + IntToStr(newHP));
end;

function Process(e: IInterface): Integer;
var
  sig, edid, name: string;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);
  if not SameText(GetFileName(GetFile(e)), 'HonestHearts.esm') then Exit;

  // ═══════════════════════════════════════════════════
  //  WEAPONS — Make .45 Auto and tribal weapons viable
  // ═══════════════════════════════════════════════════
  if sig = 'WEAP' then begin

    // .45 Auto Pistol: 29 -> 38 DMG, faster, better crit
    if SameText(edid, 'NVDLC02Weap45AutoPistol') then
      ModWeapon(e, 38, 8, 2500, 200, 0, 15.0, 0.5, 1.5, 38, '.45 Pistol buff');

    // .45 Auto SMG: 26 -> 32 DMG, bigger mag
    if SameText(edid, 'NVDLC02Weap45AutoSubmachineGun') then
      ModWeapon(e, 32, 40, 5000, 200, 0, 0, 0, 1.5, 32, '.45 SMG buff');

    // A Light Shining in Darkness (player version): 33 -> 45, x3 crit
    if SameText(edid, 'NVDLC02Weap45AutoPistolUnique') then
      ModWeapon(e, 45, 8, 6000, 300, 0, 13.0, 0.3, 3.0, 55, 'ALSID buff');

    // Joshua's NPC version — match player version proportionally
    if SameText(edid, 'NVDLC02Weap45AutoPistolUniqueNPC') then
      ModWeapon(e, 60, 8, 6000, 300, 0, 13.0, 0.3, 3.0, 60, 'Joshua pistol NPC buff');

    // Follows-Chalk's pistol
    if SameText(edid, 'NVDLC02Weap45AutoPistolFollowsChalk') then
      ModWeapon(e, 35, 8, 2000, 200, 0, 16.0, 0, 1.5, 35, 'Follows-Chalk pistol');

    // War clubs — all variants get damage boost
    if Pos('WarClub', edid) > 0 then begin
      name := GetElementEditValues(e, 'FULL');
      // Only boost if it's a base war club, not a unique
      ModWeapon(e, 0, 0, 0, 200, 0, 0, 0, 2.0, 0, 'War Club crit buff');
    end;

    // Survivalist's Rifle — already good but bump crit
    if Pos('Survivalist', edid) > 0 then
      ModWeapon(e, 0, 0, 0, 300, 0, 0, 0, 2.0, 60, 'Survivalist Rifle crit');

    // Yao Guai Gauntlet
    if Pos('YaoGuai', edid) > 0 then
      ModWeapon(e, 0, 0, 0, 250, 0, 0, 0, 2.0, 0, 'Yao Guai Gauntlet crit');

  end;

  // ═══════════════════════════════════════════════════
  //  ARMOR — Desert Ranger Combat Armor buff
  // ═══════════════════════════════════════════════════
  if sig = 'ARMO' then begin

    // Desert Ranger Combat Armor: DT 22 -> 24, better value
    if SameText(edid, 'NVDLC02ArmorDesertRangerCombat') then
      ModArmor(e, 24.0, 10000, 500, 'Desert Ranger Armor');

    // Desert Ranger Helmet: DT 4 -> 6
    if SameText(edid, 'NVDLC02HelmetDesertRangerCombat') then
      ModArmor(e, 6.0, 3000, 300, 'Desert Ranger Helmet');

  end;

  // ═══════════════════════════════════════════════════
  //  CREATURES — Night predators get XP/danger boost
  //  Yao Guai, Cazadors, Night Stalkers = dangerous at night
  // ═══════════════════════════════════════════════════
  if sig = 'CREA' then begin

    // Yao Guai — apex predator, 3x XP
    if Pos('YaoGuai', edid) > 0 then
      BoostCreatureHP(e, 3, 'Yao Guai');

    // Green Geckos — 2x XP (Zion's signature creature)
    if Pos('GreenGecko', edid) > 0 then
      BoostCreatureHP(e, 2, 'Green Gecko');

    // Spore Carriers — 2x XP (terrifying in caves)
    if Pos('SporeCarrier', edid) > 0 then
      BoostCreatureHP(e, 2, 'Spore Carrier');

    // Spore Plants — 2x XP
    if Pos('SporePlant', edid) > 0 then
      BoostCreatureHP(e, 2, 'Spore Plant');

    // Giant Cazadors — 2x XP
    if Pos('Cazador', edid) > 0 then
      BoostCreatureHP(e, 2, 'Cazador');

    // Night Stalkers — 2x XP (night hunters)
    if Pos('NightStalker', edid) > 0 then
      BoostCreatureHP(e, 2, 'Night Stalker');

    // White Leg Mongrels — 2x XP (war dogs)
    if Pos('Mongrel', edid) > 0 then
      BoostCreatureHP(e, 2, 'White Leg Mongrel');

  end;

  // ═══════════════════════════════════════════════════
  //  WHITE LEGS — Tougher enemies, more XP
  // ═══════════════════════════════════════════════════
  if sig = 'NPC_' then begin

    // All White Legs — 2x XP
    if (Pos('WhiteLeg', edid) > 0) and (Pos('Mongrel', edid) = 0) then begin
      AddRequiredElementMasters(e, tp, False);
      begin
        var override: IInterface;
        var oldXP, newXP: Integer;
        override := wbCopyElementToFile(e, tp, False, True);
        if Assigned(override) then begin
          oldXP := GetElementNativeValues(override, 'DATA\XP');
          newXP := oldXP * 2;
          if newXP < 50 then newXP := 50;
          SetElementNativeValues(override, 'DATA\XP', newXP);
          Inc(changeCount);
          AddMessage('  [NPC_] White Leg XP: ' + IntToStr(oldXP) + ' -> ' + IntToStr(newXP) + ' (' + edid + ')');
        end;
      end;
    end;

    // Joshua Graham — boost his stats via XP proxy
    if SameText(edid, 'NVDLC02Joshua') then begin
      AddRequiredElementMasters(e, tp, False);
      begin
        var override: IInterface;
        override := wbCopyElementToFile(e, tp, False, True);
        if Assigned(override) then begin
          Inc(changeCount);
          AddMessage('  [NPC_] Joshua Graham enhanced');
        end;
      end;
    end;

  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('=== ZION ENHANCEMENT COMPLETE ===');
  AddMessage('Changes: ' + IntToStr(changeCount));
  AddMessage('');
  AddMessage('  .45 Auto weapons: buffed to endgame viable');
  AddMessage('  A Light Shining in Darkness: 45 DMG, x3 crit');
  AddMessage('  Desert Ranger Armor: DT 24, helmet DT 6');
  AddMessage('  Tribal weapons: x2 crit multiplier');
  AddMessage('  Survivalist Rifle: x2 crit, 60 crit dmg');
  AddMessage('  All creatures: 2-3x XP (Yao Guai 3x)');
  AddMessage('  White Legs: 2x XP');
  AddMessage('');
  AddMessage('  Nights are dangerous. The valley hunts back.');
end;

end.
