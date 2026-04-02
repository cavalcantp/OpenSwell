# Openswell
`Openswell` aims to provide each surfer with an all-knowing surfing buddy.

## Consolidated features and architecture

Currently, the service is a simple MVP, and it includes an AI-based surfing recommender, which is able to guide surfers on where to surf, based on:
- what region the surfer is located, or wishes to surf in
- the time period they wish the surf
- their skill level
- their goals/preferences for the surfing session (e.g, "learning how to stand up", "prefer hollower waves")

The AI surfing assistant collects all this information from the interactions with the user, complements it with local swell and wind conditions, and descriptions of the most famous surfing spots in the surfer's region. Then all this information is passed through a scoring-ranking system, and recommendations are fed into the underlying foundation model that acts as an explaner, providing arguments that back the recommendations.

The architecure follows a Workflow Pattern, using Prompt Chaining to leverage the foundation model as intent identifier and explainer for the "recommender system", while keeping the scoring and ranking logic under control of the application, avoiding scoring issues related to model's probabilistic nature, since we are constrained to locally served models (llama3 via ollama).

## Ongoing iteration

As we move toward more powerful underlying models, we adopt the Tool Use Pattern and Reflection Pattern, in order to increase the systems autonomy, handling function calling suggestion to the underlying model, and allowing for re-terations driven by the model's reasoning about output quality. The amount of allowed iterations is bounded to avoid that the model falls into the trap of deep iteration, leading to increased preceived latency and cost.

## Application and Architecture Evolution

Once we start adding more features to the `Openswell` application, such as a surf board recommender system, surf trip planner, we will leverage the Routing Pattern, where a router agent distributes tasks amongst specialized agents. This way we can better optimized each specialists prompts and increase context efficiency, also avoiding unecessary iteration loops due to model confusion.

Regarding the recommender system, we can move from the current rule based system to a ML-powered one. That also goes for any other recommendatin features added.

## TODOs:
Besides the natural steps to be taken in terms of feature expansion and architectural evolution, the following topics also must be addressed:
- Increase test coverage (services, clients, not limited only to API endpoints)
- Include integration tests (use testcontaianers)
- Migrate from poetry to uv
- Containerize application
- Mock K8s manifest files
- Build simple frontend