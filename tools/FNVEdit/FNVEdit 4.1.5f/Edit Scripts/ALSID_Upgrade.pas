{
  A Light Shining in Darkness — Ascended Override

  Overrides the player-obtainable ALSID with buffed stats.
  When you pick it up in Honest Hearts, it's already upgraded.

  Run on: HonestHearts.esm (click it, Apply Script)
  Target: MnehmosMojave.esp
}

unit ALSIDUpgrade;

var
  tp: IInterface;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;

  tp := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'MnehmosMojave.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('ERROR: MnehmosMojave.esp not loaded.');
    Result := 1;
    Exit;
  end;

  AddMessage('[ALSID] Upgrading A Light Shining in Darkness...');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  override: IInterface;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'WEAP' then Exit;

  edid := EditorID(e);
  if not SameText(edid, 'NVDLC02Weap45AutoPistolUnique') then Exit;

  AddMessage('  Found: ' + GetElementEditValues(e, 'FULL') + ' [' + IntToHex(FormID(e), 8) + ']');

  // Copy as OVERRIDE (not new) into our ESP
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then begin
    AddMessage('  ERROR: Could not create override');
    Exit;
  end;

  // Apply upgrades
  SetElementEditValues(override, 'DATA\Base Damage', '58');
  SetElementEditValues(override, 'DATA\Clip Size', '8');
  SetElementEditValues(override, 'DATA\Value', '12000');

  SetElementEditValues(override, 'DNAM\Min Spread', '0.300000');
  SetElementEditValues(override, 'DNAM\Fire Rate', '2.000000');
  SetElementEditValues(override, 'DNAM\Override - Action Points', '12.000000');

  SetElementEditValues(override, 'CRDT\Critical Damage', '75');
  SetElementEditValues(override, 'CRDT\Crit % Mult', '3.500000');

  AddMessage('');
  AddMessage('  DMG:  33 -> 58');
  AddMessage('  Crit: 33/x2.0 -> 75/x3.5');
  AddMessage('  Rate: 1.0 -> 2.0');
  AddMessage('  Mag:  6 -> 8');
  AddMessage('  AP:   15 -> 12');
  AddMessage('  Spread: 0.55 -> 0.30');
  AddMessage('');
  AddMessage('  The fire inside burned brighter than the fire around him.');
end;

function Finalize: Integer;
begin
  Result := 0;
end;

end.
