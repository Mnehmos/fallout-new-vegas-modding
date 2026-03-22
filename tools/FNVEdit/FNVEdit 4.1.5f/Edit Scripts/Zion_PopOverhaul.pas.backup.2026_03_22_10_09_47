{
  Zion (Honest Hearts) Population Overhaul

  Makes Zion Valley a living, dangerous wilderness:
  - Wildlife: x3-5 (herds and packs, not loners)
  - White Legs: x3 (war parties)
  - Dead Horses / Sorrows: x2 (tribal groups)
  - Special encounters: x3 (spore carriers, yao guai)

  Run on: HonestHearts.esm (select all, Apply Script)
  Target: PopulationDensity.esp
}

unit ZionPopOverhaul;

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
    AddMessage('[Zion] ERROR: PopulationDensity.esp not loaded.');
    Result := 1;
    Exit;
  end;

  AddMessage('=== ZION VALLEY POPULATION OVERHAUL ===');
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

function Process(e: IInterface): Integer;
var
  sig, edid: string;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);
  if not SameText(GetFileName(GetFile(e)), 'HonestHearts.esm') then Exit;

  // ═══ LVLC: CREATURE SPAWN LISTS ═══
  if sig = 'LVLC' then begin

    // ── Random encounter tiers — the main wildlife system ──
    // Tier 1: Low areas (geckos, bloatflies, bighorners)
    if SameText(edid, 'NVDLC02EncRNDTier1Valley') then BoostList(e, 4, True, 'T1 VALLEY');
    if SameText(edid, 'NVDLC02EncRNDTier1ValleyRoad') then BoostList(e, 4, True, 'T1 ROAD');
    if SameText(edid, 'NVDLC02EncRNDTier1Hill') then BoostList(e, 3, True, 'T1 HILL');
    if SameText(edid, 'NVDLC02EncRNDTier1Mountain') then BoostList(e, 3, True, 'T1 MOUNTAIN');

    // Tier 2: Mid areas (cazadors, night stalkers)
    if SameText(edid, 'NVDLC02EncRNDTier2Valley') then BoostList(e, 3, True, 'T2 VALLEY');
    if SameText(edid, 'NVDLC02EncRNDTier2ValleyRoad') then BoostList(e, 3, True, 'T2 ROAD');
    if SameText(edid, 'NVDLC02EncRNDTier2Hill') then BoostList(e, 3, True, 'T2 HILL');
    if SameText(edid, 'NVDLC02EncRNDTier2Mountain') then BoostList(e, 3, True, 'T2 MOUNTAIN');

    // Tier 3: High areas (yao guai, giant cazadors)
    if SameText(edid, 'NVDLC02EncRNDTier3Valley') then BoostList(e, 2, True, 'T3 VALLEY');
    if SameText(edid, 'NVDLC02EncRNDTier3ValleyRoad') then BoostList(e, 2, True, 'T3 ROAD');
    if SameText(edid, 'NVDLC02EncRNDTier3Hill') then BoostList(e, 2, True, 'T3 HILL');
    if SameText(edid, 'NVDLC02EncRNDTier3Mountain') then BoostList(e, 2, True, 'T3 MOUNTAIN');

    // Tier 4: Extreme (alpha predators)
    if SameText(edid, 'NVDLC02EncRNDTier4Mountain') then BoostList(e, 2, True, 'T4 MOUNTAIN');

    // ── Species groups — herds and packs ──
    // Group 1: Small creatures
    if SameText(edid, 'NVDLC02EncGr1Mammal') then BoostList(e, 4, True, 'GR1 MAMMAL');
    if SameText(edid, 'NVDLC02EncGr1Mammal02') then BoostList(e, 4, True, 'GR1 MAMMAL2');
    if SameText(edid, 'NVDLC02EncGr1Insect') then BoostList(e, 5, True, 'GR1 INSECT');
    if SameText(edid, 'NVDLC02EncGr1Reptile') then BoostList(e, 4, True, 'GR1 REPTILE');

    // Group 2: Medium creatures
    if SameText(edid, 'NVDLC02EncGr2Mammal') then BoostList(e, 3, True, 'GR2 MAMMAL');
    if SameText(edid, 'NVDLC02EncGr2Insect') then BoostList(e, 3, True, 'GR2 INSECT');
    if SameText(edid, 'NVDLC02EncGr2Reptile') then BoostList(e, 3, True, 'GR2 REPTILE');

    // Group 3: Large creatures
    if SameText(edid, 'NVDLC02EncGr3Mammal') then BoostList(e, 2, True, 'GR3 MAMMAL');
    if SameText(edid, 'NVDLC02EncGr3Insect') then BoostList(e, 2, True, 'GR3 INSECT');
    if SameText(edid, 'NVDLC02EncGr3Reptile') then BoostList(e, 2, True, 'GR3 REPTILE');

    // ── Special encounters ──
    if SameText(edid, 'NVDLC02EncSpecialGeckos') then BoostList(e, 4, True, 'GECKO PACK');
    if SameText(edid, 'NVDLC02EncSpecialFlyingBugs') then BoostList(e, 5, True, 'BUG SWARM');
    if SameText(edid, 'NVDLC02EncSpecialAntsMantises') then BoostList(e, 4, True, 'ANT/MANTIS');
    if SameText(edid, 'NVDLC02EncSpecialSporeCarriers') then BoostList(e, 3, True, 'SPORE CARRIER');
    if SameText(edid, 'NVDLC02EncSpecialSporePlants') then BoostList(e, 3, True, 'SPORE PLANT');
    if SameText(edid, 'NVDLC02EncSpecialMQ03YaoGuai') then BoostList(e, 2, True, 'YAO GUAI');

    // ── Gecko variants ──
    if SameText(edid, 'NVDLC02EncCrGreenGeckoSmall') then BoostList(e, 4, True, 'GREEN GECKO SM');
    if SameText(edid, 'NVDLC02EncCrGreenGeckoMed') then BoostList(e, 3, True, 'GREEN GECKO MD');
    if SameText(edid, 'NVDLC02EncCrGreenGeckoLarge') then BoostList(e, 2, True, 'GREEN GECKO LG');

    // ── White Leg war dogs ──
    if SameText(edid, 'NVDLC02EncCrWhiteLegMongrel') then BoostList(e, 3, True, 'WHITE LEG DOG');
  end;

  // ═══ LVLN: NPC FACTION LISTS ═══
  if sig = 'LVLN' then begin

    // ── White Legs — war parties x3 ──
    if SameText(edid, 'NVDLC02EncEveWhiteLeg') then BoostList(e, 3, True, 'WHITE LEG ALL');
    if SameText(edid, 'NVDLC02EncEveWhiteLegMale') then BoostList(e, 3, True, 'WHITE LEG MALE');
    if SameText(edid, 'NVDLC02EncEveWhiteLegFemale') then BoostList(e, 3, True, 'WHITE LEG FEM');
    if SameText(edid, 'NVDLC02EncEveWhiteLegMelee') then BoostList(e, 3, True, 'WHITE LEG MELEE');
    if SameText(edid, 'NVDLC02EncEveWhiteLegRange') then BoostList(e, 3, True, 'WHITE LEG RANGE');

    // White Leg specialists
    if Pos('WhiteLegMale', edid) > 0 then BoostList(e, 2, True, 'WL SPECIALIST');
    if Pos('WhiteLegFemale', edid) > 0 then BoostList(e, 2, True, 'WL SPECIALIST');

    // ── Dead Horses — tribal groups x2 ──
    if SameText(edid, 'NVDLC02EncEveDeadHorse') then BoostList(e, 2, True, 'DEAD HORSE ALL');
    if SameText(edid, 'NVDLC02EncEveDeadHorseMale') then BoostList(e, 2, True, 'DEAD HORSE MALE');
    if SameText(edid, 'NVDLC02EncEveDeadHorseFemale') then BoostList(e, 2, True, 'DEAD HORSE FEM');
    if SameText(edid, 'NVDLC02DeadHorseRnd') then BoostList(e, 2, True, 'DEAD HORSE RND');

    // Dead Horse specialists
    if Pos('DeadHorseMale', edid) > 0 then BoostList(e, 2, True, 'DH SPECIALIST');
    if Pos('DeadHorseFemale', edid) > 0 then BoostList(e, 2, True, 'DH SPECIALIST');

    // ── Sorrows — tribal groups x2 ──
    if SameText(edid, 'NVDLC02EncEveSorrow') then BoostList(e, 2, True, 'SORROW ALL');
    if SameText(edid, 'NVDLC02EncEveSorrowMale') then BoostList(e, 2, True, 'SORROW MALE');
    if SameText(edid, 'NVDLC02EncEveSorrowFemale') then BoostList(e, 2, True, 'SORROW FEM');
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('=== ZION OVERHAUL COMPLETE ===');
  AddMessage('Changes: ' + IntToStr(changeCount));
  AddMessage('');
  AddMessage('  Wildlife Tier 1:    x3-5 (herds along valleys and roads)');
  AddMessage('  Wildlife Tier 2:    x3   (predator packs in hills)');
  AddMessage('  Wildlife Tier 3-4:  x2   (apex predators in mountains)');
  AddMessage('  Species Groups:     x2-5 (natural herd sizes)');
  AddMessage('  Special Encounters: x2-5 (spores, yao guai, bug swarms)');
  AddMessage('  White Legs:         x3   (war parties, not scouts)');
  AddMessage('  Dead Horses:        x2   (tribal hunting groups)');
  AddMessage('  Sorrows:            x2   (gathering parties)');
  AddMessage('');
  AddMessage('The valley remembers its children.');
end;

end.
