import PageLoader from "@/components/layout/PageLoader";

export default function PageFullScreenLoader() {
    return (
        <div className="absolute inset-0 z-3000 flex flex-col items-center justify-center bg-white/60 backdrop-blur-sm">
            <div className="flex flex-col items-center gap-4 rounded-xl bg-white/90 p-8 shadow-xl border border-slate-200">
                <PageLoader />
            </div>
        </div>
    )
}