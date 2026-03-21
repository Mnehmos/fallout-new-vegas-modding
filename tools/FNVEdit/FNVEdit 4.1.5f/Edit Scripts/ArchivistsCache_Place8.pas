{
  Archivist's Cache — Place v8

  NO cell retarget, NO cell override.
  Clone a donor REFR from the exact Goodsprings cell,
  change base+position, stay in same cell.
  No Cell field edit = no cell override = no crash.

  Run on: FalloutNV.esm
}

unit ArchivistsCachePlace8;

var
  tp: IInterface;
  placeCount: Integer;
  donorFound: Boolean;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  placeCount := 0;
  donorFound := False;

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

  AddMessage('[Place] v8 — Clone in same cell, no retarget');
end;

function Process(e: IInterface): Integer;
var
  sig: string;
  x, y: Double;
  trunkFormID: Cardinal;
  newRef: IInterface;
  i: Integer;
begin
  Result := 0;
  if donorFound then Exit;
  if placeCount >= 2 then Exit;

  sig := Signature(e);
  if sig <> 'REFR' then Exit;

  x := GetElementNativeValues(e, 'DATA\Position\X');
  y := GetElementNativeValues(e, 'DATA\Position\Y');

  // Goodsprings cell (-17, 0)
  // Cell bounds: X = -69632 to -65536, Y = 0 to 4096
  if (x < -69632) or (x > -65536) then Exit;
  if (y < 0) or (y > 4096) then Exit;

  donorFound := True;
  AddMessage('  Donor: ' + IntToHex(FormID(e), 8) + ' at (' + FloatToStr(x) + ', ' + FloatToStr(y) + ')');

  // Find trunk FormID
  trunkFormID := 0;
  for i := 0 to Pred(RecordCount(tp)) do begin
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistTrunk') then
      trunkFormID := FormID(RecordByIndex(tp, i));
  end;

  if trunkFormID = 0 then begin
    AddMessage('  ERROR: Trunk not found');
    Exit;
  end;

  // ═══ TRUNK — clone donor, change base+pos, NO cell retarget ═══
  AddRequiredElementMasters(e, tp, False);
  newRef := wbCopyElementToFile(e, tp, True, False);
  if Assigned(newRef) then begin
    SetElementNativeValues(newRef, 'NAME', trunkFormID);
    // Near GoodspringsArrivalMarker (-67857, 2332, 8376)
    SetElementEditValues(newRef, 'DATA\Position\X', '-67600.000000');
    SetElementEditValues(newRef, 'DATA\Position\Y', '2400.000000');
    SetElementEditValues(newRef, 'DATA\Position\Z', '8376.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
    SetElementEditValues(newRef, 'DATA\Rotation\Z', '45.000000');
    Inc(placeCount);
    AddMessage('  + Trunk: ' + IntToHex(FormID(newRef), 8));
  end;

  // BODY DISABLED — NPC placement causes crashes
  // The trunk alone is sufficient for the quest
  // Body can be added later when placement is more stable
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Place] Done: ' + IntToStr(placeCount) + ' placed (no cell override)');
end;

end.
