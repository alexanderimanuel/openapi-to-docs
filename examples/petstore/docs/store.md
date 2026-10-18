# store

Part of the [Swagger Petstore - OpenAPI 3.0](README.md) documentation.

Access to Petstore orders

[Find out more about our store](https://swagger.io)

## GET /store/inventory

**Returns pet inventories by status.**

Returns a map of status codes to quantities.

- **Auth:** `api_key` (API key in header `api_key`)
- **Operation ID:** `getInventory`

### Responses

**200**: successful operation

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `<key>` | integer (int32) | no |  | `0` |

Example:

```json
{
  "key": 0
}
```

**default**: Unexpected error

## POST /store/order

**Place an order for a pet.**

Place a new order in the store.

- **Operation ID:** `placeOrder`

### Request body

Optional.

Content types: `application/json`, `application/xml`, `application/x-www-form-urlencoded`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `petId` | integer (int64) | no |  | `198772` |
| `quantity` | integer (int32) | no |  | `7` |
| `shipDate` | string (date-time) | no |  | `"2024-01-15T09:30:00Z"` |
| `status` | string | no | Order Status. Allowed: `"placed"`, `"approved"`, `"delivered"`. | `"approved"` |
| `complete` | boolean | no |  | `true` |

Example:

```json
{
  "id": 10,
  "petId": 198772,
  "quantity": 7,
  "shipDate": "2024-01-15T09:30:00Z",
  "status": "approved",
  "complete": true
}
```

### Responses

**200**: successful operation

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `petId` | integer (int64) | no |  | `198772` |
| `quantity` | integer (int32) | no |  | `7` |
| `shipDate` | string (date-time) | no |  | `"2024-01-15T09:30:00Z"` |
| `status` | string | no | Order Status. Allowed: `"placed"`, `"approved"`, `"delivered"`. | `"approved"` |
| `complete` | boolean | no |  | `true` |

Example:

```json
{
  "id": 10,
  "petId": 198772,
  "quantity": 7,
  "shipDate": "2024-01-15T09:30:00Z",
  "status": "approved",
  "complete": true
}
```

**400**: Invalid input

**422**: Validation exception

**default**: Unexpected error

## GET /store/order/{orderId}

**Find purchase order by ID.**

For valid response try integer IDs with value <= 5 or > 10. Other values will generate exceptions.

- **Operation ID:** `getOrderById`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `orderId` | path | integer (int64) | yes | ID of order that needs to be fetched. |

### Responses

**200**: successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `petId` | integer (int64) | no |  | `198772` |
| `quantity` | integer (int32) | no |  | `7` |
| `shipDate` | string (date-time) | no |  | `"2024-01-15T09:30:00Z"` |
| `status` | string | no | Order Status. Allowed: `"placed"`, `"approved"`, `"delivered"`. | `"approved"` |
| `complete` | boolean | no |  | `true` |

Example:

```json
{
  "id": 10,
  "petId": 198772,
  "quantity": 7,
  "shipDate": "2024-01-15T09:30:00Z",
  "status": "approved",
  "complete": true
}
```

**400**: Invalid ID supplied

**404**: Order not found

**default**: Unexpected error

## DELETE /store/order/{orderId}

**Delete purchase order by identifier.**

For valid response try integer IDs with value < 1000. Anything above 1000 or non-integers will generate API errors.

- **Operation ID:** `deleteOrder`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `orderId` | path | integer (int64) | yes | ID of the order that needs to be deleted. |

### Responses

**200**: order deleted

**400**: Invalid ID supplied

**404**: Order not found

**default**: Unexpected error
