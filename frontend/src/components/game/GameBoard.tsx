import { GRID_SIZE_CONSTANT } from "@/lib/gameEngine";
import type { GameState } from "@/lib/gameEngine";

interface GameBoardProps {
  gameState: GameState;
}

export const GameBoard = ({ gameState }: GameBoardProps) => {
  const cellSize = 20;
  const boardSize = GRID_SIZE_CONSTANT * cellSize;

  return (
    <div className="relative scanlines" style={{ width: boardSize, height: boardSize }}>
      {/* Grid background */}
      <div 
        className="absolute inset-0 bg-card border-2 neon-border"
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
        className="absolute transition-all duration-100"
        style={{
          left: gameState.food.x * cellSize,
          top: gameState.food.y * cellSize,
          width: cellSize - 2,
          height: cellSize - 2,
        }}
      >
        <div className="w-full h-full bg-food rounded-sm animate-pulse shadow-[0_0_20px_hsl(var(--food))]" />
      </div>

      {/* Snake */}
      {gameState.snake.map((segment, index) => (
        <div
          key={`${segment.x}-${segment.y}-${index}`}
          className="absolute transition-all duration-100"
          style={{
            left: segment.x * cellSize,
            top: segment.y * cellSize,
            width: cellSize - 2,
            height: cellSize - 2,
          }}
        >
          <div 
            className={`w-full h-full rounded-sm ${
              index === 0 
                ? "bg-snake shadow-[0_0_15px_hsl(var(--snake-body))]" 
                : "bg-snake opacity-80"
            }`} 
          />
        </div>
      ))}

      {/* Game Over Overlay */}
      {gameState.isGameOver && (
        <div className="absolute inset-0 bg-background/90 flex items-center justify-center backdrop-blur-sm">
          <div className="text-center">
            <h2 className="text-4xl font-bold text-destructive neon-text mb-2">GAME OVER</h2>
            <p className="text-2xl text-primary">Score: {gameState.score}</p>
          </div>
        </div>
      )}
    </div>
  );
};
