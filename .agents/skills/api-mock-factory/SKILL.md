---
name: api-mock-factory
description: Automatically generates offline mock adapters, in-memory service repositories, and realistic seed fixtures from TypeScript contracts. Use standalone or as Wave 1 leaf skill in federated-orchestrator so subagents never block on external APIs or database dependencies.
---

# API & Service Mock Factory

Use this skill to create **zero-dependency, offline mock adapters and seed fixtures** directly from shared data contracts (`src/shared/types/`).

In multi-agent workflows, feature agents must never block waiting for live external APIs (like Resend, Shippo, Stripe) or live databases. This skill builds instant, type-safe in-memory stubs so parallel agents can develop and test immediately.

---

## What It Generates

For every defined interface or external integration, this skill generates:

```
src/shared/mocks/
  ├── fixtures/          # Realistic seed data (JSON/TS)
  │     ├── inventory.fixture.ts
  │     ├── logistics.fixture.ts
  │     └── messaging.fixture.ts
  ├── adapters/          # In-memory service implementations
  │     ├── mock-inventory.ts
  │     ├── mock-logistics.ts
  │     └── mock-email.ts
  └── index.ts           # Unified provider factory with live/mock toggle
```

---

## 3 Core Principles for High-Fidelity Mocks

1. **Strict Type Conformance:**  
   Every mock adapter must implement the exact same TypeScript interface as the live production service:
   ```typescript
   export interface IEmailService {
     sendAlert(to: string, subject: string, body: string): Promise<{ id: string; status: "sent" | "failed" }>;
   }
   ```
2. **Realistic Seed Data (No "test1", "foo", "bar"):**  
   Fixtures must represent realistic operational scenarios:
   * Real SKU patterns: `SKU-WH1-9042`
   * Real carrier tracking numbers: `1Z9999999999999999`
   * Proper ISO timestamps and valid UUIDs.
3. **Seamless Toggle Contract:**  
   Services are accessed via a Factory or Dependency Injection container controlled by an environment variable:
   ```typescript
   export const getEmailService = (): IEmailService => {
     if (process.env.USE_MOCKS === "true" || !process.env.RESEND_API_KEY) {
       return new MockEmailService();
     }
     return new ResendEmailService(process.env.RESEND_API_KEY);
   };
   ```

---

## Automated Mock Verification

Every generated mock adapter includes a standalone sanity test verifying that:
* Query methods return realistic fixture arrays.
* Mutation methods update in-memory state predictably.
* Simulated error modes (e.g. stock-out, carrier timeout) can be triggered for test verification.
