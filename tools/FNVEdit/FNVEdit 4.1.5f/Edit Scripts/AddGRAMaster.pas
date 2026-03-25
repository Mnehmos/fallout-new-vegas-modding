{
  Add GunRunnersArsenal.esm as master to MnehmosMojave.esp
  Then inject Mnehmos weapons into GRA vendor leveled lists.

  Run: Right-click MnehmosMojave.esp -> Apply Script
}

unit AddGRAMaster;

var
  tp, gra: IInterface;
  addCount: Integer;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  tp := nil;
  gra := nil;
  addCount := 0;

  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'MnehmosMojave.esp') then
      tp := FileByIndex(i);
    if SameText(GetFileName(FileByIndex(i)), 'GunRunnersArsenal.esm') then
      gra := FileByIndex(i);
  end;

  if not Assigned(tp) then begin
    AddMessage('ERROR: MnehmosMojave.esp not loaded');
    Result := 1;
    Exit;
  end;
  if not Assigned(gra) then begin
    AddMessage('ERROR: GunRunnersArsenal.esm not loaded');
    Result := 1;
    Exit;
  end;

  // Add GRA as master to our ESP
  AddMasterIfMissing(tp, 'GunRunnersArsenal.esm');
  AddMessage('[GRAMaster] Added GunRunnersArsenal.esm as master to MnehmosMojave.esp');
  AddMessage('[GRAMaster] Save MnehmosMojave.esp to finalize.');
end;

function Process(e: IInterface): Integer;
begin
  Result := 0;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[GRAMaster] Done. Save the ESP now.');
end;

end.
