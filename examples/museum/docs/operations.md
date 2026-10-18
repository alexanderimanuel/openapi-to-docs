# Operations

Part of the [Redocly Museum API](README.md) documentation.

Operational information about the museum.

## GET /museum-hours

**Get museum hours**

Get upcoming museum operating hours.

- **Auth:** `MuseumPlaceholderAuth` (HTTP basic)
- **Operation ID:** `getMuseumHours`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `startDate` | query | string (date) | no | Starting date to retrieve future operating hours from. Defaults to today's date. Example: `"2023-02-23"` |
| `page` | query | integer | no | Page number to retrieve. Default: `1`. Example: `2` |
| `limit` | query | integer | no | Number of days per page. Default: `10`. Maximum: 30. Example: `15` |

### Responses

**200**: Success.

Content type: `application/json`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `[].date` | string (date) | yes | Date the operating hours apply to. | `"2024-12-31"` |
| `[].timeOpen` | string | yes | Time the museum opens on a specific date. Uses 24 hour time format (`HH:mm`). Pattern: `^([01]\d\|2[0-3]):?([0-5]\d)$`. | `"09:00"` |
| `[].timeClose` | string | yes | Time the museum closes on a specific date. Uses 24 hour time format (`HH:mm`). Pattern: `^([01]\d\|2[0-3]):?([0-5]\d)$`. | `"18:00"` |

Example:

```json
[
  {
    "date": "2023-09-11",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  },
  {
    "date": "2023-09-12",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  },
  {
    "date": "2023-09-13",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  },
  {
    "date": "2023-09-14",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  },
  {
    "date": "2023-09-15",
    "timeOpen": "10:00",
    "timeClose": "16:00"
  },
  {
    "date": "2023-09-18",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  },
  {
    "date": "2023-09-19",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  },
  {
    "date": "2023-09-20",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  },
  {
    "date": "2023-09-21",
    "timeOpen": "09:00",
    "timeClose": "18:00"
  },
  {
    "date": "2023-09-22",
    "timeOpen": "10:00",
    "timeClose": "16:00"
  }
]
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
