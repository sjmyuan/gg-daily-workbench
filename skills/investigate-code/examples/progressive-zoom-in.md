# Example: Progressive Zoom-in — Checkout Flow

## User Request

"I want to fully understand how the checkout flow works, from the API call to the confirmation. Please show me all levels."

## Response

### Level 1: C2 Container Diagram (System Landscape)

Applies `<draw-c4-diagram>` (C2).

```mermaid
C4Container
    title Checkout Flow — System Landscape (C2)
    Person(customer, "Customer", "Web/Mobile user")
    System_Boundary(checkout_system, "Checkout System") {
        Container(order_service, "order-service", "Spring Boot", "Checkout orchestration")
        Container(payment_service, "payment-service", "Spring Boot", "Payment processing")
        Container(inventory_service, "inventory-service", "Spring Boot", "Stock management")
        Container(notification_service, "notification-service", "Spring Boot", "Email/SMS, Kafka consumer")
        ContainerDb(postgres, "PostgreSQL", "Relational DB", "Inventory data")
    }
    Rel(customer, order_service, "POST /checkout", "HTTPS")
    Rel(order_service, payment_service, "POST /payments", "HTTPS")
    Rel(order_service, inventory_service, "POST /inventory/reserve", "HTTPS")
    Rel(order_service, notification_service, "publishes OrderConfirmed", "Kafka")
    Rel(payment_service, notification_service, "publishes PaymentProcessed", "Kafka")
    Rel(inventory_service, postgres, "Reads/Writes", "JDBC")
```

---

### Level 2: C3 Component Diagram (order-service Internals)

Applies `<draw-c4-diagram>` (C3).

```mermaid
C4Component
    title order-service — Component Diagram (C3)
    Container_Boundary(order_service, "order-service") {
        Component(checkout_ctrl, "CheckoutController", "REST", "POST /checkout")
        Component(order_listener, "OrderEventListener", "Kafka Consumer", "Listens for PaymentProcessed")
        Component(checkout_orch, "CheckoutOrchestrator", "Application Service", "Orchestrates checkout")
        Component(order_svc, "OrderService", "Domain Service", "Order lifecycle")
        Component(payment_adapter, "PaymentAdapter", "HTTP Client", "Calls payment-service")
        Component(inventory_adapter, "InventoryAdapter", "HTTP Client", "Calls inventory-service")
        Component(event_publisher, "EventPublisher", "Kafka Publisher", "Publishes domain events")
        ComponentDb(order_db, "Order DB", "PostgreSQL", "Order persistence")
    }
    Rel(checkout_ctrl, checkout_orch, "checkout()")
    Rel(checkout_orch, order_svc, "createOrder(), confirmOrder()")
    Rel(checkout_orch, payment_adapter, "processPayment()")
    Rel(checkout_orch, inventory_adapter, "reserveItems()")
    Rel(checkout_orch, event_publisher, "publish(OrderConfirmed)")
    Rel(order_svc, order_db, "Reads/Writes", "JDBC")
    Rel(order_listener, checkout_orch, "onPaymentProcessed()")
    Container_Ext(payment_service, "payment-service", "Spring Boot", "External payment service")
    Container_Ext(inventory_service, "inventory-service", "Spring Boot", "External inventory service")
    Rel(payment_adapter, payment_service, "POST /payments", "HTTPS")
    Rel(inventory_adapter, inventory_service, "POST /inventory/reserve", "HTTPS")
```

`CheckoutOrchestrator` owns the flow; `PaymentAdapter` retries with a circuit breaker, `InventoryAdapter` fails fast on timeout.

---

### Level 3: Sequence Diagram — Checkout Flow

Applies `<draw-sequence-diagram>`. The flow carries two concerns, so it is split into two code-level diagrams.

**Order creation** (4 messages, shown here as prose to keep the example short): `POST /checkout` → `checkout(request)` → `createOrder(customerId, items)` → `Order`.

**Parallel fulfillment, confirm, publish**:

```mermaid
sequenceDiagram
    participant Orch as "checkout/CheckoutOrchestrator.java"
    participant PayAdptr as "pay/PaymentAdapter.java"
    participant InvAdptr as "inv/InventoryAdapter.java"
    participant OrderSvc as "order/OrderService.java"
    participant Pub as "event/EventPublisher.java : EventPublisher"
    participant Kafka as "org.springframework.kafka.core.KafkaTemplate"
    Orch->>PayAdptr: 1: processPayment(orderId, paymentMethod)
    Orch->>InvAdptr: 2: reserveItems(orderId, items)
    par parallel
        PayAdptr->>PayAdptr: 3: POST /payments<br/>[cross-repo → payment-service]
        PayAdptr-->>Orch: 4: paymentOK
    and
        InvAdptr->>InvAdptr: 5: POST /inventory/reserve<br/>[cross-repo → inventory-service]
        InvAdptr-->>Orch: 6: inventoryOK
    end
    Orch->>OrderSvc: 7: confirmOrder(orderId)
    OrderSvc-->>Orch: 8: confirmed
    Orch->>Pub: 9: publish(OrderConfirmedEvent)
    Pub-)Kafka: 10: send(topic, key, event)<br/>topic: order.confirmed
```

---

### Level 4: Call Stack Trace — `CheckoutOrchestrator.checkout()`

Applies `<trace-call-stack>`.

```
[1] CheckoutOrchestrator.checkout(request: CheckoutRequest)
  File: order-service/src/main/java/.../CheckoutOrchestrator.java:35
  Parameters: request={customerId="CUST-001", items=[...], paymentMethod="CREDIT_CARD"}
  Returns: OrderSummary (JSON)
  Code:
  │  35: public OrderSummary checkout(CheckoutRequest request) {
  │  36:     Order order = orderService.createOrder(request.getCustomerId(), request.getItems());
  │  37:
  │  38:     PaymentResult payment = paymentAdapter.processPayment(order.getId(), request.getPaymentMethod());
  │  39:     InventoryResult inventory = inventoryAdapter.reserveItems(order.getId(), request.getItems());
  │  40:
  │  41:     orderService.confirmOrder(order.getId());
  │  42:     eventPublisher.publish(new OrderConfirmedEvent(order.getId()));
  │  43:     return new OrderSummary(order, payment, inventory);
  ├─→ [2] OrderService.createOrder(customerId, items)
  ├─→ [3] PaymentAdapter.processPayment(orderId, paymentMethod)   [async, parallel]
  ├─→ [4] InventoryAdapter.reserveItems(orderId, items)           [async, parallel]
  ├─→ [5] OrderService.confirmOrder(orderId)
  ╰─→ [6] EventPublisher.publish(event)

[2] OrderService.createOrder(customerId: String, items: List<Item>)
  File: order-service/src/main/java/.../OrderService.java:52
  Parameters: customerId="CUST-001", items=[Item(id="SKU-001", qty=2)]
  Returns: Order(id="ORD-12345", status=PENDING)
  Code:
  │  52: public Order createOrder(String customerId, List<Item> items) {
  │  53:     Order order = new Order(customerId, items);
  │  54:     order.setStatus(OrderStatus.PENDING);
  │  55:     return orderRepository.save(order);
  ├─→ [2a] OrderRepository.save(order) — INSERT INTO orders

[3] PaymentAdapter.processPayment(orderId: String, paymentMethod: String)
  File: order-service/src/main/java/.../PaymentAdapter.java:67
  Returns: PaymentResult(status=SUCCESS, transactionId="TXN-001")
  ╰─→ HTTP POST http://payment-service/api/payments [cross-repo]
```

Frames `[4]`–`[6]` are abridged: `InventoryAdapter` posts to `inventory-service`, `confirmOrder` flips status to `CONFIRMED`, and `EventPublisher` sends to `order.confirmed`.

**Untraced branches (❓ Gap)**: payment failure path, inventory rollback, and `OrderEventListener.onPaymentProcessed()`.

The four levels compile into one document via `<compile-markdown-report>`.
