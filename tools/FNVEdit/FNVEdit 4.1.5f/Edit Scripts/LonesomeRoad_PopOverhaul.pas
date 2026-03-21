{
  Lonesome Road Population Overhaul

  Makes The Divide a true gauntlet:
  - Tunneler swarms: x5-8 (they hunt in packs)
  - Marked Men patrols: x3 (war parties, not lone scouts)
  - Deathclaws: x2-3 (territorial packs)
  - Robots: x2 (automated defense grid still active)

  Run on: LonesomeRoad.esm (select all, Apply Script)
  Target: PopulationDensity.esp
}

unit LonesomeRoadPopOverhaul;

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
    if SameText(GetFileName(FileByIndex(i)), 'PopulationDensity.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('[LR] ERROR: PopulationDensity.esp not loaded.');
    Result := 1;
    Exit;
  end;

  AddMessage('=== LONESOME ROAD POPULATION OVERHAUL ===');
  AddMessage('Target: ' + GetFileName(tp));
  AddMessage('');
end;

procedure BoostList(e: IInterface; newCount: Integer; setCalcEach: Boolean; desc: string);
var
  override, entries, entry, lvlo, lvlf: IInterface;
  i, flags: Integer;
begin
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then begin
    AddMessage('  WARNING: Could not override ' + EditorID(e));
    Exit;
  end;

  entries := ElementByName(override, 'Leveled List Entries');
  if Assigned(entries) then begin
    for i := 0 to Pred(ElementCount(entries)) do begin
      entry := ElementByIndex(entries, i);
      lvlo := ElementBySignature(entry, 'LVLO');
      if Assigned(lvlo) then begin
        if GetElementNativeValues(lvlo, 'Count') < newCount then begin
          SetElementNativeValues(lvlo, 'Count', newCount);
          Inc(changeCount);
        end;
      end;
    end;
  end;

  if setCalcEach then begin
    lvlf := ElementBySignature(override, 'LVLF');
    if Assigned(lvlf) then begin
      flags := GetNativeValue(lvlf);
      if (flags and 2) = 0 then begin
        SetNativeValue(lvlf, flags or 2);
        Inc(changeCount);
      end;
    end;
  end;

  AddMessage('  ' + desc + ': ' + EditorID(e) + ' count=' + IntToStr(newCount));
end;

procedure BoostXP(e: IInterface; mult: Integer; desc: string);
var
  override: IInterface;
  oldXP, newXP: Integer;
begin
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then Exit;

  oldXP := GetElementNativeValues(override, 'DATA\XP');
  newXP := oldXP * mult;
  if newXP < 50 then newXP := 50;
  SetElementNativeValues(override, 'DATA\XP', newXP);
  Inc(changeCount);
  AddMessage('  ' + desc + ': XP ' + IntToStr(oldXP) + ' -> ' + IntToStr(newXP));
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);
  if not SameText(GetFileName(GetFile(e)), 'LonesomeRoad.esm') then Exit;

  // ═══ LVLC: CREATURE SPAWN LISTS ═══
  if sig = 'LVLC' then begin

    // TUNNELERS — swarm x5-8
    if SameText(edid, 'NVDLC04TunnelerENC') then
      BoostList(e, 8, True, 'TUNNELER SWARM');
    if SameText(edid, 'NVDLC04TunnelerAmbusherENC') then
      BoostList(e, 6, True, 'TUNNELER AMBUSH');
    if SameText(edid, 'NVDLC04TunnelerBruteENC') then
      BoostList(e, 4, True, 'TUNNELER BRUTE');
    if SameText(edid, 'NVDLC04TunnelerVenomENC') then
      BoostList(e, 5, True, 'TUNNELER VENOM');

    // DEATHCLAWS — packs x3
    if SameText(edid, 'NVDLC04DeathClawGLENC') then
      BoostList(e, 3, True, 'DEATHCLAW');
    if SameText(edid, 'NVDLC04DeathClawYoungGLENC') then
      BoostList(e, 3, True, 'DEATHCLAW YOUNG');
    if SameText(edid, 'NVDLC04DeathClawAlphaGLENC') then
      BoostList(e, 2, True, 'DEATHCLAW ALPHA');

    // ROBOTS — defense grid x2
    if SameText(edid, 'NVDLC04SentryBotGLENC') then
      BoostList(e, 2, True, 'SENTRY BOT');
    if SameText(edid, 'NVDLC04SentryBotMGENC') then
      BoostList(e, 2, True, 'SENTRY BOT MG');
    if SameText(edid, 'NVDLC04TurretMarkIIENC') then
      BoostList(e, 3, True, 'TURRET MK2');
    if SameText(edid, 'NVDLC04TurretMarkIVENC') then
      BoostList(e, 3, True, 'TURRET MK4');
    if SameText(edid, 'NVDLC04TurretMarkVIENC') then
      BoostList(e, 2, True, 'TURRET MK6');
    if SameText(edid, 'NVDLC04TurretMarkAllENC') then
      BoostList(e, 3, True, 'TURRET ALL');

    // EYEBOTS — more support x2
    if SameText(edid, 'NVDLC04EyebotMedicalENC') then
      BoostList(e, 2, True, 'EYEBOT MED');
    if SameText(edid, 'NVDLC04EyebotRepairENC') then
      BoostList(e, 2, True, 'EYEBOT REPAIR');

    // MOLE RATS — infested x4
    if SameText(edid, 'NVDLC04MoleRatGLENC') then
      BoostList(e, 4, True, 'MOLE RAT');
    if SameText(edid, 'NVDLC04MoleRatPupGLENC') then
      BoostList(e, 5, True, 'MOLE RAT PUP');

    // GLOWING GHOULS
    if SameText(edid, 'NVDLC04NukeNCRGlowingGhoulENC') then
      BoostList(e, 4, True, 'GLOWING GHOUL NUKE');
  end;

  // ═══ CREA: XP BOOST + STAT BOOST for all creatures ═══
  if sig = 'CREA' then begin
    // Tunneler Queen — 3x XP
    if SameText(edid, 'NVDLC04TunnelerBoss') then
      BoostXP(e, 3, 'TUNNELER QUEEN');
    // Rawr — 3x XP
    if SameText(edid, 'NVDLC04DeathclawBoss') then
      BoostXP(e, 3, 'RAWR');
    // All tunneler variants — 2x XP
    if (Pos('Tunneler', edid) > 0) and (Pos('Boss', edid) = 0) and (Pos('LVL', edid) = 0) and (Pos('ENC', edid) = 0) and (Pos('Wave', edid) = 0) then
      BoostXP(e, 2, 'TUNNELER');
    // All deathclaw variants — 2x XP
    if (Pos('DeathClaw', edid) > 0) or (Pos('Deathclaw', edid) > 0) then begin
      if (Pos('Boss', edid) = 0) and (Pos('LVL', edid) = 0) and (Pos('ENC', edid) = 0) and (Pos('DEAD', edid) = 0) then
        BoostXP(e, 2, 'DEATHCLAW');
    end;
    // Sentry bots — 2x XP
    if Pos('SentryBot', edid) > 0 then begin
      if (Pos('ENC', edid) = 0) then
        BoostXP(e, 2, 'SENTRY BOT');
    end;
  end;

  // ═══ NPC_: MARKED MEN — ALL get XP boost + bosses get 3x ═══
  if sig = 'NPC_' then begin
    // Bosses — 3x XP
    if SameText(edid, 'NVDLC04MarkedMenScoutBoss') then
      BoostXP(e, 3, 'BLADE (boss)');
    if SameText(edid, 'NVDLC04MarkedMenRavagerBoss') then
      BoostXP(e, 3, 'BONESAW (boss)');
    if SameText(edid, 'NVDLC04MarkedMenMarauderBoss') then
      BoostXP(e, 3, 'BEAST (boss)');
    if SameText(edid, 'NVDLC04MarkedMenHunterBoss') then
      BoostXP(e, 3, 'BLISTER (boss)');

    // All regular Marked Men — 2x XP
    if (Pos('MarkedMen', edid) > 0) and (Pos('Boss', edid) = 0) and (Pos('TEMPLATE', edid) = 0) and (Pos('test', edid) = 0) then
      BoostXP(e, 2, 'MARKED MAN');

    // Irradiated Marked Men — 2x XP
    if Pos('NukeSilo2', edid) > 0 then
      BoostXP(e, 2, 'IRRADIATED MARKED MAN');
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('=== LONESOME ROAD OVERHAUL COMPLETE ===');
  AddMessage('Changes: ' + IntToStr(changeCount));
  AddMessage('');
  AddMessage('  Tunnelers:       x5-8 swarm, 2x XP all variants');
  AddMessage('  Deathclaws:      x2-3 packs, 2x XP all variants');
  AddMessage('  Robots:          x2-3 defense grid, 2x XP sentry bots');
  AddMessage('  Mole Rats:       x4-5 infestation');
  AddMessage('  Glowing Ghouls:  x4 irradiated zone');
  AddMessage('  Marked Men:      2x XP all variants (hand-placed, cant multiply)');
  AddMessage('  Bosses:          3x XP (Blade, Bonesaw, Beast, Blister, Queen, Rawr)');
  AddMessage('');
  AddMessage('The Divide remembers.');
end;

end.
