import { Button } from "@/components/ui/button";
import { Play, Pause, RotateCcw } from "lucide-react";
import type { GameMode } from "@/lib/gameEngine";

interface GameControlsProps {
  isPaused: boolean;
  isGameOver: boolean;
  mode: GameMode;
  score: number;
  onStart: () => void;
  onPause: () => void;
  onResume: () => void;
  onModeChange: (mode: GameMode) => void;
}

export const GameControls = ({
  isPaused,
  isGameOver,
  mode,
  score,
  onStart,
  onPause,
  onResume,
  onModeChange,
}: GameControlsProps) => {
  return (
    <div className="flex flex-col gap-4 w-full">
      {/* Score Display */}
      <div className="bg-card border border-border rounded p-4">
        <div className="text-center">
          <p className="text-muted-foreground text-sm mb-1">SCORE</p>
          <p className="text-4xl font-bold text-primary neon-text">{score}</p>
        </div>
      </div>

      {/* Mode Selection */}
      <div className="bg-card border border-border rounded p-4">
        <p className="text-muted-foreground text-sm mb-3">GAME MODE</p>
        <div className="flex gap-2">
          <Button
            variant={mode === "walls" ? "default" : "outline"}
            onClick={() => onModeChange("walls")}
            className="flex-1"
          >
            WALLS
          </Button>
          <Button
            variant={mode === "pass-through" ? "default" : "outline"}
            onClick={() => onModeChange("pass-through")}
            className="flex-1"
          >
            PASS-THROUGH
          </Button>
        </div>
      </div>

      {/* Game Controls */}
      <div className="bg-card border border-border rounded p-4">
        <p className="text-muted-foreground text-sm mb-3">CONTROLS</p>
        <div className="flex gap-2">
          {isGameOver || isPaused ? (
            <Button onClick={onStart} className="flex-1 gap-2">
              <RotateCcw className="w-4 h-4" />
              {isGameOver ? "NEW GAME" : "START"}
            </Button>
          ) : (
            <>
              <Button onClick={onPause} variant="outline" className="flex-1 gap-2">
                <Pause className="w-4 h-4" />
                PAUSE
              </Button>
            </>
          )}
        </div>
        <div className="mt-3 text-xs text-muted-foreground">
          <p>Arrow Keys or WASD to move</p>
          <p>Space to pause/resume</p>
        </div>
      </div>
    </div>
  );
};
