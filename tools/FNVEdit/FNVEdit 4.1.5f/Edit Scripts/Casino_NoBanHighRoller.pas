{
  Casino Overhaul — No Ban, High Roller Mode

  Removes winnings caps (no more getting kicked out) and
  standardizes blackjack payout to 1.5x across all casinos.

  Run on: FalloutNV.esm (select all, Apply Script)
  Target: New ESP or existing
}

unit CasinoNoBanHighRoller;

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
    tp := AddNewFile;
    if not Assigned(tp) then begin
      AddMessage('[Casino] ERROR: No target plugin. Aborting.');
      Result := 1;
      Exit;
    end;
  end;

  AddMessage('=== CASINO OVERHAUL — NO BAN, HIGH ROLLER ===');
  AddMessage('Target: ' + GetFileName(tp));
  AddMessage('');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  override: IInterface;
  oldMax: Integer;
  oldPayout: Double;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'CSNO' then Exit;
  if not SameText(GetFileName(GetFile(e)), 'FalloutNV.esm') then Exit;

  edid := EditorID(e);
  oldMax := GetElementNativeValues(e, 'DATA\Max Winnings');
  oldPayout := GetElementNativeValues(e, 'DATA\BlackJack Payout Ratio');

  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then begin
    AddMessage('  WARNING: Could not override ' + edid);
    Exit;
  end;

  // Remove winnings cap
  SetElementEditValues(override, 'DATA\Max Winnings', '999999');

  // Standardize blackjack payout to 1.5x
  SetElementEditValues(override, 'DATA\BlackJack Payout Ratio', '1.500000');

  Inc(changeCount);
  AddMessage('  ' + GetElementEditValues(override, 'FULL') + ':');
  AddMessage('    Max Winnings: ' + IntToStr(oldMax) + ' -> 999,999 (no ban)');
  if oldPayout < 1.49 then
    AddMessage('    BJ Payout: ' + FloatToStr(oldPayout) + ' -> 1.5x');
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Casino] Done: ' + IntToStr(changeCount) + ' casinos modified');
  AddMessage('The house always wins — but now so do you.');
end;

end.
