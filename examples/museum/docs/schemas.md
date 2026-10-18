# Schemas

Data models used by the [Redocly Museum API](README.md) endpoints.

## TicketType

Type of ticket being purchased. Use `general` for regular museum entry and `event` for tickets to special events.

Type: string. Allowed: `"event"`, `"general"`.

Example:

```json
"event"
```

## Date

Type: string (date).

Example:

```json
"2023-10-29"
```

## Email

Email address for ticket purchaser.

Type: string (email).

Example:

```json
"museum-lover@example.com"
```

## BuyMuseumTickets

Data to purchase a ticket.

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
  "email": "museum-lover@example.com",
  "ticketId": "a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
  "ticketDate": "2023-10-29",
  "ticketType": "event",
  "eventId": "3be6453c-03eb-4357-ae5a-984a0e574a54"
}
```

## TicketMessage

Confirmation message after a ticket purchase.

Type: string.

Example:

```json
"Museum general entry ticket purchased"
```

## TicketId

Unique identifier for museum ticket. Generated when purchased.

Type: string (uuid).

Example:

```json
"a54a57ca-36f8-421b-a6b4-2e8f26858a4c"
```

## TicketConfirmation

Unique confirmation code used to verify ticket purchase.

Type: string.

Example:

```json
"ticket-event-a98c8f-7eb12"
```

## Ticket

Ticket for museum entry, can be general admission or special event.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `ticketId` | string (uuid) | no | Unique identifier for museum ticket. Generated when purchased. | `"a54a57ca-36f8-421b-a6b4-2e8f26858a4c"` |
| `ticketDate` | string (date) | yes | Date when this ticket can be used for museum entry. | `"2023-10-29"` |
| `ticketType` | string | yes | Type of ticket being purchased. Use `general` for regular museum entry and `event` for tickets to special events. Allowed: `"event"`, `"general"`. | `"event"` |
| `eventId` | string (uuid) | no | Unique identifier for a special event. Required if purchasing tickets for the museum's special events. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |

Example:

```json
{
  "ticketId": "a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
  "ticketDate": "2023-10-29",
  "ticketType": "event",
  "eventId": "3be6453c-03eb-4357-ae5a-984a0e574a54"
}
```

## MuseumTicketsConfirmation

Details for a museum ticket after a successful purchase.

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
  "ticketId": "a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
  "ticketDate": "2023-10-29",
  "ticketType": "event",
  "eventId": "3be6453c-03eb-4357-ae5a-984a0e574a54",
  "message": "Museum general entry ticket purchased",
  "confirmationCode": "ticket-event-a98c8f-7eb12"
}
```

## TicketCodeImage

Image of a ticket with a QR code used for museum or event entry.

Type: string (binary).

Example:

```json
"<binary data>"
```

## MuseumHours

List of museum operating hours for a date range.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `[].date` | string (date) | yes | Date the operating hours apply to. | `"2024-12-31"` |
| `[].timeOpen` | string | yes | Time the museum opens on a specific date. Uses 24 hour time format (`HH:mm`). Pattern: `^([01]\d\|2[0-3]):?([0-5]\d)$`. | `"09:00"` |
| `[].timeClose` | string | yes | Time the museum closes on a specific date. Uses 24 hour time format (`HH:mm`). Pattern: `^([01]\d\|2[0-3]):?([0-5]\d)$`. | `"18:00"` |

Example:

```json
[
  {
    "date": "2024-12-31",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  }
]
```

## MuseumDailyHours

Daily operating hours for the museum.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `date` | string (date) | yes | Date the operating hours apply to. | `"2024-12-31"` |
| `timeOpen` | string | yes | Time the museum opens on a specific date. Uses 24 hour time format (`HH:mm`). Pattern: `^([01]\d\|2[0-3]):?([0-5]\d)$`. | `"09:00"` |
| `timeClose` | string | yes | Time the museum closes on a specific date. Uses 24 hour time format (`HH:mm`). Pattern: `^([01]\d\|2[0-3]):?([0-5]\d)$`. | `"18:00"` |

Example:

```json
{
  "date": "2024-12-31",
  "timeOpen": "09:00",
  "timeClose": "18:00"
}
```

## EventId

Identifier for a special event.

Type: string (uuid).

Example:

```json
"3be6453c-03eb-4357-ae5a-984a0e574a54"
```

## EventName

Name of the special event.

Type: string.

Example:

```json
"Pirate Coding Workshop"
```

## EventLocation

Location where the special event is held.

Type: string.

Example:

```json
"Computer Room"
```

## EventDescription

Description of the special event.

Type: string.

Example:

```json
"Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang)."
```

## EventDates

List of planned dates for the special event.

Type: array of string (date).

Example:

```json
[
  "2023-10-29"
]
```

## EventPrice

Price of a ticket for the special event.

Type: number (float).

Example:

```json
25
```

## SpecialEventFields

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `name` | string | no | Name of the special event. | `"Pirate Coding Workshop"` |
| `location` | string | no | Location where the special event is held. | `"Computer Room"` |
| `eventDescription` | string | no | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `dates` | array of string (date) | no | List of planned dates for the special event. | `["2023-10-29"]` |
| `price` | number (float) | no | Price of a ticket for the special event. | `25` |

Example:

```json
{
  "name": "Pirate Coding Workshop",
  "location": "Computer Room",
  "eventDescription": "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).",
  "dates": [
    "2023-10-29"
  ],
  "price": 25
}
```

## SpecialEvent

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `eventId` | string (uuid) | no | Identifier for a special event. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |
| `name` | string | yes | Name of the special event. | `"Pirate Coding Workshop"` |
| `location` | string | yes | Location where the special event is held. | `"Computer Room"` |
| `eventDescription` | string | yes | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `dates` | array of string (date) | yes | List of planned dates for the special event. | `["2023-10-29"]` |
| `price` | number (float) | yes | Price of a ticket for the special event. | `25` |

Example:

```json
{
  "eventId": "3be6453c-03eb-4357-ae5a-984a0e574a54",
  "name": "Pirate Coding Workshop",
  "location": "Computer Room",
  "eventDescription": "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).",
  "dates": [
    "2023-10-29"
  ],
  "price": 25
}
```

## SpecialEventCollection

List of upcoming special events.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `[].eventId` | string (uuid) | no | Identifier for a special event. | `"3be6453c-03eb-4357-ae5a-984a0e574a54"` |
| `[].name` | string | yes | Name of the special event. | `"Pirate Coding Workshop"` |
| `[].location` | string | yes | Location where the special event is held. | `"Computer Room"` |
| `[].eventDescription` | string | yes | Description of the special event. | `"Captain Blackbeard shares his love of the C...language. ...` |
| `[].dates` | array of string (date) | yes | List of planned dates for the special event. | `["2023-10-29"]` |
| `[].price` | number (float) | yes | Price of a ticket for the special event. | `25` |

Example:

```json
[
  {
    "eventId": "3be6453c-03eb-4357-ae5a-984a0e574a54",
    "name": "Pirate Coding Workshop",
    "location": "Computer Room",
    "eventDescription": "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).",
    "dates": [
      "2023-10-29"
    ],
    "price": 25
  }
]
```

## Error

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
