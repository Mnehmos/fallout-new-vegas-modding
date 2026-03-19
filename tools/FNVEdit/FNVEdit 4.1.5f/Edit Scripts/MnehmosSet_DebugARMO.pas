{
  Debug: Dump Bounty Hunter Duster, Desperado Cowboy Hat, Authority Glasses
  to find correct field paths for ARMO editing
}

unit MnehmosSetDebugARMO;

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
  AddMessage('[ARMO Debug] Dumping armor structures...');
end;

function Process(e: IInterface): Integer;
var
  edid: string;
begin
  Result := 0;
  if Signature(e) <> 'ARMO' then Exit;
  edid := EditorID(e);

  if SameText(edid, 'BountyHunterDuster') or
     SameText(edid, 'CowboyHat01') or
     SameText(edid, 'GlassesNCRRangerCivilian') then begin
    AddMessage('');
    AddMessage('=== ' + edid + ' ===');
    DumpElement(e, '  ', 0);
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[ARMO Debug] Done');
end;

end.
