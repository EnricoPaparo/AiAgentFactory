# Requirements Blueprint: ceramirycs

## Source Request

Miriam wants a minimal and very simple website for her cozy ceramic productions. The activity is called CeraMirycs. The site must feel modern, warm, artisanal and clean. It only needs a landing page and a contact page. Real contact details must remain empty or be shown as `da definire`: email, phone, address and Instagram. No realistic contact data may be invented.

## Goal

Create a small public website concept and implementation target for CeraMirycs that presents Miriam's ceramic work with a warm, modern, clean and handcrafted feeling, while avoiding any fabricated contact information.

## Expected Output

A minimal website with:

- One landing page.
- One contact page.
- Visual and written presentation for CeraMirycs.
- Contact fields for email, phone, address and Instagram left empty or marked `da definire`.

## Functional Requirements

- Provide a landing page for CeraMirycs.
- Provide a separate contact page.
- Present the activity as Miriam's cozy ceramic production brand.
- Include navigation between landing page and contact page.
- Include contact fields for email, phone, address and Instagram.
- Display each real contact field as empty or `da definire`.
- Avoid fabricated realistic contact values, including plausible emails, phone numbers, addresses or Instagram handles.
- Keep the content minimal and simple.

## Non-Functional Requirements

- Visual tone must be modern, warm, artisanal and clean.
- The site should feel lightweight and easy to scan.
- The design should suit handmade ceramic work rather than a generic corporate landing page.
- The pages should be responsive enough for desktop and mobile viewing.
- Text should be concise and not over-explain the project.

## Constraints

- Project artifacts must be produced inside `projects/ceramirycs/`.
- The workflow must stay in the same Codex conversation.
- Human Gates required: `approve-requirements`, `approve-solution-blueprint`, `approve-execution-plan`, `approve-final-delivery`.
- Requirement Analyst, Architect, Pipeline Designer and Knowledge Compiler must not be skipped.
- Temporary Agent Packages must be created and executed during the operational phase.
- Review and Pipeline Supervisor must run before final delivery approval.
- No previous CeraMirycs workspace may be reused.
- No realistic contact data may be invented.

## Assumptions

- The site can use placeholder copy for brand presentation as long as it does not invent operational contact details.
- The ceramic products can be described generally as cozy handmade ceramics without claiming specific catalog items, prices or production details not provided by the user.
- A static website is likely sufficient, but the final technology choice belongs to the Architect phase.
- Images or product photography have not been provided yet.

## Ambiguities

- Whether Miriam has existing product photos, logo, color preferences or typography preferences is unknown.
- Whether the output should be a coded static site, a design-only mockup, or both is not yet specified by the user.
- Hosting, domain and deployment are not specified.
- Language preference for the website copy is not explicitly stated, though the request is in Italian.

## Out Of Scope

- E-commerce, cart, checkout or payment flows.
- Product catalog management.
- Booking or commission request automation.
- Newsletter, analytics, CRM or backend systems.
- Invented contact data.
- Brand identity system beyond what is needed for a minimal website.
- Deployment unless later approved in blueprint or execution plan.

## Acceptance Criteria

- A reviewer can identify exactly two pages: landing and contacts.
- The landing page clearly names CeraMirycs and connects it to Miriam's cozy ceramic productions.
- The visual direction is warm, modern, artisanal and clean.
- The contact page includes email, phone, address and Instagram fields.
- Each contact field is blank or explicitly says `da definire`.
- No realistic placeholder contact value appears anywhere in the website or deliverable.
- Navigation between pages works.
- The site or prototype can be inspected locally.
- The final review confirms that requirements, architecture, execution plan, review and Pipeline Supervisor steps were completed before final delivery gate.

## Initial Risks

- Without images, the site may need generated or abstract visual treatment rather than real product photography.
- If the implementation stack is overcomplicated, it may violate the user's desire for a minimal and very simple site.
- Placeholder brand copy could accidentally imply facts not provided by the user.
- Contact placeholders are a strict data integrity constraint and must be checked explicitly during review.

## Stakeholders

- Miriam: site subject and eventual owner of real contact information.
- Human Maintainer: approval owner for AgentFactory Human Gates.
- Future site visitors interested in handmade ceramics.

## Priority Notes

- Highest priority: minimal two-page structure, warm artisan feel, and no invented contact data.
- Lower priority: advanced animation, complex CMS, backend or deployment.

## Reference Materials

- projects/ceramirycs/input/initial-request.md
