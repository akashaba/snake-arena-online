import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { leaderboardAPI, type LeaderboardEntry } from "@/services/api";
import { Trophy, ArrowLeft, Medal } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Leaderboard = () => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    const loadLeaderboard = async () => {
      setIsLoading(true);
      try {
        // Load all leaderboard entries (up to 100)
        const data = await leaderboardAPI.getLeaderboard({ limit: 100 });
        setEntries(data);
      } catch (error) {
        console.error('Failed to load leaderboard:', error);
        toast({
          title: "Failed to load leaderboard",
          description: "Could not fetch leaderboard data. Please try again.",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    loadLeaderboard();
  }, [toast]);

  const getRankColor = (index: number) => {
    if (index === 0) return "text-neon-orange";
    if (index === 1) return "text-neon-cyan";
    if (index === 2) return "text-neon-magenta";
    return "text-foreground";
  };

  const getRankIcon = (index: number) => {
    if (index === 0) return <Trophy className="w-6 h-6 text-neon-orange" />;
    if (index === 1) return <Medal className="w-6 h-6 text-neon-cyan" />;
    if (index === 2) return <Medal className="w-6 h-6 text-neon-magenta" />;
    return <span className="text-muted-foreground">#{index + 1}</span>;
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          <Button variant="outline" onClick={() => navigate("/")} className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back
          </Button>
          <h1 className="text-4xl font-bold text-primary neon-text">LEADERBOARD</h1>
        </div>

        <Card className="neon-border">
          <CardHeader>
            <CardTitle className="text-2xl text-center">Top Players</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="text-center py-8">Loading...</div>
            ) : (
              <div className="space-y-2">
                {entries.map((entry, index) => (
                  <div
                    key={entry.id}
                    className={`flex items-center justify-between p-4 rounded bg-card border border-border transition-all hover:border-primary ${
                      index < 3 ? "shadow-[0_0_20px_hsl(var(--primary)/0.3)]" : ""
                    }`}
                  >
                    <div className="flex items-center gap-4 flex-1">
                      <div className="w-12 flex justify-center">
                        {getRankIcon(index)}
                      </div>
                      <div className="flex-1">
                        <p className={`font-bold text-lg ${getRankColor(index)}`}>
                          {entry.username}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          Mode: <span className="text-accent">{entry.mode}</span>
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-primary">{entry.score}</p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(entry.timestamp).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Leaderboard;
