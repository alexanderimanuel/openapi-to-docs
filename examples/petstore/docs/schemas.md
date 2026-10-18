# Schemas

Data models used by the [Swagger Petstore - OpenAPI 3.0](README.md) endpoints.

## Order

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

## Category

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `1` |
| `name` | string | no |  | `"Dogs"` |

Example:

```json
{
  "id": 1,
  "name": "Dogs"
}
```

## User

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `username` | string | no |  | `"theUser"` |
| `firstName` | string | no |  | `"John"` |
| `lastName` | string | no |  | `"James"` |
| `email` | string | no |  | `"john@email.com"` |
| `password` | string | no |  | `"12345"` |
| `phone` | string | no |  | `"12345"` |
| `userStatus` | integer (int32) | no | User Status. | `1` |

Example:

```json
{
  "id": 10,
  "username": "theUser",
  "firstName": "John",
  "lastName": "James",
  "email": "john@email.com",
  "password": "12345",
  "phone": "12345",
  "userStatus": 1
}
```

## Tag

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `0` |
| `name` | string | no |  | `"string"` |

Example:

```json
{
  "id": 0,
  "name": "string"
}
```

## Pet

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `name` | string | yes |  | `"doggie"` |
| `category` | [Category](#category) | no |  |  |
| `category.id` | integer (int64) | no |  | `1` |
| `category.name` | string | no |  | `"Dogs"` |
| `photoUrls` | array of string | yes |  | `["string"]` |
| `tags` | array of [Tag](#tag) | no |  |  |
| `tags[].id` | integer (int64) | no |  | `0` |
| `tags[].name` | string | no |  | `"string"` |
| `status` | string | no | pet status in the store. Allowed: `"available"`, `"pending"`, `"sold"`. | `"available"` |

Example:

```json
{
  "id": 10,
  "name": "doggie",
  "category": {
    "id": 1,
    "name": "Dogs"
  },
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}
```

## ApiResponse

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `code` | integer (int32) | no |  | `0` |
| `type` | string | no |  | `"string"` |
| `message` | string | no |  | `"string"` |

Example:

```json
{
  "code": 0,
  "type": "string",
  "message": "string"
}
```
