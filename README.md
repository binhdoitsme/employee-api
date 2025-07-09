# employee-api

A search API to be used in Employee Search Directory for a HR company search

## Approach

- Consider search to be part of an Employee API (which is considered a microservice)
- Based on Domain-driven Design, Inversion of Control principles to make architectural decisions
- Used layered architecture, dependency inversion (using Protocol and inheritance) to separate application core (located in `services` package) from API and DB.
  - Package breakdown:
    - `controllers`: input gateway to business services
    - `services`: business logic. Now it's separated by feature (e.g. employee-related, ratelimit-related, viewconfig-related, etc.). Contain: Service class/functions, domain entity, repository interfaces (a.k.a "output ports")
    - `middlewares`: helpful middlewares to be applied on FastAPI's request handler chain
    - `infrastructure`: implementations of repository interfaces on actual DB/persistence
  - This approach may create a large number of files, but the created files are relatively light and should be easily comprehensible. To understand the system, just visit `services` to understand what the business logic is.

## Assumptions

- Employees have the following attributes:
  - id
  - org_id
  - company_id --> db column: company_id
  - first_name
  - last_name
  - contact_info: email, phone_number
  - department --> db column: department_id
  - location --> db column: location_id
  - status --> db column: status
- org_id is used as shard key, to identify that an employee belongs to a specific organization.
- Judging from frontend, let's assume we have multi-column index of (status, location_id, department_id, company_id).
- Assumed that we have Employee domain logic enforcement in services/employee.
- We are focusing more on the application side so I'm using an ORM (SQLAlchemy) and not carefully tuned the queries.

## Key decisions

- As searching function has a lot of conditions, and placing them on URL can exceed URL length -- I decided to use POST instead of GET, sacrificed cachability for flexibility
- Chose layered architecture centering around `services` layer to allow good testability, quick swap of infrastructural components (DB from SQL -> NoSQL, or rate limit store from in-memory to Redis). This also allow me to take advantage of Dependency Injection.
- Enforced pagination so as to keep responses light.
- Used `pdm` as package manager to simplify package version management.
- Used Docker & Docker compose in development to simulate the situation as close to real scenario as possible.

## Running the API

Running locally:

```(shell)
pip install pdm
pdm install
pdm dev # pdm start if don't want hot reload
```

Running via Docker compose

```(shell)
docker compose up -d
```

## API documentation

Get the API up and running, then visit <http://localhost:8000/docs> for OpenAPI specs.

## Sharing -- AI in development

### 1. AI tools usage

- In my teams, we use a wide range of AI tools, ranging from code-centric GitHub Copilot built into VSCode, to ChatGPT, Claude, Gemini or even Perplexity.
- We used them for a number of different tasks:
  - Code comprehension: We often use GPT, Claude shipped with GitHub Copilot to help us understand a codebase the first time we get in touch with it, to have a glance at what the code does and which components are implemented. Of course it's not 100% correct all the time, but we found that AI helps us understand an exotic codebase much easier, reducing time from weeks to merely days.
  - Boilerplate generation: For sections that are repetitive but not exactly the same and creating a shared function is overkill or makes codebase bloated, we use AI with a sample prompt to let it generate those sections.
  - Testing: AI helped us implement test cases from test scenario or description, given we give it the correct test scenario in advance
  - Documentation: AI also helped us generate structured code documentation that are highlighted by IDEs and understandable by humans.

### 2. Our AI best practices

- We treat AI results as assistance only. Never over-reliant on it and never agree 100% with it without understanding of what it tries to achieve and whether that's valid.
- When using AI, we try to put as much context as possible. That's why when coding, we favour GitHub Copilot, as it can read the whole codebase into its context.
