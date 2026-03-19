{
  Debug: Dump the structure of key LVLC and LVLN records
  to understand entry fields (count, level, chance, references)
}

unit PopDensityDebug;

procedure DumpElement(e: IInterface; indent: string; depth: Integer);
var
  i: Integer;
  child: IInterface;
begin
  if depth > 4 then Exit;
  AddMessage(indent + Name(e) + ' [sig=' + Signature(e) + '] val="' + GetEditValue(e) + '"');
  for i := 0 to Pred(ElementCount(e)) do begin
    child := ElementByIndex(e, i);
    DumpElement(child, indent + '  ', depth + 1);
  end;
end;

function Initialize: Integer;
begin
  Result := 0;
  AddMessage('[PopDensity Debug] Dumping leveled list structures...');
  AddMessage('');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);

  // Dump a few key lists
  if SameText(edid, 'EncWastelandNV') or
     SameText(edid, 'VEncTier1GeckoSmall') or
     SameText(edid, 'EncFiendRandom') or
     SameText(edid, 'VarNCRTrooper') or
     SameText(edid, 'EncWastelandNVWeak') then begin
    AddMessage('');
    AddMessage('=== ' + edid + ' (' + sig + ') ===');
    DumpElement(e, '  ', 0);
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[PopDensity Debug] Done');
end;

end.
