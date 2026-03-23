{
  Debug: Dump effect structures of key DLC perks
  to find EPFD float values we can change.

  Run on: All DLC ESMs loaded, select all, Apply Script
}

unit DLCPerkOverhaulDebug;

procedure DumpEffects(e: IInterface);
var
  effects, effect, epft, epfd, floatEl: IInterface;
  i, j: Integer;
  edid, etype: string;
  val: Double;
begin
  edid := EditorID(e);
  effects := ElementByName(e, 'Effects');
  if not Assigned(effects) then begin
    AddMessage('  No Effects block');
    Exit;
  end;

  for i := 0 to Pred(ElementCount(effects)) do begin
    effect := ElementByIndex(effects, i);

    // Check for Entry Point type
    etype := GetElementEditValues(ElementBySignature(effect, 'PRKE'), 'Type');
    AddMessage('  Effect[' + IntToStr(i) + '] Type=' + etype);

    // Try to read EPFD float
    epft := ElementBySignature(effect, 'EPFT');
    if Assigned(epft) then begin
      epfd := ElementByName(epft, 'EPFD - Data');
      if Assigned(epfd) then begin
        floatEl := ElementByName(epfd, 'Float');
        if Assigned(floatEl) then begin
          val := GetNativeValue(floatEl);
          AddMessage('    EPFD Float = ' + FloatToStr(val));
        end else
          AddMessage('    EPFD (not float): ' + GetEditValue(epfd));
      end;
    end;
  end;
end;

function Initialize: Integer;
begin
  Result := 0;
  AddMessage('=== DLC PERK EFFECT DEBUG ===');
end;

function Process(e: IInterface): Integer;
var
  sig, edid, srcFile: string;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'PERK' then Exit;

  edid := EditorID(e);
  srcFile := GetFileName(GetFile(e));

  if not (Pos('NVDLC', edid) > 0) then Exit;
  if GetElementEditValues(e, 'DATA - Data\Playable') <> 'Yes' then Exit;

  AddMessage('');
  AddMessage('=== ' + GetElementEditValues(e, 'FULL') + ' (' + edid + ') [' + srcFile + '] ===');
  DumpEffects(e);
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Debug] Done');
end;

end.
