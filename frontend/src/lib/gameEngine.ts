export type Position = { x: number; y: number };
export type Direction = "UP" | "DOWN" | "LEFT" | "RIGHT";
export type GameMode = "walls" | "pass-through";

export interface GameState {
  snake: Position[];
  food: Position;
  direction: Direction;
  score: number;
  isGameOver: boolean;
  mode: GameMode;
}

const GRID_SIZE = 20;

export const createInitialState = (mode: GameMode = "walls"): GameState => ({
  snake: [
    { x: 10, y: 10 },
    { x: 9, y: 10 },
    { x: 8, y: 10 },
  ],
  food: generateFood([{ x: 10, y: 10 }]),
  direction: "RIGHT",
  score: 0,
  isGameOver: false,
  mode,
});

export const generateFood = (snake: Position[]): Position => {
  let food: Position;
  do {
    food = {
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE),
    };
  } while (snake.some((segment) => segment.x === food.x && segment.y === food.y));
  return food;
};

export const getNextHeadPosition = (head: Position, direction: Direction, mode: GameMode): Position => {
  const newHead = { ...head };

  switch (direction) {
    case "UP":
      newHead.y -= 1;
      break;
    case "DOWN":
      newHead.y += 1;
      break;
    case "LEFT":
      newHead.x -= 1;
      break;
    case "RIGHT":
      newHead.x += 1;
      break;
  }

  // Pass-through mode wraps around edges
  if (mode === "pass-through") {
    if (newHead.x < 0) newHead.x = GRID_SIZE - 1;
    if (newHead.x >= GRID_SIZE) newHead.x = 0;
    if (newHead.y < 0) newHead.y = GRID_SIZE - 1;
    if (newHead.y >= GRID_SIZE) newHead.y = 0;
  }

  return newHead;
};

export const checkCollision = (head: Position, snake: Position[], mode: GameMode): boolean => {
  // Wall collision only in walls mode
  if (mode === "walls") {
    if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
      return true;
    }
  }

  // Self collision
  return snake.slice(1).some((segment) => segment.x === head.x && segment.y === head.y);
};

export const updateGame = (state: GameState): GameState => {
  if (state.isGameOver) return state;

  const head = state.snake[0];
  const newHead = getNextHeadPosition(head, state.direction, state.mode);

  // Check collision before moving
  if (checkCollision(newHead, state.snake, state.mode)) {
    return { ...state, isGameOver: true };
  }

  const newSnake = [newHead, ...state.snake];

  // Check if food is eaten
  if (newHead.x === state.food.x && newHead.y === state.food.y) {
    return {
      ...state,
      snake: newSnake,
      food: generateFood(newSnake),
      score: state.score + 10,
    };
  }

  // Remove tail if no food eaten
  newSnake.pop();

  return {
    ...state,
    snake: newSnake,
  };
};

export const changeDirection = (currentDirection: Direction, newDirection: Direction): Direction => {
  // Prevent 180-degree turns
  const opposites: Record<Direction, Direction> = {
    UP: "DOWN",
    DOWN: "UP",
    LEFT: "RIGHT",
    RIGHT: "LEFT",
  };

  if (opposites[currentDirection] === newDirection) {
    return currentDirection;
  }

  return newDirection;
};

export const GRID_SIZE_CONSTANT = GRID_SIZE;
