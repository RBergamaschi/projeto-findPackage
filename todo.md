# Plano de Implementação — Painel de Logística

## Fundação (modelo e acesso)

- [x] 1. `UserRole` (CUSTOMER, DRIVER, ADMIN) no lugar de `is_superuser`
- [x] 2. Validação de rota por `UserRole` (RBAC)

## Modelos e domínio

- [x] 3. `DriverProfile` linkado ao `User` (CNH, tipo de veículo, placa)
- [ ] 4. `Order` enriquecido
  - [ ] `description`
  - [ ] `weight`
  - [ ] `tracking_code`
  - [ ] `pickup_address_id` (endereço de origem)
  - [ ] `delivery_address_id` (endereço de destino)
  - [ ] `driver_id`
  - [ ] `estimated_delivery_at`
  - [ ] `delivered_at`
- [ ] 5. `Tracking` enriquecido
  - [ ] `event_type` (ping GPS vs evento de status)
  - [ ] `description` (ex: "Saiu para entrega")
  - [ ] `location_name` (nome legível do local)
- [ ] 6. `OrderStatusHistory` — log imutável de mudanças de status (quem fez, quando)

## Regras de negócio

- [ ] 7. Validação de transição de status (máquina de estados: PENDING → SHIPPED → DELIVERED)
- [ ] 8. Rota pública de rastreamento `GET /track/{tracking_code}` (sem autenticação)

## Operações e visibilidade

- [ ] 9. Filtros avançados nas listagens (por data, cidade, status, driver)
- [ ] 10. Dashboard / estatísticas para admin
  - [ ] Pedidos por status
  - [ ] Entregas do dia
  - [ ] Performance por entregador
  - [ ] Média de tempo de entrega

## Testes

- [ ] 11. Testes de integração nos services e rotas críticas (auth, criação de pedido, transição de status)

## Comunicação e notificações

- [ ] 12. Email de notificação (ao criar pedido, ao mudar status, ao entregar)
- [ ] 13. WebSocket para tracking em tempo real (mapa ao vivo)

## Infraestrutura avançada

- [ ] 14. Redis (cache de consultas frequentes e rate limiting distribuído)
- [ ] 15. Kafka (eventos de mudança de status publicados em tópico)
