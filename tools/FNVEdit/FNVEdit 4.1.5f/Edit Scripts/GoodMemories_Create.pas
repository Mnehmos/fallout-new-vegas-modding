{
  Good Memories — Unique Recharger Pistol
  Creates a new weapon record by cloning Recharger Pistol and modifying stats.

  Run on: WeapNVRechargerPistol in FalloutNV.esm
  Creates: WeapGoodMemories in target ESP

  After running, use console command to test:
    help "Good Memories" 4
    player.additem [FormID] 1
}

unit GoodMemoriesCreate;

var
  targetPlugin: IInterface;

function Initialize: Integer;
var
  i: Integer;
begin
  Result := 0;

  targetPlugin := nil;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'PerkOverhaul.esp') then begin
      targetPlugin := FileByIndex(i);
      Break;
    end;
  end;

  if not Assigned(targetPlugin) then begin
    targetPlugin := AddNewFile;
    if not Assigned(targetPlugin) then begin
      AddMessage('[GoodMemories] ERROR: No target plugin. Aborting.');
      Result := 1;
      Exit;
    end;
  end;

  AddMessage('[GoodMemories] Creating unique recharger pistol...');
  AddMessage('[GoodMemories] Target: ' + GetFileName(targetPlugin));
end;

function Process(e: IInterface): Integer;
var
  newWeap: IInterface;
begin
  Result := 0;

  if Signature(e) <> 'WEAP' then Exit;
  if not SameText(EditorID(e), 'WeapNVRechargerPistol') then Exit;

  AddMessage('  Found base weapon: ' + EditorID(e));

  AddRequiredElementMasters(e, targetPlugin, False);
  newWeap := wbCopyElementToFile(e, targetPlugin, True, True);

  if not Assigned(newWeap) then begin
    AddMessage('  ERROR: Failed to copy weapon record');
    Exit;
  end;

  // Identity
  SetElementEditValues(newWeap, 'EDID', 'WeapGoodMemories');
  SetElementEditValues(newWeap, 'FULL', 'Good Memories');
  SetElementEditValues(newWeap, 'DESC', 'Some memories sustain you — a warm fire, a kind word, the hum of a well-tuned capacitor. This prototype recharger was hand-tuned before the War by someone who believed good things should last. It never runs out. It never lets you down. Mnemosyne remembers the light, too.');

  // Core stats
  SetElementEditValues(newWeap, 'DNAM\Value', '6500');
  SetElementEditValues(newWeap, 'DNAM\Weight', '2.5');
  SetElementEditValues(newWeap, 'DNAM\Damage', '38');
  SetElementEditValues(newWeap, 'DNAM\Clip Size', '8');
  SetElementEditValues(newWeap, 'DNAM\Action Point Cost', '17');
  SetElementEditValues(newWeap, 'DNAM\Min Spread', '0.8');
  SetElementEditValues(newWeap, 'DNAM\Fire Rate', '5.5');
  SetElementEditValues(newWeap, 'DNAM\Health', '200');

  // Critical
  SetElementEditValues(newWeap, 'CRDT\Damage', '38');
  SetElementEditValues(newWeap, 'CRDT\% Mult', '1.5');

  AddMessage('  Created: WeapGoodMemories "Good Memories"');
  AddMessage('  FormID: ' + IntToHex(FormID(newWeap), 8));
  AddMessage('');
  AddMessage('  Stats:');
  AddMessage('    Damage:     38 (was 18)');
  AddMessage('    Crit Dmg:   38 (was 18)');
  AddMessage('    Crit Mult:  x1.5 (was x1)');
  AddMessage('    Fire Rate:  5.5 (was 4.0)');
  AddMessage('    Magazine:   8 (was 5)');
  AddMessage('    AP Cost:    17 (was 20)');
  AddMessage('    Spread:     0.8 (was 1.5)');
  AddMessage('    Weight:     2.5 (was 3.5)');
  AddMessage('    Value:      6500 (was 800)');
  AddMessage('    Health:     200 (was 75)');
  AddMessage('');
  AddMessage('  To test in-game:');
  AddMessage('    help "Good Memories" 4');
  AddMessage('    player.additem [FormID] 1');
end;

function Finalize: Integer;
begin
  Result := 0;
  AddMessage('[GoodMemories] Done. Save the ESP to keep changes.');
end;

end.
