# Product Requirements Document: AI Game Creator (Web Platform)

**1. Overview**

*   **Project Name:** Arcade Game Generator
*   **Description:** A web-based platform that empowers users to create simple 2D retro arcade-style games using natural language prompts. The platform leverages AI to generate game logic, pixel art assets, and allows users to refine their games through a conversational interface, ultimately sharing them within the platform.
*   **Goal:** To make basic game creation accessible, fun, and fast for individuals without prior coding or art design experience.

**2. Objectives**

*   Enable users to generate playable 2D arcade games from simple text prompts.
*   Provide an intuitive, conversational AI interface for refining game mechanics, aesthetics, and content.
*   Automate the generation of all necessary game code (Lua for Love2D) and pixel art assets.
*   Offer an in-browser preview of the generated game.
*   Allow users to easily share their created games via unique links within the platform.
*   Prioritize user experience for non-technical individuals.

**3. Target Audience**

*   Hobbyists and casual creators interested in making simple games.
*   Educators and students looking for an easy entry point into game design concepts.
*   Individuals who want to quickly prototype simple game ideas without technical overhead.
*   "Noob game devs" and "wannabe game devs" who prefer a prompt-driven, AI-assisted workflow.

**4. MVP Scope & Features**

*   **Core AI Game Generation Engine:**
    *   Takes a user's natural language prompt describing a game concept (e.g., "a side-scrolling game where a knight collects coins and avoids dragons").
    *   AI generates a basic game design specification (internal to the system).
    *   AI generates Lua code (for Love2D) based on the design.
    *   AI generates descriptions for all necessary pixel art assets (characters, items, tiles, UI).
*   **AI Asset Pipeline (Hybrid Approach):**
    *   AI (e.g., Gemini, Stable Diffusion) generates initial pixel art images/frames based on internal descriptions.
    *   Automated backend process uses a tool (like Aseprite CLI on the server) to:
        *   Clean up, arrange, and structure these AI-generated images into sprite sheets.
        *   Generate necessary metadata (e.g., JSON for frame data, animations).
    *   The end-user does *not* directly interact with Aseprite or any art tool.
*   **Web Platform & User Interface:**
    *   Simple landing page with a prompt input field.
    *   Conversational chat interface for game refinement (e.g., "make the knight jump higher," "change dragons to bats").
    *   In-browser game preview window (e.g., using Love.js or server-side streaming).
    *   "Generate Game" and "Refine" buttons.
    *   "Share Game" button that generates a unique, shareable link to the game playable on the platform.
*   **Game Style Focus:** Simple 2D retro arcade games (e.g., platformers, top-down shooters, maze games). Limited complexity for MVP.

**5. Technical Considerations (High-Level)**

*   **Frontend:** Web framework (e.g., React, Vue, Svelte) for the user interface.
*   **Backend:** Server-side language (e.g., Python with Flask/Django) to handle requests, manage AI interactions, and serve game data.
*   **AI Models:**
    *   Large Language Model (e.g., Gemini) for understanding prompts, generating game logic (Lua), and powering the conversational refinement.
    *   Image Generation Model (e.g., Gemini, Stable Diffusion) for creating initial pixel art concepts/frames.
*   **Asset Processing:** Aseprite CLI (or similar) running on the server for structuring AI-generated images into game-ready sprite sheets and metadata.
*   **Game Execution for Preview:** Love.js (Love2D compiled to WebAssembly) or server-side Love2D execution with streamed output.
*   **Database:** To store user prompts (if accounts are added later), generated game configurations, and shared game links.

**6. Core User Flow (MVP)**

1.  User visits the web platform.
2.  User types a game concept into the prompt box (e.g., "Pac-Man but you're a cookie avoiding kids").
3.  User clicks "Generate Game."
4.  Backend AI processes the prompt, generates Lua code and pixel art assets (using the hybrid AI + Aseprite pipeline).
5.  Game preview appears in the browser.
6.  User can chat with an AI agent to request changes (e.g., "make the cookie faster," "add another kid enemy"). The game updates in the preview.
7.  User clicks "Share Game" to get a unique link.

**7. Out of MVP Scope (Potential Future Features)**

*   User accounts and saved game libraries.
*   Advanced art customization options (e.g., style selection, color palettes).
*   Sound effect generation/selection.
*   More complex game mechanics or genres.
*   Multiplayer capabilities.
*   Downloading game source/binaries.

**8. Key Success Metrics (MVP)**

*   Users can successfully generate a playable game from a reasonable prompt.
*   The conversational refinement feature allows for meaningful game modifications.
*   The quality of generated assets is acceptable for simple arcade games.
*   Users can successfully share and play shared games.
