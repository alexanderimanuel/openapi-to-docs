# pet

Part of the [Swagger Petstore - OpenAPI 3.0](README.md) documentation.

Everything about your Pets

[Find out more](https://swagger.io)

## PUT /pet

**Update an existing pet.**

Update an existing pet by Id.

- **Auth:** `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
- **Operation ID:** `updatePet`

### Request body

**Required.** Update an existent pet in the store

Content types: `application/json`, `application/xml`, `application/x-www-form-urlencoded`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `name` | string | yes |  | `"doggie"` |
| `category` | [Category](schemas.md#category) | no |  |  |
| `category.id` | integer (int64) | no |  | `1` |
| `category.name` | string | no |  | `"Dogs"` |
| `photoUrls` | array of string | yes |  | `["string"]` |
| `tags` | array of [Tag](schemas.md#tag) | no |  |  |
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

### Responses

**200**: Successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `name` | string | yes |  | `"doggie"` |
| `category` | [Category](schemas.md#category) | no |  |  |
| `category.id` | integer (int64) | no |  | `1` |
| `category.name` | string | no |  | `"Dogs"` |
| `photoUrls` | array of string | yes |  | `["string"]` |
| `tags` | array of [Tag](schemas.md#tag) | no |  |  |
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

**400**: Invalid ID supplied

**404**: Pet not found

**422**: Validation exception

**default**: Unexpected error

## POST /pet

**Add a new pet to the store.**

- **Auth:** `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
- **Operation ID:** `addPet`

### Request body

**Required.** Create a new pet in the store

Content types: `application/json`, `application/xml`, `application/x-www-form-urlencoded`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `name` | string | yes |  | `"doggie"` |
| `category` | [Category](schemas.md#category) | no |  |  |
| `category.id` | integer (int64) | no |  | `1` |
| `category.name` | string | no |  | `"Dogs"` |
| `photoUrls` | array of string | yes |  | `["string"]` |
| `tags` | array of [Tag](schemas.md#tag) | no |  |  |
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

### Responses

**200**: Successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `name` | string | yes |  | `"doggie"` |
| `category` | [Category](schemas.md#category) | no |  |  |
| `category.id` | integer (int64) | no |  | `1` |
| `category.name` | string | no |  | `"Dogs"` |
| `photoUrls` | array of string | yes |  | `["string"]` |
| `tags` | array of [Tag](schemas.md#tag) | no |  |  |
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

**400**: Invalid input

**422**: Validation exception

**default**: Unexpected error

## GET /pet/findByStatus

**Finds Pets by status.**

Multiple status values can be provided with comma separated strings.

- **Auth:** `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
- **Operation ID:** `findPetsByStatus`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `status` | query | string | yes | Status values that need to be considered for filter. Allowed: `"available"`, `"pending"`, `"sold"`. Default: `"available"`. |

### Responses

**200**: successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `[].id` | integer (int64) | no |  | `10` |
| `[].name` | string | yes |  | `"doggie"` |
| `[].category` | [Category](schemas.md#category) | no |  |  |
| `[].category.id` | integer (int64) | no |  | `1` |
| `[].category.name` | string | no |  | `"Dogs"` |
| `[].photoUrls` | array of string | yes |  | `["string"]` |
| `[].tags` | array of [Tag](schemas.md#tag) | no |  |  |
| `[].tags[].id` | integer (int64) | no |  | `0` |
| `[].tags[].name` | string | no |  | `"string"` |
| `[].status` | string | no | pet status in the store. Allowed: `"available"`, `"pending"`, `"sold"`. | `"available"` |

Example:

```json
[
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
]
```

**400**: Invalid status value

**default**: Unexpected error

## GET /pet/findByTags

**Finds Pets by tags.**

Multiple tags can be provided with comma separated strings. Use tag1, tag2, tag3 for testing.

- **Auth:** `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
- **Operation ID:** `findPetsByTags`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `tags` | query | array of string | yes | Tags to filter by. |

### Responses

**200**: successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `[].id` | integer (int64) | no |  | `10` |
| `[].name` | string | yes |  | `"doggie"` |
| `[].category` | [Category](schemas.md#category) | no |  |  |
| `[].category.id` | integer (int64) | no |  | `1` |
| `[].category.name` | string | no |  | `"Dogs"` |
| `[].photoUrls` | array of string | yes |  | `["string"]` |
| `[].tags` | array of [Tag](schemas.md#tag) | no |  |  |
| `[].tags[].id` | integer (int64) | no |  | `0` |
| `[].tags[].name` | string | no |  | `"string"` |
| `[].status` | string | no | pet status in the store. Allowed: `"available"`, `"pending"`, `"sold"`. | `"available"` |

Example:

```json
[
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
]
```

**400**: Invalid tag value

**default**: Unexpected error

## GET /pet/{petId}

**Find pet by ID.**

Returns a single pet.

- **Auth:** `api_key` (API key in header `api_key`) or `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
- **Operation ID:** `getPetById`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `petId` | path | integer (int64) | yes | ID of pet to return. |

### Responses

**200**: successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `name` | string | yes |  | `"doggie"` |
| `category` | [Category](schemas.md#category) | no |  |  |
| `category.id` | integer (int64) | no |  | `1` |
| `category.name` | string | no |  | `"Dogs"` |
| `photoUrls` | array of string | yes |  | `["string"]` |
| `tags` | array of [Tag](schemas.md#tag) | no |  |  |
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

**400**: Invalid ID supplied

**404**: Pet not found

**default**: Unexpected error

## POST /pet/{petId}

**Updates a pet in the store with form data.**

Updates a pet resource based on the form data.

- **Auth:** `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
- **Operation ID:** `updatePetWithForm`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `petId` | path | integer (int64) | yes | ID of pet that needs to be updated. |
| `name` | query | string | no | Name of pet that needs to be updated. |
| `status` | query | string | no | Status of pet that needs to be updated. |

### Responses

**200**: successful operation

Content types: `application/json`, `application/xml`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | integer (int64) | no |  | `10` |
| `name` | string | yes |  | `"doggie"` |
| `category` | [Category](schemas.md#category) | no |  |  |
| `category.id` | integer (int64) | no |  | `1` |
| `category.name` | string | no |  | `"Dogs"` |
| `photoUrls` | array of string | yes |  | `["string"]` |
| `tags` | array of [Tag](schemas.md#tag) | no |  |  |
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

**400**: Invalid input

**default**: Unexpected error

## DELETE /pet/{petId}

**Deletes a pet.**

Delete a pet.

- **Auth:** `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
- **Operation ID:** `deletePet`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `petId` | path | integer (int64) | yes | Pet id to delete. |
| `api_key` | header | string | no |  |

### Responses

**200**: Pet deleted

**400**: Invalid pet value

**default**: Unexpected error

## POST /pet/{petId}/uploadImage

**Uploads an image.**

Upload image of the pet.

- **Auth:** `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
- **Operation ID:** `uploadFile`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `petId` | path | integer (int64) | yes | ID of pet to update. |
| `additionalMetadata` | query | string | no | Additional Metadata. |

### Request body

Optional.

Content type: `application/octet-stream`

Type: string (binary).

### Responses

**200**: successful operation

Content type: `application/json`

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

**400**: No file uploaded

**404**: Pet not found

**default**: Unexpected error
