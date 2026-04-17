CREATE OR REPLACE PROCEDURE upsert_contact(name TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE username = name) THEN
        UPDATE phonebook SET phone = upsert_contact.phone WHERE username = name;
    ELSE
        INSERT INTO phonebook(username, phone) VALUES (name, phone);
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    WHERE username ILIKE '%' || pattern || '%'
       OR phone LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_contact(identifier TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE username = identifier OR phone = identifier;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    names TEXT[],
    phones TEXT[],
    OUT failed TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    failed := ARRAY[]::TEXT[];

    FOR i IN 1..array_length(names, 1) LOOP
        BEGIN
            INSERT INTO phonebook(username, phone)
            VALUES (names[i], phones[i]);
        EXCEPTION WHEN OTHERS THEN
            failed := array_append(failed, names[i]);
        END;
    END LOOP;
END;
$$;