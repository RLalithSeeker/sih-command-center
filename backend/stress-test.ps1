Add-Type -AssemblyName System.Net.Http
$base = 'http://localhost:5000'
$script:pass = 0; $script:fail = 0
function Check($name, $cond, $detail) {
  if ($cond) { $script:pass++; Write-Host "PASS  $name" }
  else { $script:fail++; Write-Host "FAIL  $name  ::  $detail" }
}
$client = New-Object System.Net.Http.HttpClient
$client.Timeout = [TimeSpan]::FromSeconds(30)
function Raw($method, $url, $rawBody, $headers) {
  $m = New-Object System.Net.Http.HttpRequestMessage((New-Object System.Net.Http.HttpMethod($method)), "$base$url")
  if ($headers) { foreach ($k in $headers.Keys) { $m.Headers.TryAddWithoutValidation($k, $headers[$k]) | Out-Null } }
  if ($null -ne $rawBody) { $m.Content = New-Object System.Net.Http.StringContent($rawBody, [System.Text.Encoding]::UTF8, 'application/json') }
  $resp = $client.SendAsync($m).GetAwaiter().GetResult()
  $txt = $resp.Content.ReadAsStringAsync().GetAwaiter().GetResult()
  @{ status = [int]$resp.StatusCode; text = $txt }
}

Write-Host '--- A. Malformed / hostile payloads ---'
# raw body cases: (name, method, url, body, expected status)
$cases = @(
  @{ n='invalid JSON body'; m='POST'; u='/api/teams'; b='{not json!!'; e=400 },
  @{ n='empty body POST teams'; m='POST'; u='/api/teams'; b=''; e=400 },
  @{ n='array instead of object'; m='POST'; u='/api/teams'; b='[]'; e=400 },
  @{ n='null body'; m='POST'; u='/api/teams'; b='null'; e=400 },
  @{ n='wrong content-type body'; m='POST'; u='/api/teams'; b='teamName=X'; e=400 },
  @{ n='members not array (string)'; m='POST'; u='/api/teams'; b='{"teamName":"T","leadEmail":"x@x.edu","members":"six"}'; e=400 },
  @{ n='members null entries'; m='POST'; u='/api/teams'; b='{"teamName":"T","leadEmail":"x@x.edu","members":[null,null,null,null,null,null]}'; e=400 },
  @{ n='member missing gender'; m='POST'; u='/api/teams'; b='{"teamName":"T","leadEmail":"x@x.edu","members":[{"name":"A","email":"a@x.edu"},{"name":"B","email":"b@x.edu"},{"name":"C","email":"c@x.edu"},{"name":"D","email":"d@x.edu"},{"name":"E","email":"e@x.edu"},{"name":"F","email":"f@x.edu"}]}'; e=400 },
  @{ n='7 members rejected'; m='POST'; u='/api/teams'; b='{"teamName":"T","leadEmail":"x@x.edu","members":[{"name":"1","gender":"female"},{"name":"2","gender":"male"},{"name":"3","gender":"male"},{"name":"4","gender":"male"},{"name":"5","gender":"male"},{"name":"6","gender":"male"},{"name":"7","gender":"male"}]}'; e=400 },
  @{ n='XSS team name stored'; m='POST'; u='/api/teams'; b='{"teamName":"<script>alert(1)</script>","leadEmail":"x@x.edu","members":[{"name":"A","gender":"female","email":"a@x.edu"},{"name":"B","gender":"male"},{"name":"C","gender":"male"},{"name":"D","gender":"male"},{"name":"E","gender":"male"},{"name":"F","gender":"male"}]}'; e=200 }
)
foreach ($c in $cases) {
  $r = Raw $c.m $c.u $c.b $null
  Check ("A: " + $c.n) ($r.status -eq $c.e) "got $($r.status), expected $($c.e) :: $($r.text.Substring(0, [Math]::Min(120, $r.text.Length)))"
}
# find XSS team and check report.html escaping
$teams = (Raw GET '/api/teams' $null $null)
$xssTeam = ($teams.text | ConvertFrom-Json) | Where-Object { $_.teamName -match 'script' }
if ($xssTeam) {
  $rep = Raw GET '/api/report.html' $null $null
  $unescaped = $rep.text -match '<script>alert\(1\)</script>'
  Check 'A: XSS escaped in report.html' (-not $unescaped) 'raw <script> injected into report HTML'
  $csv = Raw GET '/api/export.csv' $null $null
  Check 'A: XSS survives as text in CSV (no HTML exec)' ($csv.status -eq 200) "csv status $($csv.status)"
} else { Check 'A: XSS team found for report check' $false 'team missing' }

Write-Host '--- B. Wrong methods / unknown routes ---'
$r = Raw DELETE '/api/teams' $null $null
Check 'B: DELETE /api/teams = 404' ($r.status -eq 404) "got $($r.status)"
$r = Raw GET '/api/nope/nothing' $null $null
Check 'B: unknown route = 404' ($r.status -eq 404) "got $($r.status)"
$r = Raw GET '/api/../../etc/passwd' $null $null
Check 'B: path traversal blocked' ($r.status -eq 404 -or $r.status -eq 400) "got $($r.status)"
$r = Raw PUT '/api/deliverables/whatever' '{"type":"x"}' $null
Check 'B: PUT unknown deliverable = 404' ($r.status -eq 404) "got $($r.status)"


Write-Host '--- C. Boundary values ---'
# huge team name (100KB)
$bigName = 'A' * 100000
$r = Raw POST '/api/teams' ("{`"teamName`":`"" + $bigName + "`",`"leadEmail`":`"x@x.edu`",`"members`":[{`"name`":`"A`",`"gender`":`"female`"},{`"name`":`"B`",`"gender`":`"male`"},{`"name`":`"C`",`"gender`":`"male`"},{`"name`":`"D`",`"gender`":`"male`"},{`"name`":`"E`",`"gender`":`"male`"},{`"name`":`"F`",`"gender`":`"male`"}]}") $null
Check 'C: 100KB team name handled' ($r.status -eq 200 -or $r.status -eq 413) "got $($r.status)"
# unicode
$r = Raw POST '/api/ps' '{"code":"SIH999","title":"\u0924\u0947\u091c\u0938 \u092a\u094d\u0930\u094b\u091c\u0947\u0915\u094d\u091f","category":"software"}' $null
Check 'C: unicode PS created' ($r.status -eq 200) "got $($r.status)"
# very long search query
$r = Raw GET ('/api/ps?q=' + ('z' * 5000)) $null $null
Check 'C: 5KB search query OK' ($r.status -eq 200) "got $($r.status)"
# weird types
$r = Raw POST '/api/milestones' '{"name":123,"date":456}' $null
Check 'C: numeric name/date rejected or coerced' ($r.status -eq 400 -or $r.status -eq 200) "got $($r.status)"
# past date milestone
$r = Raw POST '/api/milestones' '{"name":"Past","date":"1900-01-01"}' $null
Check 'C: past date milestone accepted' ($r.status -eq 200) "got $($r.status)"
$ms = (Raw GET '/api/milestones' $null $null).text | ConvertFrom-Json
$past = $ms | Where-Object { $_.name -eq 'Past' }
Check 'C: past milestone daysLeft negative' ($past.daysLeft -lt 0) "daysLeft=$($past.daysLeft)"

Write-Host '--- D. Load / stress ---'
$sw = [System.Diagnostics.Stopwatch]::StartNew()
for ($i = 0; $i -lt 200; $i++) { $r = Raw GET '/api/dashboard' $null $null; if ($r.status -ne 200) { break } }
$sw.Stop()
Check 'D: 200 sequential GETs all 200' ($r.status -eq 200) "stopped at $($r.status)"
Write-Host ("  sequential: 200 reqs in " + $sw.ElapsedMilliseconds + " ms")

# concurrent: 50 parallel GETs via runspace pool
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$rs = [runspacefactory]::CreateRunspacePool(1, 20); $rs.Open()
$scriptBlock = {
  param($n)
  Add-Type -AssemblyName System.Net.Http
  $c = New-Object System.Net.Http.HttpClient
  $ok = 0
  for ($i = 0; $i -lt $n; $i++) {
    try {
      $resp = $c.GetAsync('http://localhost:5000/api/dashboard').GetAwaiter().GetResult()
      if ([int]$resp.StatusCode -eq 200) { $ok++ }
    } catch { }
  }
  return $ok
}
$jobs = 1..5 | ForEach-Object {
  $pc = [System.Management.Automation.PowerShell]::Create().AddScript($scriptBlock)
  [void]$pc.AddParameter('n', 10)
  $pc.RunspacePool = $rs
  @{ pc = $pc; job = $pc.BeginInvoke() }
}
$okTotal = 0
$jobs | ForEach-Object { $okTotal += $_.pc.EndInvoke($_.job)[0] }
$rs.Close(); $rs.Dispose()
$sw.Stop()
Check 'D: 50 concurrent GETs all 200' ($okTotal -eq 50) "ok=$okTotal"
Write-Host ("  concurrent: 50 reqs in " + $sw.ElapsedMilliseconds + " ms")

# concurrent writes: 10 parallel team creations
$rs = [runspacefactory]::CreateRunspacePool(1, 10); $rs.Open()
$scriptBlock2 = {
  param($i)
  Add-Type -AssemblyName System.Net.Http
  $c = New-Object System.Net.Http.HttpClient
  $body = '{"teamName":"Load' + $i + '","leadEmail":"load' + $i + '@x.edu","members":[{"name":"A","gender":"female"},{"name":"B","gender":"male"},{"name":"C","gender":"male"},{"name":"D","gender":"male"},{"name":"E","gender":"male"},{"name":"F","gender":"male"}]}'
  $content = New-Object System.Net.Http.StringContent($body, [System.Text.Encoding]::UTF8, 'application/json')
  $resp = $c.PostAsync('http://localhost:5000/api/teams', $content).GetAwaiter().GetResult()
  return [int]$resp.StatusCode
}
$jobs2 = 1..10 | ForEach-Object {
  $pc = [System.Management.Automation.PowerShell]::Create().AddScript($scriptBlock2)
  [void]$pc.AddParameter('i', $_)
  $pc.RunspacePool = $rs
  @{ pc = $pc; job = $pc.BeginInvoke() }
}
$statuses = $jobs2 | ForEach-Object { $_.pc.EndInvoke($_.job)[0] }
$rs.Close(); $rs.Dispose()
$created = ($statuses | Where-Object { $_ -eq 200 }).Count
Check 'D: 10 concurrent team creates all 200' ($created -eq 10) "created=$created :: $($statuses -join ',')"

$h = Raw GET '/api/health' $null $null
Check 'D: server alive after stress' ($h.status -eq 200 -and $h.text -match 'ok') "got $($h.status)"
$tAfter = ((Raw GET '/api/teams' $null $null).text | ConvertFrom-Json).Count
Check 'D: all created teams persisted in memory' ($tAfter -ge 11) "teams=$tAfter"

Write-Host ''
Write-Host "==== STRESS RESULT: $script:pass passed, $script:fail failed ===="
