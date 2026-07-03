import React from "react";

// 🐾 보호동물 전체 목록용 격자형 카드 스켈레톤
export function AnimalCardSkeleton() {
  return (
    <div className="bg-white border border-border-line rounded-2xl overflow-hidden shadow-[0_2px_8px_rgba(0,0,0,0.02)] animate-pulse">
      {/* Photo area skeleton */}
      <div className="w-full aspect-square bg-zinc-200" />
      
      {/* Details area skeleton */}
      <div className="p-3 sm:p-4">
        {/* Name / Sex icon skeleton */}
        <div className="flex justify-between items-center mb-2">
          <div className="h-5 w-2/3 bg-zinc-200 rounded-md" />
          <div className="h-5 w-5 bg-zinc-200 rounded-full" />
        </div>
        
        {/* Breed & Age skeleton */}
        <div className="h-4 w-1/2 bg-zinc-200 rounded-md mb-4" />
        
        {/* Footer info (Region & Date) skeleton */}
        <div className="pt-2 border-t border-surface-variant/10 flex flex-col gap-2">
          <div className="h-3.5 w-1/3 bg-zinc-200 rounded-md" />
          <div className="h-3.5 w-3/4 bg-zinc-200 rounded-md" />
        </div>
      </div>
    </div>
  );
}

// 🎯 AI 매칭 결과용 긴 카드 스켈레톤 (반응형 대응)
export function MatchCardSkeleton() {
  return (
    <div className="bg-white border border-border-line rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row gap-4 sm:gap-5 shadow-[0_4px_12px_rgba(0,0,0,0.02)] animate-pulse overflow-hidden">
      {/* Photo skeleton */}
      <div className="w-full sm:w-[130px] h-[180px] sm:h-[130px] rounded-xl bg-zinc-200 shrink-0" />
      
      {/* Text Info skeleton */}
      <div className="flex flex-col justify-between flex-grow">
        <div>
          {/* Location skeleton */}
          <div className="h-4 w-24 bg-zinc-200 rounded-md mb-2" />
          
          {/* Title & Breed & Age skeleton */}
          <div className="flex flex-wrap gap-2 items-center mt-1">
            <div className="h-5.5 w-36 bg-zinc-200 rounded-md" />
            <div className="h-4 w-20 bg-zinc-200 rounded-md" />
            <div className="h-4 w-12 bg-zinc-200 rounded-md" />
          </div>
          
          {/* Tags skeleton */}
          <div className="flex flex-wrap gap-1.5 mt-3">
            <div className="h-6 w-16 bg-zinc-200 rounded-md" />
            <div className="h-6 w-14 bg-zinc-200 rounded-md" />
            <div className="h-6 w-16 bg-zinc-200 rounded-md" />
          </div>
        </div>
        
        {/* AI Recommendation comment box skeleton */}
        <div className="mt-4 h-[56px] w-full bg-zinc-100 rounded-xl" />
        
        {/* Details link skeleton */}
        <div className="mt-3.5 flex justify-end">
          <div className="h-4.5 w-20 bg-zinc-200 rounded-md" />
        </div>
      </div>
    </div>
  );
}
