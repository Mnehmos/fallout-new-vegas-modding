{
  Archivist's Cache — Place objects in WastelandNV

  Strategy: Find WastelandNV WRLD record, copy as override,
  then navigate to ITS persistent cell and add refs there.

  Previous scripts grabbed FFEncounterWorld's cell by mistake.
  This one explicitly starts from the WRLD record.

  Run on: FalloutNV.esm (click it, Apply Script)
}

unit ArchivistsCachePlace3;

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

  AddMessage('[Place] Placing objects in WastelandNV...');
end;

function Process(e: IInterface): Integer;
var
  sig: string;
  wrldOverride, wrldChildren, cellBlock, persCell, persGroup: IInterface;
  newRef, el: IInterface;
  noteFormID, trunkFormID: Cardinal;
  i, j: Integer;
begin
  Result := 0;
  sig := Signature(e);

  // Only process WastelandNV worldspace (FormID 000DA726)
  if sig <> 'WRLD' then Exit;
  if not SameText(EditorID(e), 'WastelandNV') then Exit;

  AddMessage('  Found WastelandNV: ' + IntToHex(FormID(e), 8));

  // Step 1: Copy WastelandNV as override
  AddRequiredElementMasters(e, tp, False);
  wrldOverride := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(wrldOverride) then begin
    AddMessage('  ERROR: Could not copy WastelandNV');
    Exit;
  end;
  AddMessage('  Copied WastelandNV to ArchivistsCache.esp');

  // Step 2: Get the world children group from the ORIGINAL (not override)
  // The override won't have children yet
  wrldChildren := ChildGroup(e);
  if not Assigned(wrldChildren) then begin
    AddMessage('  ERROR: WastelandNV has no child group in master');
    Exit;
  end;
  AddMessage('  Found world children group: ' + IntToStr(ElementCount(wrldChildren)) + ' elements');

  // Step 3: Find the persistent cell within the world children
  // It's the first CELL record in the world children group
  persCell := nil;
  for i := 0 to Pred(ElementCount(wrldChildren)) do begin
    el := ElementByIndex(wrldChildren, i);
    if Signature(el) = 'CELL' then begin
      persCell := el;
      AddMessage('  Found persistent cell: ' + IntToHex(FormID(el), 8));
      Break;
    end;
  end;

  if not Assigned(persCell) then begin
    AddMessage('  ERROR: No persistent cell found in WastelandNV children');
    Exit;
  end;

  // Step 4: Copy the persistent cell as override into our ESP
  // This should automatically create the proper group structure
  AddRequiredElementMasters(persCell, tp, False);
  persCell := wbCopyElementToFile(persCell, tp, False, True);
  if not Assigned(persCell) then begin
    AddMessage('  ERROR: Could not copy persistent cell');
    Exit;
  end;
  AddMessage('  Copied persistent cell to ArchivistsCache.esp');

  // Step 5: Find the persistent children group in our overridden cell
  persGroup := ChildGroup(persCell);
  if not Assigned(persGroup) then begin
    AddMessage('  WARNING: No persistent group yet, creating refs anyway');
    persGroup := persCell;
  end else begin
    AddMessage('  Found persistent children group');
  end;

  // Step 6: Find our base objects in ArchivistsCache.esp
  noteFormID := 0;
  trunkFormID := 0;
  for i := 0 to Pred(RecordCount(tp)) do begin
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistNote') then
      noteFormID := FormID(RecordByIndex(tp, i));
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistTrunk') then
      trunkFormID := FormID(RecordByIndex(tp, i));
  end;
  AddMessage('  Note: ' + IntToHex(noteFormID, 8) + '  Trunk: ' + IntToHex(trunkFormID, 8));

  // Step 7: Add masters for the dead wastelander
  AddRequiredElementMasters(RecordByFormID(FileByIndex(0), $000A11F7, True), tp, False);

  // Step 8: Place objects
  // Dead wastelander near Goodsprings saloon
  newRef := Add(persGroup, 'ACHR', True);
  if Assigned(newRef) then begin
    SetIsPersistent(newRef, True);
    SetElementNativeValues(newRef, 'NAME', $000A11F7);
    SetElementEditValues(newRef, 'DATA\Position\X', '-73500.000000');
    SetElementEditValues(newRef, 'DATA\Position\Y', '-74800.000000');
    SetElementEditValues(newRef, 'DATA\Position\Z', '8680.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\Z', '180.000000');
    Inc(placeCount);
    AddMessage('  + Dead wastelander: ' + IntToHex(FormID(newRef), 8));
  end else
    AddMessage('  ERROR: Could not create ACHR');

  // Trunk near saloon
  if trunkFormID > 0 then begin
    newRef := Add(persGroup, 'REFR', True);
    if Assigned(newRef) then begin
      SetIsPersistent(newRef, True);
      SetElementNativeValues(newRef, 'NAME', trunkFormID);
      SetElementEditValues(newRef, 'DATA\Position\X', '-73600.000000');
      SetElementEditValues(newRef, 'DATA\Position\Y', '-74700.000000');
      SetElementEditValues(newRef, 'DATA\Position\Z', '8680.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Z', '45.000000');
      Inc(placeCount);
      AddMessage('  + Trunk: ' + IntToHex(FormID(newRef), 8));
    end else
      AddMessage('  ERROR: Could not create trunk REFR');
  end;

  // Note near body
  if noteFormID > 0 then begin
    newRef := Add(persGroup, 'REFR', True);
    if Assigned(newRef) then begin
      SetIsPersistent(newRef, True);
      SetElementNativeValues(newRef, 'NAME', noteFormID);
      SetElementEditValues(newRef, 'DATA\Position\X', '-73480.000000');
      SetElementEditValues(newRef, 'DATA\Position\Y', '-74790.000000');
      SetElementEditValues(newRef, 'DATA\Position\Z', '8685.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\X', '-15.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Z', '90.000000');
      Inc(placeCount);
      AddMessage('  + Note: ' + IntToHex(FormID(newRef), 8));
    end else
      AddMessage('  ERROR: Could not create note REFR');
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Place] Done: ' + IntToStr(placeCount) + ' objects placed');
  AddMessage('[Place] Save to apply. Then test: player.moveto [trunk FormID]');
end;

end.
