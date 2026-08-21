import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  const callCounts = new Map<string, number>();

  pi.on("before_agent_start", async (event: any) => ({
    systemPrompt:
      event.systemPrompt +
      "\n\n## Local-model working rules\n" +
      "- Make the SMALLEST diff that satisfies the task; do not touch unrelated code.\n" +
      "- Edit ONLY the files named in the task. Do NOT re-read files you already read this session.\n" +
      "- Prefer rewriting a small file with `write` over multiple `edit` calls.\n" +
      "- After editing, run the single verification command, then stop.\n" +
      "- Remove debug prints before finishing.",
  }));

  pi.on("tool_result", async (event: any) => {
    if (!event.isError) return;
    const text = String(event.content?.[0]?.text ?? "");
    if (event.toolName === "edit" && /not found|no match|match|whitespace|could not|unchanged/i.test(text)) {
      return {
        isError: true,
        content: [{
          type: "text",
          text:
            "EDIT FAILED — almost always a whitespace / exact-text mismatch, NOT a logic error. " +
            "Re-read ONLY the target region, copy the CURRENT text verbatim (including indentation), and retry the SAME edit once. " +
            "If the file is small, rewrite the whole file with `write` instead. " +
            "Do NOT redesign and do NOT re-read other files.",
        }],
      };
    }
  });

  pi.on("tool_call", async (event: any) => {
    const key = event.toolName + ":" + JSON.stringify(event.input ?? {});
    const n = (callCounts.get(key) ?? 0) + 1;
    callCounts.set(key, n);
    if (n >= 4) {
      return {
        block: true,
        reason: "Loop guard: this exact tool call has been attempted " + n + " times. " +
          "Stop repeating it, report the last error verbatim, and try a different approach.",
      };
    }
  });

  pi.on("agent_start", async () => { callCounts.clear(); });
}
