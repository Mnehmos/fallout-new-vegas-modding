{
  Verify: Check EITM links on Mnehmos armor items
  and dump the enchantment details they point to
}

unit MnehmosSetVerifyEITM;

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
  AddMessage('[Verify] Checking Mnehmos armor EITM links...');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  eitm, enchRef: IInterface;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'ARMO' then Exit;

  edid := EditorID(e);
  if not (SameText(edid, 'ArmorArchivistDuster') or
          SameText(edid, 'HatMnehmos') or
          SameText(edid, 'GlassesRecollection')) then Exit;

  AddMessage('');
  AddMessage('=== ' + edid + ' (' + GetFileName(GetFile(e)) + ') ===');

  eitm := ElementBySignature(e, 'EITM');
  if Assigned(eitm) then begin
    AddMessage('  EITM value: ' + GetEditValue(eitm));
    AddMessage('  EITM native: ' + IntToHex(GetNativeValue(eitm), 8));

    // Try to resolve the referenced ENCH record
    enchRef := LinksTo(eitm);
    if Assigned(enchRef) then begin
      AddMessage('  Linked ENCH:');
      DumpElement(enchRef, '    ', 0);
    end else begin
      AddMessage('  WARNING: EITM does not resolve to a valid record!');
    end;
  end else begin
    AddMessage('  WARNING: No EITM field found!');
  end;

  // Also dump DNAM for DT check
  AddMessage('  DT: ' + GetElementEditValues(e, 'DNAM\DT'));
  AddMessage('  Value: ' + GetElementEditValues(e, 'DATA\Value'));
  AddMessage('  Health: ' + GetElementEditValues(e, 'DATA\Health'));
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Verify] Done');
end;

end.
