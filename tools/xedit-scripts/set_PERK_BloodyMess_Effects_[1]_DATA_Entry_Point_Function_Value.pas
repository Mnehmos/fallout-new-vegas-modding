{
  Auto-generated FNVEdit script by mnehmos.fnvedit.mcp
  Target: Set PERK BloodyMess Effects\[1]\DATA\Entry Point\Function\Value = 1.10
}

unit AutoGenScript;

var
  targetPlugin: IInterface;

procedure Initialize;
begin
  AddMessage('[fnvedit-mcp] Setting PERK BloodyMess Effects\[1]\DATA\Entry Point\Function\Value = 1.10');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
begin
  Result := 0;
  sig := Signature(e);
  
  if sig <> 'PERK' then Exit;
  edid := GetElementEditValues(e, 'EDID');
  if not SameText(edid, 'BloodyMess') then Exit;

  AddMessage('  Found: ' + edid);
  AddMessage('  Old value: ' + GetElementEditValues(e, 'Effects\[1]\DATA\Entry Point\Function\Value'));

  AddRequiredElementMasters(e, FileByName('PerkOverhaul.esp'), True);
  e := wbCopyElementToFile(e, FileByName('PerkOverhaul.esp'), False, True);

  SetElementEditValues(e, 'Effects\[1]\DATA\Entry Point\Function\Value', '1.10');
  AddMessage('  New value: 1.10');

end;

procedure Finalize;
begin
  AddMessage('[fnvedit-mcp] Script complete');
end;

end.
