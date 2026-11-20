"use client";

import { useEffect, useState } from "react";

type State = { kind: "checking" } | { kind: "ok" } | { kind: "error"; message: string };

export function HealthCheck() {
  const [state, setState] = useState<State>({ kind: "checking" });

  useEffect(() => {
    fetch("/api/health")
      .then((response) => {
        if (!response.ok) throw new Error(`The API answered ${response.status}`);
        setState({ kind: "ok" });
      })
      .catch((error: Error) => setState({ kind: "error", message: error.message }));
  }, []);

  if (state.kind === "checking") return <p className="text-ink-soft">Checking the API…</p>;
  if (state.kind === "ok") return <p className="font-bold text-approved">API and database reachable through the proxy</p>;
  return <p className="font-bold text-stamp">API not reachable: {state.message}. Is uvicorn running on port 8000?</p>;
}