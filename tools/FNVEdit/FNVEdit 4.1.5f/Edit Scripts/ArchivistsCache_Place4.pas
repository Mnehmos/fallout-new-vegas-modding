{
  Archivist's Cache — Place objects (v4)

  KEY INSIGHT: Do NOT override the persistent cell!
  It contains thousands of refs. Overriding it wipes them all out.

  Instead: Add new REFR/ACHR directly to the master's persistent group.
  xEdit will automatically create the correct override structure when saving.

  Run on: FalloutNV.esm (click it, Apply Script)
}

unit ArchivistsCachePlace4;

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

  AddMessage('[Place] v4 — Adding refs to WastelandNV persistent group...');
end;

function AddPersistentRef(persGroup: IInterface; baseFormID: Cardinal;
  x, y, z, rotZ: Double; isNPC: Boolean): IInterface;
var
  newRef: IInterface;
  refType: string;
begin
  Result := nil;

  if isNPC then
    refType := 'ACHR'
  else
    refType := 'REFR';

  // Add new ref to the persistent group — xEdit handles file assignment
  newRef := Add(persGroup, refType, True);
  if not Assigned(newRef) then begin
    AddMessage('    ERROR: Add(' + refType + ') returned nil');
    Exit;
  end;

  // Move it to our ESP
  SetElementNativeValues(newRef, 'Record Header\FormID', GetNewFormID(tp));

  // Set base object
  SetElementNativeValues(newRef, 'NAME', baseFormID);

  // Set persistent flag
  SetIsPersistent(newRef, True);

  // Set position
  SetElementEditValues(newRef, 'DATA\Position\X', FloatToStr(x));
  SetElementEditValues(newRef, 'DATA\Position\Y', FloatToStr(y));
  SetElementEditValues(newRef, 'DATA\Position\Z', FloatToStr(z));
  SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
  SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
  SetElementEditValues(newRef, 'DATA\Rotation\Z', FloatToStr(rotZ));

  Inc(placeCount);
  Result := newRef;
end;

function Process(e: IInterface): Integer;
var
  sig: string;
  wrldChildren, persCell, persGroup, el: IInterface;
  noteFormID, trunkFormID: Cardinal;
  newRef: IInterface;
  i, j: Integer;
begin
  Result := 0;
  sig := Signature(e);

  if sig <> 'WRLD' then Exit;
  if not SameText(EditorID(e), 'WastelandNV') then Exit;

  AddMessage('  Found WastelandNV: ' + IntToHex(FormID(e), 8));

  // Get world children from the MASTER file's worldspace
  wrldChildren := ChildGroup(e);
  if not Assigned(wrldChildren) then begin
    AddMessage('  ERROR: No world children');
    Exit;
  end;

  // Find the persistent cell
  persCell := nil;
  for i := 0 to Pred(ElementCount(wrldChildren)) do begin
    el := ElementByIndex(wrldChildren, i);
    if Signature(el) = 'CELL' then begin
      persCell := el;
      Break;
    end;
  end;

  if not Assigned(persCell) then begin
    AddMessage('  ERROR: No persistent cell found');
    Exit;
  end;
  AddMessage('  Persistent cell: ' + IntToHex(FormID(persCell), 8));

  // Find the persistent children group (type 8) within the cell
  persGroup := nil;
  for i := 0 to Pred(ElementCount(persCell)) do begin
    el := ElementByIndex(persCell, i);
    // Child groups show up as elements of the cell
    if Name(el) = 'Child Group' then begin
      persGroup := el;
      Break;
    end;
  end;

  // Try ChildGroup function
  if not Assigned(persGroup) then
    persGroup := ChildGroup(persCell);

  if not Assigned(persGroup) then begin
    AddMessage('  ERROR: No persistent children group found');
    Exit;
  end;

  AddMessage('  Persistent group: ' + IntToStr(ElementCount(persGroup)) + ' existing refs');

  // Find our item FormIDs
  noteFormID := 0;
  trunkFormID := 0;
  for i := 0 to Pred(RecordCount(tp)) do begin
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistNote') then
      noteFormID := FormID(RecordByIndex(tp, i));
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistTrunk') then
      trunkFormID := FormID(RecordByIndex(tp, i));
  end;
  AddMessage('  Note: ' + IntToHex(noteFormID, 8) + '  Trunk: ' + IntToHex(trunkFormID, 8));

  // Add masters
  AddRequiredElementMasters(RecordByFormID(FileByIndex(0), $000A11F7, True), tp, False);

  // Place dead wastelander
  newRef := AddPersistentRef(persGroup, $000A11F7, -73500.0, -74800.0, 8680.0, 180.0, True);
  if Assigned(newRef) then
    AddMessage('  + Dead wastelander: ' + IntToHex(FormID(newRef), 8));

  // Place trunk
  if trunkFormID > 0 then begin
    newRef := AddPersistentRef(persGroup, trunkFormID, -73600.0, -74700.0, 8680.0, 45.0, False);
    if Assigned(newRef) then
      AddMessage('  + Trunk: ' + IntToHex(FormID(newRef), 8));
  end;

  // Place note
  if noteFormID > 0 then begin
    newRef := AddPersistentRef(persGroup, noteFormID, -73480.0, -74790.0, 8685.0, 90.0, False);
    if Assigned(newRef) then
      AddMessage('  + Note: ' + IntToHex(FormID(newRef), 8));
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Place] Done: ' + IntToStr(placeCount) + ' objects placed');
end;

end.
