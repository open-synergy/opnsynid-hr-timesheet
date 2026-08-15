# Approve Leave Allocation

> **Module:** ssi_hr_holiday_documenso_signing
>
> **Extends:** ssi_hr_holiday — model `hr.leave_allocation`, aksi `05-approve`

## Modified Flow

- Anchor: at Flow base step 2 (open the record to approve), the form already shows a
  **Signature Requests** tab (injected because `_documenso_signing_create_page = True`).
  This tab is always present once this module is installed, regardless of whether
  Documenso signing is actually used for the current approval.
- The behavior below only applies **when the record's active Approval Template has a
  Documenso Signing Template configured**. If it does not, the base Flow (steps 3–4,
  Click **Approve** / click **OK**) applies unchanged, exactly as documented in
  `ssi_hr_holiday/docs/hr_leave_allocation/05-approve.md`.
- When a Documenso Signing Template **is** configured: no per-approver approval record
  is created for this document — a single `documenso.signature.request` is created and
  linked instead (during the earlier Confirm action, before this record reaches
  **Waiting for Approval**). Because there is no per-approver record naming the current
  user as an active approver, the **Approve** button (Flow base step 3) stays invisible
  for every user — it can never be clicked.
- Instead of clicking Approve, the user opens the linked request — shown under the
  **Approval Signing Request** group as the **Approval Signature Request** field in the
  **Signature Requests** tab (or via the **Open Signature Requests** button in the same
  tab) — and, on that request's own form, clicks **Send to Documenso** to send the
  document for e-signature. The designated signer(s) then sign the document outside
  Odoo, in Documenso.
- Approval completes automatically — without any button click on this Leave Allocation
  record — once the linked signature request reaches the **Signed** status (checked
  manually via **Check Status** on the request, or synced automatically by the
  connector). At that point, the base Post-Condition applies as usual: status
  automatically changes to **In Progress** (or remains **Waiting for Approval** if other
  approval levels are still pending).
- If the linked signature request is **cancelled** instead (e.g. a signer declines in
  Documenso), the record moves directly to **Rejected** — the same end state as the base
  Reject action, but triggered automatically by the cancelled request rather than by a
  user clicking Reject.
