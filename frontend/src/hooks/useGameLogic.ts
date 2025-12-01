import { useState, useEffect, useCallback, useRef } from "react";
import {
  createInitialState,
  updateGame,
  changeDirection,
  type GameState,
  type Direction,
  type GameMode,
} from "@/lib/gameEngine";

export const useGameLogic = (initialMode: GameMode = "walls") => {
  const [gameState, setGameState] = useState<GameState>(() => createInitialState(initialMode));
  const [isPaused, setIsPaused] = useState(true);
  const [speed, setSpeed] = useState(150); // ms per tick
  const gameLoopRef = useRef<NodeJS.Timeout | null>(null);

  const startGame = useCallback(() => {
    setGameState(createInitialState(gameState.mode));
    setIsPaused(false);
  }, [gameState.mode]);

  const pauseGame = useCallback(() => {
    setIsPaused(true);
  }, []);

  const resumeGame = useCallback(() => {
    if (!gameState.isGameOver) {
      setIsPaused(false);
    }
  }, [gameState.isGameOver]);

  const changeGameDirection = useCallback((newDirection: Direction) => {
    setGameState((prev) => ({
      ...prev,
      direction: changeDirection(prev.direction, newDirection),
    }));
  }, []);

  const switchMode = useCallback((newMode: GameMode) => {
    setGameState((prev) => ({
      ...createInitialState(newMode),
      mode: newMode,
    }));
    setIsPaused(true);
  }, []);

  // Game loop
  useEffect(() => {
    if (isPaused || gameState.isGameOver) {
      if (gameLoopRef.current) {
        clearInterval(gameLoopRef.current);
        gameLoopRef.current = null;
      }
      return;
    }

    gameLoopRef.current = setInterval(() => {
      setGameState((prev) => updateGame(prev));
    }, speed);

    return () => {
      if (gameLoopRef.current) {
        clearInterval(gameLoopRef.current);
      }
    };
  }, [isPaused, gameState.isGameOver, speed]);

  // Keyboard controls
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (gameState.isGameOver) return;

      switch (e.key) {
        case "ArrowUp":
        case "w":
        case "W":
          e.preventDefault();
          changeGameDirection("UP");
          break;
        case "ArrowDown":
        case "s":
        case "S":
          e.preventDefault();
          changeGameDirection("DOWN");
          break;
        case "ArrowLeft":
        case "a":
        case "A":
          e.preventDefault();
          changeGameDirection("LEFT");
          break;
        case "ArrowRight":
        case "d":
        case "D":
          e.preventDefault();
          changeGameDirection("RIGHT");
          break;
        case " ":
          e.preventDefault();
          if (isPaused && !gameState.isGameOver) {
            resumeGame();
          } else {
            pauseGame();
          }
          break;
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [gameState.isGameOver, isPaused, changeGameDirection, pauseGame, resumeGame]);

  return {
    gameState,
    isPaused,
    startGame,
    pauseGame,
    resumeGame,
    changeDirection: changeGameDirection,
    switchMode,
    setSpeed,
  };
};
