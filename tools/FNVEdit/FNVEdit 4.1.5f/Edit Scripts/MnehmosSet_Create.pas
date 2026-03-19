{
  Mnehmos Set — The Archivist's Kit
  Creates 6 unique items by cloning base game records.

  Run on: FalloutNV.esm (select all records, Apply Script)
  Target: MnehmosMojave.esp

  Items created:
    WeapBadMemories      - Caravan Shotgun clone (Guns 25)
    WeapGoodMemories     - 9mm Pistol clone (Guns 25)
    ArmorArchivistDuster - Bounty Hunter Duster clone (+1 PER, +1 INT)
    HatMnehmos           - Desperado Cowboy Hat clone (+1 PER)
    GlassesRecollection  - Authority Glasses clone (+1 INT, +1 CHR)
    WeapDejaVu           - Chance's Knife clone (fast, high crit)
}

unit MnehmosSetCreate;

var
  targetPlugin: IInterface;
  itemCount: Integer;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  itemCount := 0;

  targetPlugin := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'MnehmosMojave.esp') then begin
      targetPlugin := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(targetPlugin) then begin
    targetPlugin := AddNewFile;
    if not Assigned(targetPlugin) then begin
      AddMessage('[MnehmosSet] ERROR: No target plugin. Aborting.');
      Result := 1;
      Exit;
    end;
  end;

  AddMessage('[MnehmosSet] Creating The Archivist''s Kit...');
  AddMessage('[MnehmosSet] Target: ' + GetFileName(targetPlugin));
  AddMessage('');
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
  newRec: IInterface;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);

  // Only process from base game
  if not SameText(GetFileName(GetFile(e)), 'FalloutNV.esm') then Exit;

  // ═══════════════════════════════════════════════════
  //  BAD MEMORIES — Caravan Shotgun (Guns 25)
  // ═══════════════════════════════════════════════════
  if (sig = 'WEAP') and SameText(edid, 'WeapNVCaravanShotgun') then begin
    AddRequiredElementMasters(e, targetPlugin, False);
    newRec := wbCopyElementToFile(e, targetPlugin, True, True);
    if not Assigned(newRec) then begin
      AddMessage('  ERROR: Failed to copy ' + edid);
      Exit;
    end;

    SetElementEditValues(newRec, 'EDID', 'WeapBadMemories');
    SetElementEditValues(newRec, 'FULL', 'Bad Memories');
    SetElementEditValues(newRec, 'DESC', 'Each shell is a grudge. Each pump is a promise. The stock is scarred with tally marks — one for every lesson taught at close range. Part of the Mnehmos Archivist''s Kit. Mnemosyne remembers.');

    SetElementEditValues(newRec, 'DNAM\Value', '3500');
    SetElementEditValues(newRec, 'DNAM\Weight', '5.0');
    SetElementEditValues(newRec, 'DNAM\Damage', '70');
    SetElementEditValues(newRec, 'DNAM\Clip Size', '4');
    SetElementEditValues(newRec, 'DNAM\Action Point Cost', '26');
    SetElementEditValues(newRec, 'DNAM\Min Spread', '1.8');
    SetElementEditValues(newRec, 'DNAM\Health', '150');
    SetElementEditValues(newRec, 'DNAM\Skill', '25');

    SetElementEditValues(newRec, 'CRDT\Damage', '70');
    SetElementEditValues(newRec, 'CRDT\% Mult', '1.5');

    Inc(itemCount);
    AddMessage('  [1/6] Bad Memories (Shotgun) — FormID: ' + IntToHex(FormID(newRec), 8));
    AddMessage('         DMG:70 Crit:70 x1.5 Mag:4 AP:26 Spread:1.8 Guns:25');
  end;

  // ═══════════════════════════════════════════════════
  //  GOOD MEMORIES — 9mm Pistol (Guns 25)
  // ═══════════════════════════════════════════════════
  if (sig = 'WEAP') and SameText(edid, 'WeapNV9mmPistol') then begin
    AddRequiredElementMasters(e, targetPlugin, False);
    newRec := wbCopyElementToFile(e, targetPlugin, True, True);
    if not Assigned(newRec) then begin
      AddMessage('  ERROR: Failed to copy ' + edid);
      Exit;
    end;

    SetElementEditValues(newRec, 'EDID', 'WeapGoodMemories');
    SetElementEditValues(newRec, 'FULL', 'Good Memories');
    SetElementEditValues(newRec, 'DESC', 'Light in the hand. Steady in the dark. Some things you never forget how to do. The grip is worn smooth from years of muscle memory. Part of the Mnehmos Archivist''s Kit. Mnemosyne remembers.');

    SetElementEditValues(newRec, 'DNAM\Value', '3000');
    SetElementEditValues(newRec, 'DNAM\Weight', '1.2');
    SetElementEditValues(newRec, 'DNAM\Damage', '28');
    SetElementEditValues(newRec, 'DNAM\Clip Size', '17');
    SetElementEditValues(newRec, 'DNAM\Action Point Cost', '15');
    SetElementEditValues(newRec, 'DNAM\Min Spread', '0.8');
    SetElementEditValues(newRec, 'DNAM\Fire Rate', '7.0');
    SetElementEditValues(newRec, 'DNAM\Health', '175');
    SetElementEditValues(newRec, 'DNAM\Skill', '25');

    SetElementEditValues(newRec, 'CRDT\Damage', '34');
    SetElementEditValues(newRec, 'CRDT\% Mult', '2.0');

    Inc(itemCount);
    AddMessage('  [2/6] Good Memories (9mm Pistol) — FormID: ' + IntToHex(FormID(newRec), 8));
    AddMessage('         DMG:28 Crit:34 x2.0 Mag:17 AP:15 Rate:7.0 Guns:25');
  end;

  // ═══════════════════════════════════════════════════
  //  DEJA VU — Chance's Knife clone
  // ═══════════════════════════════════════════════════
  if (sig = 'WEAP') and SameText(edid, 'WeapNVKnifeCombatUnique') then begin
    AddRequiredElementMasters(e, targetPlugin, False);
    newRec := wbCopyElementToFile(e, targetPlugin, True, True);
    if not Assigned(newRec) then begin
      AddMessage('  ERROR: Failed to copy ' + edid);
      Exit;
    end;

    SetElementEditValues(newRec, 'EDID', 'WeapDejaVu');
    SetElementEditValues(newRec, 'FULL', 'D' + #233 + 'j' + #224 + ' Vu');
    SetElementEditValues(newRec, 'DESC', 'You''ve been here before. You''ve done this before. Your hand knows what to do. The blade moves faster than thought — it remembers the motion even when you don''t. Part of the Mnehmos Archivist''s Kit. Mnemosyne remembers.');

    SetElementEditValues(newRec, 'DNAM\Value', '5000');
    SetElementEditValues(newRec, 'DNAM\Damage', '28');
    SetElementEditValues(newRec, 'DNAM\Action Point Cost', '14');
    SetElementEditValues(newRec, 'DNAM\Health', '200');
    SetElementEditValues(newRec, 'DNAM\Speed', '1.3');

    SetElementEditValues(newRec, 'CRDT\Damage', '42');
    SetElementEditValues(newRec, 'CRDT\% Mult', '2.0');

    Inc(itemCount);
    AddMessage('  [3/6] Deja Vu (Knife) — FormID: ' + IntToHex(FormID(newRec), 8));
    AddMessage('         DMG:28 Crit:42 x2.0 AP:14 Speed:1.3');
  end;

  // ═══════════════════════════════════════════════════
  //  THE ARCHIVIST'S DUSTER — Bounty Hunter Duster clone
  // ═══════════════════════════════════════════════════
  if (sig = 'ARMO') and SameText(edid, 'BountyHunterDuster') then begin
    AddRequiredElementMasters(e, targetPlugin, False);
    newRec := wbCopyElementToFile(e, targetPlugin, True, True);
    if not Assigned(newRec) then begin
      AddMessage('  ERROR: Failed to copy ' + edid);
      Exit;
    end;

    SetElementEditValues(newRec, 'EDID', 'ArmorArchivistDuster');
    SetElementEditValues(newRec, 'FULL', 'The Archivist''s Duster');
    SetElementEditValues(newRec, 'DESC', 'Shells line the inside like chapters in a book. Every pocket holds a memory. Every scratch tells a story. The leather is worn soft but the stitching holds. It''s outlasted everything else. Part of the Mnehmos Archivist''s Kit. Mnemosyne remembers.');

    SetElementEditValues(newRec, 'DATA\Value', '5000');
    SetElementEditValues(newRec, 'DATA\Weight', '3.5');
    SetElementEditValues(newRec, 'DNAM', '11');

    Inc(itemCount);
    AddMessage('  [4/6] The Archivist''s Duster — FormID: ' + IntToHex(FormID(newRec), 8));
    AddMessage('         DT:11 Wt:3.5 Val:5000');
  end;

  // ═══════════════════════════════════════════════════
  //  MNEHMOS HAT — Desperado Cowboy Hat clone
  // ═══════════════════════════════════════════════════
  if (sig = 'ARMO') and SameText(edid, 'CowboyHat01') then begin
    AddRequiredElementMasters(e, targetPlugin, False);
    newRec := wbCopyElementToFile(e, targetPlugin, True, True);
    if not Assigned(newRec) then begin
      AddMessage('  ERROR: Failed to copy ' + edid);
      Exit;
    end;

    SetElementEditValues(newRec, 'EDID', 'HatMnehmos');
    SetElementEditValues(newRec, 'FULL', 'Mnehmos Hat');
    SetElementEditValues(newRec, 'DESC', 'Wide brim, low profile. The Archivist doesn''t need to be recognized — just remembered. The hat has seen more sunsets than most people have seen days. Part of the Mnehmos Archivist''s Kit. Mnemosyne remembers.');

    SetElementEditValues(newRec, 'DATA\Value', '2000');
    SetElementEditValues(newRec, 'DNAM', '2');

    Inc(itemCount);
    AddMessage('  [5/6] Mnehmos Hat — FormID: ' + IntToHex(FormID(newRec), 8));
    AddMessage('         DT:2 Val:2000');
  end;

  // ═══════════════════════════════════════════════════
  //  RECOLLECTION LENSES — Authority Glasses clone
  // ═══════════════════════════════════════════════════
  if (sig = 'ARMO') and SameText(edid, 'GlassesNCRRangerCivilian') then begin
    AddRequiredElementMasters(e, targetPlugin, False);
    newRec := wbCopyElementToFile(e, targetPlugin, True, True);
    if not Assigned(newRec) then begin
      AddMessage('  ERROR: Failed to copy ' + edid);
      Exit;
    end;

    SetElementEditValues(newRec, 'EDID', 'GlassesRecollection');
    SetElementEditValues(newRec, 'FULL', 'Recollection Lenses');
    SetElementEditValues(newRec, 'DESC', 'Pre-War optics, hand-ground by someone who understood precision. Everything looks clearer through the lens of experience. The world sharpens. Details emerge. Nothing escapes notice. Part of the Mnehmos Archivist''s Kit. Mnemosyne remembers.');

    SetElementEditValues(newRec, 'DATA\Value', '2500');

    Inc(itemCount);
    AddMessage('  [6/6] Recollection Lenses — FormID: ' + IntToHex(FormID(newRec), 8));
    AddMessage('         Val:2500');
  end;

end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  if itemCount = 6 then
    AddMessage('[MnehmosSet] All 6 items created successfully!')
  else
    AddMessage('[MnehmosSet] WARNING: Only ' + IntToStr(itemCount) + '/6 items created. Check errors above.');
  AddMessage('');
  AddMessage('[MnehmosSet] Save the ESP, then in-game:');
  AddMessage('  help "Bad Memories" 4');
  AddMessage('  help "Good Memories" 4');
  AddMessage('  help "Deja Vu" 4');
  AddMessage('  help "Archivist" 4');
  AddMessage('  help "Mnehmos" 4');
  AddMessage('  help "Recollection" 4');
  AddMessage('  player.additem [FormID] 1');
end;

end.
