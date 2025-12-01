import { describe, it, expect } from "vitest";
import {
  createInitialState,
  generateFood,
  getNextHeadPosition,
  checkCollision,
  updateGame,
  changeDirection,
  type Position,
  type GameState,
} from "../lib/gameEngine";

describe("gameEngine", () => {
  describe("createInitialState", () => {
    it("should create initial state with walls mode", () => {
      const state = createInitialState("walls");
      expect(state.snake).toHaveLength(3);
      expect(state.direction).toBe("RIGHT");
      expect(state.score).toBe(0);
      expect(state.isGameOver).toBe(false);
      expect(state.mode).toBe("walls");
    });

    it("should create initial state with pass-through mode", () => {
      const state = createInitialState("pass-through");
      expect(state.mode).toBe("pass-through");
    });
  });

  describe("generateFood", () => {
    it("should generate food not on snake", () => {
      const snake: Position[] = [{ x: 10, y: 10 }];
      const food = generateFood(snake);
      expect(snake.some((s) => s.x === food.x && s.y === food.y)).toBe(false);
    });
  });

  describe("getNextHeadPosition", () => {
    it("should move up correctly", () => {
      const head = { x: 10, y: 10 };
      const next = getNextHeadPosition(head, "UP", "walls");
      expect(next).toEqual({ x: 10, y: 9 });
    });

    it("should move down correctly", () => {
      const head = { x: 10, y: 10 };
      const next = getNextHeadPosition(head, "DOWN", "walls");
      expect(next).toEqual({ x: 10, y: 11 });
    });

    it("should move left correctly", () => {
      const head = { x: 10, y: 10 };
      const next = getNextHeadPosition(head, "LEFT", "walls");
      expect(next).toEqual({ x: 9, y: 10 });
    });

    it("should move right correctly", () => {
      const head = { x: 10, y: 10 };
      const next = getNextHeadPosition(head, "RIGHT", "walls");
      expect(next).toEqual({ x: 11, y: 10 });
    });

    it("should wrap around in pass-through mode", () => {
      const head = { x: 0, y: 0 };
      const next = getNextHeadPosition(head, "LEFT", "pass-through");
      expect(next.x).toBe(19);
    });
  });

  describe("checkCollision", () => {
    it("should detect wall collision in walls mode", () => {
      const head = { x: -1, y: 10 };
      const snake: Position[] = [{ x: 0, y: 10 }];
      expect(checkCollision(head, snake, "walls")).toBe(true);
    });

    it("should not detect wall collision in pass-through mode", () => {
      const head = { x: 20, y: 10 };
      const snake: Position[] = [{ x: 19, y: 10 }];
      expect(checkCollision(head, snake, "pass-through")).toBe(false);
    });

    it("should detect self collision", () => {
      const head = { x: 10, y: 10 };
      const snake: Position[] = [{ x: 11, y: 10 }, { x: 10, y: 10 }];
      expect(checkCollision(head, snake, "walls")).toBe(true);
    });

    it("should not detect collision on valid move", () => {
      const head = { x: 11, y: 10 };
      const snake: Position[] = [{ x: 10, y: 10 }];
      expect(checkCollision(head, snake, "walls")).toBe(false);
    });
  });

  describe("updateGame", () => {
    it("should move snake forward", () => {
      const state: GameState = {
        snake: [{ x: 10, y: 10 }, { x: 9, y: 10 }],
        food: { x: 15, y: 15 },
        direction: "RIGHT",
        score: 0,
        isGameOver: false,
        mode: "walls",
      };
      const newState = updateGame(state);
      expect(newState.snake[0]).toEqual({ x: 11, y: 10 });
      expect(newState.snake).toHaveLength(2);
    });

    it("should grow snake when eating food", () => {
      const state: GameState = {
        snake: [{ x: 10, y: 10 }, { x: 9, y: 10 }],
        food: { x: 11, y: 10 },
        direction: "RIGHT",
        score: 0,
        isGameOver: false,
        mode: "walls",
      };
      const newState = updateGame(state);
      expect(newState.snake).toHaveLength(3);
      expect(newState.score).toBe(10);
      expect(newState.food).not.toEqual({ x: 11, y: 10 });
    });

    it("should end game on collision", () => {
      const state: GameState = {
        snake: [{ x: 19, y: 10 }, { x: 18, y: 10 }],
        food: { x: 15, y: 15 },
        direction: "RIGHT",
        score: 0,
        isGameOver: false,
        mode: "walls",
      };
      const newState = updateGame(state);
      expect(newState.isGameOver).toBe(true);
    });
  });

  describe("changeDirection", () => {
    it("should change direction when valid", () => {
      expect(changeDirection("RIGHT", "UP")).toBe("UP");
      expect(changeDirection("UP", "LEFT")).toBe("LEFT");
    });

    it("should prevent 180-degree turns", () => {
      expect(changeDirection("RIGHT", "LEFT")).toBe("RIGHT");
      expect(changeDirection("UP", "DOWN")).toBe("UP");
      expect(changeDirection("LEFT", "RIGHT")).toBe("LEFT");
      expect(changeDirection("DOWN", "UP")).toBe("DOWN");
    });
  });
});
