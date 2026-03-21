{
  PlaceInWasteland_Template.pas
  ==============================
  Definitive xEdit script for placing objects in FNV exterior worldspaces.
  Uses the Add(wrld, 'CELL[X,Y]') API (xEdit 4.0.0+).

  HOW TO USE:
    1. Copy this file and rename for your mod
    2. Edit the CONFIG section below with your target ESP, base object, and coords
    3. Open xEdit with FalloutNV.esm + your target ESP loaded
    4. Select any record, run this script via Apply Script
    5. Save the plugin — done

  GRID CELL MATH:
    Each exterior cell = 4096 x 4096 game units.
    Grid X = Floor(posX / 4096)
    Grid Y = Floor(posY / 4096)
    Avoid exact boundary positions (-n*4096.0) — known xEdit bug.

  RECORD TYPES:
    REFR = placed objects (statics, items, containers, furniture, etc.)
    ACHR = placed humanoid NPCs
    ACRE = placed creatures (animals, robots, mutants) — FNV only, merged into ACHR in later games

  KEY FORMIDS (WastelandNV):
    Worldspace WRLD  = $000DA726
    Persistent Cell  = $000846EA
    Goodsprings area = grid cell (-17, 0), cell FormID $000DAEB9
}

unit PlaceInWasteland_Template;

// ═══════════════════════════════════════════════════════════════
//  CONFIG — Edit these values for your placement
// ═══════════════════════════════════════════════════════════════
const
  // Target plugin filename (must be loaded in xEdit)
  sTargetESP      = 'MnehmosMojave.esp';

  // Base object FormID to place (from FalloutNV.esm or any loaded master)
  // Example: $0010C847 = Sunset Sarsaparilla Crate
  iBaseObjectFID  = $0010C847;

  // Record type to create: 'REFR' for objects, 'ACHR' for NPCs, 'ACRE' for creatures
  sRecordType     = 'REFR';

  // World position in game units
  fPosX           = -67978.0;   // Goodsprings saloon area
  fPosY           = 1990.0;
  fPosZ           = 8380.0;

  // Rotation in degrees (0-360)
  fRotX           = 0.0;
  fRotY           = 0.0;
  fRotZ           = 0.0;

  // Scale (1.0 = normal)
  fScale          = 1.0;

  // Set True to make persistent (always loaded, findable via player.moveto)
  bPersistent     = False;

  // Optional EditorID for the placed reference (leave empty for none)
  sEditorID       = '';

  // WastelandNV worldspace FormID — do not change unless targeting a different worldspace
  iWastelandFID   = $000DA726;

// ═══════════════════════════════════════════════════════════════
//  END CONFIG — Do not edit below unless you know what you're doing
// ═══════════════════════════════════════════════════════════════

var
  bDone: Boolean;

function Initialize: Integer;
begin
  bDone := False;
  Result := 0;
end;

function Process(e: IInterface): Integer;
var
  targetFile: IInterface;
  wrld: IInterface;
  cell: IInterface;
  newRef: IInterface;
  gridX, gridY: Integer;
  flags: Cardinal;
  cellKey: string;
  i: Integer;
begin
  Result := 0;

  // Only run once — we use Process as an entry point but do our own work
  if bDone then Exit;
  bDone := True;

  // ── Step 1: Find the target plugin ──
  targetFile := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), sTargetESP) then begin
      targetFile := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(targetFile) then begin
    AddMessage('ERROR: Target plugin "' + sTargetESP + '" not found. Is it loaded?');
    Result := 1;
    Exit;
  end;

  AddMessage('Target plugin: ' + GetFileName(targetFile));

  // ── Step 2: Get the WastelandNV worldspace from the master file ──
  // RecordByFormID searches across all loaded files; True = resolve to winning override
  wrld := RecordByFormID(FileByIndex(0), iWastelandFID, True);

  if not Assigned(wrld) then begin
    AddMessage('ERROR: WastelandNV worldspace not found (FormID $000DA726)');
    Result := 1;
    Exit;
  end;

  AddMessage('Found worldspace: ' + Name(wrld));

  // ── Step 3: Ensure worldspace override exists in our plugin ──
  // wbCopyElementToFile with aAsNew=False, aDeepCopy=False creates an override
  wrld := wbCopyElementToFile(wrld, targetFile, False, True);
  if not Assigned(wrld) then begin
    AddMessage('ERROR: Failed to create worldspace override in target plugin');
    Result := 1;
    Exit;
  end;

  // ── Step 4: Get or create the target cell ──
  if bPersistent then begin
    // Persistent cell — always loaded, refs findable by player.moveto
    // 'CELL[P]' gets/creates the persistent cell for this worldspace
    cell := Add(wrld, 'CELL[P]', True);
    AddMessage('Using persistent cell');
  end else begin
    // Temporary cell at grid coordinates
    // Grid = Floor(position / 4096)
    gridX := Floor(fPosX / 4096.0);
    gridY := Floor(fPosY / 4096.0);
    cellKey := 'CELL[' + IntToStr(gridX) + ',' + IntToStr(gridY) + ']';
    cell := Add(wrld, cellKey, True);
    AddMessage('Using cell at grid (' + IntToStr(gridX) + ', ' + IntToStr(gridY) + ')');
  end;

  if not Assigned(cell) then begin
    AddMessage('ERROR: Failed to get/create cell. Check grid coordinates.');
    Result := 1;
    Exit;
  end;

  AddMessage('Cell: ' + Name(cell));

  // ── Step 5: Create the placed reference ──
  // sRecordType should be 'REFR', 'ACHR', or 'ACRE'
  newRef := Add(cell, sRecordType, True);

  if not Assigned(newRef) then begin
    AddMessage('ERROR: Failed to create ' + sRecordType + ' in cell');
    Result := 1;
    Exit;
  end;

  AddMessage('Created ' + sRecordType + ': ' + Name(newRef));

  // ── Step 6: Set the base object (NAME field) ──
  SetElementNativeValues(newRef, 'NAME', iBaseObjectFID);

  // ── Step 7: Set position ──
  SetElementNativeValues(newRef, 'DATA\Position\X', fPosX);
  SetElementNativeValues(newRef, 'DATA\Position\Y', fPosY);
  SetElementNativeValues(newRef, 'DATA\Position\Z', fPosZ);

  // ── Step 8: Set rotation ──
  // xEdit stores rotation in radians internally but NativeValues uses degrees for FNV
  SetElementNativeValues(newRef, 'DATA\Rotation\X', fRotX);
  SetElementNativeValues(newRef, 'DATA\Rotation\Y', fRotY);
  SetElementNativeValues(newRef, 'DATA\Rotation\Z', fRotZ);

  // ── Step 9: Set scale (only if not 1.0) ──
  if Abs(fScale - 1.0) > 0.001 then begin
    Add(newRef, 'XSCL', True);
    SetElementNativeValues(newRef, 'XSCL', fScale);
    AddMessage('Scale: ' + FloatToStr(fScale));
  end;

  // ── Step 10: Set persistent flag if requested ──
  if bPersistent then begin
    flags := GetElementNativeValues(newRef, 'Record Header\Record Flags');
    flags := flags or $00000400;  // Persistent flag
    SetElementNativeValues(newRef, 'Record Header\Record Flags', flags);
    AddMessage('Persistent flag set');
  end;

  // ── Step 11: Set EditorID if provided ──
  if sEditorID <> '' then begin
    SetElementEditValues(newRef, 'EDID', sEditorID);
    AddMessage('EditorID: ' + sEditorID);
  end;

  // ── Done ──
  AddMessage('');
  AddMessage('=== Placement Complete ===');
  AddMessage('  Type: ' + sRecordType);
  AddMessage('  Base: ' + IntToHex(iBaseObjectFID, 8));
  AddMessage('  Position: (' + FloatToStr(fPosX) + ', ' + FloatToStr(fPosY) + ', ' + FloatToStr(fPosZ) + ')');
  AddMessage('  Persistent: ' + BoolToStr(bPersistent, True));
  AddMessage('  Plugin: ' + sTargetESP);
  AddMessage('');
  AddMessage('Remember to SAVE the plugin in xEdit!');
end;

end.
