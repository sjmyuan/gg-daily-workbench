# Decision Driver and Option Prompting Guide

Used by: **define-decision-drivers**, **define-considered-options**.

## Decision driver categories

Suggest these categories when prompting the user for decision drivers:
- **Performance**: latency, throughput, resource usage
- **Cost**: licensing, infrastructure, operational, migration
- **Timeline**: delivery deadlines, team availability
- **Team expertise**: existing skills, learning curve, hiring needs
- **Maintainability**: code complexity, debugging, onboarding
- **Security**: compliance, data protection, attack surface
- **Scalability**: horizontal/vertical scaling, future growth
- **Compatibility**: existing systems, ecosystem fit, vendor lock-in

Help the user distinguish **hard constraints** (must-haves / knock-out criteria) from **soft preferences** (nice-to-haves).

## Option brainstorming prompts

When the user has only one option, prompt them to consider alternatives:
- **Do nothing / status quo**: What happens if we don't change anything?
- **Industry-standard approaches**: What do similar teams or companies do?
- **Open-source alternatives**: Are there OSS tools that address this?
- **Build vs. buy**: Should we build it ourselves or purchase a solution?
- **Incremental vs. big-bang**: Can we phase the change, or must it be all at once?
- **Greenfield rewrite**: Would starting fresh produce a better outcome than modifying?
- **Hybrid / phased**: Can we combine approaches or phase the transition?
