--- a/web/src/components/customer/FirmwareTask.tsx
+++ b/web/src/components/customer/FirmwareTask.tsx
@@ -64,3 +64,4 @@
   const base = `/customers/${encodeURIComponent(customer.id)}`;
-  const stage = customer.hasAssessment ? stageFromPrototype(state.assessment) : stageFromApi(null);
+  const { rows } = useDirectory(); // the same stage the Customers list shows for this customer
+  const stage = rows.find((r) => r.routeId === customer.id)?.stage ?? (customer.hasAssessment ? stageFromPrototype(state.assessment) : stageFromApi(null));
   const findings = res.status === "ready" ? res.result.findings : [];
--- a/web/src/components/customer/FirmwareTask.test.tsx
+++ b/web/src/components/customer/FirmwareTask.test.tsx
@@ -104,2 +104,13 @@
   });
+
+  it("the related engagement shows the customer's own stage, as the Customers list does: a snapshot in progress is not a new lead", async () => {
+    session([]);
+    const none = show("sample-c");
+    await screen.findByRole("heading", { level: 1, name: "Firmware risk assessment" });
+    expect(await within(card(/^Related engagement/)).findByText("New lead")).toBeInTheDocument();
+    none.unmount();
+    show("sample-b");
+    await screen.findByRole("heading", { level: 1, name: "Firmware risk assessment" });
+    expect(await within(card(/^Related engagement/)).findByText("Assessment in progress")).toBeInTheDocument();
+  });
 });