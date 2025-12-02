import { useEffect, useState } from "react";
import { spectateAPI, type ActivePlayer } from "@/services/api";
import { GRID_SIZE_CONSTANT } from "@/lib/gameEngine";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const SpectateGrid = () => {
  const [players, setPlayers] = useState<ActivePlayer[]>([]);

  useEffect(() => {
    const loadPlayers = async () => {
      try {
        const data = await spectateAPI.getActivePlayers();
        setPlayers(data);
      } catch (error) {
        console.error('Failed to load active players:', error);
      }
    };

    loadPlayers();
    const interval = setInterval(loadPlayers, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, []);

  const MiniGameBoard = ({ player }: { player: ActivePlayer }) => {
    const cellSize = 12;
    const boardSize = GRID_SIZE_CONSTANT * cellSize;

    return (
      <div className="relative scanlines" style={{ width: boardSize, height: boardSize }}>
        <div 
          className="absolute inset-0 bg-card/50 border neon-border"
          style={{
            backgroundImage: `
              linear-gradient(to right, hsl(var(--grid-line)) 1px, transparent 1px),
              linear-gradient(to bottom, hsl(var(--grid-line)) 1px, transparent 1px)
            `,
            backgroundSize: `${cellSize}px ${cellSize}px`,
          }}
        />

        {/* Food */}
        <div
          className="absolute"
          style={{
            left: player.food.x * cellSize,
            top: player.food.y * cellSize,
            width: cellSize - 1,
            height: cellSize - 1,
          }}
        >
          <div className="w-full h-full bg-food rounded-sm animate-pulse" />
        </div>

        {/* Snake */}
        {player.snake.map((segment, index) => (
          <div
            key={`${segment.x}-${segment.y}-${index}`}
            className="absolute"
            style={{
              left: segment.x * cellSize,
              top: segment.y * cellSize,
              width: cellSize - 1,
              height: cellSize - 1,
            }}
          >
            <div className={`w-full h-full bg-snake rounded-sm ${index === 0 ? "opacity-100" : "opacity-70"}`} />
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {players.map((player) => (
        <Card key={player.id} className="overflow-hidden">
          <CardHeader className="pb-3">
            <div className="flex justify-between items-center">
              <CardTitle className="text-lg text-primary neon-text">{player.username}</CardTitle>
              <div className="flex gap-4 text-sm">
                <span className="text-muted-foreground">Score: <span className="text-foreground font-bold">{player.score}</span></span>
                <span className="text-muted-foreground">Mode: <span className="text-accent">{player.mode}</span></span>
              </div>
            </div>
          </CardHeader>
          <CardContent className="flex justify-center">
            <MiniGameBoard player={player} />
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
