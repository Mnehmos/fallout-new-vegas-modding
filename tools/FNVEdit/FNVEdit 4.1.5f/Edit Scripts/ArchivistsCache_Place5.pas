{
  Archivist's Cache — Place v5

  Strategy: Instead of persistent refs (which require persistent cell),
  place as TEMPORARY refs in a specific exterior grid cell.

  Goodsprings saloon is at approx (-73600, -74700).
  Grid cell: X = floor(-73600/4096) = -18, Y = floor(-74700/4096) = -19

  Find that specific exterior cell in WastelandNV and add refs to it.

  Run on: FalloutNV.esm
}

unit ArchivistsCachePlace5;

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

  AddMessage('[Place] v5 — Placing in exterior grid cell...');
end;

function Process(e: IInterface): Integer;
var
  sig: string;
  cellOverride, tempGroup, newRef: IInterface;
  noteFormID, trunkFormID: Cardinal;
  gridX, gridY: Integer;
  xclc: IInterface;
  i: Integer;
begin
  Result := 0;
  sig := Signature(e);

  // Look for the specific exterior CELL at grid (-18, -19)
  if sig <> 'CELL' then Exit;

  // Check if this cell has XCLC with our target grid coords
  xclc := ElementBySignature(e, 'XCLC');
  if not Assigned(xclc) then Exit;

  gridX := GetElementNativeValues(xclc, 'X');
  gridY := GetElementNativeValues(xclc, 'Y');

  if (gridX <> -18) or (gridY <> -19) then Exit;

  // Verify this is in WastelandNV, not some other worldspace
  // Check parent chain
  AddMessage('  Found exterior cell at grid (-18, -19): ' + IntToHex(FormID(e), 8));

  // Copy cell as override (this is safe for exterior cells — they only have refs for that grid square)
  AddRequiredElementMasters(e, tp, False);
  cellOverride := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(cellOverride) then begin
    AddMessage('  ERROR: Could not copy cell');
    Exit;
  end;

  // Get or create temporary children group
  tempGroup := ChildGroup(cellOverride);
  if not Assigned(tempGroup) then begin
    AddMessage('  No child group, adding directly to cell');
    tempGroup := cellOverride;
  end else begin
    AddMessage('  Found child group: ' + IntToStr(ElementCount(tempGroup)) + ' elements');
  end;

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

  // Add master for dead wastelander
  AddRequiredElementMasters(RecordByFormID(FileByIndex(0), $000A11F7, True), tp, False);

  // Place dead wastelander
  newRef := Add(tempGroup, 'ACHR', True);
  if Assigned(newRef) then begin
    SetElementNativeValues(newRef, 'NAME', $000A11F7);
    SetElementEditValues(newRef, 'DATA\Position\X', '-73500.000000');
    SetElementEditValues(newRef, 'DATA\Position\Y', '-74800.000000');
    SetElementEditValues(newRef, 'DATA\Position\Z', '8680.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\Z', '180.000000');
    Inc(placeCount);
    AddMessage('  + Dead wastelander: ' + IntToHex(FormID(newRef), 8));
  end;

  // Place trunk
  if trunkFormID > 0 then begin
    newRef := Add(tempGroup, 'REFR', True);
    if Assigned(newRef) then begin
      SetElementNativeValues(newRef, 'NAME', trunkFormID);
      SetElementEditValues(newRef, 'DATA\Position\X', '-73600.000000');
      SetElementEditValues(newRef, 'DATA\Position\Y', '-74700.000000');
      SetElementEditValues(newRef, 'DATA\Position\Z', '8680.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Z', '45.000000');
      Inc(placeCount);
      AddMessage('  + Trunk: ' + IntToHex(FormID(newRef), 8));
    end;
  end;

  // Place note
  if noteFormID > 0 then begin
    newRef := Add(tempGroup, 'REFR', True);
    if Assigned(newRef) then begin
      SetElementNativeValues(newRef, 'NAME', noteFormID);
      SetElementEditValues(newRef, 'DATA\Position\X', '-73480.000000');
      SetElementEditValues(newRef, 'DATA\Position\Y', '-74790.000000');
      SetElementEditValues(newRef, 'DATA\Position\Z', '8685.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\X', '-15.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Z', '90.000000');
      Inc(placeCount);
      AddMessage('  + Note: ' + IntToHex(FormID(newRef), 8));
    end;
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Place] Done: ' + IntToStr(placeCount) + ' objects placed');
end;

end.
