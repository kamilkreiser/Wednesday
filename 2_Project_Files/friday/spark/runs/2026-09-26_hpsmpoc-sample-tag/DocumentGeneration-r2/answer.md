--- a/web/src/components/customer/DocumentGeneration.tsx
+++ b/web/src/components/customer/DocumentGeneration.tsx
@@ -18,6 +18,7 @@
 import { seedAssessment } from "@/lib/session";
 import { useSession } from "@/lib/store";
 import { customerApi } from "./api";
+import { extrasFor } from "./content";
 import { isApproved, latestExecutiveSummary } from "./ApiNarrative";
 import { ServiceReport } from "./ServiceReport";
 import { useAsync } from "@/lib/use-async";
@@ -89,6 +90,7 @@
   return (
     <>
       <div className="no-print">
-        <PageHeader title="Document generation" eyebrow={customer.name} tags={<><SyntheticTag /><Tag kind="deterministic">From the scored result: rules, not AI</Tag></>}
+        <PageHeader title="Document generation" eyebrow={customer.name} tags={<>{extrasFor(customer.apiId, customer.name) && <SyntheticTag />}<Tag kind="deterministic">From the scored result: rules, not AI</Tag></>}
           lead="Create documents from this customer's engagement data: the executive report, or a focused part of it." />
       </div>
       <div className="no-print grid grid-cols-1 gap-5 xl:grid-cols-[minmax(0,1fr)_22rem]">
--- a/web/src/components/customer/DocumentGeneration.test.tsx
+++ b/web/src/components/customer/DocumentGeneration.test.tsx
@@ -112,3 +112,18 @@
   });
 
+  it("B22-08: the seeded sample keeps its 'Sample data' tag; a customer the user added has none", async () => {
+    session([]);
+    const seeded = show();
+    const h1 = await screen.findByRole("heading", { level: 1, name: "Document generation" });
+    expect(within(h1.parentElement!).getByText("Sample data", { exact: true })).toBeInTheDocument();
+    seeded.unmount();
+    const { mockState } = await import("@/server/mock/store");
+    const id = "CUST-SYN-ADDED-DOC";
+    mockState().customers.push({ id, name: "Harbourside Accounting", synthetic: true, latestAssessmentStatus: null, createdAt: "2026-09-25T02:00:00Z", industry: "Professional services" });
+    pathname = `/customers/${id}/documents`;
+    render(<CustomerShell customer={customerForRoute(id)!}><DocumentGeneration /></CustomerShell>);
+    const added = await screen.findByRole("heading", { level: 1, name: "Document generation" });
+    expect(within(added.parentElement!).queryByText("Sample data", { exact: true })).toBeNull();
+  });
+
   it("/documents: pick a customer to open its documents", async () => {