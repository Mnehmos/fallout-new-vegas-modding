{
  Add OldWorldBlues.esm, DeadMoney.esm, and LonesomeRoad.esm as masters
  to MnehmosMojave.esp.

  Run: Right-click MnehmosMojave.esp -> Apply Script -> AddDLCMasters
  Then SAVE.
}

unit AddDLCMasters;

var
  tp: IInterface;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  tp := nil;

  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'MnehmosMojave.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('ERROR: MnehmosMojave.esp not loaded');
    Result := 1;
    Exit;
  end;

  AddMasterIfMissing(tp, 'DeadMoney.esm');
  AddMessage('Added DeadMoney.esm');

  AddMasterIfMissing(tp, 'OldWorldBlues.esm');
  AddMessage('Added OldWorldBlues.esm');

  AddMasterIfMissing(tp, 'LonesomeRoad.esm');
  AddMessage('Added LonesomeRoad.esm');

  AddMessage('Done. Save MnehmosMojave.esp now.');
end;

function Process(e: IInterface): Integer;
begin
  Result := 0;
end;

function Finalize: Integer;
begin
  Result := 0;
end;

end.
