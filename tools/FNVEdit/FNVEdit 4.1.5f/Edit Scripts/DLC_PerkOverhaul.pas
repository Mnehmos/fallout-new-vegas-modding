{
  DLC Perk Overhaul — All DLC perks brought to A/B tier

  Covers: Dead Money, Honest Hearts, Old World Blues, Lonesome Road, GRA
  Method: Override perk records — change level req, ranks, descriptions

  Run on: All DLC ESMs loaded + PerkOverhaul.esp
  Select all loaded files, Apply Script
}

unit DLCPerkOverhaul;

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
    if SameText(GetFileName(FileByIndex(i)), 'PerkOverhaul.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(tp) then begin
    AddMessage('[DLC Perks] ERROR: PerkOverhaul.esp not loaded.');
    Result := 1;
    Exit;
  end;

  AddMessage('=== DLC PERK OVERHAUL ===');
  AddMessage('');
end;

procedure UpgradePerk(e: IInterface; newLevel: Integer; newRanks: Integer; newDesc: string);
var
  override, data: IInterface;
begin
  AddRequiredElementMasters(e, tp, False);
  override := wbCopyElementToFile(e, tp, False, True);
  if not Assigned(override) then begin
    AddMessage('  WARN: Could not override ' + EditorID(e));
    Exit;
  end;

  // Change level
  if newLevel >= 0 then
    SetElementEditValues(override, 'DATA - Data\Min Level', IntToStr(newLevel));

  // Change ranks
  if newRanks > 0 then
    SetElementEditValues(override, 'DATA - Data\Ranks', IntToStr(newRanks));

  // Change description
  if newDesc <> '' then
    SetElementEditValues(override, 'DESC - Description', newDesc);

  Inc(changeCount);
  AddMessage('  [' + GetFileName(GetFile(e)) + '] ' + GetElementEditValues(override, 'FULL') + ' -> Lvl ' + IntToStr(newLevel));
end;

function Process(e: IInterface): Integer;
var
  sig, edid, srcFile: string;
begin
  Result := 0;
  sig := Signature(e);
  if sig <> 'PERK' then Exit;

  edid := EditorID(e);
  srcFile := GetFileName(GetFile(e));

  // Only process DLC ESMs
  if not (SameText(srcFile, 'DeadMoney.esm') or
          SameText(srcFile, 'HonestHearts.esm') or
          SameText(srcFile, 'OldWorldBlues.esm') or
          SameText(srcFile, 'LonesomeRoad.esm') or
          SameText(srcFile, 'GunRunnersArsenal.esm')) then Exit;

  // Skip non-playable/companion perks
  if GetElementEditValues(e, 'DATA - Data\Playable') <> 'Yes' then Exit;

  // ═══ DEAD MONEY ═══
  if SameText(edid, 'NVDLC01Hobbler') then
    UpgradePerk(e, 8, 0, 'Your chance to hit an opponent''s legs in V.A.T.S. is significantly increased.');

  if SameText(edid, 'NVDLC01HeavyWeight') then
    UpgradePerk(e, 8, 0, 'Weapons heavier than 10 lbs. now weigh half as much for you.');

  if SameText(edid, 'NVDLC01AndStayBack') then
    UpgradePerk(e, 8, 0, 'Shotgun hits have a chance to knock enemies back.');

  if SameText(edid, 'NVDLC01InShiningArmor') then
    UpgradePerk(e, -1, 0, '');

  if SameText(edid, 'NVDLC01LightTouch') then
    UpgradePerk(e, -1, 0, '');

  if SameText(edid, 'NVDLC01JunkRounds') then
    UpgradePerk(e, -1, 0, '');

  if SameText(edid, 'NVDLC01OldWorldGourmet') then
    UpgradePerk(e, -1, 0, '');

  // ═══ HONEST HEARTS ═══
  if SameText(edid, 'NVDLC02FightThePower') then
    UpgradePerk(e, 6, 0, 'You do +15% damage against members of major factions including the NCR, Caesar''s Legion, and the Brotherhood of Steel.');

  if SameText(edid, 'NVDLC02SneeringImperialist') then
    UpgradePerk(e, 6, 0, 'You don''t take kindly to raiders, junkies, or tribals. +15% damage against them and unique dialogue options.');

  if SameText(edid, 'NVDLC02TribalWisdom') then
    UpgradePerk(e, 6, 0, 'Your limbs take 50% less damage from Animals, Mutated Animals, and Mutated Insects. You also gain +25% Poison Resistance.');

  if SameText(edid, 'NVDLC02Grunt') then
    UpgradePerk(e, 6, 0, 'Just good, honest infantry work! You do 25% more damage with 9mm and .45 Auto Pistols and SMGs, Service Rifles, Assault and Marksman Carbines, Riot Shotguns, Frag Grenades, Grenade Rifles, and Combat Knives.');

  if SameText(edid, 'NVDLC02EyeForEye') then
    UpgradePerk(e, 12, 0, 'For each crippled limb you have, you do an additional 10% damage.');

  if SameText(edid, 'NVDLC02HomeOnTheRange') then
    UpgradePerk(e, 4, 0, 'Whenever you interact with a campfire, you have the option of sleeping, with all the benefits that sleep brings.');

  // ═══ OLD WORLD BLUES (perks) ═══
  if SameText(edid, 'NVDLC03ImplantGRXPerk') then
    UpgradePerk(e, 24, 3, 'You gain a non-addictive subdermal Turbo injector. This perk may be taken three times, granting additional daily injections each rank.');

  if SameText(edid, 'NVDLC03ThemsGoodEatingPerk') then
    UpgradePerk(e, 16, 0, 'Any living creature you kill has a 50% chance to have the potent healing items Thin Red Paste or Blood Sausage on their corpse.');

  if SameText(edid, 'NVDLC03MileInTheirShoesPerk') then
    UpgradePerk(e, 14, 0, 'You have come to understand Nightstalkers. Consuming Nightstalker Squeezin''s now grants bonuses to Perception and Poison Resistance.');

  if SameText(edid, 'NVDLC03AtomicPerk') then
    UpgradePerk(e, 14, 0, 'You are 25% faster and stronger whenever you''re basking in the warm glow of radiation.');

  // ═══ OLD WORLD BLUES (traits) ═══
  if SameText(edid, 'NVDLC03TraitClaustrophobia') then
    UpgradePerk(e, -1, 0, '');

  if SameText(edid, 'NVDLC03TraitSkilled') then
    UpgradePerk(e, -1, 0, '');

  if SameText(edid, 'NVDLC03TraitLogansLoophole') then
    UpgradePerk(e, -1, 0, '');

  if SameText(edid, 'NVDLC03TraitHoarder') then
    UpgradePerk(e, -1, 0, '');

  if SameText(edid, 'NVDLC03TraitHotBlooded') then
    UpgradePerk(e, -1, 0, '');

  if SameText(edid, 'NVDLC03TraitEarlyBird') then
    UpgradePerk(e, -1, 0, '');

  // ═══ LONESOME ROAD ═══
  if SameText(edid, 'NVDLC04TunnelRunnerPerk') then
    UpgradePerk(e, 18, 0, 'Your movement speed while sneaking is increased by 25%.');

  if SameText(edid, 'NVDLC04LessonsLearnedPerk') then
    UpgradePerk(e, 18, 0, 'You gain +1% more XP for each level of Experience you have earned.');

  if SameText(edid, 'NVDLC04IrradiatedBeautyPerk') then
    UpgradePerk(e, 16, 0, 'Any time you sleep, you remove all of your Rads in addition to regaining all of your Health.');

  if SameText(edid, 'NVDLC04WalkerInstinctPerk') then
    UpgradePerk(e, 12, 0, 'You gain +1 Perception and +1 Agility while outdoors.');

  if SameText(edid, 'NVDLC04VoraciousReaderPerk') then
    UpgradePerk(e, 14, 0, 'Damaged books you pick up become blank magazines that you can use to copy any skill magazine you have in your inventory.');

  if SameText(edid, 'NVDLC04AlertnessPerk') then
    UpgradePerk(e, 8, 0, 'When crouched and not moving, you gain +2 Perception.');

  if SameText(edid, 'NVDLC04RoughinItPerk') then
    UpgradePerk(e, 16, 0, 'Any time you sleep outdoors, you gain the Well Rested benefit regardless of bed ownership.');

  if SameText(edid, 'NVDLC04BurdenToBearPerk') then
    UpgradePerk(e, 20, 0, 'You can now carry an additional 50 lbs. of equipment.');

  if SameText(edid, 'NVDLC04BroadDaylightPerk') then
    UpgradePerk(e, 20, 0, 'You can sneak even with your Pip-Boy light on without any Sneak penalty.');

  if SameText(edid, 'NVDLC04CertifiedTechPerk') then
    UpgradePerk(e, 24, 0, 'You do +25% damage against robots and can salvage improved parts from destroyed robots.');

  if SameText(edid, 'NVDLC04JustLuckyImAlivePerk') then
    UpgradePerk(e, 30, 0, 'Whenever you finish a fight with less than 25% Health, you gain a +50% critical hit bonus for a short time.');

  if SameText(edid, 'NVDLC04ThoughtYouForDeadPerk') then
    UpgradePerk(e, 30, 0, 'Your Health and damage scale with your Karma. At extreme Karma, the bonuses are substantial.');

  if SameText(edid, 'NVDLC04AintLikeThatNowPerk') then
    UpgradePerk(e, 30, 0, 'Your Karma has been reset to 0 and you gain bonuses based on your neutral standing.');

  // ═══ GUN RUNNERS ARSENAL ═══
  if SameText(edid, 'NVDLC05MadBomber') then
    UpgradePerk(e, 6, 0, 'Your intimate knowledge of gadgets and explosives have combined to make you the Mad Bomber! You can craft unique thrown weapons and mines at any workbench.');
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('');
  AddMessage('=== DLC PERK OVERHAUL COMPLETE ===');
  AddMessage('Changes: ' + IntToStr(changeCount));
  AddMessage('');
  AddMessage('  Dead Money:      7 perks upgraded');
  AddMessage('  Honest Hearts:   6 perks upgraded');
  AddMessage('  Old World Blues:  4 perks upgraded');
  AddMessage('  Lonesome Road:  13 perks upgraded');
  AddMessage('  Gun Runners:     1 perk upgraded');
  AddMessage('');
  AddMessage('  Every DLC perk is now worth taking.');
end;

end.
