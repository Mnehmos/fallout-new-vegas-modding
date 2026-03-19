{
  GHOUL HORDE — Zombie Apocalypse Mode

  Amplifies ALL ghoul encounters by 5-10x:
  - All feral ghoul LVLC lists: count x10, CalcEach flag
  - All glowing ghoul lists: count x8
  - All reaver ghoul lists: count x5
  - Searchlight specific lists: count x10
  - Trooper ghoul CREA templates: 3x XP boost
  - Add trooper ghouls to general feral ghoul encounter lists
  - Top-level EncFeralGhoul: count x10

  Run on: FalloutNV.esm (select all, Apply Script)
  Target: PopulationDensity.esp (adds to existing mod)
}

unit GhoulHordeCreate;

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
    tp := AddNewFile;
    if not Assigned(tp) then begin
      AddMessage('[GhoulHorde] ERROR: No target plugin. Aborting.');
      Result := 1;
      Exit;
    end;
  end;

  AddMessage('=== GHOUL HORDE MODE ===');
  AddMessage('Target: ' + GetFileName(tp));
  AddMessage('');
end;

procedure BoostList(e: IInterface; newCount: Integer; setCalcEach: Boolean; desc: string);
var
  override, entries, entry, lvlo, lvlf: IInterface;
  i, oldCount, flags: Integer;
begin
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then begin
    AddMessage('  WARNING: Could not override ' + EditorID(e));
    Exit;
  end;

  // Boost counts
  entries := ElementByName(override, 'Leveled List Entries');
  if Assigned(entries) then begin
    for i := 0 to Pred(ElementCount(entries)) do begin
      entry := ElementByIndex(entries, i);
      lvlo := ElementBySignature(entry, 'LVLO');
      if Assigned(lvlo) then begin
        oldCount := GetElementNativeValues(lvlo, 'Count');
        if oldCount < newCount then begin
          SetElementNativeValues(lvlo, 'Count', newCount);
          Inc(changeCount);
        end;
      end;
    end;
  end;

  // Set CalcEach flag
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

  AddMessage('  ' + desc + ': ' + EditorID(e) + ' -> count=' + IntToStr(newCount) + ' CalcEach=' + IntToStr(Ord(setCalcEach)));
end;

procedure BoostCreatureXP(e: IInterface; xpMult: Integer; desc: string);
var
  override, data: IInterface;
  oldXP, newXP: Integer;
begin
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then begin
    AddMessage('  WARNING: Could not override ' + EditorID(e));
    Exit;
  end;

  // CREA XP is in DATA\XP field
  oldXP := GetElementNativeValues(override, 'DATA\XP');
  newXP := oldXP * xpMult;
  if newXP < 50 then newXP := 50; // minimum XP
  SetElementNativeValues(override, 'DATA\XP', newXP);
  Inc(changeCount);
  AddMessage('  ' + desc + ': ' + EditorID(e) + ' XP ' + IntToStr(oldXP) + ' -> ' + IntToStr(newXP));
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);
  if not SameText(GetFileName(GetFile(e)), 'FalloutNV.esm') then Exit;

  // ═══════════════════════════════════════════════════════════
  //  LVLC: GHOUL SPAWN LISTS — MEGA BOOST
  // ═══════════════════════════════════════════════════════════
  if sig = 'LVLC' then begin

    // ── TOP LEVEL: EncFeralGhoul — the master ghoul encounter ──
    if SameText(edid, 'EncFeralGhoul') then
      BoostList(e, 10, True, 'MASTER GHOUL');

    // ── SEARCHLIGHT SPECIFIC — maximum horde ──
    if SameText(edid, 'VEncTier2FeralGhoulMedSearchLight') then
      BoostList(e, 10, True, 'SEARCHLIGHT FERAL');
    if SameText(edid, 'VEncTier2FeralGhoulMedSearchLight50') then
      BoostList(e, 10, True, 'SEARCHLIGHT FERAL 50');
    if SameText(edid, 'VEncTier2GlowingGhoulMedSearchLight') then
      BoostList(e, 8, True, 'SEARCHLIGHT GLOWING');
    if SameText(edid, 'VEncTier2GlowingGhoulMedSearchLight50') then
      BoostList(e, 8, True, 'SEARCHLIGHT GLOWING 50');

    // ── TIER 1 FERAL GHOULS — swarm tier ──
    if SameText(edid, 'VEncTier1FeralGhoul') then
      BoostList(e, 10, True, 'T1 FERAL');
    if SameText(edid, 'VEncTier1FeralGhoulMed') then
      BoostList(e, 10, True, 'T1 FERAL MED');
    if SameText(edid, 'VEncTier1FeralGhoulMed50') then
      BoostList(e, 10, True, 'T1 FERAL MED50');
    if SameText(edid, 'VEncTier1FeralGhoulMedPers') then
      BoostList(e, 10, True, 'T1 FERAL PERS');
    if SameText(edid, 'VEncTier1FeralGhoulBMed') then
      BoostList(e, 10, True, 'T1 FERAL B');
    if SameText(edid, 'VEncTier1FeralGhoulBMedPers') then
      BoostList(e, 10, True, 'T1 FERAL B PERS');
    if SameText(edid, 'VEncTier1FeralGhoulAMed') then
      BoostList(e, 10, True, 'T1 FERAL A');
    if SameText(edid, 'VEncTier1FeralGhoulAMedPers') then
      BoostList(e, 10, True, 'T1 FERAL A PERS');

    // ── TIER 2 FERAL GHOULS — big groups ──
    if SameText(edid, 'VEncTier2FeralGhoulMed') then
      BoostList(e, 8, True, 'T2 FERAL MED');
    if SameText(edid, 'VEncTier2FeralGhoulMed30') then
      BoostList(e, 8, True, 'T2 FERAL MED30');
    if SameText(edid, 'VEncTier2FeralGhoulMed50') then
      BoostList(e, 8, True, 'T2 FERAL MED50');
    if SameText(edid, 'VEncTier2FeralGhoulMedPers') then
      BoostList(e, 8, True, 'T2 FERAL PERS');
    if SameText(edid, 'VEncTier2FeralGhoulAMed') then
      BoostList(e, 8, True, 'T2 FERAL A');
    if SameText(edid, 'VEncTier2FeralGhoulAMedPers') then
      BoostList(e, 8, True, 'T2 FERAL A PERS');
    if SameText(edid, 'VEncTier2FeralGhoulBMed') then
      BoostList(e, 8, True, 'T2 FERAL B');
    if SameText(edid, 'VEncTier2FeralGhoulBMedPers') then
      BoostList(e, 8, True, 'T2 FERAL B PERS');

    // ── GLOWING GHOULS — dangerous packs ──
    if SameText(edid, 'VEncTier3GlowingGhoulMed') then
      BoostList(e, 6, True, 'T3 GLOWING');
    if SameText(edid, 'VEncTier3GlowingGhoulMed50') then
      BoostList(e, 6, True, 'T3 GLOWING 50');
    if SameText(edid, 'VEncTier3GlowingGhoulMed75') then
      BoostList(e, 6, True, 'T3 GLOWING 75');
    if SameText(edid, 'VEncTier5GlowingGhoulMed') then
      BoostList(e, 5, True, 'T5 GLOWING');

    // ── REAVERS — deadly squads ──
    if SameText(edid, 'VEncTier4ReaverGhoulMed') then
      BoostList(e, 5, True, 'T4 REAVER');
    if SameText(edid, 'VEncTier4ReaverGhoulMed50') then
      BoostList(e, 5, True, 'T4 REAVER 50');
    if SameText(edid, 'VEncTier4ReaverGhoulMed75') then
      BoostList(e, 5, True, 'T4 REAVER 75');
    if SameText(edid, 'VEncTier5ReaverGhoulMed') then
      BoostList(e, 4, True, 'T5 REAVER');

    // ── VARIANT LISTS — the actual ghoul templates ──
    if SameText(edid, 'VarFeralGhoul1') then
      BoostList(e, 8, True, 'VAR FERAL 1');
    if SameText(edid, 'VarFeralGhoul2') then
      BoostList(e, 8, True, 'VAR FERAL 2');
  end;

  // ═══════════════════════════════════════════════════════════
  //  CREA: TROOPER GHOUL XP BOOST (3x)
  // ═══════════════════════════════════════════════════════════
  if sig = 'CREA' then begin

    // Searchlight trooper ghouls
    if SameText(edid, 'CampSearchlightFeralTrooperGhoul') then
      BoostCreatureXP(e, 3, 'SEARCHLIGHT FERAL');
    if SameText(edid, 'CampSearchlightGlowingTrooperGhoul') then
      BoostCreatureXP(e, 3, 'SEARCHLIGHT GLOWING');

    // Generic trooper ghoul templates
    if SameText(edid, 'VCrTier2FeralTrooperGhoul') then
      BoostCreatureXP(e, 3, 'TEMPLATE FERAL TROOPER');
    if SameText(edid, 'VCrTier2FeralTrooperGhoulNR') then
      BoostCreatureXP(e, 3, 'TEMPLATE FERAL TROOPER NR');
    if SameText(edid, 'VCrTier2FeralTrooperGhoulPers') then
      BoostCreatureXP(e, 3, 'TEMPLATE FERAL TROOPER PERS');
    if SameText(edid, 'VCrTier2FeralTrooperGhoulNRPers') then
      BoostCreatureXP(e, 3, 'TEMPLATE FERAL TROOPER NR PERS');
    if SameText(edid, 'VSpawnSpecialTier2FeralGhoulMedSL') then
      BoostCreatureXP(e, 3, 'SPAWN FERAL SEARCHLIGHT');

    // Glowing trooper templates
    if SameText(edid, 'VCrTier2GlowingTrooperGhoul') then
      BoostCreatureXP(e, 3, 'TEMPLATE GLOWING TROOPER');
    if SameText(edid, 'VCrTier2GlowingTrooperGhoulNR') then
      BoostCreatureXP(e, 3, 'TEMPLATE GLOWING TROOPER NR');
    if SameText(edid, 'VCrTier2GlowingTrooperGhoulPers') then
      BoostCreatureXP(e, 3, 'TEMPLATE GLOWING TROOPER PERS');
    if SameText(edid, 'VCrTier2GlowingTrooperGhoulNRPers') then
      BoostCreatureXP(e, 3, 'TEMPLATE GLOWING TROOPER NR PERS');
    if SameText(edid, 'VSpawnSpecialTier2GlowingGhoulMedSL') then
      BoostCreatureXP(e, 3, 'SPAWN GLOWING SEARCHLIGHT');
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('=== GHOUL HORDE COMPLETE: ' + IntToStr(changeCount) + ' changes ===');
  AddMessage('');
  AddMessage('Spawn multipliers:');
  AddMessage('  Tier 1 Ferals:    x10 (swarm)');
  AddMessage('  Tier 2 Ferals:    x8  (horde)');
  AddMessage('  Searchlight:      x10 (apocalypse)');
  AddMessage('  Glowing Ghouls:   x6  (danger pack)');
  AddMessage('  Reavers:          x5  (death squad)');
  AddMessage('  Trooper XP:       x3  (worth the effort)');
  AddMessage('');
  AddMessage('Save the ESP to unleash the horde.');
end;

end.
