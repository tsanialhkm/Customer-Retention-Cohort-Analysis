-- CASE 002: Data discovery

SELECT name, type
FROM sqlite_master
WHERE type IN ('table', 'view')
ORDER BY type, name;

SELECT *
FROM schema_notes;
