# Bayesian relativities and IFRS 17: useful interface material

**23 September 2026 · Two-paste review · Future-work note**

## Reuse the actuarial work already developed

The Bayesian relativities paper already develops exposure-consistent frequency and severity (§3), premium layers (§2.4), credibility updating (§7), claim development and reserves (§8), capital (§9), risk transfer (§10), validation (§11), the IFRS 17 hand-off (§12) and production controls (§13). Preserve gamma/negative-binomial derivations there and cross-reference them from Mwendo; do not repeat them as a new credit-default model.

The useful increment from the latest material is a **joined insurance, premium-finance and cash example**. It should demonstrate interfaces between established models rather than merge their outcomes.

## Proposed event case

Follow one policy and its IPF facility through:

1. Policy inception, permitted usage-based premium formula and coverage boundary.
2. Financing advance and insurer premium receipt.
3. Usage observation, forecast update and any contractually permitted billing adjustment.
4. Missed IPF payment and the lender's authorised response.
5. Effective policy modification or cancellation, if applicable.
6. Refund calculation, approval, recipient and settlement.
7. Allocation to the IPF balance and any remaining borrower obligation.
8. An incurred claim whose settlement continues after the usage or coverage change.

| Ledger | Owns | Must receive |
|---|---|---|
| Insurance pricing | Frequency, severity, exposure, indicated premium and uncertainty | Valid exposure and claim observations |
| Insurer accounting | Contract grouping, LRC/LIC, service allocation and financial reporting | Approved policy/claim cash flows and reconciliation |
| Lender | Loan balance, EIR, arrears, modification and credit shortfall | Contractual rights and actual loan/refund cash |
| SPV | Eligible purchased receivable, available cash, note obligations and waterfall | Transfer terms, collections and restrictions |

Under IFRS 17, PAA eligibility depends on its group-level criteria; changing daily usage does not alone establish a new short contract. Insurance service, premium receipts, contractual refund rights and incurred-claim obligations remain distinguishable. [IFRS 17 paragraphs 53–59 and B126–B127](https://www.ifrs.org/content/dam/ifrs/project/amendments-to-ifrs-17/ifrs-17-incorporating-the-june-2020-amendments.pdf).

### Proposed paragraph for the accounting interface

A usage observation updates evidence about exposure. Its financial consequences depend on the policy and the receiving function. Actuarial pricing may revise expected claims; the contract may permit a premium adjustment; Finance allocates service and measures liabilities; and a lender recognises a refund only through the applicable rights and cash allocation. The event record should preserve those separate decisions so that reduced future usage is never mistaken for the settlement of an existing claim or the receipt of a loan recovery.

## Capital and dependence extension

Use shared scenarios to examine motor claims, driver earnings, credit distress, protection delays and funding cash. Retain distinct insurance and credit marginal models; then specify their dependence and avoid counting the same shock twice. Report gross/ceded/net claim results separately from borrower and tranche credit losses. An insurance risk adjustment, economic capital allocation and prudential requirement answer different questions.

## Next useful deliverables

- An event-to-ledger table with dates, entity, amount, obligation, approval and reversal links.
- A numerical policy/IPF example including a delayed refund and an outstanding claim.
- A sensitivity analysis of exposure, claim severity, recovery delay and counterparty performance.
- Cross-references to the existing actuarial derivations rather than duplicated background chapters.

The advanced treasury models are optional adjacent tools. They do not change the canonical insurance likelihood merely by appearing in the pasted material.

## Shared review and calculation basis

See the [two-paste review index](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_treasury_cross_project_review_2026-09-23/00_READ_ME.md>) and [working formulations and checked examples](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/output/pricing_treasury_cross_project_review_2026-09-23/02_WORKING_FORMULATIONS_AND_EXAMPLES.md>). Catalogue IDs and source-line references are in the central package.
