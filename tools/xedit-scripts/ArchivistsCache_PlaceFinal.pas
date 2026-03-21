{
  Archivist's Cache — FINAL Placement

  Uses the clean Add(wrld, 'CELL[X,Y]') API.
  Places trunk + dead wastelander near Goodsprings saloon.

  COORDINATES: Get exact positions in-game by standing where you want
  the object and typing in console:
    player.getpos x
    player.getpos y
    player.getpos z
  Then update the constants below.

  Run on: FalloutNV.esm (click it, Apply Script)
  Requires: ArchivistsCache.esp loaded
}

unit ArchivistsCachePlaceFinal;

const
  TARGET_ESP = 'ArchivistsCache.esp';
  WASTELAND_NV = $000DA726;

  // ═══ COORDINATES — Derived from game data landmarks ═══
  // GoodspringsArrivalMarker = (-67856.8, 2332.2, 8376.0)
  // vMEGoodSpringsRef        = (-69594.8, 3438.5, 8386.9)
  // Trunk: slightly east of arrival marker (toward gas station)
  TRUNK_X = -67600.0;
  TRUNK_Y = 2400.0;
  TRUNK_Z = 8376.0;
  TRUNK_ROT = 45.0;

  // Body: north of arrival marker (toward cemetery hill)
  BODY_X = -67900.0;
  BODY_Y = 2800.0;
  BODY_Z = 8380.0;
  BODY_ROT = 270.0;

var
  tp: IInterface;

function Initialize: Integer;
var
  wrld, cell, newRef: IInterface;
  gridX, gridY: Integer;
  trunkFormID, noteFormID: Cardinal;
  i: Integer;
begin
  Result := 0;

  // Find target ESP
  tp := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), TARGET_ESP) then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('ERROR: ' + TARGET_ESP + ' not loaded.');
    Result := 1;
    Exit;
  end;

  // Find our item FormIDs
  trunkFormID := 0;
  for i := 0 to Pred(RecordCount(tp)) do begin
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistTrunk') then
      trunkFormID := FormID(RecordByIndex(tp, i));
  end;

  if trunkFormID = 0 then begin
    AddMessage('ERROR: MnehmosArchivistTrunk not found in ESP');
    Result := 1;
    Exit;
  end;

  AddMessage('[ArchivistsCache] Placing objects...');
  AddMessage('  Trunk FormID: ' + IntToHex(trunkFormID, 8));

  // Get WastelandNV
  wrld := RecordByFormID(FileByIndex(0), WASTELAND_NV, True);
  if not Assigned(wrld) then begin
    AddMessage('ERROR: WastelandNV not found');
    Result := 1;
    Exit;
  end;

  AddMasterIfMissing(tp, 'FalloutNV.esm');

  // Copy WRLD as override into our ESP so we can Add to it
  AddRequiredElementMasters(wrld, tp, False);
  wrld := wbCopyElementToFile(wrld, tp, False, True);
  if not Assigned(wrld) then begin
    AddMessage('ERROR: Could not override WastelandNV');
    Result := 1;
    Exit;
  end;
  AddMessage('  Overrode WastelandNV into ' + TARGET_ESP);

  // ═══ PLACE TRUNK ═══
  gridX := Trunc(TRUNK_X / 4096);
  if TRUNK_X < 0 then gridX := gridX - 1;
  gridY := Trunc(TRUNK_Y / 4096);

  AddMessage('  Trunk grid: (' + IntToStr(gridX) + ', ' + IntToStr(gridY) + ')');

  cell := Add(wrld, 'CELL[' + IntToStr(gridX) + ',' + IntToStr(gridY) + ']', True);
  if not Assigned(cell) then begin
    AddMessage('ERROR: Could not get/create cell for trunk');
    Result := 1;
    Exit;
  end;

  newRef := Add(cell, 'REFR', True);
  if Assigned(newRef) then begin
    SetElementNativeValues(newRef, 'NAME', trunkFormID);
    SetElementNativeValues(newRef, 'DATA\Position\X', TRUNK_X);
    SetElementNativeValues(newRef, 'DATA\Position\Y', TRUNK_Y);
    SetElementNativeValues(newRef, 'DATA\Position\Z', TRUNK_Z);
    SetElementNativeValues(newRef, 'DATA\Rotation\X', 0.0);
    SetElementNativeValues(newRef, 'DATA\Rotation\Y', 0.0);
    SetElementNativeValues(newRef, 'DATA\Rotation\Z', TRUNK_ROT);
    AddMessage('  + Trunk: ' + IntToHex(FormID(newRef), 8));
  end else
    AddMessage('  ERROR: Could not create trunk REFR');

  // ═══ PLACE DEAD WASTELANDER ═══
  gridX := Trunc(BODY_X / 4096);
  if BODY_X < 0 then gridX := gridX - 1;
  gridY := Trunc(BODY_Y / 4096);

  cell := Add(wrld, 'CELL[' + IntToStr(gridX) + ',' + IntToStr(gridY) + ']', True);
  if not Assigned(cell) then begin
    AddMessage('ERROR: Could not get/create cell for body');
    Result := 1;
    Exit;
  end;

  // Add master for dead wastelander
  AddRequiredElementMasters(RecordByFormID(FileByIndex(0), $000A11F7, True), tp, False);

  newRef := Add(cell, 'ACRE', True);  // ACRE for creatures/placed leveled NPCs in FNV
  if not Assigned(newRef) then begin
    // Fall back to ACHR if ACRE doesn't work
    newRef := Add(cell, 'ACHR', True);
  end;

  if Assigned(newRef) then begin
    SetElementNativeValues(newRef, 'NAME', $000A11F7);  // VarDEADWastelander
    SetElementNativeValues(newRef, 'DATA\Position\X', BODY_X);
    SetElementNativeValues(newRef, 'DATA\Position\Y', BODY_Y);
    SetElementNativeValues(newRef, 'DATA\Position\Z', BODY_Z);
    SetElementNativeValues(newRef, 'DATA\Rotation\X', 0.0);
    SetElementNativeValues(newRef, 'DATA\Rotation\Y', 0.0);
    SetElementNativeValues(newRef, 'DATA\Rotation\Z', BODY_ROT);
    AddMessage('  + Dead wastelander: ' + IntToHex(FormID(newRef), 8));
  end else
    AddMessage('  ERROR: Could not create body ref');

  AddMessage('');
  AddMessage('[ArchivistsCache] Done. Save and test.');
  AddMessage('  Walk to Goodsprings saloon to find the trunk.');
end;

function Finalize: Integer;
begin
  Result := 0;
end;

end.
