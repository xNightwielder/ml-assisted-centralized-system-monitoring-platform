$cpuProcesses = Get-Process | Where-Object { $_.CPU -gt 0 }
$count = $cpuProcesses.Count
Write-Output "win_system cpu_active_count=$count"