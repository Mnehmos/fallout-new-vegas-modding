{
  Archivist's Cache — Place v6

  Strategy: Find an existing REFR in Goodsprings, copy it as new record,
  then change its NAME (base object) and DATA (position).
  This preserves the correct group nesting because xEdit
  knows how to copy within the same cell group structure.

  Run on: FalloutNV.esm
}

unit ArchivistsCachePlace6;

var
  tp: IInterface;
  placeCount: Integer;
  donorRef: IInterface;
  noteFormID, trunkFormID: Cardinal;
  doPlacement: Boolean;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  placeCount := 0;
  donorRef := nil;
  doPlacement := False;

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

  // Find our item FormIDs
  noteFormID := 0;
  trunkFormID := 0;
  for i := 0 to Pred(RecordCount(tp)) do begin
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistNote') then
      noteFormID := FormID(RecordByIndex(tp, i));
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistTrunk') then
      trunkFormID := FormID(RecordByIndex(tp, i));
  end;

  AddMessage('[Place] v6 — Clone existing REFR approach...');
  AddMessage('  Note: ' + IntToHex(noteFormID, 8) + '  Trunk: ' + IntToHex(trunkFormID, 8));
end;

function Process(e: IInterface): Integer;
var
  sig: string;
  newRef: IInterface;
  x, y, z: Double;
begin
  Result := 0;

  // Already done
  if placeCount >= 2 then Exit;

  sig := Signature(e);

  // Look for any REFR in the Goodsprings area
  // We need one that's a persistent ref in WastelandNV
  if sig <> 'REFR' then Exit;

  // Check position — Goodsprings area (X ~ -68000, Y ~ 2000)
  x := GetElementNativeValues(e, 'DATA\Position\X');
  y := GetElementNativeValues(e, 'DATA\Position\Y');

  // Within Goodsprings area?
  if (x < -70000) or (x > -66000) then Exit;
  if (y < 0) or (y > 4000) then Exit;

  // Found a Goodsprings REFR! Clone it for our trunk
  if placeCount = 0 then begin
    AddMessage('  Found donor REFR near Goodsprings: ' + IntToHex(FormID(e), 8));
    AddMessage('    Base: ' + GetElementEditValues(e, 'NAME'));
    AddMessage('    Pos: ' + FloatToStr(x) + ', ' + FloatToStr(y));

    // Clone as NEW record into our ESP
    if trunkFormID > 0 then begin
      AddRequiredElementMasters(e, tp, False);
      newRef := wbCopyElementToFile(e, tp, True, True);
      if Assigned(newRef) then begin
        // Change base object to our trunk
        SetElementNativeValues(newRef, 'NAME', trunkFormID);
        // Trunk: near Goodsprings (same grid cell as donor)
        SetElementEditValues(newRef, 'DATA\Position\X', '-69800.000000');
        SetElementEditValues(newRef, 'DATA\Position\Y', '750.000000');
        SetElementEditValues(newRef, 'DATA\Position\Z', '8380.000000');
        SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
        SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
        SetElementEditValues(newRef, 'DATA\Rotation\Z', '45.000000');
        // Set persistent
        SetIsPersistent(newRef, True);
        Inc(placeCount);
        AddMessage('  + Trunk placed: ' + IntToHex(FormID(newRef), 8));
      end;
    end;
  end

  // Second clone for dead wastelander (as REFR — not ideal but ACHR copy is tricky)
  else if placeCount = 1 then begin
    AddRequiredElementMasters(e, tp, False);
    newRef := wbCopyElementToFile(e, tp, True, True);
    if Assigned(newRef) then begin
      // Change to dead wastelander
      AddRequiredElementMasters(RecordByFormID(FileByIndex(0), $000A11F7, True), tp, False);
      SetElementNativeValues(newRef, 'NAME', $000A11F7);
      // Dead wastelander: near trunk (same grid cell)
      SetElementEditValues(newRef, 'DATA\Position\X', '-69750.000000');
      SetElementEditValues(newRef, 'DATA\Position\Y', '800.000000');
      SetElementEditValues(newRef, 'DATA\Position\Z', '8380.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
      SetElementEditValues(newRef, 'DATA\Rotation\Z', '180.000000');
      SetIsPersistent(newRef, True);
      Inc(placeCount);
      AddMessage('  + Dead wastelander placed: ' + IntToHex(FormID(newRef), 8));
    end;
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Place] Done: ' + IntToStr(placeCount) + ' objects placed');
  AddMessage('[Place] Note: The note should be added to trunk inventory instead of world placement.');
end;

end.
