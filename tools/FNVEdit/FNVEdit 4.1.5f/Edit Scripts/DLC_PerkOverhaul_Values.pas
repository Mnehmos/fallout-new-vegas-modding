{
  DLC Perk Overhaul — Phase 2: Actual Effect Value Changes

  Changes EPFD float values on DLC perk effects.
  Run on PerkOverhaul.esp PERK records (select all PERKs, Apply Script).

  Uses same GetEffectFloat/SetEffectFloat pattern as base game value script.
}

unit DLCPerkOverhaulValues;

var
  changeCount: Integer;

function Initialize: Integer;
begin
  Result := 0;
  changeCount := 0;
  AddMessage('[DLC Values] Phase 2: Modifying effect values...');
end;

function GetEffectFloat(effect: IInterface): Double;
var
  epft, epfd, floatEl: IInterface;
begin
  Result := -9999.0;
  epft := ElementBySignature(effect, 'EPFT');
  if not Assigned(epft) then Exit;
  epfd := ElementByName(epft, 'EPFD - Data');
  if not Assigned(epfd) then Exit;
  floatEl := ElementByName(epfd, 'Float');
  if Assigned(floatEl) then
    Result := GetNativeValue(floatEl)
  else
    Result := GetNativeValue(epfd);
end;

procedure SetEffectFloat(effect: IInterface; newValue: Double);
var
  epft, epfd, floatEl: IInterface;
begin
  epft := ElementBySignature(effect, 'EPFT');
  if not Assigned(epft) then Exit;
  epfd := ElementByName(epft, 'EPFD - Data');
  if not Assigned(epfd) then Exit;
  floatEl := ElementByName(epfd, 'Float');
  if Assigned(floatEl) then
    SetNativeValue(floatEl, newValue)
  else
    SetNativeValue(epfd, newValue);
end;

procedure TryChange(effect: IInterface; edid: string; oldMin, oldMax, newVal: Double; desc: string);
var
  curVal: Double;
begin
  curVal := GetEffectFloat(effect);
  if (curVal > oldMin) and (curVal < oldMax) then begin
    SetEffectFloat(effect, newVal);
    AddMessage('  ' + edid + ': ' + desc + ' ' + FloatToStr(curVal) + ' -> ' + FloatToStr(newVal));
    Inc(changeCount);
  end;
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  effects, effect: IInterface;
  i, count: Integer;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'PERK' then Exit;

  edid := EditorID(e);
  effects := ElementByName(e, 'Effects');
  if not Assigned(effects) then Exit;
  count := ElementCount(effects);

  for i := 0 to Pred(count) do begin
    effect := ElementByIndex(effects, i);

    // ═══ DEAD MONEY ═══

    // Hobbler: 1.25 -> 1.40 (leg VATS accuracy)
    if SameText(edid, 'NVDLC01Hobbler') then
      TryChange(effect, edid, 1.24, 1.26, 1.40, 'leg VATS');

    // And Stay Back: 0.10 -> 0.20 (knockback chance)
    if SameText(edid, 'NVDLC01AndStayBack') then
      TryChange(effect, edid, 0.09, 0.11, 0.20, 'knockback');

    // Old World Gourmet: 0.75 -> 0.50 (food healing, lower = more bonus)
    if SameText(edid, 'NVDLC01OldWorldGourmet') then
      TryChange(effect, edid, 0.74, 0.76, 0.50, 'food heal');

    // In Shining Armor: 5 -> 8 (DT bonus)
    if SameText(edid, 'NVDLC01InShiningArmor') then
      TryChange(effect, edid, 4.9, 5.1, 8.0, 'DT bonus');

    // Light Touch: 5 -> 8 (crit bonus)
    if SameText(edid, 'NVDLC01LightTouch') then begin
      TryChange(effect, edid, 4.9, 5.1, 8.0, 'crit bonus');
      TryChange(effect, edid, -26.0, -24.0, -15.0, 'DT penalty');
    end;

    // ═══ HONEST HEARTS ═══

    // Sneering Imperialist: 1.15 -> 1.25 (damage mult)
    if SameText(edid, 'NVDLC02SneeringImperialist') then
      TryChange(effect, edid, 1.14, 1.16, 1.25, 'DMG mult');

    // Grunt: 1.25 -> 1.35 (damage mult)
    if SameText(edid, 'NVDLC02Grunt') then
      TryChange(effect, edid, 1.24, 1.26, 1.35, 'DMG mult');

    // Eye for Eye: 1.10 -> 1.15 per limb (5 effects)
    if SameText(edid, 'NVDLC02EyeForEye') then
      TryChange(effect, edid, 1.09, 1.11, 1.15, 'per-limb DMG');

    // ═══ OLD WORLD BLUES ═══

    // Atomic! speed: 1.50 -> 1.75
    if SameText(edid, 'NVDLC03AtomicPerk') then begin
      TryChange(effect, edid, 1.49, 1.51, 1.75, 'speed mult');
      TryChange(effect, edid, 1.32, 1.34, 1.50, 'DT mult');
      TryChange(effect, edid, 1.19, 1.21, 1.30, 'regen mult');
    end;

    // Hot Blooded: 1.15 -> 1.25 (damage below 50% HP)
    if SameText(edid, 'NVDLC03TraitHotBlooded') then
      TryChange(effect, edid, 1.14, 1.16, 1.25, 'low-HP DMG');

    // ═══ LONESOME ROAD ═══

    // Tunnel Runner: 1.25 -> 1.40 (sneak speed)
    if SameText(edid, 'NVDLC04TunnelRunnerPerk') then
      TryChange(effect, edid, 1.24, 1.26, 1.40, 'sneak speed');

    // Lessons Learned: scale all 26 entries up by ~1.3x
    if SameText(edid, 'NVDLC04LessonsLearnedPerk') then begin
      TryChange(effect, edid, 1.24, 1.26, 1.50, 'XP L1');
      TryChange(effect, edid, 1.25, 1.27, 1.52, 'XP L2');
      TryChange(effect, edid, 1.26, 1.28, 1.54, 'XP L3');
      TryChange(effect, edid, 1.27, 1.29, 1.56, 'XP L4');
      TryChange(effect, edid, 1.28, 1.30, 1.58, 'XP L5');
      TryChange(effect, edid, 1.29, 1.31, 1.60, 'XP L6');
      TryChange(effect, edid, 1.30, 1.32, 1.62, 'XP L7');
      TryChange(effect, edid, 1.31, 1.33, 1.64, 'XP L8');
      TryChange(effect, edid, 1.32, 1.34, 1.66, 'XP L9');
      TryChange(effect, edid, 1.33, 1.35, 1.68, 'XP L10');
      TryChange(effect, edid, 1.34, 1.36, 1.70, 'XP L11');
      TryChange(effect, edid, 1.35, 1.37, 1.72, 'XP L12');
      TryChange(effect, edid, 1.36, 1.38, 1.74, 'XP L13');
      TryChange(effect, edid, 1.37, 1.39, 1.76, 'XP L14');
      TryChange(effect, edid, 1.38, 1.40, 1.78, 'XP L15');
      TryChange(effect, edid, 1.39, 1.41, 1.80, 'XP L16');
      TryChange(effect, edid, 1.40, 1.42, 1.82, 'XP L17');
      TryChange(effect, edid, 1.41, 1.43, 1.84, 'XP L18');
      TryChange(effect, edid, 1.42, 1.44, 1.86, 'XP L19');
      TryChange(effect, edid, 1.43, 1.45, 1.88, 'XP L20');
      TryChange(effect, edid, 1.44, 1.46, 1.90, 'XP L21');
      TryChange(effect, edid, 1.45, 1.47, 1.92, 'XP L22');
      TryChange(effect, edid, 1.46, 1.48, 1.94, 'XP L23');
      TryChange(effect, edid, 1.47, 1.49, 1.96, 'XP L24');
      TryChange(effect, edid, 1.48, 1.50, 1.98, 'XP L25');
      TryChange(effect, edid, 1.49, 1.51, 2.00, 'XP L26');
    end;

    // Certified Tech: 0.25 -> 0.50 (robot DMG bonus)
    if SameText(edid, 'NVDLC04CertifiedTechPerk') then
      TryChange(effect, edid, 0.24, 0.26, 0.50, 'robot DMG');

    // Thought You Died: 1.10 -> 1.25 (karma DMG scaling)
    if SameText(edid, 'NVDLC04ThoughtYouForDeadPerk') then
      TryChange(effect, edid, 1.09, 1.11, 1.25, 'karma DMG');

    // Ain't Like That Now: 1.25 -> 1.40 (crit bonus)
    if SameText(edid, 'NVDLC04AintLikeThatNowPerk') then
      TryChange(effect, edid, 1.24, 1.26, 1.40, 'crit bonus');

    // Just Lucky I'm Alive: 1.50 -> 2.00 (crit after near-death)
    if SameText(edid, 'NVDLC04JustLuckyImAlivePerk') then
      TryChange(effect, edid, 1.49, 1.51, 2.00, 'near-death crit');

  end;
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[DLC Values] Phase 2 complete: ' + IntToStr(changeCount) + ' values changed');
end;

end.
