{
  Debug script - dump the effect structure of BloodyMess
  so we can see exactly how xEdit navigates it
}

unit PerkOverhaulDebug;

function Initialize: Integer;
begin
  Result := 0;
  AddMessage('[Debug] Starting effect structure dump...');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  effects, effect, child: IInterface;
  i, j, count, childCount: Integer;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'PERK' then Exit;

  edid := EditorID(e);
  if not SameText(edid, 'BloodyMess') then Exit;

  AddMessage('');
  AddMessage('=== BloodyMess Effect Structure ===');
  AddMessage('Element count: ' + IntToStr(ElementCount(e)));

  // List all top-level elements
  for i := 0 to Pred(ElementCount(e)) do begin
    child := ElementByIndex(e, i);
    AddMessage('  [' + IntToStr(i) + '] ' + Name(child) + ' (sig: ' + Signature(child) + ')');
  end;

  // Try to find effects
  effects := ElementByName(e, 'Effects');
  if not Assigned(effects) then begin
    AddMessage('  ElementByName "Effects" = NOT FOUND');
    effects := ElementBySignature(e, 'PRKE');
    if Assigned(effects) then
      AddMessage('  ElementBySignature "PRKE" = FOUND')
    else
      AddMessage('  ElementBySignature "PRKE" = NOT FOUND');
    Exit;
  end;

  AddMessage('  Effects found, count: ' + IntToStr(ElementCount(effects)));

  for i := 0 to Pred(ElementCount(effects)) do begin
    effect := ElementByIndex(effects, i);
    AddMessage('');
    AddMessage('  Effect[' + IntToStr(i) + ']: ' + Name(effect));
    AddMessage('    Child count: ' + IntToStr(ElementCount(effect)));

    for j := 0 to Pred(ElementCount(effect)) do begin
      child := ElementByIndex(effect, j);
      AddMessage('    [' + IntToStr(j) + '] ' + Name(child) + ' sig=' + Signature(child));

      // If this is EPFD, show its value
      if Signature(child) = 'EPFD' then begin
        AddMessage('      >>> EPFD value: ' + GetEditValue(child));
        AddMessage('      >>> EPFD native: ' + FloatToStr(GetNativeValue(child)));
      end;
    end;
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[Debug] Done');
end;

end.
