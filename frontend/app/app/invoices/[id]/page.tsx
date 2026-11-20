import { Suspense } from "react";

import { ReviewScreen, ReviewSkeleton } from "@/components/review";

export const metadata = { title: "Review invoice · Docket" };

export default function ReviewPage() {
  return (
    <Suspense fallback={<ReviewSkeleton />}>
      <ReviewScreen />
    </Suspense>
  );
}