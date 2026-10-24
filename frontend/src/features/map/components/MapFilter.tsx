import { Filter, ListRestart } from 'lucide-react'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
    DropdownMenuCheckboxItem,
} from '@/components/ui/dropdown-menu'
import { useMapStore } from '@/stores/mapStore'
import type { IncidentCategory, IncidentSeverity } from '@/types'

const CATEGORY_LABELS: Record<IncidentCategory, string> = {
    accident: 'Traffic Accident',
    road_work: 'Road Work',
    road_closure: 'Road Closure',
    pothole: 'Pothole',
    traffic_light: 'Broken Traffic Light',
    other: 'Other Incident'
}

const SEVERITY_LABELS: Record<IncidentSeverity, string> = {
    high: 'High Severity',
    medium: 'Medium Severity',
    low: 'Low Severity'
}

export default function MapFilters() {
    const { categories, severities, toggleCategory, toggleSeverity, resetFilters } = useMapStore()

    return (
        <div className="absolute top-4 right-4 z-1000">
            <DropdownMenu>
                <DropdownMenuTrigger className="flex h-10 w-10 items-center justify-center rounded-md bg-white shadow-md border border-slate-200 outline-none hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-slate-400 text-slate-700 transition-colors">
                    <Filter className="h-5 w-5" />
                </DropdownMenuTrigger>

                <DropdownMenuContent className="w-64" align="end">
                    {/* Plain header: not a group label, so no group needed */}
                    <div className="flex items-center justify-between px-2 py-1.5">
                        <span className="text-sm font-medium">Map Filters</span>
                        <button
                            type="button"
                            onClick={resetFilters}
                            className="text-xs flex items-center gap-1 text-slate-500 hover:text-slate-900 transition-colors"
                        >
                            <ListRestart className="h-3 w-3" />
                            Reset
                        </button>
                    </div>

                    <DropdownMenuSeparator />

                    <DropdownMenuGroup>
                        <DropdownMenuLabel className="text-xs text-slate-500 font-medium tracking-wider uppercase">
                            Severity
                        </DropdownMenuLabel>
                        {(Object.keys(SEVERITY_LABELS) as IncidentSeverity[]).map((severity) => (
                            <DropdownMenuCheckboxItem
                                key={severity}
                                checked={severities.includes(severity)}
                                onCheckedChange={() => toggleSeverity(severity)}
                            >
                                {SEVERITY_LABELS[severity]}
                            </DropdownMenuCheckboxItem>
                        ))}
                    </DropdownMenuGroup>

                    <DropdownMenuSeparator />

                    <DropdownMenuGroup>
                        <DropdownMenuLabel className="text-xs text-slate-500 font-medium tracking-wider uppercase">
                            Category
                        </DropdownMenuLabel>
                        {(Object.keys(CATEGORY_LABELS) as IncidentCategory[]).map((category) => (
                            <DropdownMenuCheckboxItem
                                key={category}
                                checked={categories.includes(category)}
                                onCheckedChange={() => toggleCategory(category)}
                            >
                                {CATEGORY_LABELS[category]}
                            </DropdownMenuCheckboxItem>
                        ))}
                    </DropdownMenuGroup>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    )
}