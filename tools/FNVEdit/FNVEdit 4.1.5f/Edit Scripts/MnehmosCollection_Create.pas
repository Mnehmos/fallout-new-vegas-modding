{
  THE MNEHMOS COLLECTION — Complete Arsenal
  30 unique items across all weapon/armor categories and skill tiers.

  Run on: FalloutNV.esm (select all records, Apply Script)
  Target: MnehmosMojave.esp (will be created fresh)

  MGEF Reference:
    STR: 0001515C  PER: 0001515D  END: 0001515E  CHR: 0001515F
    INT: 00015160  AGL: 00015161  LCK: 00015162
    CritChance: 0006AA5D  CarryWeight: 00031023  DT: 001630EF
}

unit MnehmosCollectionCreate;

var
  tp: IInterface;
  itemCount: Integer;
  // Store armor refs for enchant linking in Finalize
  armDuster, armJacket, armCombat, armPower, armHat, armGlasses: IInterface;
  // Store enchant base for cloning
  enchBase2, enchBase1: IInterface;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;
  itemCount := 0;

  tp := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'MnehmosMojave.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    tp := AddNewFile;
    if not Assigned(tp) then begin
      AddMessage('[Mnehmos] ERROR: No target plugin. Aborting.');
      Result := 1;
      Exit;
    end;
  end;

  AddMessage('=== THE MNEHMOS COLLECTION ===');
  AddMessage('Target: ' + GetFileName(tp));
  AddMessage('');
end;

// ─── WEAPON HELPER ──────────────────────────────────────────
procedure MakeWeapon(e: IInterface; newEdid, newName, newDesc: string;
  dmg, critDmg, clipSize, health, value: Integer;
  critMult, ap, spread, fireRate, weight: Double;
  skillReq: Integer; atkMult: Double);
var
  w: IInterface;
begin
  AddRequiredElementMasters(e, tp, False);
  w := wbCopyElementToFile(e, tp, True, True);
  if not Assigned(w) then begin
    AddMessage('  ERROR: Failed to copy ' + EditorID(e));
    Exit;
  end;

  SetElementEditValues(w, 'EDID', newEdid);
  SetElementEditValues(w, 'FULL', newName);
  if newDesc <> '' then
    SetElementEditValues(w, 'DESC', newDesc);

  // DATA block
  if dmg > 0 then SetElementEditValues(w, 'DATA\Base Damage', IntToStr(dmg));
  if clipSize > 0 then SetElementEditValues(w, 'DATA\Clip Size', IntToStr(clipSize));
  if health > 0 then SetElementEditValues(w, 'DATA\Health', IntToStr(health));
  if value > 0 then SetElementEditValues(w, 'DATA\Value', IntToStr(value));
  if weight > 0.0 then SetElementEditValues(w, 'DATA\Weight', FloatToStr(weight));

  // DNAM block
  if ap > 0.0 then SetElementEditValues(w, 'DNAM\Override - Action Points', FloatToStr(ap));
  if spread >= 0.0 then SetElementEditValues(w, 'DNAM\Min Spread', FloatToStr(spread));
  if fireRate > 0.0 then SetElementEditValues(w, 'DNAM\Fire Rate', FloatToStr(fireRate));
  if skillReq >= 0 then SetElementEditValues(w, 'DNAM\Skill Req', IntToStr(skillReq));
  if atkMult > 0.0 then SetElementEditValues(w, 'DNAM\Animation Attack Multiplier', FloatToStr(atkMult));

  // CRDT block
  if critDmg > 0 then SetElementEditValues(w, 'CRDT\Critical Damage', IntToStr(critDmg));
  if critMult > 0.0 then SetElementEditValues(w, 'CRDT\Crit % Mult', FloatToStr(critMult));

  Inc(itemCount);
  AddMessage('  [' + IntToStr(itemCount) + '] ' + newName + ' (' + IntToStr(dmg) + ' DMG, x' + FloatToStr(critMult) + ' crit) FormID: ' + IntToHex(FormID(w), 8));
end;

// ─── ARMOR HELPER ───────────────────────────────────────────
function MakeArmor(e: IInterface; newEdid, newName, newDesc: string;
  dt: Double; health, value: Integer; weight: Double): IInterface;
var
  a: IInterface;
begin
  Result := nil;
  AddRequiredElementMasters(e, tp, False);
  a := wbCopyElementToFile(e, tp, True, True);
  if not Assigned(a) then begin
    AddMessage('  ERROR: Failed to copy ' + EditorID(e));
    Exit;
  end;

  SetElementEditValues(a, 'EDID', newEdid);
  SetElementEditValues(a, 'FULL', newName);
  if newDesc <> '' then
    SetElementEditValues(a, 'DESC', newDesc);

  if value > 0 then SetElementEditValues(a, 'DATA\Value', IntToStr(value));
  if health > 0 then SetElementEditValues(a, 'DATA\Health', IntToStr(health));
  if weight > 0.0 then SetElementEditValues(a, 'DATA\Weight', FloatToStr(weight));
  if dt >= 0.0 then SetElementEditValues(a, 'DNAM\DT', FloatToStr(dt));

  Inc(itemCount);
  AddMessage('  [' + IntToStr(itemCount) + '] ' + newName + ' (DT:' + FloatToStr(dt) + ') FormID: ' + IntToHex(FormID(a), 8));
  Result := a;
end;

function Process(e: IInterface): Integer;
var
  sig, edid: string;
begin
  Result := 0;
  sig := Signature(e);
  edid := EditorID(e);
  if not SameText(GetFileName(GetFile(e)), 'FalloutNV.esm') then Exit;

  // ═══════════════════════════════════════════════════════════
  //  GUNS — PISTOLS
  // ═══════════════════════════════════════════════════════════

  // Good Memories — clone Maria (unique 9mm)
  if (sig = 'WEAP') and SameText(edid, 'WeapNV9mmPistolUnique') then
    MakeWeapon(e, 'WeapGoodMemories', 'Good Memories',
      'Light in the hand. Steady in the dark. Some things you never forget how to do. Part of the Mnehmos Collection.',
      28, 34, 17, 175, 3000, 2.0, 15.0, 0.8, 7.0, 1.2, 25, 0.0);

  // Passing Thought — clone 10mm Pistol
  if (sig = 'WEAP') and SameText(edid, 'Weap10mmPistol') then
    MakeWeapon(e, 'WeapPassingThought', 'Passing Thought',
      'Quick and forgettable — for them. By the time they realize what happened, the thought has already moved on. Part of the Mnehmos Collection.',
      30, 36, 16, 200, 4500, 1.5, 18.0, 0.7, 5.5, 1.3, 50, 0.0);

  // Final Draft — clone 12.7mm Pistol
  if (sig = 'WEAP') and SameText(edid, 'WeapNV127mmPistol') then
    MakeWeapon(e, 'WeapFinalDraft', 'Final Draft',
      'The last revision. No notes needed. Every edit has been made, every weakness struck through. What remains is definitive. Part of the Mnehmos Collection.',
      50, 50, 9, 250, 9000, 2.0, 22.0, 0.5, 2.5, 2.8, 75, 0.0);

  // ═══════════════════════════════════════════════════════════
  //  GUNS — REVOLVERS
  // ═══════════════════════════════════════════════════════════

  // First Impression — clone Lucky (unique .357)
  if (sig = 'WEAP') and SameText(edid, 'WeapNV357RevolverUnique') then
    MakeWeapon(e, 'WeapFirstImpression', 'First Impression',
      'You only get one. Make it count. The cylinder turns with a whisper and the hammer falls like a verdict. Part of the Mnehmos Collection.',
      32, 32, 6, 200, 3500, 1.5, 20.0, 0.5, 2.5, 1.5, 25, 0.0);

  // Burning Question — clone Mysterious Magnum (unique .44)
  if (sig = 'WEAP') and SameText(edid, 'WeapNV44RevolverUnique') then
    MakeWeapon(e, 'WeapBurningQuestion', 'Burning Question',
      'Demands an answer. The muzzle flash is the punctuation. Every chamber holds a question nobody wants to hear. Part of the Mnehmos Collection.',
      42, 42, 6, 225, 6000, 1.5, 24.0, 0.4, 2.0, 2.0, 50, 0.0);

  // Hindsight — clone Hunting Revolver
  if (sig = 'WEAP') and SameText(edid, 'WeapNVHuntingRevolver') then
    MakeWeapon(e, 'WeapHindsight', 'Hindsight',
      'Hindsight is 20/20. Unfortunately for them, so is your aim. Five rounds. One empty — the Archivist always leaves room for one more memory. Part of the Mnehmos Collection.',
      65, 65, 5, 250, 10000, 2.0, 26.0, 0.02, 1.8, 4.0, 75, 0.0);

  // ═══════════════════════════════════════════════════════════
  //  GUNS — SMGs
  // ═══════════════════════════════════════════════════════════

  // Rambling — clone Vance's 9mm SMG (unique)
  if (sig = 'WEAP') and SameText(edid, 'WeapNV9mmSubmachineGunUnique') then
    MakeWeapon(e, 'WeapRambling', 'Rambling',
      'Goes on and on and on. By the time it stops, nobody is left to complain about the noise. Part of the Mnehmos Collection.',
      17, 17, 40, 200, 3000, 1.5, 18.0, 1.5, 8.0, 3.0, 25, 0.0);

  // Recurring Nightmare — clone 12.7mm SMG
  if (sig = 'WEAP') and SameText(edid, 'WeapNV127mmSubmachineGun') then
    MakeWeapon(e, 'WeapRecurringNightmare', 'Recurring Nightmare',
      'The sound comes back to you in your sleep. Some things will not stay buried. The suppressor does not make it quiet — just inevitable. Part of the Mnehmos Collection.',
      36, 54, 30, 250, 12000, 1.5, 24.0, 1.2, 7.0, 4.5, 50, 0.0);

  // ═══════════════════════════════════════════════════════════
  //  GUNS — RIFLES
  // ═══════════════════════════════════════════════════════════

  // Footnote — clone Ratslayer (unique Varmint Rifle)
  if (sig = 'WEAP') and SameText(edid, 'WeapNVVarmintRifleUnique') then
    MakeWeapon(e, 'WeapFootnote', 'Footnote',
      'Small but always cited. Easy to overlook, impossible to ignore once you read the fine print. Part of the Mnehmos Collection.',
      22, 22, 10, 175, 2000, 1.5, 20.0, 0.1, 3.0, 3.5, 0, 0.0);

  // Cross-Reference — clone Trail Carbine
  if (sig = 'WEAP') and SameText(edid, 'WeapNVTrailCarbine') then
    MakeWeapon(e, 'WeapCrossReference', 'Cross-Reference',
      'One thing leads to another. Follow the trail long enough and everything connects. The lever action is smooth from years of indexed use. Part of the Mnehmos Collection.',
      55, 40, 10, 250, 6000, 1.5, 24.0, 0.3, 2.0, 5.0, 50, 0.0);

  // Long Memory — clone Service Rifle
  if (sig = 'WEAP') and SameText(edid, 'WeapNVServiceRifle') then
    MakeWeapon(e, 'WeapLongMemory', 'Long Memory',
      'Every round placed exactly where it needs to go. The sights are zeroed to memory. The action cycles like breathing. Part of the Mnehmos Collection.',
      32, 48, 24, 300, 7500, 1.5, 22.0, 0.15, 3.5, 5.0, 75, 0.0);

  // Thesis Statement — clone Anti-Materiel Rifle
  if (sig = 'WEAP') and SameText(edid, 'WeapNVAntiMaterielRifle') then
    MakeWeapon(e, 'WeapThesisStatement', 'Thesis Statement',
      'The definitive argument. Peer-reviewed at 2000 meters. There is no rebuttal to a .50 caliber conclusion. Part of the Mnehmos Collection.',
      120, 120, 10, 400, 18000, 2.0, 40.0, 0.005, 0.5, 12.0, 100, 0.0);

  // ═══════════════════════════════════════════════════════════
  //  GUNS — SHOTGUNS
  // ═══════════════════════════════════════════════════════════

  // Bad Memories — clone Caravan Shotgun
  if (sig = 'WEAP') and SameText(edid, 'WeapNVCaravanShotgun') then
    MakeWeapon(e, 'WeapBadMemories', 'Bad Memories',
      'Each shell is a grudge. Each pump is a promise. The stock is scarred with tally marks — one for every lesson taught at close range. Part of the Mnehmos Collection.',
      70, 70, 4, 150, 3500, 1.5, 26.0, 1.8, 0.0, 5.0, 25, 0.0);

  // Loud Reminder — clone Lever-Action Shotgun
  if (sig = 'WEAP') and SameText(edid, 'WeapNVLeverActionShotgun') then
    MakeWeapon(e, 'WeapLoudReminder', 'Loud Reminder',
      'Hard to ignore. Harder to forget. The lever racks with authority and the barrel speaks volumes. Part of the Mnehmos Collection.',
      78, 60, 6, 200, 5000, 1.5, 26.0, 1.5, 0.0, 5.5, 50, 0.0);

  // Last Word — clone Dinner Bell (unique Hunting Shotgun)
  if (sig = 'WEAP') and SameText(edid, 'WeapNVHuntingShotgunUnique') then
    MakeWeapon(e, 'WeapLastWord', 'Last Word',
      'End of discussion. The final punctuation in any argument. Seven shells of closure. Part of the Mnehmos Collection.',
      95, 95, 7, 300, 9000, 1.5, 28.0, 1.0, 0.0, 6.5, 75, 0.0);

  // ═══════════════════════════════════════════════════════════
  //  ENERGY WEAPONS — PISTOLS
  // ═══════════════════════════════════════════════════════════

  // Afterglow — clone Laser Pistol
  if (sig = 'WEAP') and SameText(edid, 'WeapLaserPistol') then
    MakeWeapon(e, 'WeapAfterglow', 'Afterglow',
      'The light that lingers after the source is gone. A warm pulse that stays with you — and burns through them. Part of the Mnehmos Collection.',
      18, 22, 24, 200, 3000, 1.5, 16.0, 0.5, 5.0, 1.5, 25, 0.0);

  // Phantom Limb — clone Plasma Defender
  if (sig = 'WEAP') and SameText(edid, 'WeapNVPlasmaDefender') then
    MakeWeapon(e, 'WeapPhantomLimb', 'Phantom Limb',
      'You still feel it. The sensation of something that should not be there anymore. Green plasma and ghost pain. Part of the Mnehmos Collection.',
      38, 38, 18, 225, 7000, 2.0, 20.0, 0.8, 4.0, 2.0, 50, 0.0);

  // ═══════════════════════════════════════════════════════════
  //  ENERGY WEAPONS — RIFLES
  // ═══════════════════════════════════════════════════════════

  // Bright Idea — clone Laser Rifle
  if (sig = 'WEAP') and SameText(edid, 'WeapLaserRifle') then
    MakeWeapon(e, 'WeapBrightIdea', 'Bright Idea',
      'Strikes like inspiration — sudden, focused, and blinding. The beam cuts through darkness and doubt alike. Part of the Mnehmos Collection.',
      28, 34, 28, 250, 6000, 1.5, 22.0, 0.3, 3.0, 4.5, 50, 0.0);

  // Overexposure — clone Q-35 Matter Modulator (unique Plasma Rifle)
  if (sig = 'WEAP') and SameText(edid, 'WeapNVPlasmaRifleUnique') then
    MakeWeapon(e, 'WeapOverexposure', 'Overexposure',
      'Seen too much. Absorbed too much. Now it all comes back out in searing green. The lens is cracked but the beam is true. Part of the Mnehmos Collection.',
      50, 50, 16, 300, 11000, 2.0, 28.0, 0.5, 2.5, 6.0, 75, 0.0);

  // Peer Review — clone Gauss Rifle
  if (sig = 'WEAP') and SameText(edid, 'WeapNVGaussRifle') then
    MakeWeapon(e, 'WeapPeerReview', 'Peer Review',
      'Validated by impact. The electromagnetic coils hum with accumulated knowledge and the projectile carries the weight of evidence. Part of the Mnehmos Collection.',
      130, 130, 6, 400, 18000, 2.0, 45.0, 0.01, 0.5, 8.0, 100, 0.0);

  // ═══════════════════════════════════════════════════════════
  //  EXPLOSIVES
  // ═══════════════════════════════════════════════════════════

  // Intrusive Thought — clone Thump-Thump (unique Grenade Rifle)
  if (sig = 'WEAP') and SameText(edid, 'WeapNVGrenadeRifleUnique') then
    MakeWeapon(e, 'WeapIntrusiveThought', 'Intrusive Thought',
      'Could not help yourself. The idea just appeared and before you could stop it — THUMP. Part of the Mnehmos Collection.',
      0, 0, 6, 250, 8000, 0.0, 28.0, -1.0, 0.0, 0.0, 50, 0.0);

  // Buried Memory — clone Mercy (unique Grenade MG)
  if (sig = 'WEAP') and SameText(edid, 'WeapNVGrenadeMachinegunUnique') then
    MakeWeapon(e, 'WeapBuriedMemory', 'Buried Memory',
      'Digs itself back up. No matter how deep you push it down, the ground shakes and it erupts. Part of the Mnehmos Collection.',
      0, 0, 12, 350, 15000, 0.0, 35.0, -1.0, 0.0, 0.0, 75, 0.0);

  // ═══════════════════════════════════════════════════════════
  //  MELEE
  // ═══════════════════════════════════════════════════════════

  // Deja Vu — clone Chance's Knife
  if (sig = 'WEAP') and SameText(edid, 'WeapNVKnifeCombatUnique') then
    MakeWeapon(e, 'WeapDejaVu', 'Deja Vu',
      'You have been here before. You have done this before. Your hand knows what to do. The blade moves faster than thought. Part of the Mnehmos Collection.',
      28, 42, 0, 200, 5000, 2.0, 14.0, -1.0, 0.0, 0.0, 25, 1.3);

  // Grudge — clone Super Sledge
  if (sig = 'WEAP') and SameText(edid, 'WeapSuperSledge') then
    MakeWeapon(e, 'WeapGrudge', 'Grudge',
      'Carries a lot of weight. Every swing is an accumulation of grievances, delivered with compound interest. Part of the Mnehmos Collection.',
      60, 60, 0, 300, 7000, 1.5, 32.0, -1.0, 0.0, 0.0, 50, 1.2);

  // Closure — clone Oh, Baby! (unique Super Sledge)
  if (sig = 'WEAP') and SameText(edid, 'WeapSuperSledgeUnique') then
    MakeWeapon(e, 'WeapClosure', 'Closure',
      'Finally letting go — violently. The weight of everything you have been carrying, released in one decisive arc. Part of the Mnehmos Collection.',
      80, 80, 0, 350, 12000, 2.0, 35.0, -1.0, 0.0, 0.0, 75, 1.3);

  // ═══════════════════════════════════════════════════════════
  //  UNARMED
  // ═══════════════════════════════════════════════════════════

  // Muscle Memory — clone Power Fist
  if (sig = 'WEAP') and SameText(edid, 'WeapPowerFist') then
    MakeWeapon(e, 'WeapMuscleMemory', 'Muscle Memory',
      'The body remembers what the mind forgets. The servos fire before you think. Fist meets face with practiced certainty. Part of the Mnehmos Collection.',
      45, 50, 0, 250, 8000, 2.0, 22.0, -1.0, 0.0, 0.0, 50, 1.3);

  // ═══════════════════════════════════════════════════════════
  //  ARMOR
  // ═══════════════════════════════════════════════════════════

  // Archivist's Duster — clone Bounty Hunter Duster (light, early)
  if (sig = 'ARMO') and SameText(edid, 'BountyHunterDuster') then begin
    armDuster := MakeArmor(e, 'ArmorArchivistDuster', 'The Archivist''s Duster',
      'Shells line the inside like chapters in a book. Every scratch tells a story. Part of the Mnehmos Collection.',
      11.0, 300, 5000, 3.5);
    enchBase2 := e; // Save for cloning enchant later
  end;

  // Archivist's Jacket — clone Leather Armor Reinforced (mid)
  if (sig = 'ARMO') and SameText(edid, 'ArmorLeatherReinforced') then
    armJacket := MakeArmor(e, 'ArmorArchivistJacket', 'Archivist''s Field Jacket',
      'Upgraded in the field. Leather panels reinforced with salvaged plating. Comfortable enough to sleep in, tough enough to survive in. Part of the Mnehmos Collection.',
      16.0, 400, 7000, 12.0);

  // Archivist's Combat Armor — clone Combat Armor Reinforced Mk2 (late)
  if (sig = 'ARMO') and SameText(edid, 'ArmorCombatReinforcedMark2') then
    armCombat := MakeArmor(e, 'ArmorArchivistCombat', 'Archivist''s Combat Armor',
      'Every plate tells a story. Every dent is a debt collected. Proven in the wastes. Part of the Mnehmos Collection.',
      25.0, 800, 12000, 20.0);

  // Archivist's Power Armor — clone T-51b (endgame)
  if (sig = 'ARMO') and SameText(edid, 'ArmorPowerT51b') then
    armPower := MakeArmor(e, 'ArmorArchivistPower', 'Archivist''s Power Armor',
      'The full archive, walking. Pre-War engineering modified by Post-War necessity. The Archivist''s final form. Part of the Mnehmos Collection.',
      28.0, 1200, 18000, 35.0);

  // Mnehmos Hat — clone Desperado Cowboy Hat
  if (sig = 'ARMO') and SameText(edid, 'CowboyHat01') then begin
    armHat := MakeArmor(e, 'HatMnehmos', 'Mnehmos Hat',
      'Wide brim, low profile. The Archivist does not need to be recognized — just remembered. Part of the Mnehmos Collection.',
      2.0, 150, 2000, 1.0);
    enchBase1 := e; // Save 1-effect enchant base
  end;

  // Recollection Lenses — clone Authority Glasses
  if (sig = 'ARMO') and SameText(edid, 'GlassesNCRRangerCivilian') then
    armGlasses := MakeArmor(e, 'GlassesRecollection', 'Recollection Lenses',
      'Pre-War optics, hand-ground. Everything looks clearer through the lens of experience. Part of the Mnehmos Collection.',
      0.0, 200, 2500, 0.0);

end;

// ─── ENCHANTMENT CREATION IN FINALIZE ───────────────────────
function Finalize: Integer;
var
  ench, effects, effect, efit, newEnch: IInterface;
  enchDuster, enchJacket, enchCombat, enchPower, enchHat, enchGlasses: IInterface;
  i: Integer;
  fid: Cardinal;
begin
  Result := 0;

  AddMessage('');
  AddMessage('--- Creating Enchantments ---');

  // Find the Duster enchant (2-effect) to clone from base game
  // EnchClothingDuster [ENCH:0008B608] has 2 effects — good template
  // EnchClothingHeadSunGuard [ENCH:00071B88] has 1 effect — for hat

  // We need to iterate base game to find these
  for i := 0 to Pred(RecordCount(FileByIndex(0))) do begin
    ench := RecordByIndex(FileByIndex(0), i);
    if Signature(ench) <> 'ENCH' then Continue;
    fid := FixedFormID(ench);

    // ── Hat Enchant: +1 PER (clone 1-effect hat enchant) ──
    if (fid = $00071B88) and not Assigned(enchHat) then begin
      AddRequiredElementMasters(ench, tp, False);
      enchHat := wbCopyElementToFile(ench, tp, True, True);
      SetElementEditValues(enchHat, 'EDID', 'EnchMnehmosHat');
      SetElementEditValues(enchHat, 'FULL', 'Archivist''s Vigil');
      // Already +1 PER, perfect
      AddMessage('  EnchMnehmosHat (+1 PER) = ' + IntToHex(FormID(enchHat), 8));
    end;

    // ── Duster Enchant: +1 PER, +1 INT (clone 2-effect duster enchant) ──
    if (fid = $0008B608) and not Assigned(enchDuster) then begin
      AddRequiredElementMasters(ench, tp, False);

      // Duster: +1 PER, +1 INT
      enchDuster := wbCopyElementToFile(ench, tp, True, True);
      SetElementEditValues(enchDuster, 'EDID', 'EnchMnehmosDuster');
      SetElementEditValues(enchDuster, 'FULL', 'Archivist''s Focus');
      effects := ElementByName(enchDuster, 'Effects');
      if Assigned(effects) then begin
        if ElementCount(effects) > 0 then begin
          effect := ElementByIndex(effects, 0);
          SetElementEditValues(effect, 'EFID', 'IncreasePerception "Increased Perception" [MGEF:0001515D]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Perception');
          end;
        end;
        if ElementCount(effects) > 1 then begin
          effect := ElementByIndex(effects, 1);
          SetElementEditValues(effect, 'EFID', 'IncreaseIntelligence "Increased Intelligence" [MGEF:00015160]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Intelligence');
          end;
        end;
      end;
      AddMessage('  EnchMnehmosDuster (+1 PER, +1 INT) = ' + IntToHex(FormID(enchDuster), 8));

      // Glasses: +1 INT, +1 CHR
      enchGlasses := wbCopyElementToFile(ench, tp, True, True);
      SetElementEditValues(enchGlasses, 'EDID', 'EnchMnehmosLenses');
      SetElementEditValues(enchGlasses, 'FULL', 'Archivist''s Clarity');
      effects := ElementByName(enchGlasses, 'Effects');
      if Assigned(effects) then begin
        if ElementCount(effects) > 0 then begin
          effect := ElementByIndex(effects, 0);
          SetElementEditValues(effect, 'EFID', 'IncreaseIntelligence "Increased Intelligence" [MGEF:00015160]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Intelligence');
          end;
        end;
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
      AddMessage('  EnchMnehmosLenses (+1 INT, +1 CHR) = ' + IntToHex(FormID(enchGlasses), 8));

      // Jacket: +1 PER, +1 AGL
      enchJacket := wbCopyElementToFile(ench, tp, True, True);
      SetElementEditValues(enchJacket, 'EDID', 'EnchMnehmosJacket');
      SetElementEditValues(enchJacket, 'FULL', 'Archivist''s Reflex');
      effects := ElementByName(enchJacket, 'Effects');
      if Assigned(effects) then begin
        if ElementCount(effects) > 0 then begin
          effect := ElementByIndex(effects, 0);
          SetElementEditValues(effect, 'EFID', 'IncreasePerception "Increased Perception" [MGEF:0001515D]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Perception');
          end;
        end;
        if ElementCount(effects) > 1 then begin
          effect := ElementByIndex(effects, 1);
          SetElementEditValues(effect, 'EFID', 'IncreaseAgility "Increased Agility" [MGEF:00015161]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Agility');
          end;
        end;
      end;
      AddMessage('  EnchMnehmosJacket (+1 PER, +1 AGL) = ' + IntToHex(FormID(enchJacket), 8));

      // Combat: +1 PER, +1 INT (same as duster but better armor)
      enchCombat := wbCopyElementToFile(ench, tp, True, True);
      SetElementEditValues(enchCombat, 'EDID', 'EnchMnehmosCombat');
      SetElementEditValues(enchCombat, 'FULL', 'Archivist''s Resolve');
      effects := ElementByName(enchCombat, 'Effects');
      if Assigned(effects) then begin
        if ElementCount(effects) > 0 then begin
          effect := ElementByIndex(effects, 0);
          SetElementEditValues(effect, 'EFID', 'IncreasePerception "Increased Perception" [MGEF:0001515D]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Perception');
          end;
        end;
        if ElementCount(effects) > 1 then begin
          effect := ElementByIndex(effects, 1);
          SetElementEditValues(effect, 'EFID', 'IncreaseAgility "Increased Agility" [MGEF:00015161]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '1');
            SetElementEditValues(efit, 'Actor Value', 'Agility');
          end;
        end;
      end;
      AddMessage('  EnchMnehmosCombat (+1 PER, +1 AGL) = ' + IntToHex(FormID(enchCombat), 8));

      // Power Armor: +2 PER, +1 INT
      enchPower := wbCopyElementToFile(ench, tp, True, True);
      SetElementEditValues(enchPower, 'EDID', 'EnchMnehmosPower');
      SetElementEditValues(enchPower, 'FULL', 'Archivist''s Archive');
      effects := ElementByName(enchPower, 'Effects');
      if Assigned(effects) then begin
        if ElementCount(effects) > 0 then begin
          effect := ElementByIndex(effects, 0);
          SetElementEditValues(effect, 'EFID', 'IncreasePerception "Increased Perception" [MGEF:0001515D]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '2');
            SetElementEditValues(efit, 'Actor Value', 'Perception');
          end;
        end;
        if ElementCount(effects) > 1 then begin
          effect := ElementByIndex(effects, 1);
          SetElementEditValues(effect, 'EFID', 'IncreaseIntelligence "Increased Intelligence" [MGEF:00015160]');
          efit := ElementBySignature(effect, 'EFIT');
          if Assigned(efit) then begin
            SetElementEditValues(efit, 'Magnitude', '2');
            SetElementEditValues(efit, 'Actor Value', 'Intelligence');
          end;
        end;
      end;
      AddMessage('  EnchMnehmosPower (+2 PER, +2 INT) = ' + IntToHex(FormID(enchPower), 8));
    end;
  end;

  // ── Link enchantments to armor ──
  AddMessage('');
  AddMessage('--- Linking Enchantments to Armor ---');

  if Assigned(armDuster) and Assigned(enchDuster) then begin
    SetElementNativeValues(armDuster, 'EITM', FormID(enchDuster));
    AddMessage('  Duster -> +1 PER, +1 INT');
  end;
  if Assigned(armJacket) and Assigned(enchJacket) then begin
    SetElementNativeValues(armJacket, 'EITM', FormID(enchJacket));
    AddMessage('  Jacket -> +1 PER, +1 AGL');
  end;
  if Assigned(armCombat) and Assigned(enchCombat) then begin
    SetElementNativeValues(armCombat, 'EITM', FormID(enchCombat));
    AddMessage('  Combat -> +1 PER, +1 AGL');
  end;
  if Assigned(armPower) and Assigned(enchPower) then begin
    SetElementNativeValues(armPower, 'EITM', FormID(enchPower));
    AddMessage('  Power -> +2 PER, +2 INT');
  end;
  if Assigned(armHat) and Assigned(enchHat) then begin
    SetElementNativeValues(armHat, 'EITM', FormID(enchHat));
    AddMessage('  Hat -> +1 PER');
  end;
  if Assigned(armGlasses) and Assigned(enchGlasses) then begin
    SetElementNativeValues(armGlasses, 'EITM', FormID(enchGlasses));
    AddMessage('  Glasses -> +1 INT, +1 CHR');
  end;

  AddMessage('');
  AddMessage('=== MNEHMOS COLLECTION COMPLETE: ' + IntToStr(itemCount) + ' items ===');
  AddMessage('Save the ESP to apply all changes.');
end;

end.
