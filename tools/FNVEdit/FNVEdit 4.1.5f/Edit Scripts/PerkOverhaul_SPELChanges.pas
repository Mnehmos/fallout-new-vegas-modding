{
  PerkOverhaul - Phase 2b: SPEL Value Changes + GrimReaperSprint

  Modifies the SPEL (spell/ability) records that Ability-type perks reference.
  Also modifies GrimReaperSprint Entry Point float.

  Run on ALL records (not just PERKs) — needs to hit SPEL and PERK types.

  SPEL Changes:
    PerkLifeGiver1      [00031D88]: +30 HP -> +40 HP
    PerkNerdRage        [00044CA4]: +15 DT -> +20 DT
    PerkActionBoy1      [001718B7]: +15 AP -> +20 AP
    PerkActionBoy2      [00031D90]: +30 AP -> +40 AP
    PerkActionGirl1     [001718B6]: +15 AP -> +20 AP
    PerkActionGirl2     [0007B200]: +30 AP -> +40 AP

  PERK Changes:
    GrimReaperSprint: +20 AP -> +30 AP (Entry Point float)
}

unit PerkOverhaulSPELs;

var
  changeCount: Integer;

function Initialize: Integer;
begin
  Result := 0;
  changeCount := 0;
  AddMessage('[PerkOverhaul] Phase 2b: Modifying SPEL ability values + GrimReaperSprint...');
end;

procedure ModifySPELEffect(e: IInterface; targetMag: Double; newMag: Double; desc: string);
var
  effects, effect, efitEl: IInterface;
  i: Integer;
  curMag: Double;
begin
  effects := ElementByName(e, 'Effects');
  if not Assigned(effects) then Exit;

  for i := 0 to Pred(ElementCount(effects)) do begin
    effect := ElementByIndex(effects, i);
    efitEl := ElementBySignature(effect, 'EFIT');
    if not Assigned(efitEl) then Continue;

    curMag := GetElementNativeValues(efitEl, 'Magnitude');
    if (curMag > targetMag - 0.5) and (curMag < targetMag + 0.5) then begin
      SetElementNativeValues(efitEl, 'Magnitude', newMag);
      AddMessage('  ' + desc + ': ' + FloatToStr(curMag) + ' -> ' + FloatToStr(newMag));
      Inc(changeCount);
    end;
  end;
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  fid: Cardinal;
  effects, effect, epft, epfd, floatEl: IInterface;
  i: Integer;
  oldVal: Double;
begin
  Result := 0;
  sig := Signature(e);

  // Handle SPEL records by FormID
  if sig = 'SPEL' then begin
    fid := FixedFormID(e);
    edid := EditorID(e);

    // PerkLifeGiver1 [00031D88]: +30 HP -> +40 HP
    if fid = $00031D88 then
      ModifySPELEffect(e, 30.0, 40.0, 'LifeGiver HP');

    // PerkNerdRage [00044CA4]: +15 DT -> +20 DT
    if fid = $00044CA4 then
      ModifySPELEffect(e, 15.0, 20.0, 'NerdRage DT');

    // PerkActionBoy1 [001718B7]: +15 AP -> +20 AP
    if fid = $001718B7 then
      ModifySPELEffect(e, 15.0, 20.0, 'ActionBoy Rank1 AP');

    // PerkActionBoy2 [00031D90]: +30 AP -> +40 AP
    if fid = $00031D90 then
      ModifySPELEffect(e, 30.0, 40.0, 'ActionBoy Rank2 AP');

    // PerkActionGirl1 [001718B6]: +15 AP -> +20 AP
    if fid = $001718B6 then
      ModifySPELEffect(e, 15.0, 20.0, 'ActionGirl Rank1 AP');

    // PerkActionGirl2 [0007B200]: +30 AP -> +40 AP
    if fid = $0007B200 then
      ModifySPELEffect(e, 30.0, 40.0, 'ActionGirl Rank2 AP');
  end;

  // Handle GrimReaperSprint PERK (Entry Point float)
  if sig = 'PERK' then begin
    edid := EditorID(e);
    if SameText(edid, 'GrimReaperSprint') then begin
      effects := ElementByName(e, 'Effects');
      if not Assigned(effects) then Exit;

      for i := 0 to Pred(ElementCount(effects)) do begin
        effect := ElementByIndex(effects, i);
        epft := ElementBySignature(effect, 'EPFT');
        if not Assigned(epft) then Continue;

        epfd := ElementByName(epft, 'EPFD - Data');
        if not Assigned(epfd) then Continue;

        floatEl := ElementByName(epfd, 'Float');
        if not Assigned(floatEl) then Continue;

        oldVal := GetNativeValue(floatEl);
        if (oldVal > 19.9) and (oldVal < 20.1) then begin
          SetNativeValue(floatEl, 30.0);
          AddMessage('  GrimReaperSprint: AP reward ' + FloatToStr(oldVal) + ' -> 30.0');
          Inc(changeCount);
        end;
      end;
    end;
  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[PerkOverhaul] Phase 2b complete: ' + IntToStr(changeCount) + ' values changed');
end;

end.
