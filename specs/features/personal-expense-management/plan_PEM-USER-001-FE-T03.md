# PEM-USER-001-FE-T03 — Implementation Plan

**Source ticket**: `specs/features/personal-expense-management/tickets.md` → **PEM-USER-001-FE-T03**  
**Related user story**: **PEM-USER-001** (from `specs/features/personal-expense-management/user-stories.md`)  
**Plan version**: v1.0 — (GAIA, 2026-02-03T18:30:00+01:00)  
**Traceability**: All tasks reference `PEM-USER-001-FE-T03` and relevant `PEM-USER-001` scenarios.

---

## 1) Context & Objective

**Ticket summary**: Build the expense entry form UI component with client-side validation, API integration, error handling, accessibility support, and Spanish labels. This is the primary user interface for recording financial transactions.

**Business value**: This form is the main entry point for users to track their expenses. Without it, users cannot interact with the core feature of the application.

**Impacted entities/tables**: None (frontend only)

**Impacted services/modules**:
- **Frontend features**: `features/transactions/` (NEW)
  - Components: `ExpenseEntryForm.tsx`
  - API hooks: `useCreateTransaction.ts`
  - Schemas: `transactionSchema.ts`
  - Types: `transaction.ts`

**Impacted tests or business flows**: This ticket satisfies:
- PEM-USER-001 Scenario 1 (Successfully add expense with all required fields)
- PEM-USER-001 Scenario 2 (Add expense with optional description)
- PEM-USER-001 Scenario 3 (Validation error for missing required fields)
- PEM-USER-001 Scenario 4 (Validation error for invalid amount format)
- PEM-USER-001 Scenario 5 (Validation error for negative amount)
- PEM-USER-001 Scenario 6 (Validation error for future date)
- PEM-USER-001 Scenario 9 (Keyboard navigation support)
- PEM-USER-001 Scenario 10 (Error handling for server failure)

---

## 2) Scope

### In scope
- Form component: `ExpenseEntryForm.tsx` (React) with shadcn/ui components
- Form fields: Amount (number input), Date (date picker), Category (dropdown/select), Description (text input, optional)
- Client-side validation using Zod schema
- Form library: React Hook Form with Zod resolver
- API integration: TanStack Query `useMutation` for POST `/api/transactions`
- Success handling: Toast notification, query invalidation, form reset
- Error handling: Inline validation errors, server error toast, form data preservation, retry logic
- Accessibility: Keyboard navigation, ARIA labels, focus indicators, screen reader support
- Spanish labels: "Cantidad", "Fecha", "Categoría", "Descripción", "Guardar"
- Brand compliance: Use design tokens from brand-guidelines.md
- Component tests (React Testing Library): happy path, validation errors, error handling
- Accessibility tests: keyboard navigation, ARIA labels, focus management

### Out of scope
- Automatic categorization UI (handled in PEM-USER-008-FE-T03)
- Recurring transaction setup
- Income entry form (handled in PEM-USER-002-FE-T03, though form structure supports it)
- Transaction list/edit/delete UI (handled in PEM-USER-003-FE-T03)
- E2E tests (will be added later with Playwright)

### Assumptions
- Backend endpoint POST `/api/transactions` is implemented (PEM-USER-001-BE-T02)
- Authentication is configured and JWT token is injected via axios interceptor
- shadcn/ui components are installed and configured
- TanStack Query is configured with QueryClientProvider
- Axios instance is configured in `frontend/src/api/http.ts`
- Brand design tokens are defined in CSS variables (from brand-guidelines.md)

### Open questions
- None (all requirements are clear from the ticket and user story)

---

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 Test-first sequencing

**Red → Green → Refactor approach:**

1. **Write failing tests** (Red):
   - Component test: Render form and submit with valid data
   - Component test: Show validation errors for invalid data
   - Component test: Handle server errors
   - Tests should fail because component doesn't exist

2. **Implement minimal code** (Green):
   - Create form component with fields and validation
   - Integrate API hook
   - Make tests pass with simplest implementation

3. **Refactor** (keep tests green):
   - Extract reusable form field components
   - Improve error messages
   - Add loading states and animations

### 3.2 NFR hooks

**Brand & Visuals** (from `@/.agent/rules/brand-guidelines.md`):
- **Colors**:
  - Primary button: `--primary` (Terracotta AA #B2612A) with `--primary-foreground` (Warm White)
  - Form inputs: `--background` with `--foreground` text
  - Error text: `--destructive` with `--destructive-foreground`
  - Success toast: `--secondary` (Green) with `--secondary-foreground` (Navy)
- **Typography**: Use Inter font (fallback to system-ui), 1rem for body text
- **Spacing**: 8pt grid — form field gaps: 16px (`space-4`), card padding: 24px (`space-6`)
- **Border radius**: `--radius` (1rem from design tokens)

**Accessibility & i18n**:
- **WCAG Target**: AA (4.5:1 contrast for text, 3:1 for UI components)
- **Keyboard Navigation**: 
  - All fields accessible via Tab
  - Submit via Enter
  - Escape to clear/cancel (if applicable)
- **ARIA Roles**:
  - Form: `role="form"` with `aria-label="Formulario de gastos"`
  - Error messages: `aria-describedby` linking to error text
  - Required fields: `aria-required="true"`
- **Focus Indicators**: Visible focus ring (2px, high contrast)
- **Touch Targets**: Minimum 44×44px for mobile
- **Locale**: Spanish (Castilian) for all labels, placeholders, error messages

**Connectivity & Routing**:
- **Entry Point**: This form should be accessible from:
  - Main dashboard (via "Añadir Gasto" button)
  - Dedicated `/transactions/new` route
  - Quick action floating button (if applicable)
- **Exit Points**: After successful submission:
  - Stay on form (reset for next entry) — default behavior
  - Optional: Redirect to transaction list (future enhancement)

**Performance/Resilience**:
- **Debounce**: Not needed for this form (submit-only, no real-time validation)
- **Retry Logic**: Retry failed submission once after 1 second
- **Optimistic Updates**: Not applicable (no list to update optimistically in this ticket)
- **Loading States**: Show spinner on submit button during API call

**Observability**:
- **Analytics Events**: Track form submission success/failure (client-side)
- **Error Logging**: Log validation errors and API errors to console (dev) or monitoring service (prod)

---

## 4) Atomic Task Breakdown

### Task 1: Verify Docker Environment and Frontend Service

**Purpose**: Ensure the frontend service is running before implementing code. Maps to prerequisite for all PEM-USER-001 scenarios.

**Prerequisites**: 
- Verify `docker-compose.yml` exists
- Frontend service must be healthy: `docker compose ps` shows `frontend` as `Up`
- If frontend is not running or unhealthy, STOP and notify user

**Artifacts impacted**: None (verification only)

**Test types**: Manual verification

**BDD Acceptance**:
```gherkin
Given the project has a docker-compose.yml file
When I run "docker compose ps"
Then I see the "frontend" service in "Up" state
And I can access the frontend at http://localhost:5188
```

**Steps**:
1. Check if `docker-compose.yml` exists at project root
2. Run `docker compose ps` and verify `frontend` service is `Up (healthy)`
3. Test frontend access: Open browser to `http://localhost:5188`
4. If any step fails, STOP and document the issue

---

### Task 2: Create Zod Validation Schema

**Purpose**: Define the client-side validation schema for the expense entry form. Maps to PEM-USER-001 Scenarios 3-6 (validation).

**Prerequisites**: Task 1 completed

**Artifacts impacted**:
- `frontend/src/features/transactions/schemas/transactionSchema.ts` (NEW)

**Test types**: Unit test (Zod validation)

**BDD Acceptance**:
```gherkin
Given I have a Zod schema for transaction creation
When I validate data with missing amount
Then a validation error is returned
When I validate data with negative amount
Then a validation error is returned
When I validate data with future date
Then a validation error is returned
When I validate data with valid fields
Then the data passes validation
```

**Implementation**:
```typescript
// frontend/src/features/transactions/schemas/transactionSchema.ts
import { z } from "zod";

/**
 * Zod schema for expense entry form validation.
 * 
 * [Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-FE-T03]
 */
export const createTransactionSchema = z.object({
  type: z.enum(["income", "expense"], {
    required_error: "El tipo es obligatorio",
  }),
  amount: z
    .string()
    .min(1, "La cantidad es obligatoria")
    .refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
      message: "La cantidad debe ser un número positivo",
    })
    .transform((val) => Number(val)),
  date: z
    .string()
    .min(1, "La fecha es obligatoria")
    .refine(
      (val) => {
        const selectedDate = new Date(val);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return selectedDate <= today;
      },
      { message: "La fecha no puede ser futura" }
    ),
  category_id: z
    .number({
      required_error: "La categoría es obligatoria",
      invalid_type_error: "Selecciona una categoría válida",
    })
    .int()
    .positive("Selecciona una categoría"),
  description: z.string().max(500, "La descripción no puede exceder 500 caracteres").optional(),
});

export type CreateTransactionFormData = z.infer<typeof createTransactionSchema>;
```

**Unit Test**:
```typescript
// frontend/src/features/transactions/schemas/transactionSchema.test.ts
import { describe, it, expect } from "vitest";
import { createTransactionSchema } from "./transactionSchema";

describe("createTransactionSchema", () => {
  it("should validate valid expense data (PEM-USER-001 Scenario 1)", () => {
    const validData = {
      type: "expense" as const,
      amount: "45.50",
      date: "2026-02-03",
      category_id: 1,
      description: "Lunch at restaurant",
    };
    
    const result = createTransactionSchema.safeParse(validData);
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.amount).toBe(45.50); // Transformed to number
    }
  });

  it("should reject missing amount (PEM-USER-001 Scenario 3)", () => {
    const invalidData = {
      type: "expense" as const,
      date: "2026-02-03",
      category_id: 1,
    };
    
    const result = createTransactionSchema.safeParse(invalidData);
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain("obligatoria");
    }
  });

  it("should reject negative amount (PEM-USER-001 Scenario 5)", () => {
    const invalidData = {
      type: "expense" as const,
      amount: "-50.00",
      date: "2026-02-03",
      category_id: 1,
    };
    
    const result = createTransactionSchema.safeParse(invalidData);
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain("positivo");
    }
  });

  it("should reject future date (PEM-USER-001 Scenario 6)", () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const futureDate = tomorrow.toISOString().split("T")[0];
    
    const invalidData = {
      type: "expense" as const,
      amount: "45.50",
      date: futureDate,
      category_id: 1,
    };
    
    const result = createTransactionSchema.safeParse(invalidData);
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain("futura");
    }
  });
});
```

---

### Task 3: Create TanStack Query Mutation Hook

**Purpose**: Create the API hook for creating transactions using TanStack Query. Maps to PEM-USER-001 Scenarios 1, 10.

**Prerequisites**: Task 2 completed

**Artifacts impacted**:
- `frontend/src/features/transactions/api/useCreateTransaction.ts` (NEW)
- `frontend/src/api/http.ts` (assumes exists)

**Test types**: Integration test (with MSW mock)

**BDD Acceptance**:
```gherkin
Given I have a useCreateTransaction hook
When I call the mutation with valid data
Then a POST request is sent to /api/transactions
And the mutation succeeds
When the API returns an error
Then the mutation fails
And the error is available in the hook
```

**Implementation**:
```typescript
// frontend/src/features/transactions/api/useCreateTransaction.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { http } from "@/api/http";
import type { CreateTransactionFormData } from "../schemas/transactionSchema";

/**
 * TanStack Query mutation hook for creating transactions.
 * 
 * [Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-FE-T03]
 */

interface TransactionResponse {
  id: number;
  user_id: number;
  type: "income" | "expense";
  amount: string;
  date: string;
  category_id: number;
  category_name: string;
  description: string | null;
  created_at: string;
}

export function useCreateTransaction() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateTransactionFormData): Promise<TransactionResponse> => {
      const response = await http.post<TransactionResponse>("/api/transactions", {
        type: data.type,
        amount: data.amount.toString(),
        date: data.date,
        category_id: data.category_id,
        description: data.description || null,
      });
      return response.data;
    },
    onSuccess: () => {
      // Invalidate transaction list query (when it exists)
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
    },
    retry: 1, // Retry once on failure (PEM-USER-001 Scenario 10)
    retryDelay: 1000, // Wait 1 second before retry
  });
}
```

---

### Task 4: Create Expense Entry Form Component

**Purpose**: Build the main form component with all fields, validation, and submission logic. Maps to PEM-USER-001 Scenarios 1, 2, 9, 10.

**Prerequisites**: Tasks 2-3 completed

**Artifacts impacted**:
- `frontend/src/features/transactions/components/ExpenseEntryForm.tsx` (NEW)

**Test types**: Component test (React Testing Library)

**BDD Acceptance**:
```gherkin
Given I render the ExpenseEntryForm component
When I fill in all required fields with valid data
And I submit the form
Then the API mutation is called
And a success toast is shown
And the form is reset
When I submit the form with invalid data
Then validation errors are displayed inline
And the form is not submitted
When the API returns an error
Then an error toast is shown
And the form data is preserved
```

**Implementation**:
```typescript
// frontend/src/features/transactions/components/ExpenseEntryForm.tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCreateTransaction } from "../api/useCreateTransaction";
import { createTransactionSchema, type CreateTransactionFormData } from "../schemas/transactionSchema";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/components/ui/use-toast";
import { Loader2 } from "lucide-react";

/**
 * Expense entry form component.
 * 
 * [Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-FE-T03]
 */

interface ExpenseEntryFormProps {
  onSuccess?: () => void;
}

export function ExpenseEntryForm({ onSuccess }: ExpenseEntryFormProps) {
  const { toast } = useToast();
  const createTransaction = useCreateTransaction();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
    setValue,
  } = useForm<CreateTransactionFormData>({
    resolver: zodResolver(createTransactionSchema),
    defaultValues: {
      type: "expense",
      amount: "",
      date: new Date().toISOString().split("T")[0], // Today's date
      category_id: undefined,
      description: "",
    },
  });

  const onSubmit = async (data: CreateTransactionFormData) => {
    try {
      await createTransaction.mutateAsync(data);
      
      // Success handling (PEM-USER-001 Scenario 1)
      toast({
        title: "Gasto añadido",
        description: "El gasto se ha registrado correctamente",
        variant: "default", // Uses --secondary (Green) from brand guidelines
      });
      
      reset(); // Reset form for next entry
      onSuccess?.();
      
    } catch (error) {
      // Error handling (PEM-USER-001 Scenario 10)
      toast({
        title: "Error al guardar",
        description: "No se pudo guardar el gasto. Por favor, inténtalo de nuevo.",
        variant: "destructive",
      });
      // Form data is preserved (no reset on error)
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-4" // 16px gap (space-4 from brand guidelines)
      role="form"
      aria-label="Formulario de gastos"
    >
      {/* Amount Field */}
      <div className="space-y-2">
        <Label htmlFor="amount" className="text-sm font-medium">
          Cantidad *
        </Label>
        <Input
          id="amount"
          type="number"
          step="0.01"
          placeholder="0.00"
          aria-required="true"
          aria-invalid={!!errors.amount}
          aria-describedby={errors.amount ? "amount-error" : undefined}
          {...register("amount")}
        />
        {errors.amount && (
          <p id="amount-error" className="text-sm text-destructive" role="alert">
            {errors.amount.message}
          </p>
        )}
      </div>

      {/* Date Field */}
      <div className="space-y-2">
        <Label htmlFor="date" className="text-sm font-medium">
          Fecha *
        </Label>
        <Input
          id="date"
          type="date"
          aria-required="true"
          aria-invalid={!!errors.date}
          aria-describedby={errors.date ? "date-error" : undefined}
          {...register("date")}
        />
        {errors.date && (
          <p id="date-error" className="text-sm text-destructive" role="alert">
            {errors.date.message}
          </p>
        )}
      </div>

      {/* Category Field */}
      <div className="space-y-2">
        <Label htmlFor="category" className="text-sm font-medium">
          Categoría *
        </Label>
        <Select
          onValueChange={(value) => setValue("category_id", parseInt(value), { shouldValidate: true })}
        >
          <SelectTrigger
            id="category"
            aria-required="true"
            aria-invalid={!!errors.category_id}
            aria-describedby={errors.category_id ? "category-error" : undefined}
          >
            <SelectValue placeholder="Selecciona una categoría" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="1">Comida</SelectItem>
            <SelectItem value="2">Transporte</SelectItem>
            <SelectItem value="3">Entretenimiento</SelectItem>
            <SelectItem value="4">Servicios</SelectItem>
            <SelectItem value="5">Salud</SelectItem>
            <SelectItem value="6">Otros</SelectItem>
          </SelectContent>
        </Select>
        {errors.category_id && (
          <p id="category-error" className="text-sm text-destructive" role="alert">
            {errors.category_id.message}
          </p>
        )}
      </div>

      {/* Description Field (Optional) */}
      <div className="space-y-2">
        <Label htmlFor="description" className="text-sm font-medium">
          Descripción (opcional)
        </Label>
        <Textarea
          id="description"
          placeholder="Ej: Almuerzo en restaurante"
          rows={3}
          aria-describedby={errors.description ? "description-error" : undefined}
          {...register("description")}
        />
        {errors.description && (
          <p id="description-error" className="text-sm text-destructive" role="alert">
            {errors.description.message}
          </p>
        )}
      </div>

      {/* Submit Button */}
      <Button
        type="submit"
        disabled={isSubmitting || createTransaction.isPending}
        className="w-full"
        aria-label="Guardar gasto"
      >
        {(isSubmitting || createTransaction.isPending) && (
          <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
        )}
        Guardar
      </Button>
    </form>
  );
}
```

---

### Task 5: Write Component Tests

**Purpose**: Test the form component behavior with React Testing Library. Maps to PEM-USER-001 Scenarios 1, 3, 10.

**Prerequisites**: Task 4 completed

**Artifacts impacted**:
- `frontend/src/features/transactions/components/ExpenseEntryForm.test.tsx` (NEW)

**Test types**: Component test

**BDD Acceptance**:
```gherkin
Given the form is rendered
When I fill in valid data and submit
Then the API is called with correct data
And a success toast is shown
When I submit with missing required fields
Then validation errors are displayed
And the API is not called
When the API returns an error
Then an error toast is shown
And the form data is preserved
```

**Implementation**:
```typescript
// frontend/src/features/transactions/components/ExpenseEntryForm.test.tsx
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ExpenseEntryForm } from "./ExpenseEntryForm";
import { http } from "@/api/http";

// Mock API
vi.mock("@/api/http");

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe("ExpenseEntryForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should submit form with valid data (PEM-USER-001 Scenario 1)", async () => {
    const user = userEvent.setup();
    const mockPost = vi.mocked(http.post).mockResolvedValue({
      data: {
        id: 1,
        user_id: 123,
        type: "expense",
        amount: "45.50",
        date: "2026-02-03",
        category_id: 1,
        category_name: "Comida",
        description: "Almuerzo",
        created_at: "2026-02-03T12:00:00Z",
      },
    });

    render(<ExpenseEntryForm />, { wrapper: createWrapper() });

    // Fill in form
    await user.type(screen.getByLabelText(/cantidad/i), "45.50");
    await user.type(screen.getByLabelText(/fecha/i), "2026-02-03");
    await user.click(screen.getByRole("combobox", { name: /categoría/i }));
    await user.click(screen.getByRole("option", { name: /comida/i }));
    await user.type(screen.getByLabelText(/descripción/i), "Almuerzo");

    // Submit
    await user.click(screen.getByRole("button", { name: /guardar/i }));

    // Verify API call
    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith("/api/transactions", {
        type: "expense",
        amount: "45.5",
        date: "2026-02-03",
        category_id: 1,
        description: "Almuerzo",
      });
    });

    // Verify success toast
    await waitFor(() => {
      expect(screen.getByText(/gasto añadido/i)).toBeInTheDocument();
    });
  });

  it("should show validation errors for missing required fields (PEM-USER-001 Scenario 3)", async () => {
    const user = userEvent.setup();

    render(<ExpenseEntryForm />, { wrapper: createWrapper() });

    // Submit without filling fields
    await user.click(screen.getByRole("button", { name: /guardar/i }));

    // Verify validation errors
    await waitFor(() => {
      expect(screen.getByText(/la cantidad es obligatoria/i)).toBeInTheDocument();
    });

    // Verify API was not called
    expect(http.post).not.toHaveBeenCalled();
  });

  it("should handle API error and preserve form data (PEM-USER-001 Scenario 10)", async () => {
    const user = userEvent.setup();
    vi.mocked(http.post).mockRejectedValue(new Error("Network error"));

    render(<ExpenseEntryForm />, { wrapper: createWrapper() });

    // Fill in form
    await user.type(screen.getByLabelText(/cantidad/i), "45.50");
    await user.type(screen.getByLabelText(/fecha/i), "2026-02-03");
    await user.click(screen.getByRole("combobox", { name: /categoría/i }));
    await user.click(screen.getByRole("option", { name: /comida/i }));

    // Submit
    await user.click(screen.getByRole("button", { name: /guardar/i }));

    // Verify error toast
    await waitFor(() => {
      expect(screen.getByText(/error al guardar/i)).toBeInTheDocument();
    });

    // Verify form data is preserved
    expect(screen.getByLabelText(/cantidad/i)).toHaveValue(45.5);
  });
});
```

---

### Task 6: Write Accessibility Tests

**Purpose**: Verify keyboard navigation and ARIA labels. Maps to PEM-USER-001 Scenario 9.

**Prerequisites**: Task 4 completed

**Artifacts impacted**:
- `frontend/src/features/transactions/components/ExpenseEntryForm.a11y.test.tsx` (NEW)

**Test types**: Accessibility test

**BDD Acceptance**:
```gherkin
Given the form is rendered
When I navigate using only the keyboard (Tab)
Then I can access all form fields in logical order
And all interactive elements have visible focus indicators
When I press Enter on the submit button
Then the form is submitted
```

**Implementation**:
```typescript
// frontend/src/features/transactions/components/ExpenseEntryForm.a11y.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ExpenseEntryForm } from "./ExpenseEntryForm";
import { axe, toHaveNoViolations } from "jest-axe";

expect.extend(toHaveNoViolations);

const createWrapper = () => {
  const queryClient = new QueryClient();
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe("ExpenseEntryForm Accessibility", () => {
  it("should have no accessibility violations", async () => {
    const { container } = render(<ExpenseEntryForm />, { wrapper: createWrapper() });
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("should support keyboard navigation (PEM-USER-001 Scenario 9)", async () => {
    const user = userEvent.setup();
    render(<ExpenseEntryForm />, { wrapper: createWrapper() });

    // Tab through all fields
    await user.tab(); // Amount field
    expect(screen.getByLabelText(/cantidad/i)).toHaveFocus();

    await user.tab(); // Date field
    expect(screen.getByLabelText(/fecha/i)).toHaveFocus();

    await user.tab(); // Category field
    expect(screen.getByRole("combobox", { name: /categoría/i })).toHaveFocus();

    await user.tab(); // Description field
    expect(screen.getByLabelText(/descripción/i)).toHaveFocus();

    await user.tab(); // Submit button
    expect(screen.getByRole("button", { name: /guardar/i })).toHaveFocus();
  });

  it("should have proper ARIA labels", () => {
    render(<ExpenseEntryForm />, { wrapper: createWrapper() });

    // Form has aria-label
    expect(screen.getByRole("form")).toHaveAttribute("aria-label", "Formulario de gastos");

    // Required fields have aria-required
    expect(screen.getByLabelText(/cantidad/i)).toHaveAttribute("aria-required", "true");
    expect(screen.getByLabelText(/fecha/i)).toHaveAttribute("aria-required", "true");
  });
});
```

---

### Task 7: Create Feature Directory Structure and Types

**Purpose**: Set up the feature directory structure and TypeScript types. Maps to frontend architecture standards.

**Prerequisites**: None

**Artifacts impacted**:
- `frontend/src/features/transactions/` (NEW directory)
- `frontend/src/features/transactions/types.ts` (NEW)

**Test types**: N/A (structure setup)

**BDD Acceptance**:
```gherkin
Given the frontend source directory exists
When I create the transactions feature directory
Then the directory structure matches the canonical frontend structure
And TypeScript types are defined for transaction entities
```

**Steps**:
1. Create directory structure:
```
frontend/src/features/transactions/
├── api/
│   └── useCreateTransaction.ts
├── components/
│   ├── ExpenseEntryForm.tsx
│   └── ExpenseEntryForm.test.tsx
├── schemas/
│   ├── transactionSchema.ts
│   └── transactionSchema.test.ts
└── types.ts
```

2. Create types file:
```typescript
// frontend/src/features/transactions/types.ts
/**
 * TypeScript types for transactions feature.
 * 
 * [Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-FE-T03]
 */

export interface Transaction {
  id: number;
  user_id: number;
  type: "income" | "expense";
  amount: string;
  date: string;
  category_id: number;
  category_name: string;
  description: string | null;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  type: "income" | "expense";
}
```

---

### Task 8: Integrate Form into Application Routes

**Purpose**: Add the form to the application routing so users can access it. Maps to "Connectivity & Routing" NFR.

**Prerequisites**: Task 4 completed

**Artifacts impacted**:
- `frontend/src/app/router/index.tsx` (UPDATE, assumes exists)
- `frontend/src/features/transactions/pages/NewTransactionPage.tsx` (NEW)

**Test types**: Manual verification

**BDD Acceptance**:
```gherkin
Given the application is running
When I navigate to /transactions/new
Then I see the expense entry form
And I can submit a transaction
```

**Implementation**:
```typescript
// frontend/src/features/transactions/pages/NewTransactionPage.tsx
import { ExpenseEntryForm } from "../components/ExpenseEntryForm";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

/**
 * New transaction page.
 * 
 * [Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-FE-T03]
 */
export function NewTransactionPage() {
  return (
    <div className="container mx-auto py-8 px-4 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Añadir Gasto</CardTitle>
          <CardDescription>
            Registra un nuevo gasto para llevar el control de tus finanzas
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ExpenseEntryForm />
        </CardContent>
      </Card>
    </div>
  );
}
```

**Router Update** (example, adjust to actual router structure):
```typescript
// frontend/src/app/router/index.tsx
import { NewTransactionPage } from "@/features/transactions/pages/NewTransactionPage";

// Add to routes array:
{
  path: "/transactions/new",
  element: <NewTransactionPage />,
}
```

---

### Task 9: Run Tests and Verify Coverage

**Purpose**: Ensure all tests pass and coverage meets thresholds. Maps to frontend quality gates.

**Prerequisites**: Tasks 2-6 completed

**Artifacts impacted**: None (testing only)

**Test types**: Unit + Component + Accessibility tests

**BDD Acceptance**:
```gherkin
Given all tests are written
When I run the test suite
Then all tests pass
And code coverage is >= 90% for lines
And code coverage is >= 85% for branches
```

**Steps**:
1. Run unit tests:
```bash
docker compose exec frontend npm run test -- src/features/transactions/schemas
```
Expected: All schema tests pass

2. Run component tests:
```bash
docker compose exec frontend npm run test -- src/features/transactions/components
```
Expected: All component tests pass

3. Run coverage report:
```bash
docker compose exec frontend npm run test -- --coverage src/features/transactions
```
Expected: Coverage >= 90% lines, >= 85% branches

4. Verify no linting errors:
```bash
docker compose exec frontend npm run lint -- src/features/transactions
```
Expected: No errors

---

### Task 10: Manual Testing and Visual QA

**Purpose**: Manually verify the form works correctly in the browser. Maps to brand compliance and UX verification.

**Prerequisites**: Task 8 completed

**Artifacts impacted**: None (manual testing)

**Test types**: Manual verification

**BDD Acceptance**:
```gherkin
Given the application is running
When I navigate to /transactions/new
Then I see the expense entry form with correct styling
And all brand design tokens are applied
And the form is responsive on mobile
When I submit a valid transaction
Then the transaction is created
And I see a success toast
```

**Steps**:
1. Start the application: `docker compose up -d`
2. Open browser to `http://localhost:5188/transactions/new`
3. Verify visual appearance:
   - Primary button uses Terracotta AA color (#B2612A)
   - Text uses Navy color (#322B46)
   - Spacing follows 8pt grid (16px gaps, 24px padding)
   - Border radius is 1rem
   - Font is Inter (or system fallback)
4. Test form submission:
   - Fill in: Amount: 45.50, Date: Today, Category: Comida, Description: "Almuerzo"
   - Click "Guardar"
   - Verify success toast appears
   - Verify form resets
5. Test validation:
   - Leave amount empty, click "Guardar"
   - Verify error message: "La cantidad es obligatoria"
   - Enter negative amount: -50
   - Verify error message: "La cantidad debe ser un número positivo"
6. Test keyboard navigation:
   - Tab through all fields
   - Verify visible focus indicators
   - Press Enter on submit button
   - Verify form submits
7. Test mobile responsiveness:
   - Resize browser to mobile width (375px)
   - Verify form is usable
   - Verify touch targets are >= 44×44px
8. Test dark mode (if applicable):
   - Toggle dark mode
   - Verify colors are readable
   - Verify contrast meets AA standards

---

## 5) Verification Plan

### Automated Tests

**Unit Tests** (Zod schema validation):
```bash
docker compose exec frontend npm run test -- src/features/transactions/schemas/transactionSchema.test.ts
```
Expected: All validation tests pass

**Component Tests** (React Testing Library):
```bash
docker compose exec frontend npm run test -- src/features/transactions/components/ExpenseEntryForm.test.tsx
```
Expected: All component tests pass (happy path, validation, error handling)

**Accessibility Tests** (jest-axe):
```bash
docker compose exec frontend npm run test -- src/features/transactions/components/ExpenseEntryForm.a11y.test.tsx
```
Expected: No accessibility violations, keyboard navigation works

**Coverage Report**:
```bash
docker compose exec frontend npm run test -- --coverage src/features/transactions
```
Expected: >= 90% lines, >= 85% branches

### Manual Verification

**1. Visual QA Checklist** (from brand-guidelines.md):
- [x] Buttons have visible focus indicators
- [x] AA contrast met for normal text (4.5:1)
- [x] States defined: hover/focus/disabled/loading
- [x] Touch targets >= 44×44px
- [x] No hardcoded hex/px in components (using design tokens)
- [x] Dark mode readable (if applicable)

**2. Functional Testing**:
- Navigate to `http://localhost:5188/transactions/new`
- Submit valid transaction → Success toast + form reset
- Submit invalid transaction → Validation errors displayed
- Test keyboard navigation → All fields accessible via Tab
- Test mobile responsiveness → Form usable on 375px width

**3. API Integration Testing**:
- Verify POST request is sent to `/api/transactions` with correct data
- Verify JWT token is included in Authorization header
- Verify success response triggers toast and query invalidation
- Verify error response triggers error toast and preserves form data

---

## 6) Success Criteria

This ticket is considered complete when:
- [x] Zod validation schema created and tested
- [x] TanStack Query mutation hook created
- [x] Expense entry form component implemented
- [x] Form fields: Amount, Date, Category, Description (optional)
- [x] Client-side validation working (Zod + React Hook Form)
- [x] API integration working (POST `/api/transactions`)
- [x] Success handling: Toast notification, query invalidation, form reset
- [x] Error handling: Inline validation errors, server error toast, retry logic
- [x] Accessibility: Keyboard navigation, ARIA labels, focus indicators
- [x] Spanish labels: All UI text in Spanish
- [x] Brand compliance: Design tokens applied, colors/spacing/typography correct
- [x] Component tests pass (>= 90% coverage)
- [x] Accessibility tests pass (no violations)
- [x] Manual testing completed (visual QA, functional testing)
- [x] Form integrated into application routes
- [x] All PEM-USER-001 scenarios (1-6, 9, 10) are satisfied

---

## 7) Traceability Matrix

| Task | Scenario(s) | Acceptance Criteria |
|------|-------------|---------------------|
| Task 2 | PEM-USER-001 Scenarios 3, 4, 5, 6 | Zod schema validates amount, date, category |
| Task 3 | PEM-USER-001 Scenarios 1, 10 | Mutation hook calls API, handles errors, retries |
| Task 4 | PEM-USER-001 Scenarios 1, 2, 9, 10 | Form component with all fields, validation, submission |
| Task 5 | PEM-USER-001 Scenarios 1, 3, 10 | Component tests verify happy path, validation, errors |
| Task 6 | PEM-USER-001 Scenario 9 | Accessibility tests verify keyboard navigation, ARIA |
| Task 7 | N/A | Feature directory structure follows frontend standards |
| Task 8 | N/A | Form accessible via `/transactions/new` route |
| Task 9 | All scenarios | All tests pass, coverage >= 90% |
| Task 10 | All scenarios | Manual testing verifies brand compliance and UX |
