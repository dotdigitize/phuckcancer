# Security

Never commit API tokens, database passwords, protected health information, or institutional data-use secrets.

Configuration is environment-variable driven. cBioPortal tokens must be supplied through `CBIOPORTAL_AUTH_TOKEN` and should not be logged. External data may require permission, institutional access, authentication, data-use agreements, privacy rules, and local compliance.

PhuckCancer does not expose a raw SQL execution endpoint. Database access must use parameterized SQL.
