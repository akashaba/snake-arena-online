import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { GameBoard } from "@/components/game/GameBoard";
import { GameControls } from "@/components/game/GameControls";
import { Button } from "@/components/ui/button";
import { useGameLogic } from "@/hooks/useGameLogic";
import { mockAuth, mockLeaderboardAPI, type User } from "@/services/mockBackend";
import { useToast } from "@/hooks/use-toast";
import { Trophy, Eye, LogOut, LogIn } from "lucide-react";

const Index = () => {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();
  const { toast } = useToast();
  const {
    gameState,
    isPaused,
    startGame,
    pauseGame,
    resumeGame,
    switchMode,
  } = useGameLogic("walls");

  useEffect(() => {
    const currentUser = mockAuth.getCurrentUser();
    setUser(currentUser);
  }, []);

  useEffect(() => {
    // Submit score when game is over
    if (gameState.isGameOver && gameState.score > 0 && user) {
      mockLeaderboardAPI.submitScore(gameState.score, gameState.mode);
    }
  }, [gameState.isGameOver, gameState.score, gameState.mode, user]);

  const handleLogout = async () => {
    await mockAuth.logout();
    setUser(null);
    toast({
      title: "Logged out",
      description: "See you next time!",
    });
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-5xl font-bold text-primary neon-text mb-2">NEON SNAKE</h1>
            <p className="text-muted-foreground">Classic arcade game with a cyber twist</p>
          </div>
          
          <div className="flex items-center gap-4">
            {user ? (
              <>
                <div className="text-right">
                  <p className="text-sm text-muted-foreground">Playing as</p>
                  <p className="text-lg font-bold text-primary neon-text">{user.username}</p>
                </div>
                <Button variant="outline" onClick={handleLogout} className="gap-2">
                  <LogOut className="w-4 h-4" />
                  Logout
                </Button>
              </>
            ) : (
              <Button onClick={() => navigate("/auth")} className="gap-2">
                <LogIn className="w-4 h-4" />
                Login / Sign Up
              </Button>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-8 mb-8">
          {/* Game Board */}
          <div className="flex justify-center items-start">
            <GameBoard gameState={gameState} />
          </div>

          {/* Controls */}
          <GameControls
            isPaused={isPaused}
            isGameOver={gameState.isGameOver}
            mode={gameState.mode}
            score={gameState.score}
            onStart={startGame}
            onPause={pauseGame}
            onResume={resumeGame}
            onModeChange={switchMode}
          />
        </div>

        {/* Navigation Buttons */}
        <div className="flex gap-4 justify-center">
          <Button
            variant="outline"
            onClick={() => navigate("/leaderboard")}
            className="gap-2"
          >
            <Trophy className="w-4 h-4" />
            Leaderboard
          </Button>
          <Button
            variant="outline"
            onClick={() => navigate("/spectate")}
            className="gap-2"
          >
            <Eye className="w-4 h-4" />
            Spectate
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Index;
