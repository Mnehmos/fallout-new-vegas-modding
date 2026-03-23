{
  Gunslinger Path — 8 New Pistol Perks

  Clones Gunslinger perk (has func=108 == 4.0 pistol condition),
  then changes the Entry Point ID and EPFD value for each.

  The effect-level DATA struct is named "Entry Point" and contains a FIELD
  also named "Entry Point" — requires careful path navigation.
  xEdit's wbPERKEntryPointAfterSet callback auto-fixes Function + TabCount.

  Run: Load FalloutNV.esm + PerkOverhaul.esp in xEdit.
       Right-click PerkOverhaul.esp -> Apply Script -> Gunslinger_PathPerks
}

unit GunslingerPathPerks;

const
  TARGET_ESP = 'PerkOverhaul.esp';

var
  tp, master: IInterface;
  perkCount: Integer;

function FindPerkByEdid(edid: string): IInterface;
var
  perkGroup, rec: IInterface;
  i: Integer;
begin
  Result := nil;
  perkGroup := GroupBySignature(master, 'PERK');
  if not Assigned(perkGroup) then Exit;
  for i := 0 to Pred(ElementCount(perkGroup)) do begin
    rec := ElementByIndex(perkGroup, i);
    if SameText(EditorID(rec), edid) then begin
      Result := rec;
      Exit;
    end;
  end;
end;

function CreatePerk(template: IInterface; newEdid, newName, newDesc: string;
  minLevel, entryPoint: Integer; epfdValue: Double): Boolean;
var
  newPerk, effects, effect, data, epElem, epfd: IInterface;
begin
  Result := False;

  // Clone template as NEW record
  AddRequiredElementMasters(template, tp, True);
  newPerk := wbCopyElementToFile(template, tp, True, True);
  if not Assigned(newPerk) then begin
    AddMessage('  ERROR: Clone failed for ' + newEdid);
    Exit;
  end;

  // Set identity
  SetElementEditValues(newPerk, 'EDID', newEdid);
  SetElementEditValues(newPerk, 'FULL', newName);
  SetElementEditValues(newPerk, 'DESC', newDesc);
  SetElementEditValues(newPerk, 'DATA\Min Level', IntToStr(minLevel));
  SetElementEditValues(newPerk, 'DATA\Num Ranks', '1');
  SetElementEditValues(newPerk, 'DATA\Is Playable', '1');

  // Get the first effect
  effects := ElementByName(newPerk, 'Effects');
  if not Assigned(effects) or (ElementCount(effects) < 1) then begin
    AddMessage('  ERROR: No effects on ' + newEdid);
    Exit;
  end;
  effect := ElementByIndex(effects, 0);

  // ── Change Entry Point ──
  // The DATA struct is named "Entry Point", containing field "Entry Point"
  // Try multiple path strategies

  // Strategy 1: ElementByPath with full nested path
  epElem := ElementByPath(effect, 'DATA - Entry Point\Entry Point');
  if Assigned(epElem) then begin
    SetNativeValue(epElem, entryPoint);
    AddMessage('    EP set via path (strategy 1)');
  end;

  // Strategy 2: if strategy 1 didn't find it, try alternate paths
  if not Assigned(epElem) then begin
    epElem := ElementByPath(effect, 'DATA\Entry Point');
    if Assigned(epElem) then begin
      SetNativeValue(epElem, entryPoint);
      AddMessage('    EP set via path (strategy 2)');
    end;
  end;

  // Strategy 3: via ElementBySignature + ElementByIndex
  if not Assigned(epElem) then begin
    data := ElementBySignature(effect, 'DATA');
    if Assigned(data) then begin
      epElem := ElementByIndex(data, 0);
      if Assigned(epElem) then begin
        SetNativeValue(epElem, entryPoint);
        AddMessage('    EP set via index (strategy 3)');
      end;
    end;
  end;

  // Strategy 4: SetElementNativeValues with path string
  if not Assigned(epElem) then begin
    try
      SetElementNativeValues(effect, 'DATA - Entry Point\Entry Point', entryPoint);
      AddMessage('    EP set via SetElementNativeValues (strategy 4)');
    except
      AddMessage('    WARNING: Could not set Entry Point to ' + IntToStr(entryPoint));
    end;
  end;

  // Set EPFD value
  epfd := ElementBySignature(effect, 'EPFD');
  if Assigned(epfd) then
    SetNativeValue(epfd, epfdValue)
  else
    AddMessage('    WARNING: No EPFD found');

  AddMessage('  + ' + newName + ' (Lv' + IntToStr(minLevel) +
    ', EP=' + IntToStr(entryPoint) + ', x' + FloatToStr(epfdValue) + ')');
  Inc(perkCount);
  Result := True;
end;

function Initialize: Integer;
var
  i: Integer;
  gunslinger: IInterface;
begin
  Result := 0;
  perkCount := 0;
  tp := nil;
  master := nil;

  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), TARGET_ESP) then
      tp := FileByIndex(i);
    if SameText(GetFileName(FileByIndex(i)), 'FalloutNV.esm') then
      master := FileByIndex(i);
  end;

  if not Assigned(tp) then begin
    AddMessage('[Gunslinger] ERROR: ' + TARGET_ESP + ' not loaded.');
    Result := 1;
    Exit;
  end;
  if not Assigned(master) then begin
    AddMessage('[Gunslinger] ERROR: FalloutNV.esm not found.');
    Result := 1;
    Exit;
  end;

  // Find Gunslinger as template
  gunslinger := FindPerkByEdid('Gunslinger');
  if not Assigned(gunslinger) then begin
    AddMessage('[Gunslinger] ERROR: Gunslinger perk not found in FalloutNV.esm');
    Result := 1;
    Exit;
  end;

  AddMessage('[Gunslinger] Template: Gunslinger (' + IntToHex(FormID(gunslinger), 8) + ')');
  AddMessage('[Gunslinger] Creating 8 perks...');
  AddMessage('');

  // 1. Quick Draw — EP 38 Equip Speed x1.50
  CreatePerk(gunslinger, 'MnQuickDraw', 'Quick Draw (Gunslinger)',
    'Lightning reflexes let you draw and holster pistols 50% faster.',
    4, 38, 1.50);

  // 2. Point Blank — EP 0 Weapon Damage x1.15
  CreatePerk(gunslinger, 'MnPointBlank', 'Point Blank',
    'Up close and personal. Pistols deal 15% more damage.',
    6, 0, 1.15);

  // 3. Fan the Hammer — EP 43 Attack Speed x1.20
  CreatePerk(gunslinger, 'MnFanTheHammer', 'Fan the Hammer',
    'Work the action like a pro. Pistol fire rate increased by 20%.',
    8, 43, 1.20);

  // 4. Hip Shooter — EP 34 Gun Spread x0.75
  CreatePerk(gunslinger, 'MnHipShooter', 'Hip Shooter',
    'Steady hands, tight groups. Pistol spread reduced by 25% from the hip.',
    10, 34, 0.75);

  // 5. Dead Eye — EP 2 Crit Damage x1.50
  CreatePerk(gunslinger, 'MnDeadEye', 'Dead Eye',
    'Every shot finds the weak point. Pistol critical damage increased by 50%.',
    12, 2, 1.50);

  // 6. Snap Shot — EP 40 VATS AP Cost x0.85
  CreatePerk(gunslinger, 'MnSnapShot', 'Snap Shot',
    'Instinctive targeting. Pistols cost 15% less AP in V.A.T.S.',
    14, 40, 0.85);

  // 7. Hair Trigger — EP 37 Reload Speed x1.35
  CreatePerk(gunslinger, 'MnHairTrigger', 'Hair Trigger',
    'Muscle memory takes over. Pistol reload speed increased by 35%.',
    16, 37, 1.35);

  // 8. Duelist — EP 0 Weapon Damage x1.25
  CreatePerk(gunslinger, 'MnDuelist', 'Duelist',
    'One weapon. One hand. Total mastery. Pistol damage increased by 25%.',
    18, 0, 1.25);

  AddMessage('');
  AddMessage('[Gunslinger] Done: ' + IntToStr(perkCount) + '/8 perks created');
end;

function Process(e: IInterface): Integer;
begin
  Result := 0;
end;

function Finalize: Integer;
begin
  Result := 0;
end;

end.
