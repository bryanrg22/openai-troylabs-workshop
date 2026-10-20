# Reusable ChatGPT connection reference

For the coding agent implementing Stage 4. Keep the participant's four prompts unchanged.

## Reuse the official helper

Use OpenAI's [Sign in with ChatGPT DevKit](https://github.com/openai/sign-in-with-chatgpt-devkit), especially `packages/local`. The isolated macOS demo started from source commit [`0a36fefeb913055c8c7a1a29b63d82b96b2e841a`](https://github.com/openai/sign-in-with-chatgpt-devkit/tree/0a36fefeb913055c8c7a1a29b63d82b96b2e841a/packages/local) and used a narrow local adaptation for tool-stream continuation and automatic return. That is a reproducibility reference, not a requirement to ignore newer fixes. Inspect current documentation and package availability first; do not assume a registry package exists. Keep license/change notices when adapting or redistributing it. The reference DevKit has a noncommercial license; review the actual terms before another use.

Reuse its authorization, verified identity, profile/session storage, credential refresh, model discovery, and response-stream implementation. Do not copy a signed-in profile, use another application's client credentials, or build a new OAuth flow from a guessed example. No credentials or running companion are included in this student starter. This guide does not grant account access.

The tested local adapter used Node.js 22.13+ and macOS Keychain-backed credential encryption. Windows/Linux credential adapters have not been verified by this workshop demo. Implement and test the participant's platform; never claim cross-platform readiness based on macOS success or fall back to plaintext credentials.

## Small adapter contract

Wrap the official client behind these responsibilities (conceptual names; inspect the actual SDK before coding):

- `signIn`: launch the official authorization flow from the companion and keep a distinct app profile.
- `sessionStatus`: distinguish identity, plan permission, usable models, and expired/error states.
- `listModels`: discover models available to this authorized account.
- `runResponse`: support streamed text, function calls, tool results, and continuation until actual completion.
- `signOut`: use the SDK's supported sign-out/credential cleanup path.

The helper owns account/session mechanics. The student still builds agent instructions, tool schemas, the hosted SQL/R2 handlers, the website chat, and D1 conversation persistence. A tested helper may be reused without copying the completed LaunchDesk agent.

## Website-to-companion relay

The companion binds to `127.0.0.1`, accepts only the configured HTTPS Site origin, and requires an unpredictable pairing capability. Its own portal must protect sign-in/connect operations from cross-site requests. Pair the browser without putting provider tokens in browser storage. If using a one-time URL fragment to deliver a separate local pairing capability, remove the fragment immediately after capture and never log or publish it.

A useful logical API is:

- Local status: connection/permission state, never credentials.
- Local chat/run endpoint: bounded history plus a stable request ID; pending/completed/error results support refresh recovery.
- Local tool-request queue: the model's allowlisted read-only tool name and arguments, with a unique request ID.
- Local tool-result endpoint: the result for that pending ID, consumed once with a timeout.
- Hosted tool endpoint: authenticated same-origin request that validates arguments and runs parameterized SQL or R2 lookup. Return only authorized results.

The signed-in browser relays tool requests and results, using its existing Site session only with the hosted Site. Provider OAuth tokens never leave the companion. Do not relay browser cookies to the companion. Never give it arbitrary SQL execution or arbitrary URLs to fetch. Handle unknown, expired, duplicate, or mismatched tool IDs. If the webpage is required for the relay, surface disconnection and keep saved messages intact.

## Completion and return behavior

After the SDK validates authorization, return automatically to the website's AI Assistant page. Preserve OAuth verification and callback protections; do not remove checks to make redirection work. Use the current official model/inference contract and preserve all required tool and reasoning continuation items.

In the isolated test, the final completion event could have an empty output array even though streamed output items contained real function calls. The adapter retained completed streamed items when needed and still required a genuine completion event. Treat this as a regression case to check against the chosen SDK version, not as a universal promise about provider responses. Likewise, test namespaced tools if used. Partial text, sign-in success, or a mock response is insufficient proof of a working agent.

## Verification before claiming completion

Verify sign-in and automatic return, a real model reply, a complete tool-call cycle to hosted D1, an authenticated R2 download, two distinct chats after refresh, and a follow-up using previous context. Test expired permission, provider/stream failure, companion restart, relay timeout, and duplicate requests. Re-run affected paths after fixes. Report OS, runtime, model, SDK revision/adaptations, actual checks, and untested platforms. Never include credentials or a preauthorized profile in a downloadable helper.

## Official references

- [Sign in with ChatGPT](https://developers.openai.com/siwc)
- [Registration and sign-in](https://developers.openai.com/siwc/token-sharing-open-source/sign-in)
- [Accounts and sessions](https://developers.openai.com/siwc/token-sharing-open-source/profiles-and-sessions)
- [Models and inference](https://developers.openai.com/siwc/token-sharing-open-source/models-and-inference)
- [Sites access and limits](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites)

The four-month student promotion must be activated on the same account used for the workshop. Verify its actual plan rather than treating a promotion code as an active subscription. Sites hosting access and the separate AI-plan authorization have different failure modes; diagnose the relevant one without asking the participant to buy extra access by default.
