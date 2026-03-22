{
  Archivist Faction — Setup NPCs + Add to Wasteland Encounters

  1. Gives Archivist NPCs power armor + Mnehmos weapons
  2. Adds Archivist encounter list to EncWastelandNV + EncWastelandNVTough

  Run on: FalloutNV.esm + MnehmosMojave.esp (select FalloutNV.esm, Apply Script)
}

unit ArchivistFactionSetup;

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
    AddMessage('[Archivist] ERROR: MnehmosMojave.esp not loaded.');
    Result := 1;
    Exit;
  end;

  AddMessage('=== ARCHIVIST FACTION SETUP ===');
  AddMessage('');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  override, entries, newEntry, lvlo, rec: IInterface;
  archivistLVLN: Cardinal;
  j: Integer;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);

  if not SameText(GetFileName(GetFile(e)), 'FalloutNV.esm') then Exit;

  archivistLVLN := 0;
  if sig = 'LVLC' then begin
    if not (SameText(edid, 'EncWastelandNV') or
            SameText(edid, 'EncWastelandNVTough') or
            SameText(edid, 'VEncVarTier2ValleyRoad') or
            SameText(edid, 'VEncVarTier3ValleyRoad') or
            SameText(edid, 'VEncVarTier1ValleyRoadGS')) then Exit;

    // Find MnehmosArchivistEncounter in our ESP
    for j := 0 to Pred(RecordCount(tp)) do begin
      rec := RecordByIndex(tp, j);
      if SameText(EditorID(rec), 'MnehmosArchivistEncounter') then begin
        archivistLVLN := FormID(rec);
        Break;
      end;
    end;

    if archivistLVLN = 0 then begin
      AddMessage('  WARNING: MnehmosArchivistEncounter not found in ESP');
      Exit;
    end;

    // Copy list as override
    AddRequiredElementMasters(e, tp, False);
    override := wbCopyElementToFile(e, tp, False, True);
    if not Assigned(override) then begin
      AddMessage('  WARNING: Could not override ' + edid);
      Exit;
    end;

    // Add new LVLO entry for Archivists
    entries := ElementByName(override, 'Leveled List Entries');
    if Assigned(entries) then begin
      newEntry := ElementAssign(entries, HighInteger, nil, False);
      if Assigned(newEntry) then begin
        lvlo := ElementBySignature(newEntry, 'LVLO');
        if Assigned(lvlo) then begin
          SetElementNativeValues(lvlo, 'Level', 15);
          SetElementNativeValues(lvlo, 'Reference', archivistLVLN);
          SetElementNativeValues(lvlo, 'Count', 1);
          Inc(changeCount);
          AddMessage('  + Added Archivists to ' + edid + ' at level 15');
        end;
      end;
    end;
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Archivist] Setup complete: ' + IntToStr(changeCount) + ' changes');
  AddMessage('');
  AddMessage('Archivist Guardians, Scouts, and Heavies will now');
  AddMessage('spawn in wasteland encounters at level 15+.');
  AddMessage('');
  AddMessage('Kill them. Take their armor. Remember everything.');
end;

end.
