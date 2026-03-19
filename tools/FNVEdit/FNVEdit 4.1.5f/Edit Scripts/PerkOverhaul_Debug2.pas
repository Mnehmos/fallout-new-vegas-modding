{
  Debug script 2 - deep dive into BloodyMess Effect[1]
  to find exactly where the damage multiplier float lives
}

unit PerkOverhaulDebug2;

function Initialize: Integer;
begin
  Result := 0;
end;

procedure DumpElement(e: IInterface; indent: string);
var
  i: Integer;
  child: IInterface;
begin
  AddMessage(indent + Name(e) + ' [sig=' + Signature(e) + '] val="' + GetEditValue(e) + '"');
  for i := 0 to Pred(ElementCount(e)) do begin
    child := ElementByIndex(e, i);
    DumpElement(child, indent + '  ');
  end;
end;

function Process(e: IInterface): Integer;
var
  effects, effect: IInterface;
  i: Integer;
begin
  Result := 0;
  if Signature(e) <> 'PERK' then Exit;
  if not SameText(EditorID(e), 'BloodyMess') then Exit;

  effects := ElementByName(e, 'Effects');
  if not Assigned(effects) then Exit;

  AddMessage('');
  AddMessage('=== BloodyMess Full Effect Dump ===');

  for i := 0 to Pred(ElementCount(effects)) do begin
    effect := ElementByIndex(effects, i);
    AddMessage('');
    AddMessage('--- Effect[' + IntToStr(i) + '] ---');
    DumpElement(effect, '  ');
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[Debug2] Done');
end;

end.
