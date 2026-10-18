# Tickets

Part of the [Redocly Museum API](README.md) documentation.

Museum tickets for general entrance or special events.

## POST /tickets

**Buy museum tickets**

Purchase museum tickets for general entry or special events.

- **Auth:** `MuseumPlaceholderAuth` (HTTP basic)
- **Operation ID:** `buyMuseumTickets`

### Request body

**Required.**

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `email` | string (email) | no | Email address for ticket purchaser. | `"museum-lover@example.com"` |
| `ticketId` | string (uuid) | no | Unique identifier for museum ticket. Generated when purchased. | `"a54a57ca-36f8-421b-a6b4-2e8f26858a4c"` |
| `ticketDate` | string (date) | yes | Date when this ticket can be used for museum entry. | `"2023-10-29"` |
| `ticketType` | string | yes | Type of ticket being purchased. Use `general` for regular museum entry and `event` for tickets to special events. Allowed: `"event"`, `"general"`. | `"event"` |
| `eventId` | string (uuid) | no | Unique identifier for a special event. Required if purchasing tickets for the museum's special events. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |

Example:

```json
{
  "ticketType": "general",
  "ticketDate": "2023-09-07",
  "email": "todd@example.com"
}
```

### Responses

**201**: Created.

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `ticketId` | string (uuid) | no | Unique identifier for museum ticket. Generated when purchased. | `"a54a57ca-36f8-421b-a6b4-2e8f26858a4c"` |
| `ticketDate` | string (date) | yes | Date when this ticket can be used for museum entry. | `"2023-10-29"` |
| `ticketType` | string | yes | Type of ticket being purchased. Use `general` for regular museum entry and `event` for tickets to special events. Allowed: `"event"`, `"general"`. | `"event"` |
| `eventId` | string (uuid) | no | Unique identifier for a special event. Required if purchasing tickets for the museum's special events. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |
| `message` | string | yes | Confirmation message after a ticket purchase. | `"Museum general entry ticket purchased"` |
| `confirmationCode` | string | yes | Unique confirmation code used to verify ticket purchase. | `"ticket-event-a98c8f-7eb12"` |

Example:

```json
{
  "message": "Museum general entry ticket purchased",
  "ticketId": "382c0820-0530-4f4b-99af-13811ad0f17a",
  "ticketType": "general",
  "ticketDate": "2023-09-07",
  "confirmationCode": "ticket-general-e5e5c6-dce78"
}
```

**400**: Bad request.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

**404**: Not found.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

## GET /tickets/{ticketId}/qr

**Get ticket QR code**

Return an image of your ticket with scannable QR code. Used for event entry.

- **Auth:** `MuseumPlaceholderAuth` (HTTP basic)
- **Operation ID:** `getTicketCode`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `ticketId` | path | string (uuid) | yes | Identifier for a ticket to a museum event. Used to generate ticket image. Example: `"a54a57ca-36f8-421b-a6b4-2e8f26858a4c"` |

### Responses

**200**: Scannable event ticket in image format.

Content type: `image/png`

Type: string (binary).

**400**: Bad request.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```

**404**: Not found.

Content type: `application/problem+json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `type` | string | no |  | `"object"` |
| `title` | string | no |  | `"Validation failed"` |

Example:

```json
{
  "type": "object",
  "title": "Validation failed"
}
```
