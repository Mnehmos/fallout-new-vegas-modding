{
  Debug: Dump Bad Memories and Good Memories from MnehmosMojave.esp
  to see if stat values actually applied
}

unit MnehmosSetDebugWeap;

procedure DumpElement(e: IInterface; indent: string; depth: Integer);
var
  i: Integer;
  child: IInterface;
begin
  if depth > 3 then Exit;
  AddMessage(indent + Name(e) + ' [sig=' + Signature(e) + '] val="' + GetEditValue(e) + '"');
  for i := 0 to Pred(ElementCount(e)) do begin
    child := ElementByIndex(e, i);
    DumpElement(child, indent + '  ', depth + 1);
  end;
end;

function Initialize: Integer;
begin
  Result := 0;
  AddMessage('[WeapDebug] Dumping Mnehmos weapons...');
end;

function Process(e: IInterface): Integer;
var
  edid: string;
begin
  Result := 0;
  if Signature(e) <> 'WEAP' then Exit;
  edid := EditorID(e);

  if SameText(edid, 'WeapBadMemories') or
     SameText(edid, 'WeapGoodMemories') or
     SameText(edid, 'WeapNVCaravanShotgun') then begin
    AddMessage('');
    AddMessage('=== ' + edid + ' (' + GetFileName(GetFile(e)) + ') ===');
    DumpElement(e, '  ', 0);
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[WeapDebug] Done');
end;

end.
