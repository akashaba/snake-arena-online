# Start both backend and frontend servers
# Run this from the root directory

Write-Host "🚀 Starting Neon Snake Arena servers..." -ForegroundColor Cyan
Write-Host ""

# Start backend in new terminal
Write-Host "📦 Starting Backend (http://localhost:8000)..." -ForegroundColor Green
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd backend; uv run python run.py"

# Wait a bit for backend to start
Start-Sleep -Seconds 2

# Start frontend in new terminal  
Write-Host "🎮 Starting Frontend (http://localhost:8080)..." -ForegroundColor Green
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "✅ Both servers starting!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Frontend:    http://localhost:8080" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test credentials:" -ForegroundColor Cyan
Write-Host "  Email:    neon@example.com" -ForegroundColor White
Write-Host "  Password: password123" -ForegroundColor White
Write-Host ""
