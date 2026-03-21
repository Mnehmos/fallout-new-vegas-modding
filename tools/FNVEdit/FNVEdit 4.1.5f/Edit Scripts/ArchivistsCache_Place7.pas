{
  Archivist's Cache — Place v7 (FINAL)

  The solution: Clone an existing REFR, change base+position,
  then use the virtual 'Cell' field to move it to the correct
  owning cell for its coordinates.

  Uses GetCellFromWorldspace from xEdit's shipped script
  "Put worldspace references in the right cells.pas"

  Run on: FalloutNV.esm (click it, Apply Script)
}

unit ArchivistsCachePlace7;

var
  tp: IInterface;
  placeCount: Integer;
  donorFound: Boolean;

// ─── Copied from "Put worldspace references in the right cells.pas" ───

function GetCellFromWorldspace(Worldspace: IInterface; GridX, GridY: integer): IInterface;
var
  blockidx, subblockidx, cellidx: integer;
  wrldgrup, block, subblock, cell: IInterface;
  Grid, GridBlock, GridSubBlock: TwbGridCell;
  LabelBlock, LabelSubBlock: Cardinal;
begin
  Grid := wbGridCell(GridX, GridY);
  GridSubBlock := wbSubBlockFromGridCell(Grid);
  LabelSubBlock := wbGridCellToGroupLabel(GridSubBlock);
  GridBlock := wbBlockFromSubBlock(GridSubBlock);
  LabelBlock := wbGridCellToGroupLabel(GridBlock);

  wrldgrup := ChildGroup(Worldspace);
  for blockidx := 0 to Pred(ElementCount(wrldgrup)) do begin
    block := ElementByIndex(wrldgrup, blockidx);
    if GroupLabel(block) <> LabelBlock then Continue;
    for subblockidx := 0 to Pred(ElementCount(block)) do begin
      subblock := ElementByIndex(block, subblockidx);
      if GroupLabel(subblock) <> LabelSubBlock then Continue;
      for cellidx := 0 to Pred(ElementCount(subblock)) do begin
        cell := ElementByIndex(subblock, cellidx);
        if (Signature(cell) <> 'CELL') or GetIsPersistent(cell) then Continue;
        if (GetElementNativeValues(cell, 'XCLC\X') = Grid.x) and (GetElementNativeValues(cell, 'XCLC\Y') = Grid.y) then begin
          Result := cell;
          Exit;
        end;
      end;
      Break;
    end;
    Break;
  end;
end;

// ─── Main Logic ───

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

  AddMessage('[Place] v7 — Clone + retarget Cell ownership');
end;

function PlaceClone(donorRef: IInterface; baseFormID: Cardinal;
  x, y, z, rotZ: Double; edid: string): IInterface;
var
  newRef, oldCell, ws, targetCell: IInterface;
  c: TwbGridCell;
begin
  Result := nil;

  // Clone donor as NEW record in our ESP
  AddRequiredElementMasters(donorRef, tp, False);
  newRef := wbCopyElementToFile(donorRef, tp, True, True);
  if not Assigned(newRef) then begin
    AddMessage('    ERROR: Clone failed');
    Exit;
  end;

  // Change base object
  SetElementNativeValues(newRef, 'NAME', baseFormID);

  // Set position
  SetElementEditValues(newRef, 'DATA\Position\X', FloatToStr(x));
  SetElementEditValues(newRef, 'DATA\Position\Y', FloatToStr(y));
  SetElementEditValues(newRef, 'DATA\Position\Z', FloatToStr(z));
  SetElementEditValues(newRef, 'DATA\Rotation\X', '0.000000');
  SetElementEditValues(newRef, 'DATA\Rotation\Y', '0.000000');
  SetElementEditValues(newRef, 'DATA\Rotation\Z', FloatToStr(rotZ));

  // ═══ THE KEY STEP: Retarget cell ownership ═══
  // Get the worldspace from the donor's current cell
  oldCell := LinksTo(ElementByName(newRef, 'Cell'));
  if Assigned(oldCell) then begin
    ws := LinksTo(ElementByName(oldCell, 'Worldspace'));
    if Assigned(ws) then begin
      // Compute correct grid cell from new position
      c := wbPositionToGridCell(GetPosition(newRef));
      AddMessage('    Grid cell: (' + IntToStr(c.x) + ', ' + IntToStr(c.y) + ')');

      // Find the actual CELL record for that grid position
      targetCell := GetCellFromWorldspace(ws, c.x, c.y);
      if Assigned(targetCell) then begin
        AddMessage('    Moving to cell: ' + Name(targetCell));
        SetElementEditValues(newRef, 'Cell', Name(targetCell));
      end else
        AddMessage('    WARNING: Target cell not found for grid');
    end else
      AddMessage('    WARNING: No worldspace found');
  end else
    AddMessage('    WARNING: No owning cell found');

  Inc(placeCount);
  AddMessage('  + ' + edid + ': ' + IntToHex(FormID(newRef), 8));
  Result := newRef;
end;

function Process(e: IInterface): Integer;
var
  sig: string;
  x, y: Double;
  noteFormID, trunkFormID: Cardinal;
  i: Integer;
begin
  Result := 0;
  if donorFound then Exit;

  sig := Signature(e);
  if sig <> 'REFR' then Exit;

  // Find a REFR anywhere in the Goodsprings area
  // Real coords: X ~ -68000, Y ~ 2000
  x := GetElementNativeValues(e, 'DATA\Position\X');
  y := GetElementNativeValues(e, 'DATA\Position\Y');

  if (x < -70000) or (x > -65000) then Exit;
  if (y < -1000) or (y > 5000) then Exit;

  donorFound := True;
  AddMessage('  Donor REFR: ' + IntToHex(FormID(e), 8));
  AddMessage('    Base: ' + GetElementEditValues(e, 'NAME'));
  AddMessage('    Pos: (' + FloatToStr(x) + ', ' + FloatToStr(y) + ')');

  // Find our items
  noteFormID := 0;
  trunkFormID := 0;
  for i := 0 to Pred(RecordCount(tp)) do begin
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistNote') then
      noteFormID := FormID(RecordByIndex(tp, i));
    if SameText(EditorID(RecordByIndex(tp, i)), 'MnehmosArchivistTrunk') then
      trunkFormID := FormID(RecordByIndex(tp, i));
  end;

  // Add dead wastelander master
  AddRequiredElementMasters(RecordByFormID(FileByIndex(0), $000A11F7, True), tp, False);

  // ═══ PLACE OBJECTS ═══
  // Trunk: near Goodsprings saloon (real coords from player)
  if trunkFormID > 0 then
    PlaceClone(e, trunkFormID, -67800.0, 2100.0, 8380.0, 45.0, 'ArchivistTrunk');

  // Dead wastelander: near trunk
  PlaceClone(e, $000A11F7, -67900.0, 2200.0, 8380.0, 180.0, 'DeadWastelander');
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Place] Done: ' + IntToStr(placeCount) + ' placed');
  AddMessage('[Place] Save, then: player.moveto [trunk FormID]');
end;

end.
