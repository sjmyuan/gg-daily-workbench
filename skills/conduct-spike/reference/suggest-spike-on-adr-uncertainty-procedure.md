# Suggest-Spike-On-ADR-Uncertainty Procedure

Full procedure for the `suggest-spike-on-adr-uncertainty` capability — loaded on demand when an ADR discussion hinges on unverified assumptions. Uncertainty signals: **adr-uncertainty-signals**.

1. Name the uncertainty precisely: "This decision seems to hinge on [the unverified assumption / the unknown fact / the unresolved comparison]."
2. Explain why the uncertainty matters.
3. Offer: "Would you like to spike this before finalizing the ADR?" — define a focused scope, one goal and 1–2 areas (a deliberate narrowing of the standard target), via **define-spike-scope** only when the user agrees.
4. Treat the ADR as provisional.
5. Continue the ADR flow via `draft-adr` when the user declines.
6. Record the uncertainty as a **risk** in the ADR's Consequences section — never a free-form note — and validate that the risk names the uncertainty and the decision it makes provisional.
