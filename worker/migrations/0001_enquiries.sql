CREATE TABLE IF NOT EXISTS enquiries (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  idem        TEXT UNIQUE,
  name        TEXT,
  contact     TEXT,
  visa        TEXT,
  need        TEXT,
  travel_date TEXT,
  area        TEXT,
  notes       TEXT,
  origin      TEXT,          -- the desk's own stamp, set server-side, always present
  ref         TEXT,          -- optional partner code, paid out of the desk's share
  page        TEXT,
  landing     TEXT,
  referer     TEXT,
  received_at TEXT,
  ip_country  TEXT,
  status      TEXT DEFAULT 'new',
  booked      INTEGER DEFAULT 0,
  commission  TEXT
);
CREATE INDEX IF NOT EXISTS enquiries_origin ON enquiries (origin);
CREATE INDEX IF NOT EXISTS enquiries_ref ON enquiries (ref);
CREATE INDEX IF NOT EXISTS enquiries_received ON enquiries (received_at);
