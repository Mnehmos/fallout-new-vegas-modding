{
  Debug: Dump the enchantment records used by our cloned armor
  to understand ENCH structure for creating custom ones

  Targets:
    EnchClothingDuster [ENCH:0008B608] — Bounty Hunter Duster enchant
    EnchClothingHeadSunGuard [ENCH:00071B88] — Cowboy Hat enchant
    EnchFourEyesGlasses [ENCH:00135F74] — Authority Glasses enchant
    Also: 1st Recon Beret enchant for +crit reference
}

unit MnehmosSetDebugENCH;

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
  AddMessage('[ENCH Debug] Dumping enchantment structures...');
end;

function Process(e: IInterface): Integer;
var
  edid: string;
  fid: Cardinal;
begin
  Result := 0;
  if Signature(e) <> 'ENCH' then Exit;

  fid := FixedFormID(e);
  edid := EditorID(e);

  // Duster enchant
  if fid = $0008B608 then begin
    AddMessage('');
    AddMessage('=== ' + edid + ' (Duster) ===');
    DumpElement(e, '  ', 0);
  end;

  // Cowboy hat enchant
  if fid = $00071B88 then begin
    AddMessage('');
    AddMessage('=== ' + edid + ' (Cowboy Hat) ===');
    DumpElement(e, '  ', 0);
  end;

  // Authority Glasses enchant (Four Eyes)
  if fid = $00135F74 then begin
    AddMessage('');
    AddMessage('=== ' + edid + ' (Authority Glasses) ===');
    DumpElement(e, '  ', 0);
  end;

  // Also find any enchant that adds +1 PER or +1 INT as reference
  if SameText(edid, 'EnchClothing1stReconBeret') or
     SameText(edid, 'EnchHatNCR1stReconBeret') then begin
    AddMessage('');
    AddMessage('=== ' + edid + ' (1st Recon Beret) ===');
    DumpElement(e, '  ', 0);
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[ENCH Debug] Done');
end;

end.
