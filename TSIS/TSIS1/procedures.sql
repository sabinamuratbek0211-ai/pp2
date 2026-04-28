DROP FUNCTION IF EXISTS search_contacts(TEXT);
DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS upsert_contact_extended(VARCHAR, VARCHAR, DATE, VARCHAR, VARCHAR, VARCHAR);

CREATE OR REPLACE PROCEDURE upsert_contact_extended(
    p_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR,
    p_phone VARCHAR,
    p_phone_type VARCHAR
)
AS $$
DECLARE
    v_group_id INTEGER;
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    SELECT id INTO v_contact_id FROM contacts WHERE name = p_name;

    IF v_contact_id IS NULL THEN
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (p_name, p_email, p_birthday, v_group_id)
        RETURNING id INTO v_contact_id;
    ELSE
        UPDATE contacts
        SET email = p_email,
            birthday = p_birthday,
            group_id = v_group_id
        WHERE id = v_contact_id;
    END IF;

    IF p_phone IS NOT NULL AND p_phone <> '' THEN
        INSERT INTO phones(contact_id, phone, type)
        VALUES (v_contact_id, p_phone, p_phone_type);
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups(name)
        VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        COALESCE(string_agg(ph.phone || ' (' || ph.type || ')', ', '), '') AS phones,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones ph ON c.id = ph.contact_id
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    HAVING c.name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR g.name ILIKE '%' || p_query || '%'
        OR COALESCE(string_agg(ph.phone, ', '), '') ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;