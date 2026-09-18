-- White-label deployments. A licensed copy of the site carries its licence id
-- in config, and it rides on every enquiry that copy sends, which is what the
-- licence is billed from.
ALTER TABLE enquiries ADD COLUMN licence TEXT;
CREATE INDEX IF NOT EXISTS enquiries_licence ON enquiries (licence);
