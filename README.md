# OpenSwell
`OpenSwell` aims to provide each surfer with an all-knowing surfing buddy.

## Consolidated features and architecture

Currently, the service is a simple MVP, and it includes an AI-based surfing recommender, which is able to guide surfers on where to surf, based on:
- what region the surfer is located, or wishes to surf in
- the time period they wish the surf
- their skill level
- their goals/preferences for the surfing session (e.g, "learning how to stand up", "prefer hollower waves")

The AI surfing assistant collects user input, augments it with local swell and wind conditions, and adds descriptions of famous surfing spots in the region. A scoring-ranking ("recommender") system evaluates options, and a foundation model generates explanations supporting the recommendations.

The AI surfing assistant collects all this information from the interactions with the user, augments it with local swell and wind conditions, and descriptions of the most famous surfing spots in the surfer's region. Then all this information is passed through a scoring-ranking system, and recommendations are fed into the underlying foundation model that acts as an explaner, providing arguments that back the recommendations.

API design: Leverages dependency injection and factory methods for routers and application components, improving testability and modularity of the system's components. It leverages the state Singleton to manage dependecies via lifespan events.
Agentic workflow: Follows a Workflow Pattern with prompt chaining to leverage the foundation model as an intent identifier and explainer, while scoring logic remains controlled by the business logic, avoiding scoring issues related to model's probabilistic nature, since we are constrained to locally served models (llama3 via ollama).


## Ongoing iteration

As we move toward more powerful underlying models, we adopt the Tool Use Pattern and Reflection Pattern, in order to increase the system's autonomy:
- enable the model to suggest function calls and refine outputs based on reasoning
- the amount of allowed iterations is bounded to prevent deep iteration loops, which could lead to increased preceived latency and cost.


## Application and Architecture Evolution

Once we start adding more features to the `OpenSwell` application, such as a surf board recommender system and surf trip planner, we will leverage the Routing Pattern, where a router agent distributes tasks amongst specialized agents. This way we can better optimized each specialist's prompts and increase context efficiency, also avoiding unecessary iteration loops due to model confusion.

Regarding the recommender system, we can transition from the current rule based scorer to a ML recommender, for more personalized recommendations. The same also goes for any future recommendation features added.

## TODOs:
Besides the natural steps to be taken in terms of feature expansion and architectural evolution, the following topics also must be addressed:
- Increase test coverage (services, clients, not limited only to API endpoints)
- Add proper exception handling, retries and middleware
- Include integration tests (use testcontaianers)
- Containerize application
- Mock K8s manifest files
- Build simple frontend