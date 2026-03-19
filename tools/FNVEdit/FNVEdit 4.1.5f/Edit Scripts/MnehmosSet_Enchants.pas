{
  Mnehmos Set — Custom Enchantments
  Creates 3 ENCH records by cloning existing enchants and modifying effects.
  Then assigns them to the Mnehmos armor items.

  Run on: FalloutNV.esm + MnehmosMojave.esp (select all, Apply Script)

  Creates:
    EnchMnehmosDuster  — +1 PER, +1 INT (clone Duster enchant, change effects)
    EnchMnehmosHat     — +1 PER (clone Cowboy Hat enchant, keep as-is)
    EnchMnehmosLenses  — +1 INT, +1 CHR (clone Duster enchant, change effects)
}

unit MnehmosSetEnchants;

var
  targetPlugin: IInterface;
  enchDuster, enchHat, enchLenses: IInterface;
  changeCount: Integer;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  changeCount := 0;

  targetPlugin := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'MnehmosMojave.esp') then begin
      targetPlugin := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(targetPlugin) then begin
    AddMessage('[MnehmosEnchants] ERROR: MnehmosMojave.esp not loaded. Aborting.');
    Result := 1;
    Exit;
  end;

  AddMessage('[MnehmosEnchants] Creating custom enchantments...');
  AddMessage('[MnehmosEnchants] Target: ' + GetFileName(targetPlugin));
  AddMessage('');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  fid: Cardinal;
  newEnch, effects, effect, efid, efit: IInterface;
begin
  Result := 0;
  sig := Signature(e);

  // Only process base game records for cloning
  if not SameText(GetFileName(GetFile(e)), 'FalloutNV.esm') then begin

    // But also process MnehmosMojave.esp ARMO records to assign enchants
    if SameText(GetFileName(GetFile(e)), 'MnehmosMojave.esp') then begin
      if sig = 'ARMO' then begin
        edid := EditorID(e);

        // Assign duster enchant
        if SameText(edid, 'ArmorArchivistDuster') and Assigned(enchDuster) then begin
          SetElementEditValues(e, 'EITM', Name(enchDuster));
          AddMessage('  Assigned EnchMnehmosDuster to The Archivist''s Duster');
          Inc(changeCount);
        end;

        // Assign hat enchant
        if SameText(edid, 'HatMnehmos') and Assigned(enchHat) then begin
          SetElementEditValues(e, 'EITM', Name(enchHat));
          AddMessage('  Assigned EnchMnehmosHat to Mnehmos Hat');
          Inc(changeCount);
        end;

        // Assign glasses enchant
        if SameText(edid, 'GlassesRecollection') and Assigned(enchLenses) then begin
          SetElementEditValues(e, 'EITM', Name(enchLenses));
          AddMessage('  Assigned EnchMnehmosLenses to Recollection Lenses');
          Inc(changeCount);
        end;
      end;
    end;

    Exit;
  end;

  if sig <> 'ENCH' then Exit;
  fid := FixedFormID(e);

  // ═══════════════════════════════════════════════════
  //  DUSTER ENCHANT — clone Duster enchant, make +1 PER +1 INT
  //  Base: EnchClothingDuster [ENCH:0008B608] (+5 Guns, +1 CHR)
  // ═══════════════════════════════════════════════════
  if fid = $0008B608 then begin
    if Assigned(enchDuster) then Exit; // already created

    AddRequiredElementMasters(e, targetPlugin, False);
    newEnch := wbCopyElementToFile(e, targetPlugin, True, True);
    if not Assigned(newEnch) then begin
      AddMessage('  ERROR: Failed to copy duster enchant');
      Exit;
    end;

    SetElementEditValues(newEnch, 'EDID', 'EnchMnehmosDuster');
    SetElementEditValues(newEnch, 'FULL', 'Archivist''s Focus');

    // Effect[0]: Change from +5 Guns to +1 PER
    effects := ElementByName(newEnch, 'Effects');
    if Assigned(effects) and (ElementCount(effects) > 0) then begin
      effect := ElementByIndex(effects, 0);
      // EFID points to IncreasePerception MGEF
      SetElementEditValues(effect, 'EFID', 'IncreasePerception "Increased Perception" [MGEF:0001515D]');
      efit := ElementBySignature(effect, 'EFIT');
      if Assigned(efit) then begin
        SetElementEditValues(efit, 'Magnitude', '1');
        SetElementEditValues(efit, 'Actor Value', 'Perception');
      end;
    end;

    // Effect[1]: Change from +1 CHR to +1 INT
    if Assigned(effects) and (ElementCount(effects) > 1) then begin
      effect := ElementByIndex(effects, 1);
      SetElementEditValues(effect, 'EFID', 'IncreaseIntelligence "Increased Intelligence" [MGEF:0001515E]');
      efit := ElementBySignature(effect, 'EFIT');
      if Assigned(efit) then begin
        SetElementEditValues(efit, 'Magnitude', '1');
        SetElementEditValues(efit, 'Actor Value', 'Intelligence');
      end;
    end;

    enchDuster := newEnch;
    AddMessage('  Created EnchMnehmosDuster (+1 PER, +1 INT) — FormID: ' + IntToHex(FormID(newEnch), 8));
    Inc(changeCount);
  end;

  // ═══════════════════════════════════════════════════
  //  HAT ENCHANT — clone Cowboy Hat enchant (+1 PER), keep as-is
  //  Base: EnchClothingHeadSunGuard [ENCH:00071B88] (+1 PER)
  // ═══════════════════════════════════════════════════
  if fid = $00071B88 then begin
    if Assigned(enchHat) then Exit;

    AddRequiredElementMasters(e, targetPlugin, False);
    newEnch := wbCopyElementToFile(e, targetPlugin, True, True);
    if not Assigned(newEnch) then begin
      AddMessage('  ERROR: Failed to copy hat enchant');
      Exit;
    end;

    SetElementEditValues(newEnch, 'EDID', 'EnchMnehmosHat');
    SetElementEditValues(newEnch, 'FULL', 'Archivist''s Vigil');

    // Already +1 PER — perfect, just rename it
    enchHat := newEnch;
    AddMessage('  Created EnchMnehmosHat (+1 PER) — FormID: ' + IntToHex(FormID(newEnch), 8));
    Inc(changeCount);
  end;

  // ═══════════════════════════════════════════════════
  //  GLASSES ENCHANT — clone Duster enchant, make +1 INT +1 CHR
  //  Base: EnchClothingDuster [ENCH:0008B608] (+5 Guns, +1 CHR)
  // ═══════════════════════════════════════════════════
  if (fid = $0008B608) and not Assigned(enchLenses) then begin
    // This won't fire because we already handled this fid above.
    // We need a different approach — clone the glasses enchant instead.
  end;
end;

function Finalize: Integer;
var
  newEnch, effects, effect, efit: IInterface;
  glassesEnch: IInterface;
  i: Integer;
begin
  Result := 0;

  // Create glasses enchant by cloning the duster enchant we already made
  if Assigned(enchDuster) and not Assigned(enchLenses) then begin
    enchLenses := wbCopyElementToFile(enchDuster, targetPlugin, True, True);
    if Assigned(enchLenses) then begin
      SetElementEditValues(enchLenses, 'EDID', 'EnchMnehmosLenses');
      SetElementEditValues(enchLenses, 'FULL', 'Archivist''s Clarity');

      effects := ElementByName(enchLenses, 'Effects');
      if Assigned(effects) then begin
        // Effect[0]: +1 INT
        if ElementCount(effects) > 0 then begin
          effect := ElementByIndex(effects, 0);
          SetElementEditValues(effect, 'EFID', 'IncreaseIntelligence "Increased Intelligence" [MGEF:0001515E]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Intelligence');
          end;
        end;

        // Effect[1]: +1 CHR
        if ElementCount(effects) > 1 then begin
          effect := ElementByIndex(effects, 1);
          SetElementEditValues(effect, 'EFID', 'IncreaseCharisma "Increased Charisma" [MGEF:0001515F]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Charisma');
          end;
        end;
      end;

      AddMessage('  Created EnchMnehmosLenses (+1 INT, +1 CHR) — FormID: ' + IntToHex(FormID(enchLenses), 8));
      Inc(changeCount);
    end;
  end;

  // Now assign enchants to armor — scan MnehmosMojave.esp records
  // The Process() function handles this when it encounters ARMO records
  // But since enchants were created during Process, the ARMO records
  // may have already been processed before the enchants existed.
  // So we need to do assignment here in Finalize.

  if Assigned(targetPlugin) then begin
    for i := 0 to Pred(RecordCount(targetPlugin)) do begin
      effect := RecordByIndex(targetPlugin, i);
      if Signature(effect) = 'ARMO' then begin
        if SameText(EditorID(effect), 'ArmorArchivistDuster') and Assigned(enchDuster) then begin
          SetElementNativeValues(effect, 'EITM', FormID(enchDuster));
          AddMessage('  Linked Archivist''s Duster -> EnchMnehmosDuster');
          Inc(changeCount);
        end;
        if SameText(EditorID(effect), 'HatMnehmos') and Assigned(enchHat) then begin
          SetElementNativeValues(effect, 'EITM', FormID(enchHat));
          AddMessage('  Linked Mnehmos Hat -> EnchMnehmosHat');
          Inc(changeCount);
        end;
        if SameText(EditorID(effect), 'GlassesRecollection') and Assigned(enchLenses) then begin
          SetElementNativeValues(effect, 'EITM', FormID(enchLenses));
          AddMessage('  Linked Recollection Lenses -> EnchMnehmosLenses');
          Inc(changeCount);
        end;
      end;
    end;
  end;

  AddMessage('');
  AddMessage('[MnehmosEnchants] Done: ' + IntToStr(changeCount) + ' changes made');
  AddMessage('[MnehmosEnchants] Save the ESP to apply.');
end;

end.
