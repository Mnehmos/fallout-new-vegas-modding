{
  Archivist's Cache — Place objects via xEdit

  Strategy: Find the persistent cell in FalloutNV.esm's WastelandNV worldspace,
  copy it as override, then add new persistent refs to it.

  Run on: FalloutNV.esm (click FalloutNV.esm, Apply Script)
}

unit ArchivistsCachePlace2;

var
  tp: IInterface;
  placeCount: Integer;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  placeCount := 0;

  tp := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'ArchivistsCache.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('[Place] ERROR: ArchivistsCache.esp not loaded.');
    Result := 1;
    Exit;
  end;

  AddMessage('[Place] Placing objects in Goodsprings...');
end;

function PlaceRef(cell: IInterface; baseFormID: Cardinal;
  x, y, z, rotZ: Double; edid: string; isNPC: Boolean): IInterface;
var
  newRef, persGroup, el: IInterface;
  i: Integer;
  refType: string;
begin
  Result := nil;

  // Find or create the persistent subgroup (type 8) under the cell
  persGroup := nil;
  for i := 0 to Pred(ElementCount(cell)) do begin
    el := ElementByIndex(cell, i);
    if (Signature(el) = 'GRUP') or (Name(el) = 'Child Group') then begin
      persGroup := el;
      Break;
    end;
  end;

  // If no persistent group, try ChildGroup
  if not Assigned(persGroup) then
    persGroup := ChildGroup(cell);

  if not Assigned(persGroup) then begin
    AddMessage('    No persistent group found, trying to add directly to cell');
    persGroup := cell;
  end;

  // Create the reference
  if isNPC then
    refType := 'ACHR'
  else
    refType := 'REFR';

  newRef := Add(persGroup, refType, True);
  if not Assigned(newRef) then begin
    AddMessage('    ERROR: Add(' + refType + ') failed');
    Exit;
  end;

  // Set NAME (base object)
  SetElementNativeValues(newRef, 'NAME', baseFormID);

  // Set position
  SetElementEditValues(newRef, 'DATA\Position\X', FloatToStr(x));
  SetElementEditValues(newRef, 'DATA\Position\Y', FloatToStr(y));
  SetElementEditValues(newRef, 'DATA\Position\Z', FloatToStr(z));
  SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
  SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
  SetElementEditValues(newRef, 'DATA\Rotation\Z', FloatToStr(rotZ));

  // Make persistent
  SetIsPersistent(newRef, True);

  Inc(placeCount);
  AddMessage('    Placed ' + refType + ' ' + edid + ': ' + IntToHex(FormID(newRef), 8));
  Result := newRef;
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  wrldChildren, cellBlock, cellSubBlock, cell, cellOverride: IInterface;
  noteFormID, trunkFormID: Cardinal;
  i, j, k: Integer;
begin
  Result := 0;
  sig := Signature(e);

  // Only process CELL records that belong to WastelandNV persistent cell
  // The persistent cell is FormID 0x00031E2A
  if sig <> 'CELL' then Exit;
  if FormID(e) <> $000846EA then Exit;

  AddMessage('  Found WastelandNV persistent cell: ' + IntToHex(FormID(e), 8));

  // Copy as override into our ESP
  AddRequiredElementMasters(e, tp, False);
  cellOverride := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(cellOverride) then begin
    AddMessage('  ERROR: Could not copy persistent cell');
    Exit;
  end;
  AddMessage('  Copied persistent cell to ArchivistsCache.esp');

  // Find our note and trunk FormIDs in ArchivistsCache.esp
  noteFormID := 0;
  trunkFormID := 0;
  for i := 0 to Pred(RecordCount(tp)) do begin
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistNote') then
      noteFormID := FormID(RecordByIndex(tp, i));
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistTrunk') then
      trunkFormID := FormID(RecordByIndex(tp, i));
  end;

  AddMessage('  Note FormID: ' + IntToHex(noteFormID, 8));
  AddMessage('  Trunk FormID: ' + IntToHex(trunkFormID, 8));

  // Place dead wastelander (VarDEADWastelander = 0x000A11F7)
  AddRequiredElementMasters(RecordByFormID(FileByIndex(0), $000A11F7, True), tp, False);
  PlaceRef(cellOverride, $000A11F7, -73500.0, -74800.0, 8680.0, 180.0, 'DeadWastelander', True);

  // Place note
  if noteFormID > 0 then
    PlaceRef(cellOverride, noteFormID, -73480.0, -74790.0, 8685.0, 90.0, 'ArchivistNote', False);

  // Place trunk
  if trunkFormID > 0 then
    PlaceRef(cellOverride, trunkFormID, -73600.0, -74700.0, 8680.0, 45.0, 'ArchivistTrunk', False);
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Place] Done: ' + IntToStr(placeCount) + ' objects placed');
  AddMessage('[Place] Save the ESP to apply.');
end;

end.
