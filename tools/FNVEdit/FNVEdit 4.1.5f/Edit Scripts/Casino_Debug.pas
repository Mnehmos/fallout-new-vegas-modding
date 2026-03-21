{
  Debug: Dump all 5 casino CSNO records to find gambling limit fields
}
unit CasinoDebug;

procedure DumpElement(e: IInterface; indent: string; depth: Integer);
var
  i: Integer;
  child: IInterface;
begin
  if depth > 3 then Exit;
  AddMessage(indent + Name(e) + ' [sig=' + Signature(e) + '] val="' + GetEditValue(e) + '"');
  for i := 0 to Pred(ElementCount(e)) do begin
    child := ElementByIndex(e, i);
    DumpElement(child, indent + '  ', depth + 1);
  end;
end;

function Initialize: Integer;
begin
  Result := 0;
  AddMessage('[Casino Debug] Dumping casino records...');
end;

function Process(e: IInterface): Integer;
begin
  Result := 0;
  if Signature(e) <> 'CSNO' then Exit;
  AddMessage('');
  AddMessage('=== ' + EditorID(e) + ' ===');
  DumpElement(e, '  ', 0);
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[Casino Debug] Done');
end;

end.
