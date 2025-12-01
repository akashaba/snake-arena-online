import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { SpectateGrid } from "@/components/SpectateGrid";
import { ArrowLeft } from "lucide-react";

const Spectate = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          <Button variant="outline" onClick={() => navigate("/")} className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back
          </Button>
          <h1 className="text-4xl font-bold text-primary neon-text">SPECTATE MODE</h1>
        </div>

        <div className="mb-6">
          <p className="text-muted-foreground">Watch other players in real-time</p>
        </div>

        <SpectateGrid />
      </div>
    </div>
  );
};

export default Spectate;
