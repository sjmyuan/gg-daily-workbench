# Example: C4, Sequence, and Flowchart Diagrams Focus

**Scenario**: A user already has the business context documented and only needs help producing C4 topology diagrams, sequence diagrams, and flowcharts for a real-time chat platform called "ChatFlow". The user has strong opinions about the architecture and wants to iterate on the diagrams.

**Applies**: `draw-c4-topology` and `draw-interaction-diagrams` — demonstrates diagram-focused, iterative refinement workflow covering both sequence diagrams (for runtime message flows) and flowcharts (for process logic and decision branches).

---

## Input (User's Initial Prompt)

> We're building ChatFlow, a real-time messaging platform. Here's what we have: a React SPA frontend, a WebSocket gateway, a Chat service, a User service, and we use Redis for pub/sub and MongoDB for message persistence. External: we integrate with Auth0 for SSO and S3 for file uploads. Users send messages via the gateway, which publishes to Redis. The Chat service subscribes to Redis, persists to MongoDB, and pushes back to the recipient through the gateway. I need C2 and C3 diagrams, plus sequence diagrams for: (1) sending a direct message, (2) creating a group chat. Please produce these.

---

## Capability 2: draw-c4-topology

**Since the user provided detailed architecture, the assistant skips most discovery questions and goes straight to diagramming...**

**Q1**: Do the Chat service and User service communicate directly, or only through the WebSocket gateway?

*User answers: Direct — Chat service calls User service via gRPC to get user profiles.*

**Q2**: Any other external systems besides Auth0 and S3?

*User answers: We also use Pusher for push notifications to mobile.*

**C2 Container Diagram output**:

```mermaid
C4Container
    title ChatFlow C2 — Container Diagram

    Person(user, "User", "Chat participant")

    System_Boundary(chatflow, "ChatFlow") {
        Container(spa, "SPA", "React", "Single-page web app")
        Container(ws_gw, "WebSocket Gateway", "Go", "WS connections, auth, routing")
        Container(chat_svc, "Chat Service", "Go", "Message handling and group logic")
        Container(user_svc, "User Service", "Java", "User profiles and contacts")
        ContainerDb(redis_pubsub, "Redis", "Redis", "Pub/sub for real-time messages")
        ContainerDb(mongo, "MongoDB", "MongoDB", "Message persistence")
    }

    System_Ext(auth0, "Auth0", "SSO & Identity")
    System_Ext(s3, "AWS S3", "File storage")
    System_Ext(pusher, "Pusher", "Mobile push notifications")

    Rel(user, spa, "Uses", "HTTPS/WSS")
    Rel(spa, auth0, "Authenticates", "OAuth2")
    Rel(spa, ws_gw, "Real-time messaging", "WSS")
    Rel(ws_gw, redis_pubsub, "Publishes messages", "RESP")
    Rel(chat_svc, redis_pubsub, "Subscribes", "RESP")
    Rel(chat_svc, mongo, "Persists messages", "MongoDB Driver")
    Rel(chat_svc, user_svc, "Gets user profiles", "gRPC")
    Rel(chat_svc, pusher, "Push notifications", "HTTPS")
    Rel(chat_svc, s3, "File uploads/downloads", "S3 API")
```

> **C2 takeaway**: SPA authenticates via Auth0 and holds a WebSocket to the Gateway; Chat Service consumes Redis pub/sub, persists to MongoDB, and calls User Service and Pusher.

[...user confirms...]

**C3 Component Diagram: Chat Service**:

```mermaid
C4Component
    title ChatFlow Chat Service — Component Diagram

    Container_Boundary(chat_svc, "Chat Service") {
        Component(msg_router, "Message Router", "Go goroutine", "Routes incoming messages by type")
        Component(dm_handler, "DM Handler", "Go goroutine", "Handles direct messages")
        Component(group_handler, "Group Handler", "Go goroutine", "Handles group chat logic")
        Component(persistence, "Persistence Layer", "Repository", "MongoDB CRUD operations")
        Component(notifier, "Notifier", "Adapter", "Pusher + WS push")
        Component(profile_client, "Profile Client", "gRPC Client", "User service calls")
        Component(s3_client, "S3 Client", "Adapter", "File operations")

        Rel(msg_router, dm_handler, "DM messages", "Go channel")
        Rel(msg_router, group_handler, "Group messages", "Go channel")
        Rel(dm_handler, persistence, "save/load", "func call")
        Rel(group_handler, persistence, "save/load", "func call")
        Rel(dm_handler, profile_client, "User service calls", "gRPC")
        Rel(group_handler, notifier, "push", "func call")
        Rel(dm_handler, notifier, "push", "func call")
        Rel(dm_handler, s3_client, "file ops", "func call")
    }
```

> **C3 takeaway**: The Message Router fans out by message type to DM or Group Handler; both use the Persistence Layer and Notifier, and the DM Handler also calls the Profile and S3 clients.

---

## Capability 3: draw-interaction-diagrams

**Based on the diagram-selection-guide, the assistant determines:**
- **Send DM flow** → Sequence diagram (runtime message passing between participants)
- **Create group chat flow** → Sequence diagram (runtime message passing between participants)
- **Message moderation workflow** → Flowchart (decision logic with branching)

### Direct Message Flow (Sequence Diagrams)

**The flow has 8 participants, so it is split into two diagrams (intake + delivery) to stay within the 6-lifeline budget.**

**Send DM — intake & validation**:

```mermaid
sequenceDiagram
    %% Level: container — cross-system flow
    actor Sender as "Sender SPA"
    participant GW as "WebSocket Gateway"
    participant Redis
    participant Chat as "Chat Service"
    participant User as "User Service"
    participant Mongo as "MongoDB"

    Sender->>GW: WS {"type":"dm","to":"user2","text":"Hi"}
    GW->>Redis: PUBLISH dm:events
    Chat->>Redis: SUBSCRIBE dm:events
    Chat->>Chat: validateMessage()<br/>checks sender & content size
    Chat->>Mongo: INSERT messages
    Chat->>User: gRPC GetProfile(user2)
    User-->>Chat: Profile
    Chat->>Redis: PUBLISH dm:delivery
```

**Send DM — delivery**:

```mermaid
sequenceDiagram
    %% Level: container — cross-system flow
    participant Chat as "Chat Service"
    participant Redis
    participant GW as "WebSocket Gateway"
    actor Recipient as "Recipient SPA"

    Chat->>Redis: PUBLISH dm:delivery
    GW->>Redis: SUBSCRIBE dm:delivery
    GW->>Recipient: WS {"type":"new_message",...}
    Note right of Chat: offline recipient → POST /push via Pusher
```

> **DM takeaway**: Sender → Gateway → Redis `dm:events` → Chat Service validates/persists and publishes `dm:delivery`; offline recipients fall back to Pusher.

**Group Chat Creation Flow**:

```mermaid
sequenceDiagram
    %% Level: container — cross-system flow
    actor Creator as "Creator SPA"
    participant GW as "WebSocket Gateway"
    participant Chat as "Chat Service"
    participant User as "User Service"
    participant Mongo as "MongoDB"
    participant Redis

    Creator->>GW: WS {"type":"create_group","name":"Team A","members":["u1","u2","u3"]}
    GW->>Chat: gRPC CreateGroup(req)
    Chat->>Chat: validateMembers()<br/>checks creator is allowed & member list valid
    Chat->>User: gRPC GetProfilesBatch(["u1","u2","u3"])
    User-->>Chat: profiles
    Chat->>Mongo: INSERT groups
    Chat->>Redis: PUBLISH group:notifications

    loop for each member
        Chat->>Redis: PUBLISH dm:delivery {"message":"You were added to Team A"}
    end

    Chat-->>GW: CreateGroupResponse{group_id}
    GW-->>Creator: WS {"type":"group_created","group_id":"g_abc"}
```

> **Group creation takeaway**: Creator → Gateway → Chat Service validates, batch-fetches profiles, persists the group, notifies members, and returns the group_id.

### Message Moderation Workflow (Flowchart)

**The assistant recognizes this as decision logic with branching — a flowchart is the right choice.**

```mermaid
flowchart TD
    A([Start]) --> B[User sends message]
    B --> C[Message enters moderation queue]
    C --> D{Contains banned keywords?}
    D -->|yes| E[Block message]
    E --> F[Notify sender: message rejected]
    F --> G([End])
    D -->|no| H{Sender is flagged user?}
    H -->|yes| I[Route to manual review queue]
    I --> J{Moderator approves?}
    J -->|yes| K[Deliver message]
    K --> G
    J -->|no| L[Block message]
    L --> M[Notify sender: rejected by moderator]
    M --> G
    H -->|no| N{Message contains attachment?}
    N -->|yes| O[Scan attachment: virus + content]
    O --> P{Scan passed?}
    P -->|yes| K
    P -->|no| Q[Block message]
    Q --> R[Notify sender: attachment blocked]
    R --> G
    N -->|no| K
```

> **Moderation takeaway**: Messages pass keyword, flagged-user, and attachment scans; any rejection path notifies the sender.


