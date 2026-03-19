{
  FNVEdit Pascal Script: BatchSetPerkValues.pas

  Purpose: Template for batch-editing perk records in FalloutNV.esm
  Usage:   In FNVEdit, select records → Apply Script → choose this file

  Docs:    xEdit scripting reference: https://tes5edit.github.io/docs/
}

unit BatchSetPerkValues;

// -------------------------------------------------------
// Configuration — edit these before running
// -------------------------------------------------------
const
  // Set to True to preview changes without saving
  DRY_RUN = True;

  // Example: force all perks named in PERK_NAMES to be level 1 req
  TARGET_LEVEL_REQ = 1;

// List perk EditorIDs to target (leave empty to target ALL perks)
var
  PERK_NAMES: array of string;

// -------------------------------------------------------

procedure Initialize;
begin
  AddMessage('BatchSetPerkValues starting...');
  AddMessage('DRY_RUN = ' + BoolToStr(DRY_RUN));

  // Define which perks to target
  SetLength(PERK_NAMES, 3);
  PERK_NAMES[0] := 'Finesse';
  PERK_NAMES[1] := 'BetterCriticals';
  PERK_NAMES[2] := 'CriticalBanker';
end;

function ShouldProcessPerk(EditorID: string): Boolean;
var
  i: Integer;
begin
  // If no filter defined, process all
  if Length(PERK_NAMES) = 0 then begin
    Result := True;
    Exit;
  end;

  Result := False;
  for i := 0 to High(PERK_NAMES) do begin
    if SameText(EditorID, PERK_NAMES[i]) then begin
      Result := True;
      Exit;
    end;
  end;
end;

function Process(e: IInterface): Integer;
var
  EditorID: string;
  levelReqElement: IInterface;
begin
  Result := 0;

  // Only process PERK records
  if Signature(e) <> 'PERK' then Exit;

  EditorID := GetEditValue(ElementBySignature(e, 'EDID'));

  if not ShouldProcessPerk(EditorID) then Exit;

  AddMessage('Processing perk: ' + EditorID);

  // --- Read current values ---
  // PERK records have conditions under DATA\CTDA elements
  // Level requirement is typically in the conditions list

  // For a simple value edit example: change perk rank count
  // (DATA element contains Trait, Playable, Hidden, Level, NumRanks, etc.)
  // levelReqElement := ElementByPath(e, 'DATA\Level');
  //
  // if Assigned(levelReqElement) then begin
  //   AddMessage('  Level req: ' + GetEditValue(levelReqElement));
  //   if not DRY_RUN then
  //     SetEditValue(levelReqElement, IntToStr(TARGET_LEVEL_REQ));
  // end;

  AddMessage('  [TODO: add your specific edits here]');
end;

procedure Finalize;
begin
  AddMessage('BatchSetPerkValues complete.');
  if DRY_RUN then
    AddMessage('DRY RUN — no changes were saved.');
end;

end.
