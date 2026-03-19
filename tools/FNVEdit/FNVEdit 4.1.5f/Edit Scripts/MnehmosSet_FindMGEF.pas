{
  Quick: Find Agility MGEF and verify all SPECIAL MGEFs
}
unit FindMGEF;
function Initialize: Integer;
begin
  Result := 0;
  AddMessage('[MGEF] Searching for SPECIAL increase effects...');
end;
function Process(e: IInterface): Integer;
var
  edid: string;
begin
  Result := 0;
  if Signature(e) <> 'MGEF' then Exit;
  edid := EditorID(e);
  if Pos('Increase', edid) = 1 then
    AddMessage('  ' + edid + ' [MGEF:' + IntToHex(FixedFormID(e), 8) + ']');
end;
function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[MGEF] Done');
end;
end.
