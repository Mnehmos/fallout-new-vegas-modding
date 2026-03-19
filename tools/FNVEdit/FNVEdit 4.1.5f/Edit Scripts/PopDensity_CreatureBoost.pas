{
  PopulationDensity - Phase 1: Creature Density Boost

  Modifies LVLC (creature leveled lists) to increase population:
  1. Top-level encounter lists (EncWasteland*): increase Count on entries
  2. VEnc tier lists: add "Calculate for each item" flag
  3. Key faction LVLN lists: increase Count for patrol encounters

  Run on FalloutNV.esm — select ALL records, Apply Script.
  Creates overrides in PopulationDensity.esp.
}

unit PopDensityCreatureBoost;

var
  changeCount: Integer;
  targetPlugin: IInterface;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  changeCount := 0;

  // Find or prompt for target plugin
  targetPlugin := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'PopulationDensity.esp') then begin
      targetPlugin := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(targetPlugin) then begin
    targetPlugin := AddNewFile;
    if not Assigned(targetPlugin) then begin
      AddMessage('[PopDensity] ERROR: No target plugin selected. Aborting.');
      Result := 1;
      Exit;
    end;
  end;

  AddMessage('[PopDensity] Phase 1: Creature & NPC Density Boost');
  AddMessage('[PopDensity] Target: ' + GetFileName(targetPlugin));
  AddMessage('');
end;

procedure BoostListCounts(e: IInterface; newCount: Integer; desc: string);
var
  entries, entry, lvlo: IInterface;
  i, oldCount: Integer;
  override: IInterface;
begin
  entries := ElementByName(e, 'Leveled List Entries');
  if not Assigned(entries) then Exit;

  // Add masters then copy as override into our ESP
  AddRequiredElementMasters(e, targetPlugin, False);
  override := wbCopyElementToFile(e, targetPlugin, False, True);
  if not Assigned(override) then begin
    AddMessage('  WARNING: Could not copy ' + EditorID(e) + ' as override');
    Exit;
  end;

  entries := ElementByName(override, 'Leveled List Entries');
  if not Assigned(entries) then Exit;

  for i := 0 to Pred(ElementCount(entries)) do begin
    entry := ElementByIndex(entries, i);
    lvlo := ElementBySignature(entry, 'LVLO');
    if not Assigned(lvlo) then Continue;

    oldCount := GetElementNativeValues(lvlo, 'Count');
    if oldCount < newCount then begin
      SetElementNativeValues(lvlo, 'Count', newCount);
      Inc(changeCount);
    end;
  end;

  AddMessage('  ' + desc + ': ' + EditorID(e) + ' entries boosted to count=' + IntToStr(newCount));
end;

procedure SetCalcEachFlag(e: IInterface; desc: string);
var
  override, lvlf: IInterface;
  flags: Integer;
begin
  // Add masters then copy as override
  AddRequiredElementMasters(e, targetPlugin, False);
  override := wbCopyElementToFile(e, targetPlugin, False, True);
  if not Assigned(override) then Exit;

  lvlf := ElementBySignature(override, 'LVLF');
  if not Assigned(lvlf) then Exit;

  // Set "Calculate for each item in count" flag (bit 1 = value 2)
  flags := GetNativeValue(lvlf);
  if (flags and 2) = 0 then begin
    SetNativeValue(lvlf, flags or 2);
    AddMessage('  ' + desc + ': ' + EditorID(e) + ' +CalcEach flag');
    Inc(changeCount);
  end;
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);

  // Only process base game records (not our overrides)
  if not SameText(GetFileName(GetFile(e)), 'FalloutNV.esm') then Exit;

  // ═══ LVLC: Creature Lists ═══
  if sig = 'LVLC' then begin

    // Main wasteland encounter — boost all entries to count 2
    if SameText(edid, 'EncWastelandNV') then
      BoostListCounts(e, 2, 'WASTELAND');

    if SameText(edid, 'EncWastelandNVWeak') then
      BoostListCounts(e, 2, 'WASTELAND-WEAK');

    if SameText(edid, 'EncWastelandNVTough') then
      BoostListCounts(e, 2, 'WASTELAND-TOUGH');

    // Wasteland gecko encounter — more geckos
    if SameText(edid, 'EncWastelandNVGecko') then
      BoostListCounts(e, 2, 'GECKO');

    // Robot encounters
    if SameText(edid, 'EncRobotArmyWastelandNV') then
      BoostListCounts(e, 2, 'ROBOTS');

    // Top-level VEnc tier lists — set CalcEach so Count matters
    if (Pos('VEncTier', edid) = 1) and (Pos('75', edid) = 0) and
       (Pos('50', edid) = 0) and (Pos('30', edid) = 0) then begin
      // Base tier lists (no percentage suffix) — boost count and set CalcEach
      BoostListCounts(e, 2, 'TIER-BASE');
      SetCalcEachFlag(e, 'TIER-BASE');
    end;

    // Feral ghoul encounters — double up
    if SameText(edid, 'EncFeralGhoul') then
      BoostListCounts(e, 2, 'FERAL-GHOUL');

    // Super mutant encounters
    if SameText(edid, 'EncSuperMutantAll') then
      BoostListCounts(e, 2, 'SUPER-MUTANT');

    if SameText(edid, 'EncSuperMutantGunOrMelee') then
      BoostListCounts(e, 2, 'SUPER-MUTANT');

    // Cazador — more danger
    if SameText(edid, 'EncCazador') then
      BoostListCounts(e, 2, 'CAZADOR');

    // Coyote packs
    if SameText(edid, 'EncCoyote') then
      BoostListCounts(e, 3, 'COYOTE-PACK');

    // Giant mantis
    if SameText(edid, 'EncGiantMantis') then
      BoostListCounts(e, 2, 'MANTIS');

    // Radscorpion
    if SameText(edid, 'EncRadScorpion') then
      BoostListCounts(e, 2, 'RADSCORPION');

    // Deathclaw tier lists — boost but carefully
    if SameText(edid, 'VEncDeathclawTier1') then
      BoostListCounts(e, 2, 'DEATHCLAW');

    // Nightstalker
    if SameText(edid, 'VEncNightStalkerTier1') then
      BoostListCounts(e, 2, 'NIGHTSTALKER');
  end;

  // ═══ LVLN: NPC/Faction Lists ═══
  if sig = 'LVLN' then begin

    // Fiend encounters — more fiends per spawn
    if SameText(edid, 'EncFiendRandom') or
       SameText(edid, 'EncFiendGun') or
       SameText(edid, 'EncFiendMelee') or
       SameText(edid, 'EncFiendRifle') then
      BoostListCounts(e, 2, 'FIEND');

    // NCR patrol encounters — more troopers
    if SameText(edid, 'EncNCRTrooper') or
       SameText(edid, 'EncNCRTrooperGun') then
      BoostListCounts(e, 2, 'NCR-PATROL');

    // Wastelander encounters — more civilians
    if SameText(edid, 'VarWastelander') or
       SameText(edid, 'VarWastelanderMale') then
      BoostListCounts(e, 2, 'WASTELANDER');

    // Powder Ganger encounters
    if SameText(edid, 'VarNCRCFPowderGangerGun') or
       SameText(edid, 'VarNCRCFPowderGangerMelee') then
      BoostListCounts(e, 2, 'POWDER-GANGER');

    // Legion wasteland encounters
    if SameText(edid, 'VarLegionWastelandRecruit') or
       SameText(edid, 'VarLegionWastelandVeteran') then
      BoostListCounts(e, 2, 'LEGION');
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[PopDensity] Phase 1 complete: ' + IntToStr(changeCount) + ' entries modified');
  AddMessage('[PopDensity] Save the ESP to apply changes.');
end;

end.
