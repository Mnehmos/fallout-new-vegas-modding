{
  PerkOverhaul - Phase 2 Value Changes
  Modifies actual EPFD float values inside Entry Point effects.

  xEdit structure path:
    Effect -> Entry Point Function Parameters [EPFT] -> EPFD - Data -> Float

  Changes:
    BloodyMess:       1.05x -> 1.10x damage
    Toughness:        +3/+6 DT -> +4/+8 DT
    DemolitionExpert: 1.2/1.4/1.6x -> 1.25/1.50/1.75x
    Educated:         +2 -> +3 skill points/level
    SwiftLearner:     1.1/1.2/1.3x -> 1.15/1.30/1.45x XP
}

unit PerkOverhaulValues;

var
  changeCount: Integer;

function Initialize: Integer;
begin
  Result := 0;
  changeCount := 0;
  AddMessage('[PerkOverhaul] Phase 2: Modifying effect values...');
end;

function GetEffectFloat(effect: IInterface): Double;
var
  epft, epfd, floatEl: IInterface;
begin
  Result := -9999.0;
  // Path: effect -> "Entry Point Function Parameters" [EPFT] -> "EPFD - Data" -> "Float"
  epft := ElementBySignature(effect, 'EPFT');
  if not Assigned(epft) then Exit;

  epfd := ElementByName(epft, 'EPFD - Data');
  if not Assigned(epfd) then Exit;

  floatEl := ElementByName(epfd, 'Float');
  if Assigned(floatEl) then
    Result := GetNativeValue(floatEl)
  else
    Result := GetNativeValue(epfd);
end;

procedure SetEffectFloat(effect: IInterface; newValue: Double);
var
  epft, epfd, floatEl: IInterface;
begin
  epft := ElementBySignature(effect, 'EPFT');
  if not Assigned(epft) then Exit;

  epfd := ElementByName(epft, 'EPFD - Data');
  if not Assigned(epfd) then Exit;

  floatEl := ElementByName(epfd, 'Float');
  if Assigned(floatEl) then
    SetNativeValue(floatEl, newValue)
  else
    SetNativeValue(epfd, newValue);
end;

procedure TryChange(effect: IInterface; edid: string; oldMin, oldMax, newVal: Double; desc: string);
var
  curVal: Double;
begin
  curVal := GetEffectFloat(effect);
  if (curVal > oldMin) and (curVal < oldMax) then begin
    SetEffectFloat(effect, newVal);
    AddMessage('  ' + edid + ': ' + desc + ' ' + FloatToStr(curVal) + ' -> ' + FloatToStr(newVal));
    Inc(changeCount);
  end;
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  effects, effect: IInterface;
  i, count: Integer;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'PERK' then Exit;

  edid := EditorID(e);
  effects := ElementByName(e, 'Effects');
  if not Assigned(effects) then Exit;
  count := ElementCount(effects);

  for i := 0 to Pred(count) do begin
    effect := ElementByIndex(effects, i);

    if SameText(edid, 'BloodyMess') then
      TryChange(effect, edid, 1.04, 1.06, 1.10, 'damage');

    if SameText(edid, 'Toughness') then begin
      TryChange(effect, edid, 2.9, 3.1, 4.0, 'DT rank1');
      TryChange(effect, edid, 5.9, 6.1, 8.0, 'DT rank2');
    end;

    if SameText(edid, 'DemolitionExpert') then begin
      TryChange(effect, edid, 1.19, 1.21, 1.25, 'rank1');
      TryChange(effect, edid, 1.39, 1.41, 1.50, 'rank2');
      TryChange(effect, edid, 1.59, 1.61, 1.75, 'rank3');
    end;

    if SameText(edid, 'Educated') then
      TryChange(effect, edid, 1.9, 2.1, 3.0, 'skill pts');

    if SameText(edid, 'SwiftLearner') then begin
      TryChange(effect, edid, 1.09, 1.11, 1.15, 'XP rank1');
      TryChange(effect, edid, 1.19, 1.21, 1.30, 'XP rank2');
      TryChange(effect, edid, 1.29, 1.31, 1.45, 'XP rank3');
    end;
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[PerkOverhaul] Phase 2 complete: ' + IntToStr(changeCount) + ' values changed');
end;

end.
