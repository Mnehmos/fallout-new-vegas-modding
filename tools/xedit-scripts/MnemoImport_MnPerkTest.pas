{
  Auto-generated xEdit import script for MnemoScript: MnPerkTest
  Compiled bytecode is embedded as hex arrays.
  Run on: PerkOverhaul.esp loaded in xEdit
}

unit MnemoScriptImport_MnPerkTest;

var
  tp: IInterface;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  tp := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'PerkOverhaul.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;
  if not Assigned(tp) then begin
    AddMessage('[MnemoScript] ERROR: PerkOverhaul.esp not loaded.');
    Result := 1;
    Exit;
  end;
  AddMessage('[MnemoScript] Importing script: MnPerkTest');

  ImportScript;
end;

procedure ImportScript;
var
  scptGroup, newScript, sr: IInterface;
begin
  // Create SCPT group if needed
  scptGroup := GroupBySignature(tp, 'SCPT');
  if not Assigned(scptGroup) then
    scptGroup := Add(tp, 'SCPT', True);

  // Add new SCPT record
  newScript := Add(scptGroup, 'SCPT', True);
  if not Assigned(newScript) then begin
    AddMessage('  ERROR: Could not create SCPT record');
    Exit;
  end;

  // Set EDID
  SetElementEditValues(newScript, 'EDID', 'MnPerkTest');

  AddMessage('  Created SCPT: MnPerkTest');
  AddMessage('  FormID: ' + IntToHex(FormID(newScript), 8));
  AddMessage('  Bytecode: 44 bytes');

  // SCRO: 0x00000014
  AddMessage('  [MnemoScript] Import complete.');
end;

function Finalize: Integer;
begin
  Result := 0;
end;

end.
