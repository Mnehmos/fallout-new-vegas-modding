{
  Mnehmos Collection — Add to Gun Runner Vendors
  Adds all Mnehmos weapons/armor to the appropriate Gun Runner store tiers.

  Run on: FalloutNV.esm + MnehmosMojave.esp (select FalloutNV.esm, Apply Script)

  Vendor tiers:
    Tier 1-2: Guns 0-25 items (early)
    Tier 3:   Guns 50 items (mid)
    Tier 4:   Guns 75 items (late)
    Tier 5:   Guns 100 items (endgame)
    Energy tiers: Energy weapons
}

unit MnehmosCollectionVendors;

var
  tp: IInterface;
  changeCount: Integer;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  changeCount := 0;

  tp := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'MnehmosMojave.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('[Vendors] ERROR: MnehmosMojave.esp not loaded. Aborting.');
    Result := 1;
    Exit;
  end;

  AddMessage('[Vendors] Adding Mnehmos Collection to Gun Runner stores...');
  AddMessage('');
end;

function FindMnehmosItem(edid: string): IInterface;
var
  i: Integer;
  rec: IInterface;
begin
  Result := nil;
  for i := 0 to Pred(RecordCount(tp)) do begin
    rec := RecordByIndex(tp, i);
    if SameText(EditorID(rec), edid) then begin
      Result := rec;
      Exit;
    end;
  end;
end;

procedure AddToVendorList(vendorList: IInterface; itemEdid: string; level: Integer);
var
  item, override, entries, newEntry, lvlo: IInterface;
begin
  item := FindMnehmosItem(itemEdid);
  if not Assigned(item) then begin
    AddMessage('  WARNING: Could not find ' + itemEdid + ' in MnehmosMojave.esp');
    Exit;
  end;

  // Copy vendor list as override
  AddRequiredElementMasters(vendorList, tp, False);
  AddRequiredElementMasters(item, tp, False);
  override := wbCopyElementToFile(vendorList, tp, False, True);
  if not Assigned(override) then begin
    AddMessage('  WARNING: Could not override ' + EditorID(vendorList));
    Exit;
  end;

  // Add new entry
  entries := ElementByName(override, 'Leveled List Entries');
  if not Assigned(entries) then Exit;

  newEntry := ElementAssign(entries, HighInteger, nil, False);
  if not Assigned(newEntry) then begin
    AddMessage('  WARNING: Could not add entry to ' + EditorID(vendorList));
    Exit;
  end;

  lvlo := ElementBySignature(newEntry, 'LVLO');
  if not Assigned(lvlo) then Exit;

  SetElementNativeValues(lvlo, 'Level', level);
  SetElementNativeValues(lvlo, 'Reference', FormID(item));
  SetElementNativeValues(lvlo, 'Count', 1);

  Inc(changeCount);
  AddMessage('  + ' + itemEdid + ' -> ' + EditorID(vendorList) + ' (lvl ' + IntToStr(level) + ')');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'LVLI' then Exit;
  if not SameText(GetFileName(GetFile(e)), 'FalloutNV.esm') then Exit;

  edid := EditorID(e);

  // ═══ GUNS TIER 1-2 (Early, Guns 0-25) ═══
  if SameText(edid, 'GunRunnerStoreTier1') then begin
    AddToVendorList(e, 'WeapGoodMemories', 1);     // 9mm pistol
    AddToVendorList(e, 'WeapBadMemories', 1);       // Caravan shotgun
    AddToVendorList(e, 'WeapFirstImpression', 1);   // .357 revolver
    AddToVendorList(e, 'WeapRambling', 1);           // 9mm SMG
    AddToVendorList(e, 'WeapFootnote', 1);           // Varmint rifle
    AddToVendorList(e, 'WeapDejaVu', 1);             // Knife
  end;

  // ═══ GUNS TIER 3 (Mid, Guns 50) ═══
  if SameText(edid, 'GunRunnerStoreTier3') then begin
    AddToVendorList(e, 'WeapPassingThought', 8);     // 10mm pistol
    AddToVendorList(e, 'WeapBurningQuestion', 8);    // .44 revolver
    AddToVendorList(e, 'WeapRecurringNightmare', 8); // 12.7mm SMG
    AddToVendorList(e, 'WeapCrossReference', 8);     // Trail Carbine
    AddToVendorList(e, 'WeapLoudReminder', 8);       // Lever shotgun
    AddToVendorList(e, 'WeapGrudge', 8);             // Super Sledge
    AddToVendorList(e, 'WeapMuscleMemory', 8);       // Power Fist
  end;

  // ═══ GUNS TIER 4 (Late, Guns 75) ═══
  if SameText(edid, 'GunRunnerStoreTier4') then begin
    AddToVendorList(e, 'WeapFinalDraft', 15);        // 12.7mm pistol
    AddToVendorList(e, 'WeapHindsight', 15);         // Hunting Revolver
    AddToVendorList(e, 'WeapLongMemory', 15);        // Service Rifle
    AddToVendorList(e, 'WeapLastWord', 15);          // Hunting Shotgun
    AddToVendorList(e, 'WeapClosure', 15);           // Oh Baby clone
    AddToVendorList(e, 'WeapIntrusiveThought', 15);  // Grenade Rifle
  end;

  // ═══ GUNS TIER 5 (Endgame, Guns 100) ═══
  if SameText(edid, 'GunRunnerStoreTier5') then begin
    AddToVendorList(e, 'WeapThesisStatement', 20);   // Anti-Mat Rifle
    AddToVendorList(e, 'WeapBuriedMemory', 20);      // Grenade MG
  end;

  // ═══ ENERGY TIER 1-2 (Early) ═══
  if SameText(edid, 'GunRunnerStoreEnergyTier1') then begin
    AddToVendorList(e, 'WeapAfterglow', 1);          // Laser Pistol
  end;

  // ═══ ENERGY TIER 3 (Mid) ═══
  if SameText(edid, 'GunRunnerStoreEnergyTier3') then begin
    AddToVendorList(e, 'WeapPhantomLimb', 8);        // Plasma Defender
    AddToVendorList(e, 'WeapBrightIdea', 8);         // Laser Rifle
  end;

  // ═══ ENERGY TIER 4 (Late) ═══
  if SameText(edid, 'GunRunnerStoreEnergyTier4') then begin
    AddToVendorList(e, 'WeapOverexposure', 15);      // Plasma Rifle
  end;

  // ═══ ENERGY TIER 5 (Endgame) ═══
  if SameText(edid, 'GunRunnerStoreEnergyTier5') then begin
    AddToVendorList(e, 'WeapPeerReview', 20);        // Gauss Rifle
  end;

  // ═══ ARMOR — add to main Gun Runner store ═══
  if SameText(edid, 'GunRunnerHQStoreGuns') then begin
    AddToVendorList(e, 'ArmorArchivistDuster', 1);
    AddToVendorList(e, 'HatMnehmos', 1);
    AddToVendorList(e, 'GlassesRecollection', 1);
    AddToVendorList(e, 'ArmorArchivistJacket', 8);
    AddToVendorList(e, 'ArmorArchivistCombat', 15);
    AddToVendorList(e, 'ArmorArchivistPower', 20);
  end;

end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('[Vendors] Done: ' + IntToStr(changeCount) + ' items added to vendor lists');
  AddMessage('[Vendors] Save the ESP to apply.');
end;

end.
