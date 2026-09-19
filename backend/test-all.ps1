$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName System.Net.Http
$base = 'http://localhost:5000'
$pass = 0; $fail = 0
function Check($name, $cond, $detail) {
  if ($cond) { $script:pass++; Write-Host "PASS  $name" }
  else { $script:fail++; Write-Host "FAIL  $name  ::  $detail" }
}
function Req($method, $url, $body) {
  try {
    $client = New-Object System.Net.Http.HttpClient
    $m = New-Object System.Net.Http.HttpRequestMessage((New-Object System.Net.Http.HttpMethod($method)), "$base$url")
    if ($body) {
      $json = $body | ConvertTo-Json -Depth 5
      $m.Content = New-Object System.Net.Http.StringContent($json, [System.Text.Encoding]::UTF8, 'application/json')
    }
    $resp = $client.SendAsync($m).GetAwaiter().GetResult()
    $txt = $resp.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    @{ status = [int]$resp.StatusCode; data = ($txt | ConvertFrom-Json) }
  } catch { @{ status = -1; data = $null; err = $_ } }
}

# 1. Health
$h = Req GET '/api/health'; Check 'health ok+memory' ($h.status -eq 200 -and $h.data.ok -and $h.data.mode -eq 'memory') ($h.status)

# 2. Seed data
$ps = Req GET '/api/ps'; Check 'GET /api/ps seed=3' ($ps.status -eq 200 -and $ps.data.Count -eq 3) "$($ps.data.Count)"
$psSearch = Req GET '/api/ps?q=SIH25123'; Check 'PS search by sihId' ($psSearch.status -eq 200 -and $psSearch.data.Count -eq 1 -and $psSearch.data[0].title -match 'soil') "$($psSearch.data.Count)"
$takenMarked = @($ps.data | Where-Object { $_.id -eq 'ps1' -and $_.takenBy -eq 'Demo Spartans' })
Check 'PS takenBy marked' ($takenMarked.Count -eq 1) "count=$($takenMarked.Count)"
$mentors = Req GET '/api/mentors'; Check 'GET /api/mentors seed=2' ($mentors.status -eq 200 -and $mentors.data.Count -eq 2) "$($mentors.data.Count)"
$teams = Req GET '/api/teams'; Check 'GET /api/teams seed=1' ($teams.status -eq 200 -and $teams.data.Count -eq 1) "$($teams.data.Count)"
$t1 = $teams.data[0]
$ms = Req GET '/api/milestones'; Check 'milestones seed=3 +daysLeft' ($ms.status -eq 200 -and $ms.data.Count -eq 3 -and $ms.data[0].daysLeft -eq 14) "$($ms.data[0].daysLeft)"

# 3. Team validation
$bad = Req POST '/api/teams' @{ teamName='Bad5'; leadEmail='bad@x.edu'; members=@(1..5 | ForEach-Object { @{ name="M$_"; gender='male'; email="m$_@x.edu" } }) }
Check 'POST team 5-members rejected 400' ($bad.status -eq 400 -and $bad.data.error -match 'exactly 6') ($bad.status)
$allm = Req POST '/api/teams' @{ teamName='AllMale'; leadEmail='am@x.edu'; members=@(1..6 | ForEach-Object { @{ name="M$_"; gender='male'; email="m$_@x.edu" } }) }
Check 'POST team 0-female rejected 400' ($allm.status -eq 400 -and $allm.data.error -match 'female') ($allm.status)
$noname = Req POST '/api/teams' @{ leadEmail='x@x.edu'; members=@() }
Check 'POST team no-name rejected 400' ($noname.status -eq 400) ($noname.status)
$mem = @(1..6 | ForEach-Object { $g = if ($_ -eq 1) { 'female' } else { 'male' }; @{ name="TM$_"; gender=$g; email="tm$_@x.edu" } })
$good = Req POST '/api/teams' @{ teamName='Test Titans'; leadEmail='titans@x.edu'; members=$mem }
Check 'POST valid team 200 + id' ($good.status -eq 200 -and $good.data.id) "status=$($good.status)"
$tid = $good.data.id
$dv = Req GET "/api/deliverables/$tid"; Check 'new team gets 4 deliverables' ($dv.status -eq 200 -and $dv.data.Count -eq 4) "$($dv.data.Count)"

# 4. PS selection + duplicate guard
$dup = Req POST "/api/teams/$tid/select-ps" @{ psId='ps1' }
Check 'select-ps duplicate blocked 400' ($dup.status -eq 400 -and $dup.data.error -match 'Already taken') ($dup.status)
$okps = Req POST "/api/teams/$tid/select-ps" @{ psId='ps2' }
Check 'select-ps valid 200' ($okps.status -eq 200 -and $okps.data.psId -eq 'ps2') ($okps.status)
$badps = Req POST "/api/teams/$tid/select-ps" @{ psId='nope' }
Check 'select-ps invalid PS 400' ($badps.status -eq 400) ($badps.status)

# 5. Mentor assignment
$auto = Req POST "/api/teams/$tid/auto-mentor" @{}
Check 'auto-mentor assigns least-loaded' ($auto.status -eq 200 -and $auto.data.mentorId) "$($auto.data.mentorId)"
$badm = Req POST "/api/teams/$tid/assign-mentor" @{ mentorId='nope' }
Check 'assign-mentor invalid 400' ($badm.status -eq 400) ($badm.status)

Check 'seed team readiness=25' ($t1.readiness -eq 25) "got $($t1.readiness)"

# 6. Deliverables -> readiness 100
foreach ($ty in @('github','ppt','video','report')) {
  $u = Req PUT "/api/deliverables/$tid" @{ type=$ty; link="https://x/$ty"; status='approved' }
  Check "PUT deliverable $ty approved" ($u.status -eq 200) ($u.status)
}
$uBad = Req PUT "/api/deliverables/$tid" @{ type='github'; status='bogus' }
Check 'PUT bad status rejected' ($uBad.status -eq 400) ($uBad.status)
$tm = Req GET "/api/teams/$tid"
Check 'readiness=100 after all approved' ($tm.status -eq 200 -and $tm.data.readiness -eq 100) "$($tm.data.readiness)"

# 7. Dashboard filters
$dash = Req GET '/api/dashboard'
Check 'dashboard total=2' ($dash.status -eq 200 -and $dash.data.total -eq 2) "$($dash.data.total)"
$dashR = Req GET '/api/dashboard?status=ready'
Check 'dashboard ?status=ready =1' ($dashR.status -eq 200 -and $dashR.data.total -eq 1) "$($dashR.data.total)"
$dashP = Req GET '/api/dashboard?status=pending'
Check 'dashboard ?status=pending =1' ($dashP.status -eq 200 -and $dashP.data.total -eq 1) "$($dashP.data.total)"
$dashC = Req GET '/api/dashboard?category=hardware'
Check 'dashboard ?category=hardware =0' ($dashC.status -eq 200 -and $dashC.data.total -eq 0) "$($dashC.data.total)"

# 8. Exports
try { $csv = Invoke-WebRequest "$base/api/export.csv" -UseBasicParsing } catch { $csv = $null }
Check 'export.csv 200 + header' ($csv -and $csv.StatusCode -eq 200 -and $csv.Content -match '"Team","PS","Mentor"') ($csv.StatusCode)
try { $rep = Invoke-WebRequest "$base/api/report.html" -UseBasicParsing } catch { $rep = $null }
Check 'report.html 200 + table' ($rep -and $rep.StatusCode -eq 200 -and $rep.Content -match '<table>') ''

# 9. Milestones validation
$badMs = Req POST '/api/milestones' @{ name='X'; date='not-a-date' }
Check 'milestone bad date 400' ($badMs.status -eq 400) ($badMs.status)
$okMs = Req POST '/api/milestones' @{ name='Demo day'; date='2026-12-01' }
Check 'milestone create 200' ($okMs.status -eq 200 -and $okMs.data.id) ($okMs.status)

# 10. 404 routes
$n404 = Req GET '/api/teams/nope'
Check 'GET unknown team 404' ($n404.status -eq 404) ($n404.status)

# 11. Frontend files
$fe = 'C:\Users\starl\woxsen\SEM 5\Fullstack (notes)\sih-command-center\frontend'
foreach ($pg in @('index.html','ps.html','teams.html','mentors.html','deliverables.html')) {
  Check "frontend $pg exists" (Test-Path "$fe\$pg") ''
}
$js = Get-Content "$fe\js\app.js" -Raw
Check 'app.js points at localhost:5000' ($js -match 'localhost:5000|:5000/api') ''
$todo = Select-String -Path "$fe\js\app.js" -Pattern 'TODO|FIXME|lorem'
Check 'no TODO/FIXME in app.js' (-not $todo) ''

Write-Host ''
Write-Host "==== RESULT: $pass passed, $fail failed ===="
