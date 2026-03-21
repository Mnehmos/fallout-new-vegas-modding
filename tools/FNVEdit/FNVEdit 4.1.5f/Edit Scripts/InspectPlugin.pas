{
  Inspect Plugin — dump record type counts and key records
  Run on any plugin to see what it contains
}

unit InspectPlugin;

var
  typeCounts: TStringList;

function Initialize: Integer;
begin
  Result := 0;
  typeCounts := TStringList.Create;
  typeCounts.Sorted := True;
  typeCounts.Duplicates := dupIgnore;
  AddMessage('[Inspect] Counting records by type...');
end;

function Process(e: IInterface): Integer;
var
  sig: string;
  idx: Integer;
begin
  Result := 0;
  sig := Signature(e);

  idx := typeCounts.IndexOf(sig);
  if idx >= 0 then
    typeCounts.Objects[idx] := TObject(Integer(typeCounts.Objects[idx]) + 1)
  else
    typeCounts.AddObject(sig, TObject(1));
end;

function Finalize: Integer;
var
  i, count, total: Integer;
begin
  Result := 0;
  total := 0;

  AddMessage('');
  AddMessage('=== RECORD TYPE SUMMARY ===');
  AddMessage('');

  for i := 0 to Pred(typeCounts.Count) do begin
    count := Integer(typeCounts.Objects[i]);
    total := total + count;
    if count > 0 then
      AddMessage('  ' + typeCounts[i] + ': ' + IntToStr(count));
  end;

  AddMessage('');
  AddMessage('Total: ' + IntToStr(total) + ' records across ' + IntToStr(typeCounts.Count) + ' types');

  typeCounts.Free;
  AddMessage('[Inspect] Done');
end;

end.
