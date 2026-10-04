import AccidentMap from "@/features/map/components/AccidentMap"
import { Button } from "@/components/ui/button";

export default function MapPage() {
  return (
    <div className="flex flex-col h-screen w-screen bg-slate-50">
      <header className="h-14 border-b bg-white px-4 flex items-center justify-between shadow-xs z-10">
        <div className="flex items-center gap-2">
          <h1 className="font-bold text-base text-slate-800">Accident Manager</h1>
          <span className="text-xs text-slate-500 font-mono">Live Incident Map</span>
        </div>

        <div className="flex items-center gap-2">
          <Button onClick={() => alert("Report accident clicked")}>
            Report Incident
          </Button>

          <Button variant="outline" size="sm">
            Filters
          </Button>
        </div>
      </header>

      <main className="flex-1 relative">
        <AccidentMap />
      </main>
    </div>
  )
}