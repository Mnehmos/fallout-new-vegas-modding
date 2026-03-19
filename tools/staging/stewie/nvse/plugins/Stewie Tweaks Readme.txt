Stewie Tweaks v9.80 ReadMe

Each of the plugin's features can be enabled using the in-game Pause->Settings->Tweaks menu (requires rebooting the game to apply changes), or should be enabled in the mod INI 'Data\NVSE\Plugins\nvse_stewie_tweaks.ini' as desired. 
If the INI doesn't exist you should download it from the mod page, or create an empty file in the required folder if the mod page is unavailable.

Run the game with the plugin active to populate the INI.

Setting Guide:
b... - a boolean value (0 or 1) - setting to 0 will disable the feature and 1 will enable it.
i... - an integer value (whole numbers) e.g. 0, -101, 17
f... - a float value (decimals) e.g. 1.0, -5.6442, 0.104
s... - a string value e.g. "You are too weak to use this weapon."

----------------
[INI]
bSortAlphabetically
Sort the mod's ini alphabetically.

bPrependNewSettings
Add new settings to the top of sections instead of the bottom.

bMultiINISupport
Allow INIs in the Data\\NVSE\\Plugins\\Tweaks\\INIs folder to overwrite the main INI.

----------------

[Tweaks]
To enable any Tweaks, set them to ' = 1' instead of ' = 0'.

bInlineVanillaFunctions
Optimizes the most frequent/expensive functions for various scenarios to decrease save/loading times and improve general performance. If you're using 'New Vegas Tick Fix' make sure it's updated (v9.6+).
Requires separate download.
Options (Inlines):
  bMisc - general inlines
  bPathing - inlines related to pathing
  bSaveLoad - inlines related to saving/loading
  bMenus - inlines related to the UI
  bDynamicCasts - inlines related to typecasting
  bProcess - inlines related to actors and their processes
  bAudio - inlines related to audio
  bScripts - inlines related to scripts
  bRendering - inlines related to the renderer

bNoScreenshotPopup
Stops the "Screenshot: File ... created" pop-up appearing at the top right corner of the screen.
Options (Screenshot Popup):
  bPrintToConsole - make the message appear in console instead of just removing it altogether
  sSoundName - editor ID of the sound to play
  fSoundVolume - volume of sound

bNoKarmaMessages
Stops the sounds and messages for good and bad karma.
Options (Karma Messages):
  bRemoveEvilMessage
  bRemoveEvilSound
  bRemoveGoodMessage
  bRemoveGoodSound
  iRepeatKarmaSoundIgnoreTime - stops the bad karma sound repeating within the provided time (in milliseconds)
  iKarmaIncreaseThreshold - ignore karma messages and sounds if the increase in karma is below this value
  iKarmaDecreaseThreshold - ignore karma messages and sounds if the decrease in karma is below this value
  
bNoCrippleCriticalMessages
Removes the crippled or critical messages.
Options (Cripple-Critical Messages):
  bPatchCritical - remove critical hit messages
  bPatchCripple - remove crippled enemy limb messages

bAimingSpeed
Remove the movement penalty associated with aiming.
Options (Aiming Speed):
  bPatchMelee - remove the penalty for melee blocking
  bPatchNonMelee - remove the penalty for iron sighting

bNoAudioDistortion
Remove the audio distortion effect applied to actors wearing masks and intercoms.
Options (Audio Distortion):
  bDeepFried - apply the distortion to all sounds, not just NPCs wearing masks

bNoScrollwheelPOVChange
Stops the point of view changing when zooming in/out (scrolling)
Options (Scrollwheel POV):
  bDisableFirstToThird
  bDisableThirdToFirst

bFasterSleepWait
Decreases the amount of time spent waiting between hours in the sleep and wait menus.
Options (Sleep Wait):
  iWaitTimeMS - time spent waiting between hours in milliseconds
  bDontScaleWithTimescale - makes the wait time unaffected by the current timescale (e.g. sgtm command)

bNoPipBoyInCombat
Disallows use of the Pip-Boy during combat.
Options (No PipBoy In Combat):
  bShowMessage - enable corner messages "No Pip-Boy in combat" or "Not enough AP to use Pip-Boy in combat"
  bAllowPipboyUsingActionPoints - allow the use of Pip-Boy for iPipboyAPCost action points
  iPipboyAPCost - number of action points used
  sNotEnoughAPMessage - message shown without enough Action Points
  sNotAllowedMessage - message shown if opening the Pip-Boy isn't allowed
  
bJumpingCostsAP
Makes jumping cost Action Points.
Options (Jumping Costs AP):
  iJumpAPCost - number of action points used
  bJumpWithoutEnoughAP - if set to 0, you will only be able to jump if you have enough AP
  bCombatOnly - only require action points during combat

bNoXPBarInCombat
Delay XP pop-ups till the end of combat.
Options (Combat XP):
  iCombatXPDelayMS - the amount of time after combat till the XP message will be shown

bNoSkillTags
Hides the [Perk], [Speech], [Barter], etc. tags from dialogue options.
Options (No Skill Tags):
  bRemoveRedOutline - removes the red outline on dialogue options where the skill check would fail
  iRemoveTags - 
    Mode 0 - Does not remove the skill tags
    Mode 1 - Removes the entire tag i.e. [Speech 20] Yes... -> Yes...
    Mode 2 - Only removes the number : i.e. [Speech 10/20] No... -> [Speech] No...
  bAddPercentSymbol - show the % symbol on TTW percentage based speech checks (e.g. [Speech 20%] -> [Speech%])
  bRemoveFailedSuccessText - removes the [SUCCESS] and [FAILED] from responses
  bNoXPPopupInDialogue - hides XP pop-ups if earned during dialogue
  bHideMiscStats - don't show 'Speech Successes' and 'Speech Failures' in stats menu and challenge update corner messages

bMovementPenalties
Adds a configurable movement penalty for when the player is moving backwards or aiming.
Options (Slower Backpedaling):
  iLeftStrafeSpeedPercentage - moving left
  iRightStrafeSpeedPercentage - moving right
  iBackSpeedPercentage - moving backwards
  iBackLeftSpeedPercentage - moving diagonally back and left
  iBackRightSpeedPercentage - moving diagonally back and right
  iFrontLeftSpeedPercentage - moving diagonally forward and left
  iFrontRightSpeedPercentage - moving diagonally forward and right
  iMeleeAimSpeedPercentage - modifier when blocking
  iAimSpeedPercentage - modifier when iron sighting
  iReloadOrJamSpeedMultiplier - modifier while reload and weapon jam animations are playing
  iFiringWeaponSpeedMultiplier - modifier while firing an automatic weapon
  
bHardcoreTweaks
Enable toggling of individual hardcore features, regardless of the game's hardcore setting.
Options (Hardcore Tweaks):
  bAmmoWeight - toggle ammo having weight
  bEssentialCompanions
  bSleepingHeals - toggle sleeping healing the player - NOTE: does not affect sleeping in player-owned beds as this is a scripted effect.
  
bOverencumberedTweak
Enables running and jumping for Action Points while over-encumbered.
Options (Over Encumbered):
  iAPDrainCost - amount AP is drained by every iAPDrainIntervalMS
  iAPDrainIntervalMS - rate at which AP is drained (in milliseconds)
  iJumpAPCost - action points used to jump
  bJumpWithoutEnoughAP - allows jumping while over-encumbered with 0 AP
  bRemoveEncumbranceMessage - removes the "You are over-encumbered and cannot run!" message
  bAllowRunWithoutEnoughAP - allows running while over-encumbered with 0 AP
  bWeightBasedAPPenalty - scale the AP drain by how overencumbered you are, i.e. iAPDrainCost * CurrentWeight/MaxWeight 
  bInCombatOnly - only decrease action points when running while in combat
  fAPRegenMult - multiplier applied to action point regeneration while moving

bEnteringVATSCostsAP
Adds an AP penalty for entering VATS.
Options (Entering VATS Costs AP):
  iEnterVATSAPCost - action points used to enter VATS
  bNoVATSIfNotEnoughAP - stops VATS entering if there is not enough AP to fire the current weapon
  bFailOnly - only charge AP if there were no targets found
  bChargeOnVATSNoTargetsExit - instead of charging AP when entering VATS, charge it if you exit VATS without selecting a target

bImprovedAutosave
Use incremental save slots for autosave, optionally fullsaving every rotation.
Options (Save Manager):
   iReloadCurrentSaveKey - hotkey to reload the current loaded save (as if the player died)
   iCreateSaveKey - hotkey to create a named save
   iIncrementalSaveKey - hotkey to create a slot save
   iMaxIncrementalSaveCount - number of incremental save slots
   iAutoSaveTimer - delay between timed autosaves in seconds
   iMaxAutoSaveCount - number of autosave slots, when the max slot is reached it will begin overwriting from slot 0
   bPeriodicFullsave - create a full (named) save every time the max slot is reached
   bHideAutosaveMessage - hide the mod and vanilla autosave messages
   bSaveOnLocationDiscovered - autosave when a location is discovered
   bSaveOnQuestCompleted - autosave when a quest is completed
   bSaveOnExitGame - autosave when exiting the game
   bSaveOnPickpocket - autosave when closing the container menu after successfully pickpocketing
   bSaveOnCraft - autosave when closing the recipe menu after crafting an item
   bSavePreLevelUp - autosave before the levelup menu is shown
   iMinAutosaveInterval - prevents autosaves within this time of each other (in seconds) - affects vanilla and timed autosaves
   iIncrementalSaveSlotChangeInterval - only increase the incremental save slot if it's been this long since last slot change (in seconds); e.g. when set to 60 seconds, any saves made within 0-60s of the first save in a slot will all overwrite each other - after that 60s a new slot is used
   bPreventAutosaveInCombat - prevents timed autosaves in combat if in [Danger], saves occur between 0-8 seconds after combat ends
   bPreventScriptedSaves - prevents scripts saving the game (via SaveGame, ForceSave, AutoSave and SystemSave commands) - does not prevent vanilla autosaves e.g. saving on cell enter, use the settings menu for those
   bPreventAutosaveInTGM - prevent timed autosaves if godmode is enabled
   bReplaceContinueWithQuicksave - replaces the pause menu's 'Continue' button with a button to create an incremental save
   bAllSavesResetAutosaveTimer - reset the autosave timer when any saves are made - disabling this ensures there will be saves every iAutoSaveTimer seconds but leads to more saves
   bHighlightActiveSave - highlight the active save in the saves list

bNoAltTabPause
Stops the game showing the pause menu on alt-tab, recommend pairing with OneTweak's "Active in Background" option to keep the game running when alt-tabbed.
Options (No Alt-Tab Pause):
  bMuteSounds - mute sounds (excluding music) on alt-tab

bJumpWhileAiming
Allows jumping while aiming or blocking.

bMidairFastTravel
Allows fast-travel in midair.

bNoXPMessages
Stops the XP pop-up and associated sound.
Options (Disable XP Messages):
  bKills
  bDiscoverLocation
  bRewardXPCommand
  bSpeechChallenges
  bHacking
  bLockPick
  bDisarmMines

bBetterAutoWalk
Moving left or right does not cancel auto-walk (Q key).
Options (Better Autowalk):
  bAllowBackwardsAutowalk - allows backwards autowalking by starting the autowalk while moving backwards

bDebugLockpickMenu
Shows the debug lock-pick menu on all lock-pick menus (cheat).

bNoPipboyOnAltTab
Stops the Pip-Boy showing if tab is pressed while alt is held.

bNoUnconciousMessage
Stops the "Actor is now unconscious" message.

bManualReload
Stops the player automatically reloading when the clip is emptied.
Options (Manual Reload):
  bNoReloadOnAmmoPickup - prevents the automatic reload when ammo is picked up and your weapon is empty.
  bPreventFiringAnimWhenEmpty - prevents the firing animation if the clip is empty.
  iAutoReloadClipSizeThreshold - weapons whose magazine is this size or below will reload automatically.
  bAutoWeaponsPlayEmptyClipSound - play the empty clip sound when the clip is emptied for automatic weapons
  bAutoWeaponsOnly - keep automatically reloading semi-fire weapons
  bReloadWhenFiringWithEmptyClip - reload when trying to fire with an empty clip

bUseWASDAsArrowKeys
Allows use of WASD keys in menus, and space to accept - will not function if the keys conflict with menu key-binds.
Also adds a hotkey "TAB" to close any menus excluding Dialogue.
Options (Menu WASD):
  bAlwaysAllowWASD - always allow WASD movement keys by ignoring WASD+E XML menu hotkeys
  bWASDKeysRepeat - holding a WASD key repeats the action, as with arrow keys
  bNoSpaceClosesContainer - stops the space key closing containers
  bInventorySelectionAlwaysVisible - stops the inventory selection disappearing when activating an item with keyboard input
  bContainerDefaultToRightSide - makes the selection default to the right hand side when opening a container menu
  bShiftScalesMapZoomSpeed - holding shift scales the zoom speed
  bShiftScalesContainerArrowKeys - holding shift scales the arrow key scroll speed in containers
  bShiftScalesMousewheel - holding shift scales the mouse-wheel scroll by 4 for all menus
  bMapMenuWASD - holding alt allows WASD to move the map menu, up/down zooms
  bMapMenuWASDCentersSelectionReticle - using map menu WASD resets the selection reticle to the center of the screen
  bSelectWithEKey - make the 'E' key behave like spacebar in menus
  bTabReturnsToInventory - make tab return to the Inventory rather than closing the Pip-Boy for the Weapon Mod and Repair menus
  bListWraparound - make pressing up/down while at the top/bottom of a container jump to the bottom/top
  bHighlightContinueAtMainMenu - automatically highlight the 'Continue' option at the main menu

bHideEnemyMarkers
Hides the enemy markers from the compass.
Options (Compass):
  bShowFiringEnemies - show enemies who are currently firing their weapon (enemies performing an attack animation)

bEquipBrokenItems
Allows equipping of broken items (to allow repair with weapon repair kits or skill bonus from apparel).

bIgnoreCompanionsVATS
Stops VATS targeting companions.
Options (Ignore Companions in VATS)
  bCombatOnly - allow targeting companions in VATS if outside combat

bDontShowContainerAfterLockpick
Stops the container menu showing automatically when opening with lock-pick or a key.

bDontOpenDoorsAfterLockpick
Stop doors being activated automatically when opening with lock-pick or a key.

bKeepPipboyLightOnCellChange
Stops the Pip-Boy light turning off when entering an exterior cell.
Options (Pipboy Light Cell Change):
  bCheckNight - only turn the Pip-Boy light off if it's daytime in the exterior

bLockpickAllowMouse
Allows the use of left clicking to rotate during lock-pick (in addition to the default WASD).

bNoHackingRetryDelay
Removes the delay between hacking attempts (same as changing the game-setting iHackingRetryMilliseconds to 0).

bJumpWhileOverencumbered
Allow jumping while over-encumbered.

bNoMaxCasinoBet
Removes the max bet in casinos and makes increments above 1500 increase by 500 (from 100 default).

bFasterSaveMenuClose
Removes a hard-coded 3 second delay before menu closing when saving using the pause menu.

bNoQuestFailedPopup
Stops the QUEST FAILED showing upon failing a quest.
Options (No Quest Failed):
  bQuestFailedOnlyIfStarted - show the QUEST FAILED but only if the quest was started
  
bNoLocationPopup
Stops the Location Discovered showing.

bNoAmmoCasings
Stops shooting earning the player ammo casings.

bFasterHackingTransition
Decreases the delay after a successful hack by 2.5 seconds.

bKeepRouletteBetAmount
Don't reset the bet amount to 1 after playing roulette.

bConsoleNumpadSupport
Adds support for the numpad buttons /*-+., enter and 0-9 to be used in console.

fCraftedItemHealthPct
Set the condition of the items returned from crafting (default is 80%).

bAllowActivateWhileAnimPlays
Allows activating while firing, reloading, jumping, landing etc. - This means you can start reloading, open a door and finish reloading on the other side.

bPatchUnseenCellName
Appends a * to the activation prompt of doors leading to interior cells that have not been visited e.g. "Door to Saloon*".
Options (Unvisited Cell Indicator):
  bUnnameUnvisitedCells - obscure the cell name to unvisited cells, e.g. Door to...
  bPatchRespawnedCellName - append a + to the activation prompt of doors leading to cells that have re-spawned
  bShowVisitedCellsPrompt - show a * on Visited cells instead of unvisited

bSkipDeathcamHotkey
Adds a hot-key "Left-Alt" to instantly end the player death-cam.

bDescriptiveMarkerAddedMessage
Adds the marker location name to the "Marker marker added." pop-up.

bNoVATSTargetInvisible
Disallow targeting invisible enemies in VATS.

bRemoveDownloadsButton
Removes the useless downloads button from the main menu.

bHideInvisibleUndiscoveredLocations
Only show unvisited locations on the compass if they are marked on the map.

bCompassNPCHeightIndicator
Use custom icons to show whether an NPC is above or below the player (texture path : Data/Textures/Interface/HUD/glow_hud_tick_mark_above.dds and ""/glow_hud_tick_mark_below.dds).
Options (Compass Height Indicator): 
  iHeightThreshold - distance above/below the player before the custom icons are used
  
bCompassQuestHeightIndicator
Use custom icons to show whether a quest marker is above or below the player.
  
bCompassNPCDistanceBasedAlpha
Fade the compass NPC pips based on distance to the player, uses game-settings fSneakMaxDistance and fSneakExteriorDistanceMult.

bCompassLocationDistanceBasedAlpha
Fade the compass location markers based on distance to the player.

bDisableCompassEdgeAlpha 
Disable the alpha effect given to pips on the right edge of compass.

bNoSkillBooksAbove100
Prevents consumption of books if skill level is already at 100.

bNoMinCompanionMapDistance
Removes minimum distance companions are shown on the world map.

bMapShowUnconsciousCompanions
Show unconscious companions on the map, in red.

bCompanionPipColorChange
Customize the color of companions on the compass.
Options (Companion HUD Color):
  uRGB - the red/green/blue value of the color in hexadecimal

bDisableShowQuestLocation
Disables the functionality of the "Show Location" button on the quest menu.

bDisableFastTravel
Disables fast travel.

bRememberBobbyPinHealth
Remembers the bobby pin health between locks (works through saves)

bNoEquippedWeaponMovementPenalty
Removes the movement penalty when holding a weapon.

bRemoveWeaponDamageBuffer
Removes the damage buffer provided for weapons above 75% condition.

bKeepCrosshairWhenAiming
Keep the cross-hair on the screen when aiming with non-scoped weapons.

bRepeatJumping
Holding the jump button repeatedly jumps.

bRemoveSneakLabel
Removes the [HIDDEN] etc. label from the HUD.

bTabClosesTerminals
Adds a hotkey Tab to close terminals.

bTabBackInStartMenu
Adds a hotkey Tab to go back in the start/pause menu.

bContinueGameHotkey
Adds a debug hotkey to continue the game from the loading/start menu for mod development ONLY (since if you press the hotkey too early, mods that utilize JIP's MenuMode 4 will not get a chance to run).

bLevelUpScrollWheelSupport
Adds scroll-wheel support for the -+ skills in the level up menu.

bNoLTRTOnPipboy
Use the Pip-Boy texture without LT and RT painted on when a controller is connected.

bNoRedCrosshairOnEnemies
Stops the cross-hair turning red on enemies.

bAllowOpenPipboyDuringCameraShake
Allows opening of the Pip-Boy when the screen is shaking (will reset the screen shake).

bLeftAndRightCancelEachOther
Makes holding left and right movement keys not move the player (vanilla would move the player left).

bFixEnhancedCameraGroundSinkBug 
Provides a workaround for a bug in the Enhanced Camera mod where the player would sink into the ground when changing from first to third person.

bTalkWhileSneakingIfShiftIsHeld
While sneaking, holding shift will talk to an NPC instead of pickpocketing them.
Options (Talk While Sneaking):
  bInvert - require holding shift to pickpocket

bChargedAttacksCostAP
Adds an Action Points penalty for performing charged unarmed attacks.
Formula: 
  Min(iChargedAttackAPCostMax, iChargedAttackAPCost + (fChargedAttackWeaponWeightAPMult * weaponWeight))
Options (Charged Attacks):
  iChargedAttackAPCost - base number of action points used
  fChargedAttackWeaponWeightAPMult - extra action points per point of weight for the current weapon
  iChargedAttackAPCostMax - max AP cost for a charged attack
  bPreventIfNotEnoughAP - perform normal attacks when holding attack without enough AP

bAddInventoryDropItemHotkey
Adds a hot-key 'Q' to drop the currently selected item from the Pip-Boy menu.

bInstantContinueButton
Skip the "Continue from your last saved game?" prompt when clicking continue game in the main menu.

bUseCustomSniperZoomRate
Set how quickly scoped weapons zoom.
Options (Scope Zoom):
  fScopeFOVTimeChange - rate at which scoped weapons will zoom in, vanilla is 0.25, setting to 0 zooms instantly
  bZoomOutAtSameRate - make the setting also affect zooming out
 
bDistanceBasedQuestMarkerVisibilty
Hide quest markers beyond a set distance.
Options (Quest Marker):
  fMaxExteriorQuestMarkerDistance - maximum exterior distance from which to show quest markers
  fMaxInteriorQuestMarkerDistance - maximum interior distance from which to show quest markers

bQuickUse
Holding shift will equip/use the cross-hair item. Right clicking on a non-armor item will equip it.
Options (Quick Use):
  bRealtimeQuickUse - Holding shift will equip/use the cross-hair item during game-play
  bContainerRightClick - right clicking an inventory item while in a container will equip the item (excludes armor)
  bContainerHotkey - adds a hot-key 'F' to use the selected item in a container (excludes armor)
  bBookSupport - allows quick use on books
  bNoteSupport - show the Book Menu when quick-using notes (requires textures and XML from Book Menu Restored)
  bShowItemStats - show item stats e.g. DPS, DAM, DT and DR while shift is held
  bShowReReadOnSeenNotes - show 'Re-read' on the prompt for notes that have already been read
  bWhileAimingController - quick use when activating while aiming when using a controller

bDecreasedDialogueClickDelay
Halves the delay before you can click on a dialogue option when having a conversation (500ms->250ms).

bHideUnknownNPCNames
Hide NPC names on the prompt if they haven't spoken to the player.
Options (NPC Names):
  bShowNameOnDeadNPCs - show the name if the NPC is dead

bReduceXP
Scale all earned XP.
Options (Reduced XP):
  fXPMultiplier - multiplier applied to earned XP, the result is rounded up
  bPreventRounding - don't ceil the earned XP, storing the fractional component in the cosave

bVatsExitKey
Adds hotkeys Tab and Right Click to instantly end the VATS killcam.
Options (VATS Exit Key):
  bInstantEnd - instantly end VATS playback rather than waiting for the current action to end

bDontSetQuestWhenCompletingObjectives
Don't set the current quest when completing objectives without having a quest active.

bNoExitHacking
Don't allow exiting the hacking menu if an attempt has been made.
Options (Terminal Exit):
  bFailOnEarlyExit - lock out of the terminal if exiting after making an attempt

bSlotsAutoSpinHotkey
Holding W will continually spin the slot machine.

bUKKeyboard
Use the UK Keyboard layout for console and other menus.

bRemoveQuestObjectiveAddedText
Hides the text for added objectives from the main HUD.
Options (Quest Added):
  bHideCompletedObjectivePopup - hides the quest completed objective text

bPickLocksEvenWithKey
Holding shift allows picking a lock/terminal even if you have the key.
Options (Pick Locks With Key):
  bInvert - make holding shift allow using the key to the lock/terminal

bRememberConsoleHistory
Stores/restores console history from ConsoleHistory.txt.
Options (Console):
  iSentHistoryMaxSize - max number of commands to store (default is 200)

bConsoleHistoryNoStoreDuplicates
Prevents consecutive duplicate commands being added to the console's input history list.

bNoKillcamKillSound
Stops the 'Quest Added' sound playing whenever a cinematic killcam is shown.

bNoGrabOwnedItems
Disallows grabbing (Z key) of owned items.

bSkipIntroVideo
Automatically skips the main menu video once loading is finished.

bFirstPersonVATS
Forces VATS firing camera to play in first person.

bAllowUnsafeFastTravel
Allows fast-traveling from indoors (you must be careful not to travel out of scripted areas).
Options (Unsafe Fast Travel):
  bShowWarning - show a warning when travelling from restricted areas.

bRemoveLandingAnim
Stops the landing animation playing.

bHoldCrouchToSneak
Makes sneaking holdable rather than toggle-able.

bFastTravelCostsSpecialNukaBottles
Makes fast travel cost 1 Nuka-Cola Quantum, Quartz or Victory.
Options (Fast Travel Costs Items):
  sItemRequiredMessage - message shown when trying to fast travel without the required items
  sItemRemovedMessage - message shown when items are removed upon fast travel
  sItemEditorID - editor ID of the item or formlist to remove an item from instead of nuka cola

bDisableSellingItems
Removes the ability to sell items in the barter menu.

bUseCustomBarterPriceMultipliers
Set custom buy/sell multipliers for each item type (applied before perk modifiers).
Options (Barter Prices):
  bConstantPurifiedWaterPrice - don't scale the price of purified water
  ; multipliers when you are selling an item
  fSellMultArmor 
  fSellMultWeapon
  fSellMultAid
  fSellMultAmmo
  fSellMultMisc
  fSellMultWeaponMod
  ; multipliers when you are buying an item
  fBuyMultArmor
  fBuyMultWeapon
  fBuyMultAid
  fBuyMultAmmo
  fBuyMultMisc
  fBuyMultWeaponMod

bNumberedDialogHotkeys
Adds hot-keys 0-9 to select dialogue options (recommended use with VUI+).
Options (Dialog Hotkeys):
  bPrependDialogNumberHotkeys - display list numbers for topics in dialogue
  bTabClicksLastTopic - add hotkey 'Tab' to choose the last option.
  
bNoAutoContinueDialog
Stops dialogue with NPCs being skipped automatically unless Shift is held.

bNoSkipDialog
Prevent manually skipping dialog with NPCs when clicking.

bDisableHitShader
Disables the radial blur when damaged (optionally only when in god-mode).
Options (Hit Shader):
  bOnlyDisableInGodmode

iMaxCharacterLevel
Sets the max player level and disables the hard-coded +5 per DLC.

bTerminalInstantDisplayHotkey
Adds hot-keys shift and right mouse button to instantly display the current terminal text, and left mouse to speed up display of submenus.

bSwapKeyboardYZKeys
Swap the Y and Z keys.

bReloadingWithFullClipSwitchesAmmoType
Reloading with a full clips switches ammo type.

bBetterFlycam
Adds AutoMove, flying up and down using Jump and Crouch, rotating pressing Z and C, and scrolling changes flight speed.
Options (Flycam):
  fAimSpeedMult - speed multiplier while aim is pressed
  fRunSpeedMult - speed multiplier while run is pressed
  fScrollSpeedScale - multiplier for how much the mouse scroll-wheel influences fly speed
	fRotateSpeedMult - rotation speed multiplier
  bSmoothCamera - adds a hotkey 'Reload' to enable a smooth/cinematic camera

bNPCsDropWeaponHolsteredWeapon  
Allow enemies to drop weapons on death even if they are not out.

bDisableReloadingNonEmptyClip
Prevents reloading if the weapon's clip is not empty.
Options (Disable Reloading Non-Empty Clip):
  bEnergyWeaponsOnly - only prevent reloading energy weapons
  bExcludeLoopingReloadWeapons - allow reloading non-empty weapons if they use a looping reload

bDisableGrenadeIndicator
Removes the grenade indicator from the HUD.

bWeightlessWornPowerArmor
Power armor is weightless while equipped.
Options (Weightless Worn Power Armor):
  bRequireTorsoArmorForWeightlessHelmet - make power armor helmets only weightless if torso power armor is also equipped
  bRequirePowerArmorTraining - only make power armor weightless for the player/teammates if they have the Power Armor Training perk
  fWeightMult - multiplier applied to worn armor weight
  
bWeightlessWornArmor
Armor is weightless while worn.
Options (Weightless Worn Armor):
  fWeightMult - multiplier applied to worn armor weight

bShiftScreenshotHidesMenus
Holding shift when taking a screen-shot hides the menus.

bFastTravelWithEnemiesNearby
Allows fast travel while enemies are nearby.

bFastTravelOverencumbered
Allow fast travel when over-encumbered, as the Long Haul perk does.

bNoKnockdownInGodmode
Disables the player being knocked down when in god-mode, may break scripted sequences.

bDoubleTapReloadToChangeAmmoType
Double tapping the reload key will change ammo types.
Options (Double Reload Swaps Ammo Type): 
	bAllowMultipleQuickChanges - pressing Reload additional times will swap the ammo type
	iAmmoSwapTimeMS - time in milliseconds that the Reload key must be pressed within to swap ammo types

bForceLockpickNoBreakLock
Failing a lock-pick force attempt breaks a bobby pin instead of the lock.
Options (Lockpick):
  bLockpickForceResetPinHealth - reset the current bobby pin health when failing to force a lock
  bPreventUseLockWithNoBobbyPins - prevents the LockPick Menu opening when the player has no bobby pins
  sBobbyPinBreakMessage - message shown when a bobby pin breaks

bDisableControllerDeadzones
Set a custom dead-zones for controller thumb-sticks, allowing finer movement and aiming.
Options (Controller Deadzone): 
  iControllerDeadzone - dead-zone value (between 0 and 32767)

bFasterControllerPOVRotate
Increase controller rotation speed of the vanity camera when looking around with POV held.

bHideCursorInDialog
Hide cursor while in Dialogue menus.
Options (Dialog Hide Mouse): 
  bOnlyWhenNPCSpeaks - only hide the cursor while the NPC is talking

bFasterTitleMenu
Remove the wait for the Fallout New Vegas logo to be at full alpha.
Options (Faster Main Menu):
  bSkipLoadScreenWait - skip the 0-3s wait for the current load screen to fade out

bShiftIgnoresFriendlyVATS
Holding shift ignores friendly NPCs when entering VATS.
Options (VATS):
  bHideFriendliesByDefault - inverts mod behavior so holding shift SHOWS friendly NPCs.

iPerksPerLevel
Perks to earn per level - note: Perks that show a menu after being selected are incompatible with each other, e.g. Intense Training and Tag!.

bDisableExplosionInFaceIMOD
Disables the radial blur when an explosion occurs nearby.

bModifySkillPointsEarned
Modifies skill points earned on level-up.
The formula is : iSkillPointBase + ceil(Intelligence * fPointsPerInt)
Options (Skill Points):
  iSkillPointBase - base skill points before Intelligence bonus is added
  fPointsPerInt - skill points earned per intelligence

bLuckDoesntAffectGambling
Removes the luck skill's effect on gambling by initializing the Gambling Menus with a luck of 5.
Options (Gambling Luck Override):
  iBaseLuck - value to use for luck:
    - above 5 gives an advantage
    - below 5 gives a disadvantage
    - 5 removes luck's effect on gambling

bRemoveChemWarnOffIMOD
Removes the chem worn off screen effect.
  
bAdjustableScopeZoom
Allows scroll-wheel to zoom while using a scope.
Options (Adjustable Zoom):
	fZoomRate - rate at which weapons are zoomed
	fShiftZoomModifier - multiplier applied to zoom rate while shift is held
  bResetZoomOnWeaponChange - resets the current zoom when changing weapons
  bZoomableNonScopedWeapons - allow zooming on non-scoped weapons
  bSmoothScrollZoom - apply smoothing to the change in zoom
  bDpadSupport - prevent DPAD hotkeys while aiming and use DPAD Up/Down for zooming
  bBinocularsOnly - only allow zooming on weapons with no projectile (e.g. binoculars)
  iScopeResetTimeMS - resets the current zoom if unscoped for this long, set to 0 to disable
  fMinFOV - minimum scope FOV (max zoom)
	fMaxFOV - maximum scope FOV (minimum zoom)
  fMinFOVMult - minimum multiplier applied to weapon FOV (max-zoom)
  fMaxFOVMult - maximum multiplier applied to weapon FOV (min-zoom)
  iZoomInKey - key to zoom in (while held)
  iZoomOutKey - key to zoom out (while held)
  
bPopupMenusDontMoveCursor
Prevents pop-up menus moving the mouse to the center of the screen.

bAddNightVisionToggle
Pressing the iTogglePipboyLight key while aiming with a night vision weapon toggles off the night vision effect.
Options (Night Vision):
  bDisableVisionByDefault - disables night vision for weapons until the toggle key has been pressed
  bAllowNightVisionDuringDay - allow night vision during daytime
  sToggleOnSound - sound to play when enabling night vision
  sToggleOffSound - sound to play when disabling night vision

bScopeHoldBreath
Holding shift decreases scope wobble at the cost of Action Points.
Options (Hold Breath):
  iScopeHoldBreathAPDrain - AP cost per interval
  iScopeHoldBreathAPDrainIntervalMS - interval length in milliseconds
  fScopeHoldBreathWobbleMult - wobble multiplier while breath is held
  bRequireWeaponStrength - only allow holding breath if you have the required weapon strength
  bRequireWeaponSkill - only allow holding breath if you have the required weapon skill
  iHoldBreathKey - scancode of keyboard key to hold breath
  bActivateHoldsBreath - hold breath while the Activate bind is held
  
bPowerArmorScalesFallDamage
Wearing power armor scales fall damage.
Options (Power Armor):
  fFallDamageMult - fall damage multiplier
  bPlayerOnly - only affect the player

bAgilityScalesMovementSpeed
Agility is scaled by fAgilityMovementSpeedMult for every point above or below 5, the latter slowing down the player.
The formula is: speedMult = normalSpeedMult * (1 + (agility - 5) * fAgilityMovementSpeedMult).
Options (Agility Scales Movement Speed):
  fAgilityMovementSpeedMult - additional movement multiplier per agility point above 5. Agility below 5 is scaled down.
  bNPCs - scale NPC movement speeds
	bPlayer - scale player movement speeds

bDisableWeaponFOV
Disables zooming when aiming with non-scoped weapons.
Options (Weapon FOV):
  bExcludeNonSightedWeapons - only disable the zoom for weapons that have ironsights

bDisableHolsteredWeaponFOVZoom
Disables zooming when aiming with a weapon holstered.

bNoCapitaliseContainerCategories
Stops the container category titles being capitalized (you will need to change the AMMO title game-setting since it's capitalized in the actual setting, unlike Aid, Weapons and Armor).

bUnequipBrokenArmor
Automatically unequip armor when it breaks.
Options (Unequip Broken Armor):
  sArmorBreakMessage - UI message when armor breaks

bWeaponRequirementsMatter
Don't allow equipping of weapons without the required strength and skill.
Options (Weapon Requirements Matter):
  bIgnoreStrengthRequirement - ignore strength requirement for all weapons
  bIgnoreNonHeavyStrengthRequirement - ignore strength requirement for weapons that aren't of type 'Two Hand Launcher' or Two Hand Handle'
  bIgnoreSkillRequirement - ignore skill requirement
  bIgnoreThrowables - ignore requirements for grenades, mines and throwable weapons
  sSkillAndStrengthRequiredMessage - shown if you don't meet the strength and skill requirements to use a weapon
	sStrengthRequiredMessage - shown if you don't meet the strength requirements to use a weapon
	sSkillRequiredMessage - shown if you don't meet the skill requirements to use a weapon
  
bSneakAttackWithoutCrouching
Allow sneak attacks while standing.

bDisableLoadingScreenTips
Removes the tips from loading screens.

bDisableCompanionKillcam
Prevents the killcam being activated by companion kills.

bPauseOnSaveLoad
Automatically pause the game when loading a save.

bDisableInteriorFog
Removes non-static fog from interiors.
Options (Interior Fog Remover):
  fFogFarDistanceThreshold - distance over which far fog is removed - setting too low will cause visual bugs in some caves

bImprovedHacking
Improves various aspects of the hacking mini-game.
Options (Hacking):
  bNoSingleCharacterAttempts - prevents single character attempts while hacking, i.e. clicking on "/" will do nothing rather than waste an attempt and clutter the guesses output.
  bRemoveDudIfAllowanceFull - remove a dud instead of replenishing allowance if allowance is already full
  bNoAllowRepeatWords - prevent attempts at guessing the same word
  bNoSpecialInputPrinting - don't print the clicked on string with the "Dud Removed" and "Allowance replenished." messages
  bNoRemoveGuessedWords - make 'Dud removed.' ignore guessed words (unless they're the only words left)
  bCompactGuesses - prints guesses as a single line without the 'Entry denied', e.g. HORIZON (1/7)
  bOverscroll - make scrolling to the edge of the screen wrap around to the other side (controller or WASD)
  bMarkGuessesAsDuds - turn incorrect guesses into ..... when clicking on them
  bMarkGuessesAsDudsKeepMatchingCharacters - keep matching characters when marking guesses as duds, e.g. A.S..ING
  iAllowanceReplenishedBonus - give a bonus number of attempts when finding a 'Replenish Allowanced' instead of setting attempts to the max (e.g. 4 in vanilla)

bLockNeedsKeyShowName
Adds the name of the required key to the end of the sImpossibleLock message. Note: some keys are just named "Key" in the base game - see https://fallout.wiki/wiki/Fallout:_New_Vegas_keys

bScopeVisibleAPHP
Adjust visibility of HUD elements while scoped.
Options (Scope HUD Visibility):
  iFlags - hexadecimal value containing the sum of all the desired flags. e.g. 0x00000001 would just be ActionPoints visible; 0x00000003 is HitPoints and ActionPoints; 0x000011A0 would be XpMeter, Messages, SneakMeter and RegionLocation visible.
Flags:
 ActionPoints = 0x1
 HitPoints = 0x2
 RadiationMeter = 0x4
 EnemyHealth = 0x8
 QuestReminder = 0x10
 RegionLocation = 0x20
 ReticleCenter = 0x40
 SneakMeter = 0x80
 Messages = 0x100
 Info = 0x200
 Subtitles = 0x400
 Hotkeys = 0x800
 XpMeter = 0x1000
 BreathMeter = 0x2000
 ExplosivePositioning = 0x4000
 CrippledLimbIndicator = 0x8000
 HardcoreMode = 0x10000

bDelayPostCombatLevelUp
Adds a 3s delay after combat before the LevelUp menu will show.

bJumpingDoesntDropGrabbedItem
Stops the grabbed item being dropped when jumping.

bNoMapMarkerAddedPopup
Disables the Map Marker Added popup.

bGodmodePreventsLegCrippleSound
Prevents the leg crippled sound in godmode.

bNonSelectablePlayerInConsole
Prevents the player being selected when clicking in console.

bExtraConsoleDetails (enabled by default)
Adds extra information when a ref is selected in the console.
Options (Extra Console Details):
  bUseFullHelp - show the extra details from the ToggleFullHelp command (attached scripts etc.)
  bCellName - show the current player cell name at the top left
  bCellEditorId - show the editor ID of the current player cell at the top left
  bMeshPath - show the mesh path of the selected ref

bPrintErrorsToConsole
Print vanilla debug errors to console.
Options (Logging):
  bGeneralErrors - print general errors
  bHavokErrors - print Havok errors
  bHavokOldRigidBodyErrors - print 'Old hkpRigidBody' errors
  bSaveLoadErrors - print save/load errors
  bGeneralMessages - print various general messages
  
bHideMiscQuestItems
Hide quest items in the misc Pip-Boy page
Options (Hide Misc Items):
  bDontHideStarCaps - show Sunset Sarsaparilla Star caps
  
bPickpocketOverhaul
Alters the pickpocket formula to take into account item weight, target perception and detection value. Note: the game-settings fPickpocketMaxChance and fPickPocketMinChance are still applied.
Options (Pickpocket Overhaul):
  bRewardXP - gain XP from successful pickpocketing
  bShowPickpocketSuccessRate - add the pickpocket success chance to the bottom of the container menu
  sSuccessMessage - message shown at the bottom of the container menu containing success percentage
  bReversePickpocketPenaltyLiveGrenadesOnly - only lose karma when reverse pickpocketing if it's a live explosive
  bPickpocketKarmaFriendlyNPCsOnly - only lose karma when pickpocketing from non-hostile NPCs
  bIgnoreFreeItems - allow taking free items (e.g. keys) without getting caught as in vanilla
  fBaseChance
  fPlayerSneakMult
  fItemValueMult
  fItemWeightMult
  fTargetPerceptionMult
  fDetectionValueMult
  fPlayerLuckMult
  fPlayerAgilityMult
  fWornItemChanceMult - multiplier applied to items that are currently worn
Formula:
	PickPocketChance = fBaseChance + (playerAgility	* fPlayerAgilityMult) + (playerLuck * fPlayerLuckMult) + (playerSneak	* fPlayerSneakMult)
		- (targetPerception * fTargetPerceptionMult) - (detectionValue * fDetectionValueMult) - (itemValue * fItemValueMult) - (itemWeight * fItemWeightMult))
  
  If the item is worn by the NPC, the total chance is multiplied by fWornItemChanceMult.

  XPReward = itemWeight * fItemWeightMult + (itemValue * fItemValueMult) + targetPerception

bRepairsRewardXP
Earn XP when repairing items.
Options (Repair):
  iRepairRewardXP - XP rewarded per item

bKillsRewardAP
Earn Action Points when killing outside of VATS.
Options (Kill AP Reward):
  iKillRewardAmount - AP rewarded per kill
    
bNoHUDHotkeyPopup
Prevent the hotkey wheel showing when holding a hotkey.

bClipSizeMatters
Prevent firing if you don't have enough ammo for one burst.

bHUDShowRegionNames
Show interior cell names in the HUD region text where the 'Mojave Wasteland' text is.
Options (Region Names):
  bRegionNamesUpdateNearMapMarkers - show the name of map markers when approaching them

bNoCompanionKillXP
Don't reward XP for companion kills - stops companion's attack damage increasing the 'player dealt damage' used when comparing for iXPDeathRewardHealthThreshold.
Options (Companion Kill XP):
  bCompanionHitsCountAfterPlayerDamage - companion hits count towards the iXPDeathRewardHealthThreshold after the player has hit the NPC

bHideAmmoLabel
Hide the clip/remaining label from the main HUD.
Options (Clip Rounds):
  bShowTotalRemaining - show the total ammo count instead of clip/remaining

bNoAPRegenWhileOverencumbered
Scales AP regeneration while over-encumbered.
Options (Overencumbered AP):
  fOverencumberedAPRegenScale - scale applied to the Action Points regen rate while over-encumbered
  bWhileMovingOnly - only apply the scale while the player is moving

bDisableCharacterRespec
Disable the character recreation script that runs when leaving the spawn area.

bNoReputationMessages
Disables the reputation pop-ups and messages.
Options (Reputation):
  bHidePopups - prevent the pop-up menus that require being click out of (e.g. Vilified)
  bHideGainMessages - prevent the top left corner messages when gaining reputation
  bHideLossMessages - prevent the top left corner messages when losing reputation
  bHideNonScriptedLossesIfAtMin - prevent loss pop-up and message only if already at the min reputation and if the change was not from a script command
  bHideNonScriptedGainsIfAtMax - prevent gain pop-up and message only if already at the max reputation and if the change was not from a script command
  
bShowInventorySortButton
Add a button to sort/filter the inventory, specified by menus\prefabs\lStewieAl\SortInventoryButton.xml.
Use Shift/Control click to cycle through filtering modes.
Options (Inventory Button):
  bBarter - add button to the Barter menu
  bContainer - add button to the Container menu
  bPipBoy - add button to the Inventory menu
  iMode
    0 - Hide by Weight
    1 - Sort by Weight
    2 - Hide Quest Items
    3 - Hide by Weight and Quest Items
    4 - Hide by Weight and Quest Items and Sort By Weight
    5 - Sort by Value Per Weight,
    6 - Show Healing Items,
    7 - Show Food Items,
    8 - Show Water Items,
	9 - Show Radiation Decreasing Items

  iHideModeFlags - hexadecimal value containing the sum of all the desired flags. e.g. 0x282 would prevent Show Radiation Decreasing Items, Show Food Items and Sort By Weight.
    0x1 - Hide by Weight
    0x2 - Sort by Weight
    0x4 - Hide Quest Items
    0x8 - Hide by Weight and Quest Items
    0x10 - Hide by Weight and Quest Items and Sort By Weight
    0x20 - Sort by Value Per Weight,
    0x40 - Show Healing Items,
    0x80 - Show Food Items,
    0x100 - Show Water Items,
	0x200 - Show Radiation Decreasing Items
    
  fHideWeightThreshold - threshold weight for hiding items in Hide By Weight modes
  bUseAlphaForEnabledIndicator - brighten the sort button while sorting/filtering is active instead of using a separate icon for inactive sorting
  iControllerHotkey - button to toggle sorting
  iControllerCycleModeKey - button to cycle through sorting modes
    5 -  Start
    6 -  Back
    9 -  A
    10 - B
    11 - X
    12 - Y
    15 - LB
    16 - RB
    17 - LS
    18 - RS

bClickingActiveTabTogglesSorting
Clicking on the current Pip-Boy inventory tab toggles sorting/filtering.

bAllowRebindNumkeys
Show the number hotkeys in the Controls menu and allow binding controls to the DPAD (note it will conflict with any bound weapon hotkeys). Note Darnified UI does not support additional items in this menu due to a bug.

bDisableWeaponHotkeys
Ignore the DPAD and 1-9 weapon keys outside the Pip-Boy.

bDisableHUDCrippledLimbIndicator
Prevents the vaultboy showing on the HUD when a limb is crippled (not the 'LMB' text).

bConsoleBackground
Adds a background to the console, specified by menus\prefabs\lStewieAl\ConsoleBackground.xml.

bIndividialItemStats
Show weight and value for an individual item when viewing stacks of items, instead of the entire stack's weight/value.

bOnlyAllowWaitWhileSitting
Only allow waiting while the player is sat down or in godmode.
Options (Sleep Wait):
  bSitWaitShowMessage - show a message when waiting is prevented
  sSitToWaitMessage - ui message shown when attempting to wait while standing
  bSitWaitShowTime - show a message with the current time when waiting is prevented


bAddRGBSliders
Add RGB sliders for the main HUD color to the settings menu. Note Darnified UI does not support additional items in this menu due to a bug.
Options (RGB Sliders):
  bTerminalsUseHUDColor - make terminals copy the HUD color

bShowCurrencyInContainers
Show faction currencies in the misc page for containers, and show Caps in the Pip-Boy misc tab.

bHideGrenadeIndicatorForNoDamageExplosions
Hide the grenade indicator for projectiles whose explosions do no damage.

bUnspokenNPCIndicator
Add a * to the prompt for NPCs who haven't been spoken to.

bNoScaleNpcDamageThresholdByCondition
Don't scale NPC armor damage threshold based on condition.

bNoScaleNpcDamageResistanceByCondition
Don't scale NPC armor damage resistance based on condition.

bNoScaleNpcDamageByCondition
Don't scale damage by NPCs based on their weapon condition.

bSortUnavailableRadiosToBottom
Fix a vanilla bug where unavailable radios aren't sorted to the bottom of the list.

bRemoveFollowerTopics
Prevents companions saying when they are injured, needing ammo, weapons etc.

bDisableTutorialMessages
Disables hard-coded one-time tutorial menu messages, e.g. hacking, lockpick, Pip-Boy. Does not disable non-hardcoded messages such as "Press V to use VATS" etc. 

bBarterCheckActorBuySellFlags
Make vendors obey their Buy/Sell flags, hiding items the vendor doesn't accept.
Options (Barter Use Buy Sell Flags):
  bAmmoRequiresWeapons - only buy/sell ammo if vendor buys/sells weapons
  sPerkEditorID - editor ID of a perk for ignoring the buy/sell flags

bKeepSelectedConsoleRef
Remembers the selected ref when closing the console (provided it is still loaded).

bNoFastTravelTimeChange
Don't progress time or hardcore needs when fast traveling.

bSleepInOwnedBeds
Allow sleeping in owned beds.

bDetectedByWhom
Show the names of actors detecting you while sneaking, e.g. Replaces [DETECTED] with [Detected by: Easy Pete, Sunny Smiles, and 2 others]
Options (Detected By Whom):
  iMaxNameCount - names to display before showing "and N others"
  sDetected - starting string for list ([Detected by: )
	sActors - string shown when the max name count is 0
	sOthers - string shown when more than iMaxNameCount actors are detecting the player
	sPlural - appended to 'and %d other(s)'

bRunningCostsAP
Adds an Action Points cost for running.
The formula is: apCost = fAPDrainCostBase + ((5 - Endurance) * fRunAPEnduranceMult).
apCost action points are removed every iAPDrainIntervalMS milliseconds.
Options (Running Costs AP):
  fAPDrainCostBase - base action points cost
  fRunAPEnduranceMult - endurance multiplier
  fSneakAPDrainCostBase - base action points cost while sneaking
  fSneakRunAPEnduranceMult - endurance multiplier while sneaking
  iAPDrainIntervalMS - time between AP reductions
  bAllowRunWithoutEnoughAP - always allows running, preventing AP gain when at 0
  fRunSpeedMult - speed multiplier applied while running overencumbered

bHideCompletedQuests
Don't display completed quests in the Pip-Boy Quests tab.

bHoldWaitKeyToShowMenu
Makes the sleep/wait button require to be held instead of instantly showing when pressed.
Options (Wait Key):
  iKeyHoldTimeMS - time the wait key must be held before the wait menu is shown

bUseFallout3AudioDistortion
Use a distortion algorithm similar to the one in Fallout 3 for NPCs wearing masks (sounds more metallic and less muffled)

bKeepXPBarWhenClosingMenus
Stops the XP bar being hidden when closing a menu (e.g. Hacking, Dialogue or Lockpicking)

bPickLocksWithoutSkill
Allow picking locks of any level.
Options (Remove Lock Skill Requirement):
  bModifyDifficulty - scale the difficulty of locks based on your skill deficit
    Formula: sweetSpot = vanillaSweetSpot * (skillLevel / skillReq)

bHackTerminalsWithoutSkill
Allow hacking terminals of any level.

bTurnFurtherWhileSeated
Increase the maximum rotation while seated to -115° <-> 115° (from vanilla -90° <-> 90°) in first person, and full 360° in third person.

bLootUnconsciousVictims
Allows unconscious actors to be looted.

bColorRecentlyAddedMapMarkers
Show map markers added this session in red. Map markers given to you are displayed in red until the save is reloaded.

bOpenPipboyToInventoryByDefault
Makes the Pip-Boy always open to the inventory page when the MenuMode key is pressed (F1/F2/F3 still navigate to their respective categories).
Options (Default Pipboy Tab):
  iTab - default category and tab to open
  STATS
    Status = 0,
	SPECIAL = 1,
	Skills = 2,
	Perks = 3,
	General = 4,
	Last-Selected When Closing Pip-Boy = 5
  ITEMS
	Weapons = 16,
	Apparel = 17,
	Aid = 18,
	Misc = 19,
	Ammo = 20,
	LastSelected = 21,
  DATA
	LocalMap = 32,
	WorldMap = 33,
	Quests = 34,
	Misc = 35,
	Radio = 36,
	LastSelected = 37,


bShowWeaponAmmoUseInMenus
Show the ammo used per shot when viewing a weapon in the inventory. e.g. when viewing a Tri-Beam Laser Rifle, the ammo display will be "MF Cell x 3".

bNoPlaceMarkerPopup
Don't show the Place/Remove marker when placing markers on the map.
Options (Place Marker Popup):
  bPlaceMarkerShiftToReset - makes right clicking always place the map marker (instead of toggling it being placed/removed). If shift is held while clicking, the marker will be removed.
  bResetIfHovered - makes right clicking place the map marker, removing only if hovering over an existing marker

b24HourSleepWaitClock
Changes the sleep/wait clock to be in 24 hour format.

b12HourPipboyClock
Changes the Pip-Boy clock to be in 12 hour format.

bContainerRespawnsMessage
Adds a warning in the subtitles bar if the opened container is set to respawn.
Options (Container Respawn Warning):
  sWarningText - warning message shown on containers that respawn
  bHideOnNPCs - hide the warning on NPCs

bLocalMapRespawnedCellIndicator
Show respawned cells as red, and visited cells as white on the local map.
Options (Respawned Cell Indicator):
  bColorRespawnedCells - color respawned cells in red
  bColorUnvisitedCells - color unvisited cells in white

bNoPlaceMarkerPopup
Don't show the Place/Remove marker when placing markers on the map.

bBetterPickupPrompt
Show the value and weight for a whole stack of items while looting and indicate the weight in red if it would overencumber you.

bHideEquippedItemsInBarter
Hides equipped items in the barter menu.

bHideEquippedItemsInContainers
Hides equipped items in the containers.

bNoFoodWornOffMessage
Prevents the 'worn off' message for chems.
Options (No Worn Off Messages):
  bFoodOnly - only hide food worn off messages

iDateFormat
Use a custom date format for the Pip-Boy and Sleep/Wait menus.
Values - 0: MM.DD.YY, 1: DD.MM.YY, 2: YY.MM.DD

bQuestTextVisibleWhileAiming
Stops the quest/location texts being hidden when aiming.

bAllowTeammatesUseMeltdown
Allow teammates to use the meltdown effect if the player has the Meltdown perk.

bNoSelfExplosionDamage
Prevents damage from your own explosions (NPCs can still harm themselves).

bNoSelfMeltdownDamage
Prevents damage from your own explosions from the meltdown perk.
Options (No Self Meltdown Damage):
  bPreventDamageByTeammates - prevent teammates triggering meltdown and damaging the player
  bPreventDamageToTeammates - prevent teammates being damaged by meltdown
  bPreventDamageToNonHostiles - prevent damage to non-hostile NPCs from meltdown explosions

bHoldToActivate
Hold the activate key instead of pressing it to activate various objects:
Options (Activate Key):
  bContainers - looting and searching NPCs
  bFurniture - interacting with furniture (includes beds)
  bWater - drinking from a tap or puddle
  bCrafting - campfires, crafting benches and reload benches
  bTakeItemsWhileKeyHeld - takes items while the activate key is held (doesn't activate containers, NPCs etc.)
   iActivateKeyTakeItemsHoldTimeMS - delay before items will be taken with bTakeItemsWhileKeyHeld
   bAutoPickupEncumbranceThreshold  - prevent auto-pickup of items that would encumber the player, unless the player is already encumbered
  bStealing - delay stealing the first item within iStealTimerMS milliseconds
  iStealTimerMS - interval (in milliseconds) after stealing where no delay is required to steal again

bRememberPipboyScrollPositions
Store Pip-Boy scroll positions between sessions (per save).

bNoWeaponConditionDamagePenalty
Weapons always deal their max damage regardless of condition.

bPlayerMeleeDamageIgnoresScale
Makes the player's melee damage independent of their height/scale.

bHideMapMarkerFactionReputation
Hide the faction reputation from map markers on the world map.

bCompareWeaponStats
Show - and + on weapon DPS/DAM relative to the equipped weapon.

bSleepWaitAnywhere
Allow sleeping/waiting anywhere.
Options (Sleep Wait Anywhere):
  bCombat
  bInRadiation
  bMidair
  bTakingDamage
  bUnderwater
  bTrespassing

bNoInteriorBlackLoadingScreen
Remove the black loading screen when loading an interior cell, and prevent actors being faded in.
Options (Interior Transition):
  bFadeIn - fade the edges of the screen based on the fFadeToBlackFadeSeconds game-setting

bCharacterMeleeDamageIgnoresScale
Stops NPC and player scale affecting their melee damage.

bSkipSkillMenuIfNoPointsToAssign
Skip the assign skill points screen if you have no points to assign but have perks to assign.

bCustomArmorConditionPenalty
Allow a custom scale applied to armor DR/DT based on their condition.
Formula: dtScale = (health > 0.5 ? 1 : (1 - (0.5 - health) * fScale))
Options (Armor Condition Penalty):
  fScale - scale applied to DR/DT when below the condition threshold

bHittingWeaponsDoesntDamageThem
Prevents player and enemy weapons being damaged when shot at.

bNoExteriorLoadScreens
Removes load screen backgrounds when exiting interiors (intentionally excludes when loading a save).

bUltrawideSupport
For ultrawide (21:9) fixes the bugs: 
- The size of the "Fade-to-black" transition now takes up the entire screen instead of a small rectangle (as seen when loading a save or transitioning between areas).
- Adjusts the FOV for various rendered menus such as the Vigor Tester, Terminal and LockPick menus, and the HUDMainMenu for scope zoom. This fixes the menus being too zoomed in.
Options (Ultrawide Support):
  fMenuFOVScale - scale applied to menus/scope. Vanilla uses 0.75.

bCharacterNonMeleeDamageIgnoresScale
Stops NPC and player scale affecting their non-melee damage.

bPlayerNonMeleeDamageIgnoresScale
Stops player scale affecting non-melee damage.

bWeightlessAidItems
Makes aid items weightless in non-hardcore.

bWeightlessItems
Makes items weightless (by category).
Options (Weightless Items):
  bArmor
  bAid
  bAmmo
  bWeapons
  bMisc
  
bHideCrosshairInFirstPerson
Hides the crosshair in first person (keeping it in third person).  

bHideCrosshairInThirdPerson
Hides the crosshair in third person (keeping it in first person).

bNoCasinoBans
Prevents bans from casinos.

bNoSneakAttacksCriticals
Disables sneak attack criticals by the player.

bNPCsCanSneakCritPlayer
Allows NPCs to land sneak attack criticals on the player and on each other.
- can be used alongside bNoSneakAttacksCriticals (making it "No Player Sneak Attack Criticals")

bNPCsCanDisarmPlayer
Allows NPCs to disarm the player.

bSneakCriticalsOnlyMeleeWeapons
Only allow sneak attack criticals with melee weapons.

bShowQuestAndNoDRDTItemsInRepairMenu
Unhide quest items and armors with no DR or DT from the repair services menu.

bDisableGodmodeOnLoad
Disables godmode when loading/reloading a save.

bInvertContainerTitleScrollwheelDirection
Inverts the direction of category change when using scroll-wheel on a container's title.

bHUDFatigueIndicator
Adds a fatigue indicator similar to the FOD and H2O labels in hardcore.

bAllowWeaponHotkeysAndPipBoyWhileReloading
Allows switching weapons using weapon hot-keys, and opening the Pip-Boy while reloading.

bNoDisarmCompanions
Prevents companions being their weapons in combat.

bAllowFiringWhileLanding
Allows firing weapons while lower body animations are playing.

bFireWhileAiming
Allows firing weapons while aiming in and out.

bDontAllowConsoleTillLoadingIsDone
In vanilla it's possible to load a save using the console before settings (e.g. disable controller) have been loaded, this prevents opening the console till this loading has finished.

bPowerAttackWhileOverencumbered
Allow melee power attacks while overencumbered.

bSlowBreathRegen
Slowly regenerate the H2O meter when not underwater instead of instantly refilling it when resurfacing.
Options (Water Breath):
  fBreathRegainRate - rate at which breath is restored to max - setting to 1.0 restores the entire bar in 1 second, 0.5 in 2 seconds etc.
  bShowBreathMeterOutOfWater - show the breath meter when not underwater if it's not 100%

bNoteMenuShowSeparateMenu
Show the scroll menu when clicking on a note in the Pip-Boy (requires textures and XML from Book Menu Restored).
Options (Note Menu):
  bRequireShiftHeld - require the shift key to be held to show the note menu

bDontSetQuestWhenObjectivesAdded
Don't set the current quest when gaining a new objective when you have no quest active.

bSpinWeaponsSoundFix
Fixes a bug where looping attack weapons would not play their attack sound when briefly stopped. 
For example in the base game, tapping and then holding the fire button with the Flamer or Mini-gun held would result in no fire sound playing.

bTurnSlowerWhileAiming
Scale look rotation speed while aiming.
Options (Turn Speed):
  fAimingScaleX - scale applied to X axis rotation while aiming
  fAimingScaleY - scale applied to Y axis rotation while aiming

bShowSneakLabelWhileStanding
Show the [Sneak] indicator while standing.

bVATSAutoTargetHead
Automatically target the head when entering VATS.

bOnlyChangeCameraHeightIfPOVKeyHeld
Scrolling only changes camera height if the 'Change View' key is held.

bCompareArmorStats
Show - and + on armor DT and DR relative to the equipped armors.

bAllowVATSWhileAnimsPlay
Allow entering VATS while animations play (e.g. while jumping).

bRobotCompanionsHealWithScrapMetal
Heal robotic companions with scrap metal instead of stimpaks.
Options (Robot Companion Healing):
  fBase - base health restored per scrap metal
  fRepairMult - bonus health restored per player repair skill
  fRoboticsExpertBonus - bonus health restored if the player has the robotics expert perk
  sHealingItemName - editor ID of the healing item for robots
  
bCustomScreenshotFormat
Automatically convert taken screenshots into various formats. Currently supported formats are: jpg, tiff and bmp.
Options (Screenshot Format):
  bCopyToClipboard - copies the screenshot to the clipboard
	sExtension - file format (jpg, tiff, png or bmp)
	iJpgQuality - jpg quality (0-100)
	sTiffCompression - tiff compression (None, Rle, LZW)
	iTiffColorDepth - tiff color depth (1, 4, 8, 24 or 32)

bModConsolePrintsIncludeName
When a mod prints to the console, prepend the [Modname] to the text. Optionally print the formid of the script that printed it.
Options (Mod Console Prints):
  bIncludeScriptID - prepend the script ID instead of the mod name

bScaleRadioSongVolumeDuringDialogue
Scale the volume of radio songs while in conversation with an NPC.
Options (Radio Volume):
  fDialogueSongVolumeMult - multiplier applied to song volume during dialogue

bScaleMusicVolumeDuringDialogue
Scale the volume of ambient music while in conversation with an NPC.
Options (Music Volume):
  fDialogueMusicVolumeMult - multiplier applied to music volume during dialogue

bUseFirstPersonEmptyClipSound
Use the first person empty clip sound in third person (it's louder).

bMenuSearch
Add Control F to search various menus.
Options (Menu Search):
  bMapMenu - MapMenu (Local Map, World Map, Quests, Notes, Challenges and Radio)
  bInventoryMenu - InventoryMenu (Pip-Boy)
  bStatsMenu - StatsMenu (Effects, Skills, Perks, Reputations, Misc Stats)
  bBarterMenu - BarterMenu
  bContainerMenu - ContainerMenu
  bLevelUpMenuSearch - LevelUpMenu (perks)
  bRecipeMenuSearch - RecipeMenu
  bSaveMenuSearch - StartMenu save/load 
  bRemoveFilterWhenClosingSearch - refresh the menu when closing the search (set to 0 if you want to use keyboard hotkeys to navigate filtered menus)
  bClearInputWhenReopeningSearch - clear the input string when focusing the search-bar, forced to 1 if bRemoveFilterWhenClosingSearch is also 1
  bQuestIncludeObjectives - also search objective text when filtering quests
  bQuestIncludeCompletedObjectives - include completed objectives if bQuestIncludeObjectives is enabled
  
bAllowKeyboardAndMouseWithControllerConnected
Allow use of keyboard and mouse to move around (excludes menus) while a controller is connected.

bScaleCriticalDamage
Multiply critical damage for all weapons.
Options (Critical Hits):
  fCriticalDamageMult - multiplier applied to weapon damage for critical hits

bCookableGrenades
Holding grenades decreases their detonation timer.
Options (Cookable Grenades):
  bDisableGrenadeDistanceIncrease - always throw grenades the same distance regardless of time held
  bOvercookedGrenadesExplode - overcooked grenades will explode in your hand
  fMinGrenadeTimer - minimum detonation timer for thrown grenades
  bPlaySound -  play a sound every second a grenade is held
  bTimerCountdown - play the sound for the last 3 seconds of the timer
  sSoundName - editor ID of the sound to play
  sSoundNameAlt - editor ID of the sound to play for the final second when using countdown

bUseConsoleOutputFile
Automatically set the console output file.
Options (Console Output):
  sFilename - the name of the output file e.g. ConsoleOut.txt
  
bCacheQuestAndNoteMenu
Speed up the quest and note menus by only recreating them if your quest/notes state has changed, and not creating the challenges list if you're viewing the notes tab.

bKeepHolotapePlayingWhenSelectingOtherNotes
Don't stop the current holotape's audio when clicking on other (non-audio) notes.

bSmoothIronsightsCameraTransition
Smooth the ironsights animation by interpolating between the non-aiming and aiming camera positions.
Options (Smooth Iron Sights Camera):
    iAimTransitionTimeMS - time taken to transition between the camera positions
    iEasingFunction - which easing function will be applied to the movement (see https://easings.net/)
    - 0: None
    - 1: OutSine
    - 2: OutCirc
    - 3: InOutSine
    - 4: InOutCirc
    - 5: OutQuart
    - 6: InOutQuart
    - 7: OutCubic

bDisableNeedsMessages
Prevents the messages when hardcore needs and radiation levels increase/decrease.
Options (Disable Needs Messages):
  bRadiation
	bHunger
	bDehydration
	bSleep

bCrouchWhileEquippingWeapons
Allows crouching while (un)equipping weapons, the crouch animation is queued after the equip.

bRecentlyDeadNPCIndicator
Shows recently killed NPCs on the compass until they have been moused over.
Options (Recently Dead NPC Indicator):
  iDeadActorMaxTimerMS - maximum time an NPC tick will be shown for after their death
  bPlayerOrTeammateKillsOnly - only show NPCs killed by the player or companions
  bPlayerDamagedOnly - only show NPCs damaged by the player (and companions unless 'ignore companion XP is enabled')
  uRGB - color of indicators in hexadecimal

iHUDMaxCompassNPCTicks 
Set the maximum NPCs to show on compass, overriding the vanilla gamesetting and allowing more than the vanilla maximum of 10.

bControllerBackButtonDoesntClosePipBoy
Prevents the Back button closing the Pip-Boy.

bAutoWeaponNoFiringDelay
Allows firing automatic weapons even if they are animating already (e.g. miniguns spinning up).
Options (No Firing Delay):
  bIncludeHeavyWeapons - ignore the need for heavy weapons (animation type >= 8) to spin up before firing

bMinBloodSplatterHealthDamage
Only show blood splatters if their damage is above a minimum health damage threshold.
Options (Blood Splatters):
  fMinHealthDamage - minimum health damage of an attack for blood splatters to show

bVATSStopBurstIfTargetDead
Stop firing the current burst in VATS if the target is already dead, e.g. the 10mm SMG which fires 3 rounds in a burst in VATS

bHoldAndReleaseThrowables
Allows hold/releasing for throwables similar to grenades.
Options (Holdable Throwables):
  bMineSupport - allow holding mines before throwing them

bAllowSleepWaitWithReducedMaxHealth
Allows sleep/waiting while max health is reduced by effects - making it possible to sleep with a temporary effect like -50hp, while still preventing sleeping while taking damage.
	
bLevelDifferenceAffectsCombatXP
Makes kill XP depend on the level difference between the player and killed actor.
Formula: iXPRewardBase + (killedLevel - playerLevel) * fXPLevelDifferenceScale
Options (XP Formula):
  iXPRewardBase - base XP rewarded for all kills
  fXPLevelDifferenceScale - additional XP rewarded per point of level difference between player and killed actor

bSwapAmmoWithWeaponHolstered
Allow swapping ammo types while weapon is holstered.

bPowerArmorNeedsNoTraining
Allows wearing power armor without the Power Armor Training perk.

bColoredHUDBars
Colors the HP and AP bars red when they are low. Note that temporary effects that raise max HP will show the bar in red at a higher percentage, this is intended to indicate that your health will be low when the buff wears off.
Options (Colored HUD Bars):
 fRedHealthThreshold - threshold ratio of current/max Health for coloring HP bar red
 fRedActionPointsThreshold - threshold ratio of current/max Action Points for coloring AP bar red

bSpeedMultScalesJumpHeight
Scale NPC and player jump height based on their speedmult actor value.

bStealingSendsNoAlarm
Don't alert actors when stealing their items (excludes pickpocketing).

bSneakCriticalsHeadshotsOnly
Only allow sneak attack criticals to the head.

bSortPipboyNotes
Sort the Pip-Boy Notes tab alphabetically, and/or by whether they're read.
Options (Note Sorting):
  iNoteSortingMode:
    0 - Alphabetical
    1 - Unread notes first
    2 - Unread first, alphabetically

bSortPipboyQuests
Sort the Pip-Boy Quests tab.
Options (Quest Sorting):
  bActiveFirst - show active quest at the top of the list
  iQuestSortingMode:
    0 - Alphabetical
    1 - Uncompleted quests first
    2 - Uncompleted first, alphabetically

bDisableAchievements
Disables steam/gog achievements.

bShowWeaponPoisonEffects
Include weapon poison effects when viewing weapons in the Pip-Boy.

bHideUnavailableRadios
Hide unavailable radios in the Pip-Boy.

bStatsMenuPercentageXP
Show XP in the Stats Menu as a percentage.

bUnequipWeaponMods
Allow unequipping weapon mods from the Item Mod Menu, additionally hide duplicates and sort mods alphabetically.
Options (Weapon Modding): 
  bHideModButtonForNonModdableWeapons - hide the Mod button if a weapon cannot have weapon mods
  bItemModMenuShowUnownedMods - show unowned weapon mods in the menu
  sRemoveItemModSound - editor ID of the sound to play when removing weapon mods (note: VUI+ has its own sounds that it plays when you click on weapon mods)
  bRequireWorkbench - only allow weapon modding if at a workbench
  bDebug - allow applying weapon mods even if you don't have them
  bDebugInGodMode - allow applying weapon mods even if you don't have them if godmode is enabled
  sViewMods - button prompt shown if you don't have mods

bDifficultyDoesntAffectNPCToNPCDamage
Stops NPC-NPC damage using the fDiffMultHPByPC gamesetting, with multipliers for NPC/teammate damages. Companion<->companion damage uses fDamageToTeammateMult.
Options (NPC Damage):
  fNPCToNPCDamageMult - multiplier applied to damage from one NPC to another
  fDamageByTeammateMult - multiplier for damage dealt by companions to NPCs
  fDamageToTeammateMult - multiplier for damage dealt to companions by NPCs

bDisableCombatMusic
Prevents combat music playing.

bKeepBrokenItemsEquipped
Prevent the message when a weapon breaks and keep it equipped.

bPickpocketWornItems
Allow pickpocketing items NPCs have equipped.
Options (Pickpocket Worn Items):
  bHolsteredWeaponsOnly - only allow taking holstered weapons

bMoveDuringVATSPlayback
Allow movement during VATS killcams.

bClickingShowsTerminalText
Make clicking while a note is being displayed on a computer first show the rest of the page, or skip to the next page if the current page is fully displayed.

bInvertPipboyRepairMenuSorting
Place high condition items at the bottom of the repair list.

bDisableRegionBordersKeepMessage
Allow movement outside world borders, showing the 'Leaving Region' warning repeatedly. Functionally equivalent to adding bBorderRegionsEnabled = 0 under [General] in FalloutCustom.ini, but retains the ui warning.

bRecurringChallengeIndicator
Adds an indicator that a challenge is recurring when viewed in the Pip-Boy. "(Recurring)" appears beside the progress e.g. 4/10 (Recurring)
Options (Recurring Challenge Indicator)
  sRecurringText - display on recurring challenges

bCustomSubtitleDistance
Modify how far away general subtitles are shown. For long distances you may need to increase the iSpeakSoundLipDistance gamesetting from its default of 750.
Options (Subtitles):
  fSubtitleDistance - distance to show subtitles from - vanilla is 500 units
  
bScopeVisibilityDelay
Delay the display of scopes when aiming in, and optionally prevent scoped aiming while reloading.
Options (Scoped Weapons):
	iScopeVisibilityDelayMS - required aiming time before the scope overlay is applied
	bStopAimingWhileReloading - aim out while reloading or weapon is jamming
  bAlwaysShowWeaponAnimation - forces the 'uses 1st person iron sights anims' flag on all weapons
  bDelayInThirdPerson - delay scopes in 3rd person
  
bLocationDiscoveredCornerMessage
Display the location discovered text as a corner message as in Fallout 3.

bNoHealingInCombat
Prevent use of aid items that heal HP or limbs while in [Danger].
Options (No Healing In Combat):
  sNoHealingItemsInCombatMessage - corner message shown when attempting to heal in combat
	
bHideRanksInTraitMenu
Hide 'Ranks' in the description for traits in the Trait menu, since it's a holdover from the LevelUp menu perk selection screen.

bSortPerkMenu
Sort the LevelUp Perk Menu.
Options (Perk Sorting):
  iPerkSortingMode:
    0 - Alphabetical
    1 - Reverse level sorting
    2 - Available first, alphabetically
    3 - By source mod first, alphabetically

bLessRestrictiveVATSMenu
Allow dequeuing actions and exiting vats while zooming in/out.

bNoTurningAnim
Suppress player turning animations to prevent the glide when stopping while turning.

bCustomAddToInventoryMessageTimer
Customize the length of time the 'Added to inventory' message is shown.
Options (Message Times):
  fAddItem - time the 'added to inventory' message is shown (in seconds)
  
bHideRedCrosshairOnDistantInvisibleTargets
Prevent the red crosshair when mousing over invisible enemies in the distance.

bRememberWeaponAmmos
Remember ammo type and count (optional) for all player weapons. Data is stored in the vanilla save, and is removed if loading without the tweak active, or if the weapons are deleted/unloaded.
Options (Remember Weapon Ammos):
  bInventoryOnly - forget stored ammo/type when weapons are dropped or transferred (to decrease save size)
  bIncludeCount - remember ammo count as well as type (regenerating ammo weapons always have their count stored)
  
bFatalNonSneakCritsAlwaysGib
Make fatal non-sneak critical hits always explode or dismember limbs.
Options (Critical Hits Gib):
  bOnlyCritsGib - prevent non-critical hits exploding or dismembering limbs
  
bNoFreeBarterItems
Set a price for 'free' items (e.g. ammo casings), calculated after barter buy/sell multipliers.
Options (Barter Items):
  fFreeItemCost - cost for buying items with no value
  
bLocationalMeleeDamage
Make melee and unarmed damage use limb damage multipliers.
Options (Melee Locational Hits):
  bPlayerAttacks - use hit multiplier for attacks by the player
	bNonPlayerAttacks - use hit multiplier for attacks by NPCs on the player
  bNpcToNpcAttacks - use hit multiplier for attacks on NPCs by NPCs

bQueueWeaponHolsteringWhileAnimsPlay
Pressing holster weapon while animations play will holster when the anims finish, instead of doing nothing as in vanilla.

bNoLockFailedTerminals
Don't lock terminals when they are failed.

bDelayPostCombatReputationPopup
Delay the reputation change popup dialog till 3 seconds after combat.

bNoPlayerNameLimit
Remove the limit on the number of characters in the player's name.

bSkipVigorTesterSpecialPages
Skip to the vigor tester review page.

bGrabbingItemsIsCrime
Make grabbing owned items carry the same faction penalty as stealing.
Options (Grabbing Items Is Crime):
  fMinValue - minimum item stack value to be considered stealing

bCustomSpecialPoints
Set a custom number of SPECIAL points to allocate, minimum is 7 (one in each skill).
Options (SPECIAL Points):
  iNumPointsToAllocate - total SPECIAL points after distributing points from the Vigor Tester or Special Book (TTW).

bAllowWeaponHotkeysWhileFiring
Use weapon hotkeys while firing.

bMoveDuringOpenPipboyAnim
Allow movement during the open Pip-Boy animation.

bHipFireAnimsWhileScoped
Use non-ironsight anims and recoil patterns for scoped weapons to prevent weapons lingering in your face when un-scoping after firing.
Note that this requires alternate animations as the hip fire recoil patterns for some weapons - e.g. the Scoped Varmint Rifle - look awful while scoped.

bRestore2Hotkey
Restores the '2' weapon hotkey. Requires "Data/menus/prefabs/lStewieAl/2Hotkey.xml". Controller users will need to bind ammo swap some other way (e.g. using bDoubleTapReloadToChangeAmmoType).
Options (Weapon Hotkeys):
  iSecondSlotKey - scancode of the keyboard hotkey
  bUseKeybindsOnLabels - use the name of the bound hotkey on the wheel instead of 1/2/3...


bEncumbranceIncludesGrabbedItems
Include the weight of the grabbed ('Z' key) item stack weight when determining if player is overencumbered.

bUseAnimVariants
Allow use of anim variants, similar to firing animation variants - requires both 1st and 3rd person animation files.
Options (Anim Variants):
  bReloads - allow reload variations
  bEquips - allow equip/unequip variations
  bAims - allow aim/aimIS variations
	
bCustomHackingAnswerLength
Use a custom formula for hacking answer length.
Options (Hacking Formula):
  fBaseWordLength - base word length
	fDifficultyWordLengthMult - multiplier applied on difficulty before adding to word length
	fComputerWhizLengthBonus - characters removed from answer if you have the computer whiz perk
	fOddTerminalIDBonus - characters added to answer if terminal ref ID is odd
	iMaxWordLength - maximum answer length (maximum 12)
	iMinWordLength - minimum answer length (minimum 2, note: there aren't many words in the hacking dictionary.txt file that are two characters long)
	iMinAttempts - minimum guesses
	iMaxAttempts - maximum guesses

bNoCompassPipsIfNotInDanger
Hide all NPCs on the compass if you aren't in [Danger].

bForceHiResWeaponModels
Use 1st person (high-res) models for NPCs' weapons.

bShowDoorsOnCompass
Show nearby doors on the compass.
Options (Compass Doors):
  iExteriorMaxDistance - maximum distance to show doors in exteriors
	iInteriorMaxDistance - maximum distance to show doors in interiors
	bVisitedIndicator - color the doors of visited cells (excludes doors leading to worldspaces)
	bFadeIconByDistance - scale the door icon's alpha based on distance to the player
	uVistedRGB - visited cell red/green/blue color in hexadecimal, e.g. 0xFF0088

bCriticalHitMessagesIncludeLimbName
Include the limb name in critical hit messages. e.g. 'Critical strike on Easy Pete's Torso'

bMenuFadesIgnoreTimescale
Make menu fading in/out ignore timemult.

bActivatingDoesntStandUp
Make activating while using furniture not stand up, instead use movement to stand while seated.

bNoSkillMessageIfIncreaseIsZero
Prevent the 'skill increased by 0' if reading a book with no bonus. Additionally display fractional skill book increases to two decimal places.

bCompassFadeLeftSide
Fade icons for NPCs, doors etc. on the left side of the compass. Useful if using a centered compass.

bConsoleTextShadow
Darkens the console output text and adds a faint shadow for readability.

bMinigamesPlayXPSoundAtMaxLevel
Play the XP gained sound when hacking or lockpicking at max player level.

bVATSHipFire
Entering VATS while not aiming will shoot from the hip for all shots fired (does not affect accuracy).

bAlternateLevelupSounds
Play an alternate level-up sound every A or B levels. If A is a multiple of B, the larger number wins ties. 
Options (Alt Levelup Sound):
  iLevelA - Play sSoundA every iLevelA levels
	iLevelB - Play sSoundB every iLevelB levels
	sSoundA - editor ID of sound to play every iLevelA levels
	sSoundB - editor ID of sound to play every iLevelB levels
For example with iLevelA = 2 and iLevelB = 3:
Level 2: - Sound A
Level 3: - Sound B
Level 4: - Sound A
Level 5: - vanilla
Level 6: - Sound B (matches both iLevelA and iLevelB, but iLevelB is larger)

bReloadJamsAffectedByAgility
Make reload jams affected by reload speed multipliers.

bRunSlowerInWater
Scale movement speed when walking/running through water depending on much you are immersed.
Options (Water Scales Movement Speed):
  fWadingMovementMult - max movement speed penalty when wading through water

bPipboyLightAndHolsteringIgnoreTimescale
Make using Pip-Boy light or holster hotkeys not take longer when time is slowed down.

bHostilesUseNeutralColorOnCompass
Make hostiles on the compass use the HUDMain color instead of HUDAlt (red).

bAgilityScalesJumpHeight
Scale jump height based on agility.
Formula:
  jumpHeight = 1 + ( fAgilityMult * (agility - 1) )
Options (Agility Affects Jump Height):
  fAgilityMult - multiplier added per agility point above 1

bUsingKeysRewardsXP
Gain XP when using keys on locks.
Formula:
  RewardXP = iUseKeyRewardXP + (vanilla lock XP) * fLockRewardXPScale
Options (Key XP Reward):
  iUseKeyRewardXP - base XP rewarded for using a key on a container/door
  fLockRewardXPScale - scale applied to the vanilla XP gained based on the lock level, impossible locks do not grant XP
  bRequireSkill - only reward XP if you meet the lock skill requirement

bUsingNotesRewardsXP
Gain XP when using notes to unlock terminals.
Formula:
  RewardXP = iUseNoteRewardXP + (vanilla hack XP) * fLockRewardXPScale
Options (Note XP Reward):
  iUseNoteRewardXP - base XP rewarded for using a note on a terminal
  fLockRewardXPScale - scale applied to the vanilla XP gained based on the lock level, impossible locks do not grant XP
  bRequireSkill - only reward XP if you meet the terminal skill requirement

bAnimDebugging
Prints which anims are currently active into the top left of the console {you can type ToggleDebugText (TDT) to see console output with the console closed}.

bPartialReloads
Add support for 'partial' reload anims when reloading with a non-empty clip. Makes the game select animations ending in '_partial' for the player if their clip is empty.

bNPCsEarnAmmoCasings
Make NPCs earn ammo casings when firing their weapons.

bDrowningDrainsAP
Drain action points before taking damage when drowning.

bFasterEnterLockpickMenu
Speed up the animation for entering the lockpick menu.

bPreventInactiveWindowScrolling
Prevent scroll-wheel affecting windows outside NV.

bAddItemUsesItemIcon
Use the item icon (if it exists) in 'added to inventory' messages (you will need an icon replacer or they will be off-centered), instead of always using the gift icon.

bAllowWeaponHotkeysWhileEquipping
Allow use of weapon hotkeys while switching weapons.

bShowNearestUndiscoveredLocation
Always show the nearest undiscovered location on the compass or map.
Options (Show Closest Location):
  bMapMenu - show the closest undiscovered location on the map
  bCompass - show the closest undiscovered location on the compass

bWeaponCycleUpDownHotkeys
Use left/right controller d-pad to cycle through hotkeyed weapons.

bRepairRequiresWeaponSkill
Disallow repairing if repair skill is less than the weapon's skill requirement. i.e. you need 75 repair skill to fix a weapon that requires 75 energy weapons skill.

bMaxVATSDistanceUsesWeaponRange
Use the player's weapon max range to determine the max VATS targeting distance - e.g. you can target enemies further with a sniper rifle than a 9mm pistol.
Options (VATS Uses Weapon Distance):
  fMaxDistance - maximum range to check for targets
	fMinDistance - minimum range to check for targets
	fRangeMult - multiplier applied to the weapon's max range

bLessFrequentPlayerPainSounds
Add a minimum interval between player pain sounds.
Options (Combat Sounds):
  iMinPlayerPainSoundIntervalMS - minimum time between player pain sounds in milliseconds
  
bMoreFrequentNPCLightUpdates
Calculate actor light levels (used for sneaking) more frequently - may incur a minor performance penalty if the interval is too low.
Options (Detection Light Timer):
  fIntervalTimer - time between updates (in seconds), vanilla is 3 seconds

bBetterMapZoom
Makes zooming in the local and world map center on where the cursor is instead of the middle of the screen.

bLockPickMenuKeyboardMovement
Use left/right movement to control the bobby pin, and jump and forward/back to spin the screwdriver.
Options (Lockpick Menu Movement):
  fBaseSpeed -  base speed for left/right bobby pin movement
  fShiftScale - scale applied to movement speed while shift is held
  fCtrlScale - scale applied while ctrl is held

bSavingDoesntClosePauseMenu
Keep the pause menu open after saving the game.

bContainerMenuStoreAllHotkey
Hold shift to store all visible (i.e. not filtered out via category/menu search etc.) items from the left hand side into the current container.
Options (Container Store All):
  sStoreAll - replacement label for 'Take All' when shift is held

bContainerTakeAllDoesntCloseMenu
Prevent the 'take all' button closing the container.

bTakeAllConfirmation
Show a confirmation message when taking all items from a container.
Options (Take All Confirmation):
  sMessageText - confirmation message for taking all items
	iMinItemCount - minimum number of items for the message to appear

bBloodyMessGibTargetedLimbOnly
Prevents bloody mess dismembering/exploding limbs that weren't hit. In vanilla there's a random chance an npc's limb is removed when shooting their torso.

bDeselectHotkeys
Makes it possible to remove a hotkey for an item by attempting to assign it the slot it has already.

bSortRecipeMenu
Sort the recipe menu.
Options (Recipe Sorting):
  iRecipeSortingMode:
    0 - Alphabetical
    1 - Craftable recipes first
    2 - Craftable first, alphabetically
    3 - Sort recipes whose skills requirements are met first

bReloadSoundsAffectedByTimescale
Scale reload sound pitch and length based on the game time multiplier (e.g. while using turbo).

bNoPoisonConfirm
Remove the confirmation prompt when poisoning a weapon, and replace the warning popups with a corner message instead.

bNoAmmoFromTakingNPCWeapon
Don't earn extra ammo when taking an NPCs weapon. In the base game, you can earn a random amount of ammo (based on clip size) when taking the equipped weapon of an NPC who died (before reloading the game).
e.g. taking a .357 revolver will give anywhere between 0-6 ammo.

bNoExitConfirm
Skip the exit confirmation when clicking Quit Game in the main menu.

bLivingAnatomyShowDR
Show damage resistance when using the living anatomy perk, and remove decimal places. Additionally hides the DR/DT if they are zero.
Options (Living Anatomy):
  bAlwaysShowHealth - show the targeted NPC's health-bar even if they have max health

bPreviewPerksOnLevelUp
Always show the perk screen when leveling up even if you have no points to assign.

bPlaceMarkersAtLocations
Makes right clicking in the map menu to place a marker place it directly on the hovered location.
Options (Place Marker At Location):
  bLocalMapDoors - add support for doors on the local map

bAllowPickpocketIfAlreadyCaught
Allow pickpocketing even if the NPC has caught you previously.

bHideCrosshairWhileReloading
Hide the crosshair while reloading.

bHideCrosshairInKillcams
Hide the crosshair during killcams.

bHideHealthbarInKillcams
Hide the health-bar during killcams.

bHUDRotatesWithVanityCam
Move the compass when rotating while holding the POV button for the vanity camera.

bHUDWeaponNameLabel
Show the current weapon name above AP when it's equipped.
Customizable by editing 'menus/prefabs/lStewieAl/WeaponNameLabel.xml'
Options (HUD Weapon Name Label):
  bShowOnReadyWeapon - show the weapon name when it is unholstered
  bInstantChange - instantly change the displayed label text if visible when changing weapons
  iFadeInTimeMS - time to fade in the label (in milliseconds)
  iDisplayTimeMS - time to display the fully shown label (in milliseconds)
  iFadeOutTimeMS - time to fade out the label (in milliseconds)

bCompressDuplicateConsoleMessages
Append -#count to consecutive duplicate single line console messages.

bNoPipboyIdleAnims
Prevent the Pip-Boy idle anims (used for swaying left/right in vanilla) from playing. In vanilla these are: 
Characters\male\IdleAnims\1stPPipBoyWaver.kf etc.

bSaveCharacterSelector
Add a character selector for filtering the save/load menu, to make it easy to find saves from different created with different character names.
Uses: menus\prefabs\lStewieAl\SaveCharacterSelector.xml
Options (Character Selector):
  sAllText - text to display in the Save/Load menu while character filter isn't applied

bNoFastTravelIfLegsCrippled
Prevent fast travel if a leg is crippled.
Options (Fast Travel Crippled Limbs):
  sLimbsCrippledMessage - corner message shown when attempting to fast travel with broken limbs

bHotkeyHolstersWeaponIfEquipped
Pressing the hotkey for the current equipped weapon will holster or draw instead of unequipping.
Options (Current Weapon Hotkey):
  bDontHolsterWeapon - pressing the weapon key for an already equipped weapon will do nothing (instead of unequipping)

bPreventRepairIfNotAtWorkbench
Prevent repairing items if you aren't looking at a workbench.

bImprovedRaceMenu
Allow panning the camera with right click or Y on controller, and increase min zoom.
Options (Improved Race Menu):
  bNoAnims - prevent the player swaying while in the menu
  fPanXScale - scale the right click pan X direction movement speed
	fPanYScale - scale the right click pan Y direction movement speed

bMapMarkersShowFactionName
Show the faction name underneath the map marker name, e.g. (Goodsprings - Neutral).
Options (Map Marker Factions):
  bRequireReputation - only show location reputations if you have reputation with that faction

bRightClickChangesToPreviousContainerCategory
Make right clicking the category cycle to the previous category in container/barter/recipe menus.

bInvalidBSFadeNodePrints
Disables the '[Tweaks] Invalid BSFadeNode Detected - Linked Obj ID: %08X' warning.
If you're an author I recommend you leave it on so you know which of your meshes are broken. Setting is hidden (add bInvalidBSFadeNodePrints=0 under [Tweaks] to disable)

bHideReputationTabIfEmpty
Hides the Stats menu reputation tab and button if you don't have any faction reputations (mainly for use with TTW).

bShowActiveQuestNotesShowsAllStartedQuests
Make the 'Show Active Quest Notes' button show notes for all started, non-completed quests.

bHideHotkeyedItemsInBarter
Hides hotkeyed items in the barter menu.

bHideHotkeyedItemsInContainers
Hides hotkeyed items in the container menu.

bNumberedComputerHotkeys
Adds hotkeys 0-9 to select options in the computers menu.
Options (Computer Hotkeys):
  bPrependOptionNumber - display list numbers for menu options

bShowBookEffects
Show book effects when viewing them in the Pip-Boy. e.g. 'Permanent Speech +1'.
Options (Book Effects):
  sPrefix - prefix before the 'Skill +1' text shown under Effects

bAutoContinueGame
Automatically continue game at the start menu.

bSortMiscStats
Sort the misc stats page of the Stats menu.
Options (Misc Stat Sorting):
  iSortMode - sorting mode
    0 - Alphabetical Vanilla + unsorted modded
    1 - Alphabetical
    2 - By Value
    3 - Alphabetical/Zeros Last

bTakeAllInCompanionContainers
Show the 'Take All' button when viewing companion inventories.

bPreventBushPassthroughSounds
Prevent sounds playing when walking through bushes.

bSynchronizeContainerCategories
Synchronize the left/right item categories like in Fallout 4.
Options (Synchronized Container Categories): 
  bPreventSwitchWhenEmptyingCategory - prevent the category automatically changing when transferring the last item in a category

bRandomizeKillcamMode
Randomly alternate between cinematic/player view kill-cams.

bNoDamageMeleeWeaponIfTargetDead
Don't decrease the health of a melee weapon when hitting dead NPCs.

bLockpickHackingMessageShowsCurrentSkill
Show the current lockpick/hacking skill levels in the 'You need X skill to hack this terminal' messages.
Options (Lockpick/Hacking Messages):
  sLockpickMessage
  sHackingMessage 

bNoDropWeaponSoundOnPlayerDeath
Prevent the unequip sound when the player dies.

bToggleControllerIfAttackPressed
Allow clicking or pressing A to toggle keyboard/controller.
Options (Toggle Controller If Attack Pressed):
  bPreventControllerConnectedPopup - prevent the 'Turn off 360 Controller in the Controls...' popup

bBillyGoatMode
Allow adjusting the max walking, jumping and autowalk angles. Vanilla is 47 degrees.
Options (Slope Climbing):
  fWalkAngle - max angle in degrees (between 0 and 90)
  fJumpAngle - max angle while jumping
  fAutoWalkAngle - max angle while automove is enabled

bNoPlayerAnimMovement
Prevent the player moving if movement keys aren't pressed to avoid anims causing sliding.

bRepairItemsPreview
Show the weapons/armors which can repair the hovered item by holding ALT and opening the repair menu.
Options (Repair Items Preview):
  sButtonLabel - button label shown while key is held

bExplosionKnockdownAvoidanceUsesStrength
Make explosion knockdown avoidance chance use strength instead of agility.

bMousewheelScrollsWeaponHotkeys
Add mousewheel to scroll through hotkeyed weapons.
Options (Mousewheel Scrolls Weapon Hotkeys)
  bInvert - invert the weapon swap direction

bCapSkillsBySPECIAL
Cap the levelup menu max skill values based on SPECIAL skills.
Options (SPECIAL Caps Skills):
  iSkillCap - max value for skills
	fSkillBase - base value
	fSPECIALMult - multiplier applied to SPECIAL skills
	fLuckMult - multiplier applied to luck
  
Formula: skillCap = min(iSkillCap, fSkillBase + (specialVal * fSPECIALMult) + luckVal * fLuckMult)
Strength - Melee Weapons
Perception - Energy Weapons, Explosives, Lockpick
Endurance - Big Guns, Survival, Unarmed
Charisma - Barter, Speech
Intelligence - Medicine, Repair, Science
Agility - Guns, Sneak

bRunAndGunAPInCombatOnly
Only use the fActionPointsRunAndGunMult gamesetting when in combat.

bDisarmingMinesPicksThemUp
Automatically pick up explosives after disarming them.

bCritChanceIgnoresFireRate
Don't scale crit chance for automatic weapons by their fire rate.

bHideHotkeyedItemsInRepairLists
Hide hotkeyed items in the item repair menu.

bStatsMenuShowEffectTimeRemaining
Show the time remaining for effects in the Stats menu (excludes named effects like 'Psycho' or 'Well Rested').
Options (Stats Menu Effect Durations):
  bDisplayInSeconds - display the time remaining in seconds

bAmmoLabelUseLongName
Use the longer name for ammo on the HUD (will clip with other HUD elements, intended for use with mods like HUD Editor).
Options (Ammo Label):
 bUsePipboyName - use the shorthand name for ammo (e.g. MF Cell instead of Microfusion Cell)

bPerBulletLoopingReloads
Require pressing reload N times to load N rounds for looping reload weapons.
Options (Looping Reloads):
  iMaxQueueLength - max number of bullets to queue by pressing reload multiple times, set to 0 for no limit
  iRoundsPerReloadPress - number of bullets to queue per reload press

bNoPlayerStaggerAnims
Disable player stagger animations when limbs are crippled.

bConsolePrintsIncludeTimestamp
Include a timestamp in console messages.
Options (Mod Console Prints):
  sTimeFormat - timestamp format

bScalePlayerMeleeReach
Scale the distance the player hit with melee weapons.
Options (Melee Reach):
  fReachMult - multiplier applied to melee weapon range
  fMinReach - minimum weapon reach
  fMaxReach - maximum weapon reach
  
bPlacedMarkerHeightIndicator
Add an indicator whether the player placed marker is above or below if the marker is in another cell.
Options (Player Placed Marker):
  bUseDoorIcon - Use glow_hud_compass_pc_marker_door.dds for doors.

bNoLockEncounterZoneLevels
Don't freeze the level of encounter zones when they are first visited. 
In the base game any dungeon visited at a low level will be stuck at that level for the rest of your playthrough, resulting in weak enemies and low level loot when you visit it again.
This tweak changes that so that there is no difference in level between entering a new dungeon and a previously visited one.
	
bChangingContainerCategoryScrollsToTop
Scroll to the top when changing container/barter categories.

bMorePreciseRadMeter
Display radiation level to two decimal places.
Options (RAD Meter):
  sFormat - format for radiation meter text, supports 0-9 decimal places with %.1f, %.2f etc.

bAimingUnholstersWeapons
Unholster weapons when aiming.

bShowAlternateAmmoTypesAvailableInMenus
Show a + beside ammo count in inventory menus if you have any alternate ammos.

bReloadWhileFiring
Allow reloading while firing anims play.

bRepairScalesCraftingCondition
Scale initial health of crafted items based on repair skill.
  
bScaleExplosionShake
Scale the camera/HUD shake caused by explosions.
Options (Explosion Shake):
  fCameraMult - multiplier applied to camera shake
	fHUDMult - multiplier applied to HUD shake

bMarkNearbyLocationsOnMap
Permanently reveal nearby location markers on the Pip-Boy map.
Options (Add Nearby Markers To Map):
  fDistance - radius of circle around player to add markers

bPreventStealingCapsAfterRepair
Place caps in merchant containers instead of their inventory when using repair services.
Options (No Stealing After Repair):
  bRemoveIfNoVendorContainer - destroy the caps if the merchant has no vendor container

bPreventNPCComments
Prevent NPCs commenting on various player actions.
Options (Prevent NPC Topics):
  iFlags - hexadecimal value containing the sum of all the desired flags. e.g. 0x8A0 would prevent KnockOverObject, LockedTerminalOrContainerInCrosshair and ZKeyObject.
Flags:
 Greeting = 0x1
 SwingMeleeWeapon = 0x2
 ThrowGrenade = 0x4
 FireWeapon = 0x8
 LayMine = 0x10
 ZKeyObject = 0x20
 Jump = 0x40
 KnockOverObject = 0x80
 StandOnFurniture = 0x100
 InIronsights = 0x200
 DestroyObject = 0x400
 LockedTerminalOrContainerInCrosshair = 0x800
 SneakActorInCrosshair = 0x1000

bCompanionsUseLocationFontOnMap
Use the same font as locations for companions on the map. Vanilla is hardcoded to use font 2.

bRemoveDeadNPCCrippleCriticalMessages
Remove queued cripple/critical messages for dead NPCs. This prevents the spam of 'Limb crippled...' after a target dies from explosions for example.

bShowUsePasswordOnTerminalsWithNote
Show 'Use Password' on terminals if you have the password note. Additionally marks terminals as unlocked once you've opened them with the note.
Options (Hacking HUD Prompt):
  sUsePassword - prompt when you already have the terminal's password note

bHideReadNotes
Hide notes that have been read already in the notes menu.

bExplosionKnockbackDirectionFix
Push targets away from explosions instead of the actor who created them. This also allows you to move yourself with your own explosions.

bShowBarterTotalWhenOverSellLimit
Show the total barter amount when the total is more than the merchant's caps.

bAllowAidAtMaxHealth
Allow using stimpaks, super stimpaks and doctors bags when at max health/limb condition.
Options (Allow Aid At Max Health):
  bStimpaks
  bSuperStimpaks
  bDoctorsBags

bBarterQuantityMenuShowsPrice
Show the total price of the selected quantity menu items when bartering.

bContainerQuantityMenuShowsWeight
Show the total weight of the selected quantity menu items in containers.

bFixKillChallengeSourceWeapon
Use the last weapon that damaged an NPC instead of the currently equipped weapon for kill challenges.
Note: weapons that are scripted to directly use the Kill command will not increase the challenges.

bPreventNoFastTravelMessage
Prevent the sNoFastTravelUndiscovered message when clicking on an undiscovered map marker.
Options (Prevent No Fast Travel Message):
  bPlaySound - play a 'cancel' sound when trying to click on an undiscovered marker

bExplosionsDontPushTakeableItems
Prevent explosions moving items if they're collectible.

bNoDespawnVisibleStuckProjectiles
Prevent stuck projectiles despawning if you're facing them.

bSeparateHorizontalSensitivity
Use a separate slider for horizontal/vertical sensitivity.
Options (Separate Sensitivity Sliders):
  fVerticalSensitivity - stores the vertical sensitivity (modifiable in the vanilla settings menu)

bWeaponVisibleDuringDialogue
Keeps player weapon visible while in dialogue.

bNPCsDropLiveGrenades
Crippling/killing an enemy mid-throw causes them to drop the live grenade.

bSneakingDoesntForcePowerAttacks
Allow melee/unarmed non-power attacks while sneaking - requires separate anims.

bSilentSneakPowerAttacks
Make melee/unarmed power attacks silent if sneaking.

bTogglePOVWhenHolsteringWeapon
Toggle 1st person when readying a weapon, and 3rd when holstering.

bPowerAttackIfBlocking
Remove the melee power attack delay while blocking.
Options (Power Attack If Blocking):
  bOnlyIfBlocking - only allow power attacks when blocking

bDisarmRequiresSkill
Add random chance mines will not disarm or explode instantly based on the weapon's skill requirements.
If a disarm fails, there's a chance the mine will instantly explode.
Options (Disarm Requires Skill):
  fExplodeMult - multiplier applied to instant explosion chance
  fDisarmMult - multiplier applied to disarm chance
Formula:
  disarmChance = fDisarmMult * (playerSkill + perception - 5) * 100.0F / requiredSkill
  explodeChance = fExplodeMult * (requiredSkill - playerSkill + (5 - luck)) * 2

bSelectUnavailableRadios
Allow selecting unavailable radios to use when back in range.

bRadioStaticDecreasesSongVolume
Make songs quieter when static is playing near the edge of a radio's range.

bRadioKeepPositionWhenLoading
If a song is playing on the radio, don't rewind it when loading a save that has the same song playing.

bWeaponImpactEffects
Spawn sparks and play impact sounds when equipped/holstered weapons are hit.

bDoubleJump
Allow jumping in mid-air.
Options (Double Jumping):
  iMaxJumpCount - max additional jumps
  fJumpHeightScale - scale applied to mid-air jumps
  iAPCost - action Point cost to jump in mid-air
  sJumpSound - sound played when jumping in mid-air
  fJumpVolume - volume of double jump sound
  fMidairTimer - time (in seconds) after falling where initial jumps don't increase the jump counter
  bKeepHeight - don't reset the fall damage height when jumping in mid-air
  sPerkEditorID - editor ID of the perk required to allow double jumping
  bRequirePowerArmor - require a power armor torso to double jump

bExplosionRadiusBuff
Make inner 30% of explosion radius deal full damage and minimum damage at radius be 20%.
Options (Explosion Formula):
  fInnerRadius - radius that deals 100% damage
  fOuterRadiusDamage - damage dealt at the outer radius
  bAffectPlayer - damage dealt affects the player

bDetachedBeams
Prevent beam projectiles sticking to the weapon barrel when turning.

bMoreReponsiveControllerAiming
Significantly smoothens the right thumbstick deadzone curve for looking around. Recommend pairing with bDisableControllerDeadzones.

bAllowDuplicateControlBinds
Allow binding multiple controls to the same button in the vanilla settings menu. The base game swaps the controls around when you try this.

bCrippledLegsScaleJumpHeight
Scale jump height if legs are crippled.
Options (Crippled Jump Height):
  fOneLegJumpHeightMult - jump height scale with one crippled leg
  fTwoLegsJumpHeightMult - jump height scale with two crippled legs

bPipBoyTabHotkeysDontCloseMenu
Prevent the Pip-Boy tab hotkeys (F1/F2/F3 by default) closing the Pip-Boy.

bMoreDetailedStatsMenu
Show the value modifier amount in the (+) and (-) for skills, and show skills/specials above 10/100. VUI+ strongly recommended.

bLethalHitsIncreaseLimbChallenges
Increase limb cripple/knockback challenges even if the attack killed the target.

bTerminalFadeTime
Adjust the time the terminal menu fades out when closed with keyboard/controller.
Options (Terminal Close Fade):
  fFadeLength - length of time the terminal menu fades for when closed with keyboard/controller

bReloadingWithNoAmmoSwapsAmmoTypes
Change ammo types when reloading with no ammo.

bMainMenuContinueIcon
Show the image of the save to load when 'Continue' is hovered at the main menu.

bEnteringVATSDoesntUnholsterWeapon
Don't unholster weapon when using VATS without selecting a target.

bPowerArmorPreventsScreenBlood
Prevent screen blood effect if your hit body part is wearing power armor.

bPowerArmorScalesLimbDamage
Scale limb damage for hits on power armor.
Options (Power Armor Scales Limb Damage):
  fHeadScale - scale applied to head damage while wearing a power armor helmet
  fLimbScale - scale applied to limb damage while wearing a power armor torso
  iMode - who to affect
  - 1: NPC
  - 2: Player
  - 3: All

bPreventHittingHolsteredWeapons
Make projectiles pass through NPC holstered weapons.
Options (Shoot Through Weapons):
  bIgnoreUnholstered - ignore hitting unholstered weapons (prevents disarming)
  bAllowHitsInVATS - allow hitting weapons in VATS

bCrippledLimbsPlayPainSoundWhenFalling
Play pain sounds when falling with crippled legs.
Options (Crippled Limb Fall Pain Sound):
  fHeightThreshold - distance fallen to play pain sound/imod when either leg is crippled

bHideQuestItemWeightAndValue
Hide the weight and value of quest items in the Pip-Boy.

bNPCsDetectMineExplosions
Alert nearby NPCs when mines explode.

bTerminalGreyReadNotes,
Grays notes after reading them in the terminal (not retroactive).

bSortEquipableAmmo
Sorts usable ammo to the top of the Pip-Boy inventory. Not compatible with yUI/ySI.

bHideCapsAddedMessages
Hide item added messages for caps.

bSplashDamageTorsoGibbing
Gives projectile splash damage a chance to trigger bloody mess torso explosions.

bFreeWildWasteland
Allow selecting wild wasteland without using a trait point.

bInvertCameraX
Invert the camera X movement.

bClearNearbyPlayerMarker
Remove player placed marker when nearby.
Options (Clear Nearby Player Marker):
  fDistance - distance to remove the marker

bLightStepAffectsCompanions
Give companions light step if player has the perk.

bVATSAPDisplayIncludesReloadCost
Include the cost of a reload (fActionPointsReload gamesetting) when queuing a VATS attack that will cause a reload.

bSkipVeryEasyLocksAtMaxSkill
Automatically unlock very easy locks when lockpick skill is maxed.
Options (Auto Unlock Locks):
  iThreshold - difference in lock/skill level for automatically unlocking the lock
  fRewardXPScale - scale applied to rewarded XP

bMultithreadedHackingMenu
Multithreads the setup of the hacking words list to reduce lag when hacking a terminal.

bMarkNotesUnread
Adds right click to mark a note as unread.

bCustomPopupIcons
Adds configurable icons to popup messages.
Options (UI Message Icons):
  sRadiationIncrease
  sRadiationDecrease
  sRadiationSick
  sRadiationNotSick
  sDehydrationIncrease
  sDehydrationDecrease
  sDehydrationSick
  sDehydrationNotSick
  sHungerIncrease
  sHungerDecrease
  sHungerSick
  sHungerNotSick
  sSleepDeprivationIncrease
  sSleepDeprivationDecrease
  sSleepDeprivationSick
  sSleepDeprivationNotSick
  sChemsAddicted

bNoGibSoundWhenEnteringCells
Prevent body part explosion sounds when entering cells.

bInteriorExteriorMapDoorIcon
Use a separate icon for local map doors which lead to an exterior. Uses 'Interface\Icons\Local Map\iron_exterior_door.dds' and 'Interface\Icons\Local Map\iron_interior_door.dds' for exterior/interior doors respectively.

bChallengeMenuIcons
Use challenge icons in the Pip-Boy challenges menu (requires a mod that adds icons to the Challenge forms).

bPauseHolotapes
Make clicking on the current holotape pause it, double tapping pause resets the holotape.
Options (Pause Holotapes):
  bPauseInDialogMenu - pause holotapes while the Dialog menu is open

bImprovedWeather
Prevent weather changes when fast traveling short distances.
Options (Improved Weather):
  fFastTravelWeatherChangeDistanceThreshold - minimum fast travel distance for a weather change

bHUDMarkerNameIndicator
Show the name of the nearest triangle location marker you're looking towards.
Options (HUD Marker Name):
  bHideUndiscoveredNames - whether names of undiscovered locations should be hidden
  iShowDistance - mode for showing distance to the location
    0 - off
	1 - meters
	2 - feet
  fMaxAngle - max angle to show location name
  fAngleOffset - offset of angle (to account for the triangle being off-centered)
  fDelay - delay (in seconds) before name is shown
  bShowPlayerMarkers - show distance to the player placed marker
  sPlayerMarkerName - name when viewing player placed marker

bScaleAshpileSize
Scale the size of ashpiles depending on actor size - note some creatures such as Bloatflies have large bounds which affects their ashpile size.
Options (Ashpile Scale):
  fMinScale - minimum scale applied to ashpiles
  fMaxScale - maximum scale applied to ashpiles (set to 0 for no limit)

bTargetProjectilesInVATS
Allow targeting projectiles in VATS. The percentage hit chance doesn't take the visibility of the projectile into account, only the distance + player skill.
Options (VATS Target Projectiles):
  bMines - allow targeting mines

bStartMenuQuickLoad
Add support for the QuickLoad key in the Main/Pause menus.

bShowQuestObjectivesOnCellChange
Show quest objectives when changing cells.
Options (Quest Reminders On Cell Change):
  fMinInterval - prevent showing objectives again within this time (in seconds)

bContactMines
Instantly detonate mines when they are stood on.
Options (Contact Mines):
  bPlayer - affect the player
  bNPCs - affect NPCs

bAutoWeaponJamWhileFiring
Allow firing anim jams to play while firing an automatic weapon. In vanilla only the first shot can jam. Note that you need to edit the fWeaponConditionJam1/fWeaponConditionJam2... gamesettings to add a chance for any jams while firing.

bClickToExitLoadScreens
Require clicking to exit load screens.
Options (Click To Load):
  bHideWheel - hide the loading wheel when loading is finished
  bLoadGameOnly - don't require clicking through fast travel/exterior load screens

bHideCursorInMessageMenu
Hide the cursor in the message popup windows.

bChanceBasedKillcams
Give a chance the cinematic/player view killcam will play when killing the last of a combat group.
Options (Killcam):
  fChance - percentage chance the cinematic/player view killcam will play when killing the last of a combat group

bQuestTextVisibleInMenus
Keep the quest/location added text visible in the Pip-Boy and Hacking menus, and while sitting down.

bSkipLoadSaveConfirmationPrompt
Skip the confirmation prompt when loading a save.
Options (Skip Load Confirmation):
  bMainMenuOnly - only skip the confirmation at the main menu

bColorWeaponCndLabel
Allow coloring the weapon low condition label.
Options (Weapon Condition Label):
  fFlashThreshold - threshold health percent for weapon label to blink
  fColorThreshold - threshold health percent for weapon label to turn red

bArmorConditionLabel
Add an armor condition label to the HUD.
Options (HUD Armor Condition)
  sArmorLabel - label shown beside the armor meter
  sWeaponLabel - replacement label beside the weapon meter (leave blank to use vanilla string)
  fFlashThreshold - threshold health percent for label to blink
  fColorThreshold - threshold health percent for label to turn red
  fVisibilityThreshold - threshold health percent for label to turn visible (set to 0 to disable)
  iLabelOffsetX - offset applied to the X position of the armor condition label
  iLabelOffsetY - offset applied to the Y position of the armor condition label
  bUseWeaponPos - use weapon label position if no weapon is equipped

bMoveAmmoTypeLabel
Moves the ammo type label to under the ammo count.

bArmorPreventsBloodDecals
Prevent blood decals for attacks that don't penetrate target DT.

bEnemyHealthbarShowBuffedHP
Include health modifiers in enemy healthbars (e.g. buffout).

bSleepOnChairs
Sleep when waiting on chairs.

bSleepWaitSliderShowsWakeTime
Show the wake time on the sleep/wait slider instead of hours.

bCripplingDoesntDisarm
Prevent NPCs dropping their weapons when arms are crippled.

bKeepFallHeightOnLoad
Prevent fall height being reset when loading a save.

bReviveUnconsciousCompanions
Use stimpaks to revive unconscious companions.
Options (Revive Unconscious Companions):
  fUnconsciousTime - duration companions stay knocked out (set to 0 to use the vanilla fEssentialDeathTime gamesetting)
  sPrompt - prompt shown when mousing over an unconscious companion
  bReviveWhenChangingCells - automatically revive companions when changing cells


bHeatbeatSoundsFade
Fade the volume of heartbeat sounds, reset the volume when taking damage.
Options (Heartbeat Sounds Fade):
  fDuration - duration for the sound fading in seconds
  iEasingFunction - which easing function will be applied to the volume
    - 0: None
    - 1: OutSine
    - 2: OutCirc
    - 3: InOutSine
    - 4: InOutCirc
    - 5: OutQuart
    - 6: InOutQuart
    - 7: OutCubic

bArmorSoundsPlayIn3D
Play armor foley sounds in 3D when in 3rd person.

bSortPipboyRepairMenu
Sort the Pip-Boy repair menu.
Options (Pipboy Repair Menu Sorting):
  bMatchedItemFirst - whether items matching the repair target should be shown first
  iSortMode - sorting mode
    - 0: Alphabetical
    - 1: Value/Weight

bDisableStealthEffectInPipboy
Disable the invisibility effect from stealth boys etc. while the Pip-Boy is open.

bBarterShowCapsChange
Show the final caps after a transaction beside player/merchant caps.
Options (Barter Show Transaction Caps):
  iMode - display mode
  - 0: show { current -> final } for the caps display
  - 1: show the final caps display and adjust the text brightness

bCompanionsDontUseAmmo
Don't remove ammo from companions when they fire weapons.

bAmmoBurstCaseCountFix
Give a chance to earn multiple ammo casings from weapons that use more than 1 ammo per shot.

bReallocateSkillPointsOnLevelup
Allow reassigning all skill points when leveling up.

bUseWeaponRepairKitsInRepairMenu
Show repair kits in the weapon repair menu.
Options (Use Repair Kits In Repair Menu):
  sRepairText - text to display instead of 'Repair' if you only have repair kits

bStrengthAffectsAllThrowables
Make the fThrowingStrengthPenalty gamesetting also affect grenades and mines.

bMapRemembersPosition
Remember the last viewed position in the Map Menu.
Options (Remember Map Position):
  bSavePersistent - remember the map position for each save

bMapRecenterHotkey
Add a hotkey to recenter the map menu.
Options (Map Recenter Hotkey):
  iEasingTimeMS - duration of the recenter movement
  iEasingFunction - which easing function will be applied to the movement
    - 0: None
    - 1: OutSine
    - 2: OutCirc
    - 3: InOutSine
    - 4: InOutCirc
    - 5: OutQuart
    - 6: InOutQuart
    - 7: OutCubic

bMapLocationDisplayDistance
Show the distance or time to the hovered location marker in the Map Menu.
Options (Map Extra Marker Info):
  fTimeMult - multiplier applied to the displayed times
  fDistMult - multiplier applied to the displayed distances
  iDisplayMode - display mode
  - 0: Meters
  - 1: Feet
  - 2: Real Time
  - 3: Game Time

bBarterAffectsRepairCosts
Scale NPC repair prices based on your barter skill and perk modifiers.
Options (Barter Affects Repair Costs):
  fCostBase - base cost
  fCostMult - price decrease per barter point
  fCostMin - minimum multiplier

bContainersShowEquippedAmmo
Show the 'equipped' square beside equipped ammos in containers.

bQuantityMenuRespectsCompanionCarryCap
Limit the quantity menu max count when transferring items that would overburden a companion.

bDialogueKeepVoiceActingNotes
Display the voice acting notes e.g. {afterthought} in dialogue.

bMeleeImpactEffectsFollowTarget
Make melee blood decals follow the target instead of floating in midair.

bRaceMenuAllowFemaleFacialHair
Allow selecting facial hair on female characters in the Race menu.

bPrintNewModsOnLoad
Print which mods are new when loading a save created without them.

bBetterCaravanMenu
Improves usability of the Caravan minigame. Requires separate download.
Options (Better Caravan)
  bDebug - print various debug statements to help test the minigame
  iModCardCount - number of deck cards to randomly modify
  iModCardMode - deck modification mode, Add/Remove/Replace iModCardCount random cards in the player's deck after deck building
    0 - Add
    1 - Remove
    2 - Replace

bCustomLocationDiscoveredSound
Customize the sound played when discovering a location.
Options (Location Discovered Sound)
  sEditorID - editor ID of the sound to play when discovering a location

bVATSTargetPlayerProjectiles
Allow targeting projectiles created by the player in VATS.

bBlackJackTotalDisplay
Show a display of your hand values in BlackJack.

bCapitalizeRecipeCategories
Show recipe menu categories in full caps.

bPerksAffectFistWeaponSpeed
Allow weapon attack speed perks to affect the unarmed fists weapon.

bKeyRepeatAcceleration
Scroll faster after holding the key for some time.
Options (Key Repeat Acceleration):
  iDelay - delay before multiplier is applied
  fRateMult - multiplier applied to scrolling speed
  iDelayAlt - delay before the alternative multiplier is applied
  fRateMultAlt - multiplier applied to scrolling speed

bVATSDequeueWeaponShotsOnDisarm
Remove queued VATS attacks on NPC weapons if they get disarmed.

bSemiAutoQueue
Queue the next shot for semi-automatic weapons if the trigger is pulled within a specified time frame before the current shot is completed.
Options (Firing Queue)
  fQueuePreAnimEnd - time window (in seconds) before a weapon's firing animation ends during which the next shot can be pre-queued. Vanilla is 0.5 seconds.
  fQueuePreAttackTextKey - time window (in seconds) before the weapon's firing animation 'a: key' where the next shot can be pre-queued. Vanilla is 0 seconds (not a feature).

bShowCaravanCardsInMiscTabs
Show caravan cards in the misc tab for containers and barter.

bSubtitlesShowActorNames
Show the speaker's name in subtitles.

bShowModNameInPerkDescriptions
Show the source mod of perks in the perk menu.
Options (Perks Show Source Mod):
  sPrefix - prefix shown before the mod name
  bPipBoy - show mod name in the PipBoy

bLockpickRememberBobbyPinAngle
Don't reset the bobby pin angle when it breaks.

bNPCsTakeLimbFallDamage
Make NPCs take limb damage when falling.

bFallDeathsCauseDismemberment
Dismember/explode actor's legs if they die from a short/long fall.

bControllerTriggerDeadzones
Adds a configurable deadzone for LT/RT if used for the attack control.
Options (Controller Trigger Deadzones)
  iDeadzoneLT - deadzone for the left trigger (0-255)
  iDeadzoneRT - deadzone for the right trigger (0-255)

bExtendLockpickSpotRange
Expands the lockpick sweetspot range to the edges of the screen.

bContainerEncumbranceIndicator
Show container weight in red if taking an item will overencumber you.

bPreventTeammateFootstepSounds
Prevent companion footstep sounds playing.

bWeaponModdingSkillRequirement
Prevent modding weapons if you don't meet the weapon's skill requirements.

bNoEnvironmentRadiationInFullPowerArmor
Prevent environmental radiation when wearing full power armor.

bHapticPipboy
Vibrate controllers when changing Pip-Boy tabs.

bHiddenFragsFix
Allow fragging unplayable explosives NPCs have equipped, e.g. Ghost People's Gas Tanks.

bPlantingLiveGrenadesRequiresWeaponSkill
Prevent reverse pickpocketing live grenades if you don't meet the weapon skill requirements.

bDisplayItemEffectTotals
Show item effect totals in the Pip-Boy e.g. HP +26(3s) -> HP +78 (26x3s).

bDisableInventoryRightClickDrop
Prevent right clicking dropping items in the Pip-Boy.

bNoHotkeyEquipSounds
Prevent equip/unequip sounds when using weapon hotkeys.

bNoCompanionItemDamage
Prevent companion items taking damage.

bAutoUnlockTerminals
Automatically skip the hacking minigame if your science skill is over the terminal's science requirement.
Options (Auto Unlock Terminals):
  iThreshold - difference in lock/skill level for automatically unlocking the lock
  fRewardXPScale - scale applied to rewarded XP

bReloadingPreventsWeaponHotkeys
Prevent using weapon hotkeys while reloading.

bTimescaleAffectsMinigames
Scale minigame speed by the global time multiplier.

bWaterSourcesShowH2O
Show the H2O restored instead of HP when viewing water sources.
Options (Water Sources Show H2O):
  bRequireShiftHeld - require holding shift to view the alternate stats

bTabClosesPipboyFromKeyAndLimbMenus
Make tab close the pipboy from within the Inventory keys and Stats limb selection submenus

bMapSelectableCompanions
Allow clicking on hired companions in the map to summon them.
Options (Map Selectable Companions):
  sSummonAll - text shown on the summon all button when you have multiple companions
  bAllowSummonUnconsious - allow summoning unconsious companions

bEnduranceScalesMinFallHeight
Scale player minimum fall damage height by endurance.
Formula: fJumpFallHeightMin * (1 + (fBaseBonus + (endurance - 5) * fEnduranceMult))
Options (Endurance Scales Min Fall Height):
  fBaseBonus
  fEnduranceMult

bJumpSwimsUpwards
Make jumping swim upwards while underwater.
Options (Jump Swims Upwards):
  fSpeedScale - speed of up/downwards movement
  bSwimUpWhileAutowalking - automatically swim upwards if automove is enabled

bArmorCausesSinking
Make player sink if armor is heavy.
Options (Armor Causes Sinking):
  fRateNone - sink rate with no armor equipped
  fRateLight - sink rate with light armor equipped
  fRateMedium - sink rate with medium armor equipped
  fRateHeavy - sink rate with heavy armor equipped

bReputationShowsFameInfamy
Show fame and infamy values in the stats menu.
Options (Reputation Shows Fame):
  bPercentage - show fame/infamy as a percentage of the max reputation
  sFame - name for Fame stat
  sInfamy - name for Infamy stat

bRepairAllConfirmation
Add a confirmation when selecting 'Repair All' in the repair services menu.
Options (Repair All Confirmation):
  iPriceThreshold - repairs costing less than this amount won't ask for confirmation
  sMessage - confirmation message

bPreventNPCAddiction
Prevent NPCs gaining addiction status effects.

bNoDialogueZoom
Prevent the camera zooming in when entering dialogue.

bSeparateAlcoholEffects
Allow using different alcohols to stack their effects.

bGodModePreventsJamAnims
Prevent player weapon jam anims in godmode.

bScaleWeaponVolume
Allow scaling player/npc weapon fire sound volume.
Options (Weapon Volume Scaling):
  fPlayerScale - scale applied to player weapon fire sounds
  fNonPlayerScale - scale applied to non-player weapon fire sounds

bExplodingDestructibleIndicator
Show explosive destructibles on the grenade indicator.

bVATSIgnoreNonExplosiveProjectiles
Prevent targeting non-explosive projectiles in VATS.

bSleepHealingMinDuration
Require sleeping for some time before health is restored on unowned beds.
Options (Sleep Healing):
  iMinDuration - minimum sleep hours before player is healed
  bMiscStatRequiresSleepDuration - only increase the 'times slept' misc stat if you sleep for the min duration

bUseHitLocationInCinematicKillcams
Make the (non-VATS) cinematic killcam focus on the hit body part.

bScaleRadioVolume
Scale the volume of radio music and conversations independently.
Options (Radio Volume Scaling):
  fMusicScale - scale applied to radio music volume
  fDialogueScale - scale applied to radio dialogue volume

bVATSThrowablesUseVisibility
Scale thrown (non-grenade) hit percentages based on body part visibility.

bVATSStopFollowingDeadTargets
Stop rotating to follow targets once they are dead.

bReplaceHelpWithConsole
Replace the 'Help' pause menu button with a button for opening the console.
Options (Help Button Replacer):
  sButtonLabel - pause menu console label

bAutoReadNotes
Automatically open the note menu when notes are added to the player in dialog, containers or barter. Requires Book Menu Restored.
Options (Auto Read Notes):
  bHolotapeSupport - automatically play holotapes (after dialog ends)
  sHolotapeMessageTitle - title shown in the holotape confirmation messagebox
  sHolotapeMessageText - text shown in the holotape confirmation messagebox (leave blank to skip messagebox)

bHostilesPrioritizePlayer
Force attackers to prioritize player over companions.
Options (Hostiles Prioritize Player):
  fSwapToPlayerChanceStartCombat - chance to override a companion with player on combat start
  fSwapToPlayerChanceMidCombat - chance to override a companion with player during combat
  iPlayerDetectionThreshold - detection level required to switch to targeting the player

bEmboldenTagSkills
Show tag skills in bold in the Stats menu.

bRestoreLockedDoorSound
Play the unused DRSLocked sound when activating a lock you can't open.

bRadiationCausesRadioStatic
Add static to the pipboy radio when in an irradiated area.
Signal Strength is between 0 and 100.
Formula: Signal Strength -= fStaticMult * RadiationLevel
Options (Radiation Affects Radio):
  fStaticMult - multiplier applied to radiation

bDialogMenuDebugging
Show the topic editor id beside topics in the Dialog Menu.

bCharacterRadiation
Allow radiation to apply to Characters instead of only Creatures and the player.
Options (Character Radiation):
  bAllowRadiationStages - allow radiation stages to apply to everyone, not just the player

bActorsStickToSlopes
Prevent actors from shooting forward into the air when walking down slopes and stairs.

bGodModeAllowsCraftingWithoutRequirements
Allow crafting items without their requirements if godmode is enabled.

bKarmaTitleShowsValue
Show karma value in the Stats menu.

----------------
[Hotkeys]
To use any hotkeys, replace the ' = 0 ' with the scancode of the desired key, according to http://fose.silverlock.org/fose_command_doc.html#DirectX_Scancodes. If the link dies, just search for 'DirectX Scancodes'.
For example, 'iOpenMapKey = 50' sets the open map key to be M.

iScreenshotKey - default: Print Scrn
iPipboyStatsKey - default: F1
iPipboyItemsKey - default: F2
iPipboyDataKey - default: F3
iVATSAcceptKey - default: E
iConsoleKey - default: ~
iExitToMainMenuKey - exits to main menu
iExitGameKey - quits the game
iDisableCollisionKey - disables player collision while held
iTogglePipboyLightKey - toggles the Pip-Boy light, and the night vision scope effect if bAddNightVisionToggle is enabled
iHolsterWeaponKey - holster the current weapon, disables holding reload to holster weapon
iOpenQuestsKey - GameMode key to open the Pip-Boy quests tab, J key switches to the tab while in the Pip-Boy Menu
iOpenRadioKey - GameMode key to open the Pip-Boy radios tab, P key switches to the tab while in the Pip-Boy menu
iRadioVolumeDownKey - GameMode key to decrease the radio volume
iRadioVolumeUpKey - GameMode key to increase the radio volume
iToggleMenusKey - toggles the visibility of all menus (as the ToggleMenus command)
iToggleTrueIronSightsKey - toggles true ironsights mode
iToggleCrosshairKey - toggles visibility of the crosshair
iOpenLocalMapKey - GameMode key to open the Pip-Boy local map, N key switches to the map while in the Pip-Boy Menu
iToggleSneakIndicatorKey - toggles whether the sneak indicator is hidden
iDropEquippedWeaponKey - drops the equipped weapon
iNextRadioStationKey - select the next radio station
iPrevRadioStationKey - select the previous radio station
iSkipRadioSongKey - skip the current radio song or topic

iOpenMapKey - GameMode key to open the Pip-Boy world map, M key switches to the map while in the Pip-Boy Menu
Options (Map Hotkey):
  bShowLocalMapInInteriors - open the local map when in interiors
  
iRepeatActivateKey - continually presses the use key while held
Options (Repeated Activate Key): 
  bOnlyTakeItems - only take items while the key is held

iHideHUDKey - hides various elements on the main HUD
Options (Hide HUD Key): 
  bHideCompass - hide the compass/HP bar
  bHideAmmo - hide the ammo/AP bar
  bHideHardcoreNeeds - hide H2O, FOD and SLP indicators
  bHideSneak - hide the sneak indicator
  bHideByDefault - hide the HUD when loading a save

iEquipLastWeaponKey - equips the last equipped weapon
Options (Equip Last Weapon Hotkey):
  bIgnoreThrowables - don't set the last equipped weapon to be a thrown weapon
  bIgnoreNonDamageWeapons - ignore non-melee weapons with no projectiles
  bMousewheelSupport - add mousewheel to change weapons

iToggleSmoothCameraKey - toggles a cinematic camera, smoothing mouse/controller movements
Options (Smooth Camera):
  bDisableWhileAiming - disable the smooth camera while aiming

iPlaceMapMarkerAtPlayerPosKey - places the map marker at your current position
Options (Place Marker Hotkey):
  sMessage - message to show, leave blank for none
  sSound - editor ID of sound to play

iToggleSightingNodeHotkey - switch to using ##SightingNode2 if the weapon has one, toggle resets when changing weapons - the weapon FOV is multiplied by the node's scale
Options (Alt Sighting Node):
  bHotkeyWhileAimingOnly - ignore the swap hotkey unless aiming

----------------
Orphaned subsettings:  
(Skill Books):
  sReadBookSkillTooHighMessage - message shown when trying to read a book at max skill

----------------
[GameSettings]
GameSetting values can be written which are applied after esps have loaded.
Additionally, settings from ini files in the Data/NVSE/Plugins/Tweaks/Settings/ folder.
For example:
iLevelsPerPerk = 1
fPlayerDeathReloadTime = 3
fWorldMapMinZoom = 0.25
fLocalMapMinZoom = 0.25