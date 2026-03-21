{
  Archivist's Cache — Place objects in Goodsprings

  Creates REFR/ACHR records using xEdit's proven placement system.
  Run on: FalloutNV.esm (select it, Apply Script)
  Target: ArchivistsCache.esp

  Places:
  1. Dead wastelander near Goodsprings cemetery
  2. Note on the body
  3. Trunk near Goodsprings Source
}

unit ArchivistsCachePlace;

var
  tp: IInterface;
  worldspace, pcell, pcellGroup: IInterface;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;

  // Find ArchivistsCache.esp
  tp := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'ArchivistsCache.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('[Place] ERROR: ArchivistsCache.esp not loaded. Aborting.');
    Result := 1;
    Exit;
  end;

  AddMessage('[Place] Placing Archivist''s Cache objects in Goodsprings...');
  AddMessage('[Place] Target: ' + GetFileName(tp));
end;

function PlaceAtCoords(baseRef: IInterface; x, y, z, rotX, rotY, rotZ: Double;
  refEditorId: string; isPersistent: Boolean): IInterface;
var
  newRef, el: IInterface;
  sig: string;
begin
  Result := nil;
  sig := Signature(baseRef);

  // Determine if ACHR or REFR based on base record type
  if (sig = 'NPC_') or (sig = 'LVLN') then begin
    // Place as ACHR
    newRef := Add(pcellGroup, 'ACHR', True);
  end else begin
    // Place as REFR
    newRef := Add(pcellGroup, 'REFR', True);
  end;

  if not Assigned(newRef) then begin
    AddMessage('  ERROR: Could not create reference');
    Exit;
  end;

  // Set editor ID
  if refEditorId <> '' then begin
    Add(newRef, 'EDID', True);
    SetElementEditValues(newRef, 'EDID', refEditorId);
  end;

  // Set base object (NAME)
  SetElementNativeValues(newRef, 'NAME', FormID(baseRef));

  // Set position and rotation (DATA)
  SetElementEditValues(newRef, 'DATA\Position\X', FloatToStr(x));
  SetElementEditValues(newRef, 'DATA\Position\Y', FloatToStr(y));
  SetElementEditValues(newRef, 'DATA\Position\Z', FloatToStr(z));
  SetElementEditValues(newRef, 'DATA\Rotation\X', FloatToStr(rotX));
  SetElementEditValues(newRef, 'DATA\Rotation\Y', FloatToStr(rotY));
  SetElementEditValues(newRef, 'DATA\Rotation\Z', FloatToStr(rotZ));

  // Set persistent flag
  if isPersistent then
    SetIsPersistent(newRef, True);

  Result := newRef;
end;

function Process(e: IInterface): Integer;
var
  sig: string;
  wrldOverride, cellOverride: IInterface;
  deadWastelander, noteBase, trunkBase: IInterface;
  newRef: IInterface;
  i: Integer;
begin
  Result := 0;
  sig := Signature(e);

  // Only process the WastelandNV worldspace record
  if sig <> 'WRLD' then Exit;
  if not SameText(EditorID(e), 'WastelandNV') then Exit;

  AddMessage('  Found WastelandNV worldspace');

  // Copy worldspace as override into our ESP
  AddRequiredElementMasters(e, tp, False);
  wrldOverride := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(wrldOverride) then begin
    AddMessage('  ERROR: Could not copy worldspace');
    Exit;
  end;

  // Get the persistent cell group
  // The persistent cell is the first child group of the worldspace
  pcell := ChildGroup(wrldOverride);
  if not Assigned(pcell) then begin
    AddMessage('  ERROR: No child group for worldspace');
    Exit;
  end;

  // Find the persistent cell within the child group
  pcellGroup := nil;
  for i := 0 to Pred(ElementCount(pcell)) do begin
    if Signature(ElementByIndex(pcell, i)) = 'CELL' then begin
      pcellGroup := ElementByIndex(pcell, i);
      Break;
    end;
  end;

  // If no persistent cell found, try getting it differently
  if not Assigned(pcellGroup) then begin
    // Try to get the persistent group directly
    pcellGroup := pcell;
  end;

  AddMessage('  Got persistent cell group');

  // Find our base objects in ArchivistsCache.esp
  deadWastelander := nil;
  noteBase := nil;
  trunkBase := nil;

  // Find VarDEADWastelander in FalloutNV.esm
  deadWastelander := RecordByFormID(FileByIndex(0), $000A11F7, True);
  if Assigned(deadWastelander) then
    AddMessage('  Found dead wastelander: ' + Name(deadWastelander))
  else
    AddMessage('  WARNING: Dead wastelander not found');

  // Find our note and trunk in ArchivistsCache.esp
  for i := 0 to Pred(RecordCount(tp)) do begin
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistNote') then
      noteBase := RecordByIndex(tp, i);
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistTrunk') then
      trunkBase := RecordByIndex(tp, i);
  end;

  if Assigned(noteBase) then
    AddMessage('  Found note: ' + Name(noteBase))
  else
    AddMessage('  WARNING: Note not found');

  if Assigned(trunkBase) then
    AddMessage('  Found trunk: ' + Name(trunkBase))
  else
    AddMessage('  WARNING: Trunk not found');

  // ═══ PLACE OBJECTS ═══

  // Dead wastelander near cemetery
  if Assigned(deadWastelander) then begin
    AddRequiredElementMasters(deadWastelander, tp, False);
    newRef := PlaceAtCoords(deadWastelander, -73500.0, -74800.0, 8680.0, 0, 0, 180.0, 'MnehmosDeadWastelander', True);
    if Assigned(newRef) then
      AddMessage('  Placed dead wastelander: ' + IntToHex(FormID(newRef), 8))
    else
      AddMessage('  ERROR: Failed to place dead wastelander');
  end;

  // Note near the body
  if Assigned(noteBase) then begin
    newRef := PlaceAtCoords(noteBase, -73480.0, -74790.0, 8685.0, -15.0, 0, 90.0, 'MnehmosNoteRef', True);
    if Assigned(newRef) then
      AddMessage('  Placed note: ' + IntToHex(FormID(newRef), 8))
    else
      AddMessage('  ERROR: Failed to place note');
  end;

  // Trunk near Goodsprings Source
  if Assigned(trunkBase) then begin
    newRef := PlaceAtCoords(trunkBase, -73600.0, -74700.0, 8680.0, 0, 0, 45.0, 'MnehmosTrunkRef', True);
    if Assigned(newRef) then
      AddMessage('  Placed trunk: ' + IntToHex(FormID(newRef), 8))
    else
      AddMessage('  ERROR: Failed to place trunk');
  end;

  AddMessage('');
  AddMessage('[Place] Done. Save the ESP to apply placements.');
end;

function Finalize: Integer;
begin
  Result := 0;
end;

end.
