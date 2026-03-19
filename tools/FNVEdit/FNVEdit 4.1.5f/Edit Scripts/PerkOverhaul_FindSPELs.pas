{
  Find all SPEL references from Ability-type perk effects
  for perks we want to modify
}

unit FindSPELs;

function Initialize: Integer;
begin
  Result := 0;
  AddMessage('[FindSPELs] Scanning for Ability-type perk effect SPELs...');
  AddMessage('');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  effects, effect, prke, data, abil: IInterface;
  i, count: Integer;
  etype: string;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'PERK' then Exit;

  edid := EditorID(e);

  // Only check our target perks
  if not (SameText(edid, 'StrongBack') or SameText(edid, 'LifeGiver') or
          SameText(edid, 'ActionBoy') or SameText(edid, 'ActionGirl') or
          SameText(edid, 'Finesse') or SameText(edid, 'NerdRage') or
          SameText(edid, 'GrimReaperSprint') or SameText(edid, 'FastMetabolism') or
          SameText(edid, 'AdamantiumSkeleton') or SameText(edid, 'Cannibal') or
          SameText(edid, 'LongHaul') or SameText(edid, 'PackRat') or
          SameText(edid, 'WeaponHandling') or SameText(edid, 'Commando') or
          SameText(edid, 'Gunslinger') or SameText(edid, 'Sniper') or
          SameText(edid, 'SilentRunning') or SameText(edid, 'MathWrath') or
          SameText(edid, 'Comprehension') or SameText(edid, 'Retention')) then Exit;

  effects := ElementByName(e, 'Effects');
  if not Assigned(effects) then Exit;
  count := ElementCount(effects);

  for i := 0 to Pred(count) do begin
    effect := ElementByIndex(effects, i);
    prke := ElementBySignature(effect, 'PRKE');
    if not Assigned(prke) then Continue;

    etype := GetElementEditValues(prke, 'Type');

    if SameText(etype, 'Ability') then begin
      data := ElementBySignature(effect, 'DATA');
      if Assigned(data) then begin
        abil := ElementByName(data, 'Ability');
        if Assigned(abil) then
          AddMessage(edid + ' [Rank ' + GetElementEditValues(prke, 'Rank') + ']: SPEL = ' + GetEditValue(abil));
      end;
    end;

    if SameText(etype, 'Entry Point') then begin
      AddMessage(edid + ' [Rank ' + GetElementEditValues(prke, 'Rank') + ']: Entry Point (float, already handled)');
    end;
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[FindSPELs] Done. Use these SPEL FormIDs to find and modify the actual stat values.');
end;

end.
